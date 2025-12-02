# Deep Research Prompt: GPU-Generator Stability Integration Modeling

**Project**: Off-Grid AI Inference Research  
**Date**: 2025-12-01  
**Purpose**: Comprehensive research prompt for modeling GPU cluster power dynamics with natural gas generator stability constraints  
**Target Deliverables**: Stability model, scheduler design rules, miner coordination strategies, optional BESS analysis

---

## EXECUTION INSTRUCTIONS

**Phase Priority**: Start with **Phase 1 (Generator Parameter Extraction)**, then proceed to **Phase 2 (GPU Power Characterization)** in parallel or immediately after. Phases 3-4 require outputs from both Phase 1 and Phase 2.

**Output Format**: 
1. **Initial Deliverable**: Create `research-findings.md` with structured findings for review (parameter tables, data gaps, calculations, literature review, confidence levels)
2. **After Review/Approval**: Produce full formatted deliverables (`stability-model.md`, `scheduler-design.md`, optional `bess-optional-analysis.md`)

See Section 9.2 for detailed output format strategy.

---

## 1. EXECUTIVE CONTEXT

### 1.1 Project Overview

This research models the integration of NVIDIA H100 GPU clusters with natural gas generators for off-grid AI inference deployment. The **core operating model** uses **shaped ramps** (small GPU steps) and **optional miner shedding** to keep net load changes within generator tolerances, making BESS **optional rather than required** for GPU ramp control.

**Key Operating Model**:
- **1 MW generator** feeding up to **0.5 MW ASIC miners** (flexible ballast) and **0.5 MW H100 GPUs**
- GPUs brought online in **small batches** (1-10 GPUs at a time)
- Generator sees only **tiny steps** (single H100 = 0.7 kW = 0.07% of 1 MW generator)
- **Optional miner shedding** to keep net load flat (swap miners for GPUs in equal kW chunks)
- **No BESS required** for GPU ramp control (generator inertia + shaped ramps sufficient)

**Research Goals**:
1. **Maximum GPU ramp rates** (GPUs per second) that respect generator step/ramp limits
2. **Scheduler design rules** for shaped ramps (batch sizes, timing)
3. **Miner coordination strategies** (when/how to shed miners for faster ramps)
4. **BESS as optional enhancement** (useful for reliability/codes, not required for ramp control)
5. **Risk classification** (GREEN/YELLOW/RED) based on ramp rates, not BESS presence

### 1.2 Key Constraint: Power Availability & Ramp Rate Limits

From H100 economics analysis (H100-CONSOLIDATED-ANALYSIS.md, Section 3.4):
- **Generator capacity is fixed** (e.g., 1 MW in reference scenario)
- **Reference Scenario**: 1 MW generator → 0.5 MW ASIC miners (flexible ballast) + 0.5 MW H100 GPUs
- **PCIe H100**: 0.35 kW per GPU → ~1,428 GPUs for 500 kW (theoretical max)
- **SXM H100**: 0.7 kW per GPU → ~714 GPUs for 500 kW (theoretical max)
- **Power constraint**: Generator step/ramp limits, not just total capacity
- **Single GPU step**: 0.7 kW (SXM) or 0.35 kW (PCIe) = 0.07% or 0.035% of 1 MW generator (trivial)

### 1.3 Deployment Strategy (Verified at 95% Confidence)

**Recommended Mix**: 80-85% PCIe H100, 15-20% SXM H100
- PCIe delivers **40% more inference throughput per kilowatt** for single-GPU workloads
- PCIe achieves profitability at **75-80% utilization** at market rates ($2.29/hour)
- SXM requires premium pricing (>$3.10/hour) or NVLink-exploiting workloads

---

## 2. KNOWN PARAMETERS

### 2.1 GPU Power Characteristics (From H100 Economics Analysis)

#### H100 PCIe Power Specifications
- **TDP**: 350W per GPU (continuous maximum)
- **Memory**: 80GB HBM2e
- **Memory Bandwidth**: 2.0 TB/s
- **Power Efficiency**: 8.65 TOPS/Watt (sparse), 1.00-1.29 TFLOPS/Watt (dense)
- **Source**: NVIDIA official specs [22][25], verified benchmarks [2][34][35][36]

#### H100 SXM Power Specifications
- **TDP**: 700W per GPU (continuous maximum)
- **Memory**: 80GB HBM3
- **Memory Bandwidth**: 3.35 TB/s
- **Power Efficiency**: 5.65 TOPS/Watt (sparse), 0.89-1.04 TFLOPS/Watt (dense)
- **Source**: NVIDIA official specs [22][25], verified benchmarks [2][34][35][36]

#### Power Draw Assumptions (Currently Unvalidated - NEEDS RESEARCH)
- **Idle State**: Unknown (assumed 50-100W per PCIe GPU, 100-200W per SXM GPU)
- **Model Loading**: Unknown (assumed 200-300W per PCIe GPU, 400-600W per SXM GPU)
- **Inference Burst**: Unknown (assumed 300-350W per PCIe GPU, 600-700W per SXM GPU)
- **Sustained Inference**: Unknown (assumed 250-300W per PCIe GPU, 500-600W per SXM GPU)
- **Ramp Rate**: Unknown (assumed 50-200 kW/s for 100-GPU cluster)

**CRITICAL RESEARCH NEED**: Empirical power draw profiles for H100 PCIe under inference workloads

### 2.2 Generator Parameters (From Caterpillar Technical Analysis)

#### Available Generator Models (Natural Gas)

| Model | Rated Power (ekW) | Efficiency | Inertia (kg⋅m²) | Max Step Load | Start Time | Governor |
|-------|-------------------|------------|-----------------|---------------|------------|----------|
| **CG170-16** | 1,560 | 43.30% | >44.6 | ~20-25% | >30s (ramp) | TEM |
| **CG260-16** | 4,500 | 44.60% | **710** | **16%** | >60s (ramp) | TEM |
| **G3516C** | 1,660 | ~40.6% | ~150 (est.) | 50-75% | <30s | ADEM A3/A4 |
| **G3520 Fast Resp** | 2,500 | 45.30% | ~37 (rotor) + eng | **100%** | **10s** | ADEM A4 |
| **G3520H** | 2,519 | 45.30% | ~37 (rotor) + eng | G1 Limits | >30s | ADEM A4 |
| **G3616 A4** | 3,729 | ~42% | High (>1000) | Low (ramp) | Slow (minutes) | ADEM A4 |

**Source**: `data/generators/caterpillar/Caterpillar-Technical-Analysis.md`, Section 7.2

#### Critical Data Gaps (From Caterpillar Analysis)

**MISSING PARAMETERS** (not in public datasheets):
- ❌ **Inertia constant (H)** in seconds - NOT published (only kg⋅m² available)
- ❌ **RoCoF limits** (Hz/s) - NOT published
- ❌ **Voltage dip %** for load steps - Only "ISO 8528 compliant" stated
- ❌ **Governor droop defaults** - "Typical 2-5%" but not model-specific
- ❌ **AVR/exciter gains** - NOT in brochures

**RESEARCH NEED**: Convert kg⋅m² to H (seconds) using formula: H = J × ω² / (2 × S_base)

Where:
- J = mass moment of inertia (kg⋅m²)
- ω = angular velocity (rad/s) = 2π × f / p (f = frequency Hz, p = pole pairs)
- S_base = generator MVA rating

### 2.3 Generator Stability Formulas (From Glossary & Calculator)

#### Rate of Change of Frequency (RoCoF)
```
RoCoF = -ΔP_cluster / (2 × H_eff × S_base)
```

Where:
- ΔP_cluster = total cluster power change (MW)
- H_eff = inertia constant (seconds)
- S_base = generator MVA rating

#### Frequency Deviation (Steady-State)
```
ΔF/F_nom ≈ -R_eff × (ΔP_cluster / P_rated)
```

Where:
- R_eff = governor droop (p.u., typically 0.03-0.05 for 3-5%)
- ΔP_cluster = load step (MW)
- P_rated = generator rated power (MW)

#### Cluster Power Step Calculation
```
ΔP_cluster = N_batch × ΔP_gpu
```

Where:
- N_batch = number of GPUs changing state simultaneously (controlled by scheduler)
- ΔP_gpu = power change per GPU (kW) - typically 0.25-0.5 kW for phase transitions

**Key Insight**: We control N_batch (batch size) to keep steps small. Single GPU = 0.7 kW max (SXM) = trivial on 1 MW generator.

**CRITICAL RESEARCH NEED**: 
- Determine optimal batch sizes (N_batch) for different generator models
- Determine timing between batches (seconds) to respect ramp rate limits
- Validate that GPU power changes can be staged (power cap ramping, checkpoint/hold points)

---

## 3. RESEARCH QUESTIONS

### 3.1 GPU Power Characterization (HIGH PRIORITY)

**Question 1.1**: What is the actual power draw profile of H100 PCIe GPUs during inference workloads?

**Required Measurements**:
- Idle state power (watts, duration)
- Model loading power (watts, duration, ramp rate kW/s)
- Inference burst power (peak watts, duration, ramp rate kW/s)
- Sustained inference power (average watts, variance)
- Power draw during batch size changes
- Power draw during model switching

**Research Methods**:
- Literature search: NVIDIA power management white papers, academic GPU power profiling studies
- Industry benchmarks: Lambda Labs, Hyperstack, RunPod power consumption data
- Community data: GitHub llama.cpp power discussions, Reddit r/LocalLLaMA power reports
- Empirical validation: If access available, measure with nvidia-smi or NVML API

**Expected Output**: Power draw profile table with time-series data for each operational phase

---

**Question 1.2**: What is the correlation coefficient (C) between GPU power draws in a multi-GPU cluster?

**Required Analysis**:
- How synchronized are power changes across N GPUs?
- Does correlation vary by workload type (single-GPU inference vs multi-GPU tensor parallelism)?
- Does correlation vary by batch size?
- What is the worst-case correlation (perfect synchronization = C = 1.0)?

**Research Methods**:
- Literature search: GPU cluster power correlation studies, data center power dynamics
- Industry data: Cloud provider power monitoring dashboards (if available)
- Modeling: Assume worst-case C = 1.0 for conservative design, best-case C = 0.3-0.7 for typical workloads

**Expected Output**: Correlation coefficient ranges by workload type and cluster size

---

**Question 1.3**: What are the acceptable power step scenarios under shaped ramp control?

**Required Scenarios**:
- Small batch ramps: 1-10 GPUs changing state simultaneously
- Staged phase transitions: Preload → full-power in batches (e.g., 10 GPUs every 0.5 seconds)
- Time windows: Generator ramp rate limits determine timing (e.g., 20 kW/s max = ~28 GPUs/second for SXM)
- Multiple clusters: Can clusters coordinate ramps to stay within generator limits?

**Research Methods**:
- Design scenarios: Calculate step sizes for various batch sizes (1, 5, 10, 20 GPUs)
- Generator limits: Match batch sizes to generator step/ramp tolerances
- Scheduler design: Determine optimal batch sizes and timing for each generator model
- Conservative assumption: Design for worst-case (all GPUs in batch change simultaneously)

**Expected Output**: Acceptable power step scenarios with batch sizes and timing for each generator model

---

### 3.2 Generator Parameter Extraction (HIGH PRIORITY)

**Question 2.1**: What are the inertia constants (H_eff) in seconds for each Caterpillar generator model?

**Required Conversions**:
- Convert kg⋅m² to H (seconds) using formula above
- Account for flywheel inertia (if present)
- Account for engine inertia contribution
- Verify against industry standards (typical H = 3-6 seconds for natural gas gensets)

**Research Methods**:
- Extract from Caterpillar-Technical-Analysis.md (Section 7.2)
- Literature search: Generator inertia constant databases, IEEE standards
- Engineering calculations: Use known formulas with generator specifications
- Cross-reference: Compare with similar generator models from other manufacturers

**Expected Output**: H_eff (seconds) for each generator model: CG170-16, CG260-16, G3516C, G3520, G3520H, G3616

---

**Question 2.2**: What are the RoCoF limits (Hz/s) for each Caterpillar generator model?

**Required Parameters**:
- Maximum Hz/s the generator can tolerate before protection trips
- Typical range: 0.5-2.0 Hz/s for natural gas engines
- Protection settings: Underfrequency relay trip points
- Recovery capability: Can generator recover from high RoCoF events?

**Research Methods**:
- Literature search: IEEE standards for frequency protection, generator protection studies
- Industry data: Generator protection relay settings, manufacturer application guides
- Conservative assumption: Use 0.5 Hz/s if not found (most restrictive)
- Cross-reference: Compare with ISO 8528-5 transient performance classes

**Expected Output**: RoCoF limits (Hz/s) for each generator model, protection trip points

---

**Question 2.3**: What are the governor droop settings (R_eff) for each Caterpillar generator model?

**Required Parameters**:
- Steady-state frequency deviation per unit load change
- Typical range: 3-5% (0.03-0.05 p.u.) for isochronous mode
- Model-specific defaults: May vary by control system (TEM vs ADEM A4)
- Isochronous vs droop mode: Which mode is used for off-grid operation?

**Research Methods**:
- Extract from Caterpillar technical documentation
- Literature search: Governor control systems, isochronous vs droop operation
- Industry standards: IEEE 1547 for distributed generation, ISO 8528-5
- Conservative assumption: Use 5% (0.05 p.u.) if not found

**Expected Output**: R_eff (p.u. or %) for each generator model and control mode

---

**Question 2.4**: What are the frequency deviation tolerance limits (±Hz) for each generator model?

**Required Parameters**:
- ±Hz range before protection trips
- Typical: ±0.5 Hz (59.5-60.5 Hz for 60 Hz nominal)
- Protection settings: Underfrequency and overfrequency relay trip points
- Recovery time: How quickly can generator return to nominal frequency?

**Research Methods**:
- Literature search: Generator protection standards, frequency tolerance studies
- Industry data: Protection relay settings, manufacturer specifications
- Standards: ISO 8528-5 frequency tolerance classes (G1/G2/G3)
- Conservative assumption: Use ±0.5 Hz if not found

**Expected Output**: Frequency deviation tolerance (±Hz) and protection trip points for each model

---

### 3.3 Stability Model Calculations (MEDIUM PRIORITY)

**Question 3.1**: What is the maximum safe GPU count per generator model without BESS?

**Required Calculations**:
- For each generator model (CG170-16, CG260-16, G3516C, G3520, G3520H, G3616):
  - Calculate RoCoF for worst-case GPU cluster power step
  - Calculate frequency deviation for worst-case step
  - Compare against generator limits
  - Determine maximum N (GPUs) that keeps RoCoF and ΔF within limits

**Calculation Steps**:
1. Assume worst-case: 100 GPUs ramping from idle to full load simultaneously (C = 1.0)
2. Calculate ΔP_cluster = C × N × ΔP_gpu
3. Calculate RoCoF = -ΔP_cluster / (2 × H_eff × S_base)
4. Calculate ΔF = -R_eff × (ΔP_cluster / P_rated)
5. Iterate N until RoCoF < RoCoF_limit AND |ΔF| < ΔF_limit

**Expected Output**: Maximum safe GPU count per generator model, risk classification (GREEN/YELLOW/RED)

---

**Question 3.2**: What are the risk zones (GREEN/YELLOW/RED) for GPU ramp rates?

**Risk Classification Framework** (based on ramp rates, not BESS presence):
- **GREEN**: Safe operation with shaped ramps, no BESS required
  - GPU ramp rate < 50% of generator max ramp rate
  - GPU step size < 50% of generator max step size
  - Margin of safety > 2x
  - Example: 1 MW gen, 20 kW/s max ramp → <10 GPUs/second (SXM) is GREEN
  
- **YELLOW**: Caution, tighter scheduler control required
  - GPU ramp rate 50-80% of generator max ramp rate
  - GPU step size 50-80% of generator max step size
  - Margin of safety 1.25-2x
  - Miner coordination recommended for faster ramps
  
- **RED**: Unsafe, reduce ramp rate or add BESS
  - GPU ramp rate > 80% of generator max ramp rate
  - GPU step size > 80% of generator max step size
  - Margin of safety < 1.25x
  - Requires slower ramps OR small BESS buffer

**Expected Output**: Risk classification matrix (GPU ramp rate × Generator model → GREEN/YELLOW/RED)

---

### 3.4 Scheduler Design & Miner Coordination (HIGH PRIORITY)

**Question 4.1**: What are the maximum GPU ramp rates (GPUs per second) that respect generator step/ramp limits?

**Required Calculations**:
- Maximum safe step size (kW) per generator model
- Maximum safe ramp rate (kW/s) per generator model
- GPU power per step (0.7 kW for SXM, 0.35 kW for PCIe)
- Maximum GPUs per step = MaxStep_kW / Power_per_GPU
- Maximum GPUs per second = MaxRamp_kW_per_s / Power_per_GPU

**Calculation Example** (1 MW generator, 20% max step, 20 kW/s max ramp):
- Max step = 200 kW
- Max GPUs per step = 200 kW / 0.7 kW = ~285 GPUs (SXM) or 571 GPUs (PCIe)
- Max ramp = 20 kW/s
- Max GPUs per second = 20 kW/s / 0.7 kW = ~28 GPUs/s (SXM) or 57 GPUs/s (PCIe)

**Expected Output**: Maximum GPU ramp rates (GPUs per step, GPUs per second) for each generator model

---

**Question 4.2**: How should GPU scheduler implement shaped ramps?

**Required Design**:
- Batch size selection (how many GPUs change state at once)
- Timing between batches (seconds between steps)
- Preload → full-power phase transitions (controlled ramp, not instant)
- Checkpoint/hold points in job pipeline
- Power cap ramping (30% → 100% in steps)

**Design Principles**:
- Never allow large instantaneous steps (e.g., 100 GPUs jumping 30% → 100% simultaneously)
- Stage GPU power changes in small increments
- Insert brief pauses between phases to allow generator to stabilize
- Coordinate with miner control (if miners present)

**Expected Output**: Scheduler design rules and algorithms for shaped ramps

---

**Question 4.3**: How should miner coordination work with GPU ramps?

**Required Analysis**:
- Miner shedding strategies (pre-emptive vs reactive)
- Coordination timing (how precisely can miners match GPU steps?)
- Miner response time (how fast can miners turn on/off?)
- Net load control (keeping P_gen constant vs allowing small ramps)
- Miner flexibility limits (minimum miner load, granularity)

**Control Strategies**:
- **Path A**: Let generator ramp (no miner changes, slower but simpler)
- **Path B**: Keep generator flat (shed miners as GPUs ramp, faster but more complex)
- **Path C**: Hybrid (mix of both strategies)

**Expected Output**: Miner coordination strategies and control algorithms

---

### 3.5 BESS as Optional Enhancement (LOW PRIORITY)

**Question 5.1**: When might a small BESS still be beneficial despite not being required?

**Potential Benefits** (even if not strictly required):
- **Easier to build and tune**: Simpler control logic, more forgiving of misconfigurations
- **Easier to operate**: Less exposure to "close to limit" conditions
- **Reliability**: Ride-through for electrical faults, engine hiccups
- **Codes compliance**: May be required by local codes/standards
- **Bootstrap buffer**: Cover "first wave" of GPUs with zero drama

**Research Questions**:
- What size BESS (kWh, kW) provides meaningful benefit without being oversized?
- Cost-benefit analysis: Small BESS + simpler controls vs No BESS + complex controls
- When is BESS actually cheaper in total lifecycle cost?

**Expected Output**: BESS as optional enhancement analysis (not core requirement)

---

### 3.5 Integration Scenarios (LOW PRIORITY)

**Question 5.1**: How do multiple GPU clusters affect generator stability?

**Required Analysis**:
- Correlation between clusters: Are power steps synchronized across clusters?
- Worst-case: All clusters ramp simultaneously
- Best-case: Power steps are staggered/uncorrelated
- Scheduler coordination: Can clusters coordinate ramps to stay within generator limits?
- Impact on ramp rate limits: Do multiple clusters require slower individual ramp rates?

**Expected Output**: Multi-cluster stability analysis and scheduler coordination strategies

---

**Question 5.2**: How does generator load level affect stability?

**Required Analysis**:
- Does generator stability improve or degrade at partial load?
- Typical operation: Generator at 50-80% load with GPU clusters
- Headroom for power steps: More headroom = better stability?
- Efficiency trade-offs: Higher load = better efficiency but less headroom

**Expected Output**: Stability analysis across generator load levels (20%, 50%, 80%, 100%)

---

## 4. EXPECTED DELIVERABLES

### 4.1 Initial Deliverable (For Review)

**File**: `research/generator-integration/research-findings.md` (or `research-findings-initial.md`)

**Purpose**: Structured findings document for review before final formatting

**Contents**:
- **Parameter Tables**: 
  - Generator parameters (H_eff, R_eff, RoCoF limits, ΔF limits) with values, units, sources, confidence levels
  - GPU power characteristics (idle, loading, inference, ramp rates) with values, units, sources, confidence levels
- **Data Gaps Documentation**: 
  - Missing parameters explicitly listed
  - Assumptions clearly stated with justification
  - Conservative estimates used when data unavailable
- **Key Calculations**: 
  - Formulas with worked examples
  - Methodology validation
  - Example: Maximum safe GPU count calculation for G3520 generator
- **Literature Review Summary**: 
  - Sources found (20+ target)
  - URLs and citations
  - Key findings from each source
  - Source quality assessment
- **Confidence Assessment**: 
  - Confidence level for each parameter (50%, 65%, 75%, 85%, 95%)
  - Justification for each confidence level
  - Risk assessment for low-confidence parameters
- **Recommendations**: 
  - Next steps for empirical validation
  - Additional research needed
  - Assumptions requiring validation

**Review Criteria**:
- Are all critical parameters present?
- Are confidence levels appropriate?
- Are assumptions reasonable and conservative?
- Are data gaps acceptable for modeling purposes?
- Should any parameters be re-researched before final documentation?

### 4.2 Final Deliverables (After Review/Approval)

**File 1**: `models/gpu-generator-stability/stability-model.md`
- Generator parameter table (H_eff, R_eff, RoCoF limits, ΔF limits) for all models
- GPU power characterization table (idle, loading, inference, ramp rates)
- Maximum GPU ramp rates (GPUs per step, GPUs per second) per generator model
- Risk classification matrix (GREEN/YELLOW/RED) based on ramp rates
- Stability calculation methodology and formulas
- Example calculations: 100 PCIe GPU cluster ramp on G3520 generator
- **Format**: Full formatted markdown document ready for project use

**File 2**: `models/gpu-generator-stability/bess-sizing.md`
- BESS capacity requirements (kWh) by GPU cluster size and generator model
- BESS power rating requirements (kW) by GPU cluster size
- BESS response time requirements and specifications
- BESS cost estimates (if available)
- Trade-off analysis: BESS size vs generator headroom
- **Format**: Full formatted markdown document ready for project use

**File 3**: `models/gpu-generator-stability/research-findings.md` (Final Version)
- Literature review summary (expanded from initial findings)
- Source citations and URLs (complete bibliography)
- Data gaps and assumptions documented (final status)
- Confidence levels for each parameter (validated)
- Recommendations for empirical validation (prioritized)
- **Format**: Comprehensive research documentation

### 4.2 Secondary Deliverables

**File 4**: `models/gpu-generator-stability/parameter-database.csv`
- Structured data table: Generator model × Parameter × Value × Source × Confidence

**File 5**: `models/gpu-generator-stability/calculation-examples.md`
- Step-by-step worked examples
- Edge cases and boundary conditions
- Sensitivity analysis (what if H_eff is 10% higher?)

---

## 5. RESEARCH METHODOLOGY

### 5.1 Source Priority

**Tier 1 (Highest Priority)**:
- Caterpillar technical documentation (data/generators/caterpillar/)
- NVIDIA power management white papers
- IEEE standards for generator protection and frequency regulation
- Industry application guides (Caterpillar, Cummins, etc.)

**Tier 2 (High Priority)**:
- Academic papers on generator stability, GPU power profiling
- Industry benchmarks (Lambda Labs, Hyperstack, RunPod)
- BESS manufacturer specifications (Tesla, Fluence, etc.)

**Tier 3 (Medium Priority)**:
- Community discussions (GitHub, Reddit, forums)
- Engineering handbooks and textbooks
- Cross-referencing with similar generator models

### 5.2 Confidence Levels

**95% Confidence**: Parameters from manufacturer specifications or IEEE standards
**85% Confidence**: Parameters from peer-reviewed academic sources
**75% Confidence**: Parameters from industry benchmarks or application guides
**65% Confidence**: Parameters estimated from similar models or engineering calculations
**50% Confidence**: Conservative assumptions when data unavailable

### 5.3 Documentation Standards

- All parameters must include: Value, Units, Source, Confidence Level
- All calculations must show: Formula, Input values, Output values, Units
- All assumptions must be explicitly stated
- All data gaps must be documented with recommended next steps

---

## 6. CRITICAL ASSUMPTIONS TO VALIDATE

### 6.1 GPU Power Assumptions (Currently Unvalidated)

1. **Correlation Coefficient (C)**: Assumed 0.3-0.7 for typical workloads, 1.0 for worst-case
   - **Validation Needed**: Empirical measurement on multi-GPU cluster

2. **Power Ramp Rate**: Assumed 50-200 kW/s for 100-GPU cluster
   - **Validation Needed**: Measure actual ramp rates during model loading

3. **Idle Power**: Assumed 50-100W per PCIe GPU
   - **Validation Needed**: Measure with nvidia-smi on idle H100 PCIe

4. **Sustained Inference Power**: Assumed 250-300W per PCIe GPU (70-85% of TDP)
   - **Validation Needed**: Measure during sustained inference workloads

### 6.2 Generator Assumptions (Currently Unvalidated)

1. **H_eff Conversion**: Assumed formula H = J × ω² / (2 × S_base) is correct
   - **Validation Needed**: Cross-reference with generator engineering literature

2. **RoCoF Limits**: Assumed 0.5-2.0 Hz/s if not found
   - **Validation Needed**: Find actual protection relay settings or manufacturer specs

3. **Governor Droop**: Assumed 5% (0.05 p.u.) if not found
   - **Validation Needed**: Extract from Caterpillar control system documentation

---

## 7. SUCCESS CRITERIA

### 7.1 Minimum Viable Deliverable

- [ ] H_eff (seconds) calculated for at least 3 generator models
- [ ] RoCoF limits determined for at least 3 generator models
- [ ] Maximum safe GPU count calculated for at least 1 generator model (G3520 recommended)
- [ ] BESS sizing calculated for 100 PCIe GPU cluster on G3520 generator
- [ ] Risk classification framework implemented
- [ ] All assumptions documented with confidence levels

### 7.2 Complete Deliverable

- [ ] All 6 generator models fully characterized
- [ ] GPU power profiles documented (even if estimated)
- [ ] Ramp rate limits validated with example calculations
- [ ] Scheduler design algorithms documented and validated
- [ ] Miner coordination strategies fully specified
- [ ] BESS optional analysis completed (if researched)
- [ ] Literature review complete with 20+ sources
- [ ] All data gaps documented with research recommendations

---

## 8. REFERENCES & CONTEXT FILES

### 8.1 Key Project Documents

- **H100 Economics Analysis**: `research/inference-economics/h100-deployment-economics/H100-CONSOLIDATED-ANALYSIS.md`
  - Section 3.4: Off-grid deployment decision framework
  - Section 6.2: Required generator-GPU integration research
  - Section 7: Authoritative claims (95% confidence verified)

- **Caterpillar Generator Analysis**: `data/generators/caterpillar/Caterpillar-Technical-Analysis.md`
  - Section 7.2: Consolidated data table with generator parameters
  - Section 7.3: JSON dataset with structured parameters

- **Glossary**: `docs/GLOSSARY.md`
  - Generator terminology (H_eff, RoCoF, R_eff, etc.)
  - GPU power dynamics terminology
  - Standardized units and symbols

- **Generator Risk Calculator**: `models/generator-risk-calculator/GeneratorRisk-v1.csv`
  - Existing formulas and calculation framework
  - Risk classification (GREEN/YELLOW/RED)

### 8.2 Key Citations from H100 Analysis

- Hardware specifications: [22][25][2][34][35][36]
- Performance benchmarks: [56] MLPerf, [57] Argonne LLM-Inference-Bench
- Power efficiency: Verified at 95% confidence
- TCO calculations: PRICING-PUZZLE case study methodology

---

## 9. RESEARCH TIMELINE & EXECUTION STRATEGY

### 9.1 Phase Priority

**RECOMMENDED EXECUTION ORDER**:

1. **Phase 1: Generator Parameter Extraction** (4-6 hours) - **START HERE**
   - Extract generator parameters from Caterpillar docs
   - Convert kg⋅m² to H (seconds)
   - Research RoCoF limits and frequency tolerance
   - **Rationale**: Foundational data required for all stability calculations

2. **Phase 2: GPU Power Characterization** (6-8 hours) - **PARALLEL OR IMMEDIATELY AFTER PHASE 1**
   - Literature search for H100 power profiles
   - Research GPU power control capabilities (power capping, staging)
   - Document assumptions and data gaps
   - **Rationale**: Can proceed in parallel with Phase 1 (no dependencies)

3. **Phase 3: Stability Calculations** (4-6 hours) - **AFTER PHASES 1 & 2 COMPLETE**
   - Implement stability formulas
   - Calculate maximum GPU ramp rates (GPUs per step, GPUs per second)
   - Create risk classification matrix (based on ramp rates, not BESS)
   - **Rationale**: Requires generator parameters from Phase 1 and GPU power data from Phase 2

4. **Phase 4: Scheduler Design & Miner Coordination** (4-6 hours) - **AFTER PHASE 3 COMPLETE**
   - Design GPU scheduler algorithms for shaped ramps
   - Design miner coordination strategies
   - Document power-aware job design principles
   - **Rationale**: Requires ramp rate limits from Phase 3

**Phase 4b: BESS Optional Analysis** (2-3 hours) - **OPTIONAL, AFTER PHASE 4**
   - Analyze when small BESS might be beneficial (not required)
   - Cost-benefit analysis: BESS vs complex controls
   - Small BESS sizing (if used): seconds to tens of seconds buffer
   - **Rationale**: Optional enhancement, not core requirement

5. **Phase 5: Documentation** (2-4 hours) - **FINAL PHASE**
   - Write stability model document
   - Write BESS sizing document
   - Create parameter database
   - Document research findings
   - **Rationale**: Final formatting and consolidation

**Total Estimated Time**: 20-30 hours

### 9.2 Output Format Strategy

**INITIAL DELIVERABLE**: Structured findings document for review

**File**: `research/generator-integration/research-findings.md` (or `research-findings-initial.md`)

**Contents**:
- **Parameter Tables**: Generator and GPU parameters with values, units, sources, confidence levels
- **Data Gaps**: Explicitly documented missing parameters and assumptions
- **Key Calculations**: Formulas with worked examples showing methodology
- **Literature Review**: Summary of sources found, URLs, key findings
- **Confidence Assessment**: Confidence level for each parameter with justification
- **Recommendations**: Next steps for empirical validation or additional research

**Purpose**: 
- Validate data quality and assumptions before committing to full formatted documents
- Allow feedback on data gaps and confidence levels
- Enable iteration on findings before final documentation
- Provide clear audit trail of research process

**AFTER REVIEW/APPROVAL**: Produce full formatted deliverables

**Files**:
- `models/gpu-generator-stability/stability-model.md` (full formatted document)
- `models/gpu-generator-stability/scheduler-design.md` (full formatted document)
- `models/gpu-generator-stability/bess-optional-analysis.md` (optional, if BESS research conducted)
- `models/gpu-generator-stability/parameter-database.csv` (structured data)
- `models/gpu-generator-stability/calculation-examples.md` (worked examples)

**Benefits of This Approach**:
- Ensures data quality before final documentation
- Allows course correction if assumptions are incorrect
- Provides clear path from research → review → final deliverables
- Maintains research transparency and auditability

---

## 10. NEXT STEPS AFTER RESEARCH COMPLETE

1. **Empirical Validation** (if hardware access available):
   - Benchmark H100 PCIe power profiles
   - Measure GPU power correlation
   - Test generator frequency response

2. **Model Refinement**:
   - Update stability model with empirical data
   - Refine scheduler design rules with actual GPU power measurements
   - Validate ramp rate limits and risk classifications

3. **Integration with Economics Model**:
   - Add optional BESS costs to off-grid TCO calculations (if BESS chosen)
   - Update deployment recommendations with ramp rate constraints
   - Create complete off-grid deployment decision framework with scheduler requirements

---

## 11. OPERATING MODEL CLARIFICATION

### 11.1 Core Principle: Shaped Ramps, No BESS Required

**Key Operating Model** (from project convergence):
- **1 MW generator** feeding **0.5 MW ASIC miners** (flexible ballast) + **0.5 MW H100 GPUs**
- GPUs brought online in **small batches** (1-10 GPUs at a time)
- Generator sees only **tiny steps** (single H100 = 0.7 kW = 0.07% of 1 MW generator)
- **Optional miner shedding** to keep net load flat (swap miners for GPUs in equal kW chunks)
- **No BESS required** for GPU ramp control (generator inertia + shaped ramps sufficient)

### 11.2 Control Strategies

**Path A - Generator Ramp (No Miner Changes)**:
- Start: P_gen = 500 kW, P_miner = 500 kW, P_gpu = 0
- Turn on GPUs in small batches (e.g., 1 GPU every X seconds)
- Let generator ramp up: P_gen increases to cover new GPUs
- Eventually: P_gen = 1000 kW, P_miner = 500 kW, P_gpu = 500 kW
- **No BESS required**, just patience and shaped ramps

**Path B - Keep Generator Flat (Miner Shedding)**:
- Start: P_gen = 1000 kW, P_miner = 1000 kW, P_gpu = 0
- Turn on GPUs in small batches, simultaneously shed equivalent miner kW
- Net load stays constant: P_gen = 1000 kW
- Eventually: P_gen = 1000 kW, P_miner = 500 kW, P_gpu = 500 kW
- **No BESS required**, just coordinated control

**Path C - Hybrid**:
- Mix of generator ramping and miner shedding
- Optimize for speed (miner shedding) or simplicity (generator ramp)

### 11.3 BESS as Optional Enhancement

BESS is **NOT required** for GPU ramp control, but may still be beneficial for:
- **Reliability**: Ride-through for electrical faults, engine hiccups
- **Codes compliance**: May be required by local standards
- **Easier operation**: More forgiving of misconfigurations
- **Cost-benefit**: Small BESS + simpler controls vs No BESS + complex controls

If BESS is used, it should be **small** (50-200 kWh, seconds to tens of seconds buffer), not large energy storage.

### 11.4 Research Focus

This research should focus on:
1. **Generator step/ramp limits** (not BESS sizing)
2. **Scheduler design** (batch sizes, timing)
3. **Miner coordination** (optional, for faster ramps)
4. **BESS optional analysis** (cost-benefit, not requirement)

---

**END OF RESEARCH PROMPT**

