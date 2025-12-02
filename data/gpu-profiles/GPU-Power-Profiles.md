# GPU POWER PROFILES - DOCUMENTATION

**Version:** 2.1  
**Last Updated:** 2025-12-02  
**Status:** Updated with consolidated research findings from 4 independent research efforts  
**Primary Source:** `research/gpu-phase-research/CONSOLIDATED-SUMMARY.md`

---

## Purpose

This document consolidates GPU power characteristics for H100 (PCIe and SXM) based on research findings and manufacturer specifications. **These are modeling assumptions** suitable for construction planning and partner selection. Empirical validation with real-world measurements is planned for future phases but is not required for current planning purposes.

---

## H100 PCIe Power Specifications

### Manufacturer Specifications

| Parameter | Value | Source |
|-----------|-------|--------|
| **TDP (Total Board Power)** | 350 W (default/maximum) | `docs/nvidia-manuals/H100-PCIe-Product-Brief-PB-11133.pdf` |
| **Power Mode (300W sense-pin)** | 310 W (down-rated) | `docs/nvidia-manuals/H100-PCIe-Product-Brief-PB-11133.pdf` |
| **Memory** | 80GB HBM2e | `docs/nvidia-manuals/H100-PCIe-Product-Brief-PB-11133.pdf` |
| **Memory Bandwidth** | 2.0 TB/s | `docs/nvidia-manuals/H100-PCIe-Product-Brief-PB-11133.pdf` |

### Power Management APIs (NVML)

**Reference:** `docs/nvidia-manuals/NVML-API-Reference-Guide.pdf`

The NVIDIA Management Library (NVML) provides APIs for power management and monitoring:

**Key Power Management Functions:**
- `nvmlDeviceSetPowerManagementLimit()` - Set power cap limit (in milliwatts)
- `nvmlDeviceGetPowerManagementLimitConstraints()` - Get min/max power limits
- `nvmlDeviceGetPowerUsage()` - Get current power consumption
- `nvmlDeviceGetPowerManagementLimit()` - Get current power limit setting

**Power Capping Capabilities:**
- Dynamic power limit adjustment during runtime
- Per-GPU power control
- Power limit constraints based on hardware capabilities
- Thermal monitoring integration

**Note:** NVML provides the **tools** (APIs) for power management, but does not provide **empirical power profiles** for inference workloads. Power profile values in this document remain modeling assumptions requiring empirical validation.

### Monitoring APIs (DCGM)

**Reference:** `docs/nvidia-manuals/NVIDIA-DCGM-User-Guide.md`

The NVIDIA Data Center GPU Manager (DCGM) provides fleet-wide monitoring and management:

**Key Monitoring Capabilities:**
- Fleet-wide GPU power monitoring
- Power usage tracking and logging
- Health checks and diagnostics
- Performance metrics collection
- Integration with orchestration systems

**Use Cases:**
- Monitor cluster-level power consumption
- Track power-aware scheduler behavior
- Diagnose power-related issues
- Collect power traces for analysis

**Note:** DCGM provides **monitoring tools** but does not provide **empirical power profiles** for inference workloads. Power profile values in this document remain modeling assumptions requiring empirical validation.

### Power Profile (Inference Workloads) - Refined Estimates

**Status:** ✅ **REFINED ESTIMATES** - Based on validated research data (steady-state inference) and workload characteristics (phase transitions)

**Validation Status:**
- ✅ **Steady-State Inference:** Validated from academic research (50-80% of TDP)
- ⚠️ **Phase Transitions:** Inferred from workload characteristics and validated steady-state
- ⚠️ **Idle Power:** Refined estimate based on research (not directly measured)

| Phase | Estimated Power | Duration | Confidence | Notes |
|-------|----------------|----------|------------|-------|
| **Idle (Cold)** | 35-45 W | Continuous | Medium | System powered, no model loaded (from consolidated research) |
| **Idle (Warm)** | 60-80 W | Continuous | **High** | Model loaded, KV cache active (✅ validated from multiple sources) |
| **Launch** | 85-140 W | <1 s | Medium | Inferred: 30-50% of inference (system overhead) |
| **Model Load** | 170-200 W | 10-60 s | Medium | Inferred: 60-70% of inference (memory-intensive, gradual ramp) |
| **Warmup** | 300-350 W | 10-60 s | Medium-High | ⚠️ **Hidden danger** - Sustained near-peak (86-100% of TDP) |
| **Prefill** | 300-330 W | 200-500 ms | **High** | Compute-bound spike (86-94% of TDP, ✅ validated) |
| **Decode (Steady-State)** | 220-260 W | Continuous | **High** | ✅ **VALIDATED** - Memory-bound plateau (63-74% of TDP) |
| **Peak** | 310-350 W | Rare | **High** | Hard ceiling, rarely reached (89-100% of TDP) |
| **Cleanup** | 85-200 W | 1-5 s | Medium | Inferred: Resource de-allocation |
| **Teardown** | 60-100 W | 1-3 s | Medium | Inferred: Final shutdown |

### Power Step Estimates (Refined)

| Transition | ΔP (per GPU) | Ramp Rate | Duration | Confidence | Notes |
|-----------|--------------|-----------|----------|------------|-------|
| **Idle → Prefill** | +0.15-0.25 kW | 10 kW/s (cluster) | 150-250 ms | Medium-High | ⚠️ Critical transition - rapid ramp |
| **Idle → Launch** | +0.05-0.10 kW | Gradual | <1 s | Medium | System initialization |
| **Launch → Model Load** | +0.03-0.06 kW | Gradual | 1-10 s | Medium | Memory-intensive, gradual ramp |
| **Model Load → Warmup** | +0.10-0.18 kW | 3-4 kW/s (per-GPU) | 1-5 s | Medium | ⚠️ Significant step - warmup is "hidden danger" |
| **Warmup → Decode** | -0.05 to -0.10 kW | Gradual | 200-500 ms | Medium | Prefill spike → steady decode |
| **Decode → Idle** | -0.15 to -0.20 kW | <50 ms (instant) | <50 ms | **High** | ⚠️ Instant drop - load rejection risk |
| **Inference → Cleanup** | -0.08 to -0.20 kW | <50 ms | 50-500 ms | Medium | Resource de-allocation |
| **Cleanup → Idle** | -0.03 to -0.12 kW | <50 ms | 50-500 ms | Medium | Final shutdown |

**Key Assumption (Refined):** Per-GPU power step during warmup phase: **0.2-0.25 kW** (refined from 0.6 kW based on validated inference power levels)

**Previous Assumption:** 0.6 kW (conservative, may overestimate)
**Refined Estimate:** 0.2-0.25 kW (more realistic based on validated steady-state inference: 220-260W decode vs. idle: 60-80W = 140-200W step)

**⚠️ Critical Finding from Consolidated Research:**
- **Warmup phase is "hidden danger"** - Sustained 300-350W (86-100% of TDP) for 10-60 seconds
- Most likely phase to trigger generator overload
- Power step from idle to warmup: **0.24-0.29 kW** (300-350W - 60-80W)
- Conservative design should use **0.25-0.30 kW** for warmup step calculations

---

## H100 SXM Power Specifications

### Manufacturer Specifications

| Parameter | Value | Source |
|-----------|-------|--------|
| **TDP (Total Board Power)** | 700 W (maximum) | `docs/nvidia-manuals/NVIDIA H100 GPU Whitepaper.pdf` |
| **Memory** | 80GB HBM3 | `docs/nvidia-manuals/NVIDIA H100 GPU Whitepaper.pdf` |
| **Memory Bandwidth** | 3.35 TB/s | `docs/nvidia-manuals/NVIDIA H100 GPU Whitepaper.pdf` |

### Power Profile (Inference Workloads) - Modeling Assumptions

**Status:** ✅ **MODELING ASSUMPTIONS** - Based on PCIe estimates scaled by TDP ratio (2:1), suitable for planning

| Phase | Estimated Power | Duration | Notes |
|-------|----------------|----------|-------|
| **Idle** | 60-120 W | Continuous | Estimated (2× PCIe idle) |
| **Launch** | 200-300 W | 1-5 s | Job initialization |
| **Model Load** | 400-600 W | 10-60 s | Loading weights |
| **Warmup** | 600-700 W | 5-30 s | Initial inference passes |
| **Steady-State Inference** | 500-700 W | Continuous | Sustained inference |
| **Cleanup** | 300-400 W | 1-5 s | De-allocation |
| **Teardown** | 100-200 W | 1-3 s | Final shutdown |

### Power Step Estimates

| Transition | ΔP (per GPU) | Transition Time | Notes |
|-----------|--------------|-----------------|-------|
| Idle → Launch | 100-240 W | 50-500 ms | Sharp step |
| Launch → Model Load | 200-400 W | 1-10 s | Gradual ramp |
| Model Load → Warmup | 100-200 W | 1-5 s | Moderate step |
| Warmup → Inference | 0-100 W | 1-10 s | Stabilization |
| Inference → Cleanup | -200 to -400 W | 50-500 ms | Sharp drop |
| Cleanup → Idle | -100 to -300 W | 50-500 ms | Moderate drop |

**Key Assumption:** Per-GPU power step during warmup phase: **1.2 kW** (2× PCIe, used in calculator scenarios)

---

## Cluster-Level Power Dynamics

### Correlation Coefficients

**Status:** ✅ **MODELING ASSUMPTIONS** - Based on research findings, suitable for planning and risk assessment

| Scenario | Estimated Correlation (C) | Confidence | Notes |
|----------|--------------------------|------------|-------|
| **Tensor Parallelism** | 0.9-1.0 | Medium-High | Worst-case - all GPUs synchronized (✅ validated) |
| **Synchronous Warmup** | 0.7-0.9 | Medium-High | Many GPUs starting simultaneously (worst case) |
| **General Inference** | 0.5-0.7 | Medium | Typical operation range (✅ validated) |
| **Batch Inference** | 0.5-0.7 | Medium | Similar workloads scheduled together |
| **Pipeline Parallelism** | 0.3-0.5 | Medium | Partial synchronization (✅ validated) |
| **Data Parallelism** | 0.3-0.5 | Medium | Independent processing (✅ validated) |
| **Staggered Launch** | 0.3-0.5 | Medium | Scheduler spreads transitions over time |
| **Random Workloads** | 0.1-0.3 | Low | Independent job scheduling |

**Current Calculator Assumption:** C = 0.8 for worst-case scenarios

**✅ Validated from Consolidated Research:**
- **Conservative design:** C = 0.9-1.0 (Tensor Parallelism worst-case)
- **Typical operation:** C = 0.5-0.7 (General Inference)
- **Best-case:** C = 0.3-0.5 (Data Parallelism)

**Recommendation:** Use C = 0.9 for conservative generator design (worst-case Tensor Parallelism)

### Cluster Power Step Calculation

```
ΔP_cluster = C × N × ΔP_gpu
```

**Example:**
- 1024 GPUs × 0.6 kW × 0.8 correlation = **491.52 kW** cluster step

### Ramp Rate Calculation

```
RampRate = ΔP_cluster / Δt_event
```

**Example:**
- 491.52 kW ÷ 1 s = **491.52 kW/s** ramp rate

---

## Measurement Limitations

### nvidia-smi / NVML Limitations

**Critical Finding:** nvidia-smi under-samples power on A100 and H100 GPUs:

- **Sampling Rate:** Only 25% of runtime is sampled
- **Sampling Window:** 25 ms window every 100 ms
- **Impact:** Fast transients (<100 ms) are not accurately captured
- **Implication:** Cannot rely on nvidia-smi for sub-second power transients relevant to generator stability

### Recommended Measurement Approach

**For accurate power profiling:**
1. **External Power Meter:** Yokogawa WT5000 or similar (<10 ms sampling)
2. **Phase-Shifting Techniques:** Micro-benchmarking to recover accurate short-term statistics
3. **Multiple Measurement Points:** Node-level, rack-level, and cluster-level monitoring
4. **Validation:** Cross-reference with nvidia-smi for steady-state values only

---

## Research Findings Summary

### From GPU-Generator Stability Research

1. **Training vs Inference:**
   - Training workloads: ~76% of rated node TDP on average
   - Inference workloads: Estimated 50-80% of TDP depending on utilization
   - **Pattern:** Real workloads rarely sustain 100% of TDP over long windows

2. **Power Fluctuations:**
   - Large GPU clusters can cause "power fluctuations of hundreds of megawatts within only seconds"
   - Per-rack power can range from 30 to 100+ kW with abrupt changes
   - Workloads are bursty and hard to predict, especially in interactive inference

3. **Scheduler Impact:**
   - Schedulers often co-schedule similar work on many GPUs (increases correlation)
   - Queueing effects and cooling-aware scheduling can desynchronize activity
   - Without mitigation, large correlated ramps are realistic

---

## Validation Status and Future Work

### Current Validation Status

**✅ Validated (High Confidence):**
- **Steady-state decode power:** 220-260W (63-74% of TDP) - ✅ Validated from multiple sources
- **Prefill power:** 300-330W (86-94% of TDP) - ✅ Validated
- **Warm idle power:** 60-80W (17-23% of TDP) - ✅ Validated from multiple sources
- **TDP:** 350W PCIe, 700W SXM - Manufacturer specifications
- **Peak power:** 310-350W (89-100% of TDP) - ✅ Validated

**⚠️ Refined Estimates (Medium-High Confidence):**
- **Warmup power:** 300-350W (86-100% of TDP) - ⚠️ **Hidden danger** - Sustained near-peak for 10-60s
- **Cold idle power:** 35-45W (10-13% of TDP) - Inferred from A100 data
- **Model loading power:** 170-200W (49-57% of TDP) - Inferred from workload characteristics
- **Power steps:** 0.2-0.25 kW (refined from 0.6 kW) - Based on validated inference power
- **Ramp rates:** 0.8-1.5 kW/s (per-GPU typical), 10 kW/s (cluster synchronized) - Disagreement exists, use 10 kW/s for conservative design

**❌ Still Needs Measurement (Low Confidence):**
- **Exact cold idle power** - Direct H100 measurement needed (currently inferred from A100)
- **Phase transition timing** - Power traces needed for exact durations
- **Ramp rates** - Disagreement exists (0.8-1.5 kW/s vs 10 kW/s) - External metering needed to resolve
- **Model-specific variations** - Power profiles for different model sizes (7B vs 70B)
- **Framework-specific profiles** - vLLM vs TGI vs TensorRT-LLM comparisons

### Planned Empirical Validation

**Note:** MLPerf and academic paper research is in progress (see `docs/MLPERF-ACADEMIC-VALIDATION-PLAN.md`). Post-construction validation with direct measurements is planned.

| Parameter | Current Refined Estimate | Confidence | Future Validation Method |
|-----------|------------------------|------------|-------------------------|
| **H100 PCIe idle (warm)** | 60-80W | **High** | ✅ Validated from multiple sources |
| **H100 PCIe idle (cold)** | 35-45W | Medium | Inferred from A100 data, direct measurement needed |
| **H100 PCIe power step** | 0.2-0.25 kW (idle→inference) | Medium-High | Based on validated inference (220-260W) vs idle (60-80W) |
| **Steady-state decode** | 220-260W | **High** | ✅ Validated from multiple sources |
| **Prefill power** | 300-330W | **High** | ✅ Validated |
| **Warmup power** | 300-350W | Medium-High | ⚠️ Hidden danger - sustained near-peak |
| **Model loading power** | 170-200W | Medium | Inferred from workload characteristics |
| **Multi-GPU correlation** | 0.3-0.7 (typical), 0.9-1.0 (worst-case) | Medium-High | ✅ Validated ranges from research |
| **Ramp rates (kW/s)** | 0.8-1.5 kW/s (per-GPU), 10 kW/s (cluster) | Medium | Disagreement exists - use 10 kW/s for conservative design |

### Future Measurement Plan

1. **Deploy external power metering** on H100 systems post-construction
2. **Measure power profiles** for:
   - Idle state
   - Model load phase
   - KV-cache warmup
   - Steady decode
   - Batch-size changes
3. **Compute empirical correlation coefficients** across GPUs and nodes
4. **Validate nvidia-smi limitations** with external metering
5. **Refine modeling assumptions** based on empirical data

---

## Usage in Calculator

### Current Calculator Assumptions (Updated)

The generator risk calculator uses these estimated values:

| Parameter | Value Used | Refined Estimate | Source | Notes |
|-----------|-----------|------------------|--------|-------|
| **ΔP_gpu (PCIe)** | 0.6 kW | **0.2-0.25 kW** | Refined estimate | Previous: Conservative overestimate. Refined: Based on validated inference (250-280W) vs. idle (60-80W) |
| **ΔP_gpu (SXM)** | 1.2 kW | **0.4-0.5 kW** | Refined estimate (2× PCIe) | Scaled from PCIe refined estimate |
| **Correlation (C)** | 0.8 | 0.3-0.7 (typical) | Research-based | Current: Worst-case. Refined: Typical operation range from research |
| **Transition Time (Δt)** | 1-30 s | 1-30 s | Workload-based | No change |

**Recommendation:** Update calculator to use refined estimate (0.2-0.25 kW) for more realistic modeling, while keeping 0.6 kW as worst-case conservative bound.

### Calculator Scenarios

**Scenario 1: G3520 Fast Response + GPU Warmup (Current Assumption)**
- 1024 GPUs × 0.6 kW × 0.8 correlation = 491.52 kW
- G3520 (4000 kW, 100% block load capable)
- Result: **GREEN** - 12.3% step, well within limits

**Scenario 1 (Refined Estimate):**
- 1024 GPUs × 0.225 kW × 0.8 correlation = 184.32 kW
- G3520 (4000 kW, 100% block load capable)
- Result: **GREEN** - 4.6% step, well within limits (more realistic)

**Scenario 2: CG260-16 + GPU Warmup (Current Assumption)**
- Same GPU configuration (491.52 kW)
- CG260 (4300 kW, 16% max first step)
- Result: **GREEN** - 11.4% step, within first step limit

**Scenario 2 (Refined Estimate):**
- 1024 GPUs × 0.225 kW × 0.8 correlation = 184.32 kW
- CG260 (4300 kW, 16% max first step)
- Result: **GREEN** - 4.3% step, well within limits (more realistic)

**Note:** Refined estimates show significantly lower power steps, indicating current assumptions are conservative. This provides additional safety margin but may lead to over-engineering.

---

## References

1. **NVIDIA H100 Specifications:** 
   - `docs/nvidia-manuals/H100-PCIe-Product-Brief-PB-11133.pdf` - H100 PCIe technical specifications
   - `docs/nvidia-manuals/NVIDIA H100 GPU Whitepaper.pdf` - H100 architecture and specifications
2. **Power Management APIs:**
   - `docs/nvidia-manuals/NVML-API-Reference-Guide.pdf` - NVML API for power capping and monitoring
3. **Monitoring APIs:**
   - `docs/nvidia-manuals/NVIDIA-DCGM-User-Guide.md` - DCGM for fleet-wide GPU monitoring
4. **GPU Phase Research (Consolidated):** `research/gpu-phase-research/CONSOLIDATED-SUMMARY.md` - ✅ **Primary source** - Validated parameters from 4 independent research efforts
5. **GPU-Generator Stability Research:** `research/gpu-generator-stability/GPU-GENERATOR-STABILITY-CONSOLIDATED-ANALYSIS.md`
6. **Perplexity Research Findings:** `research/gpu-generator-stability/perplexity-research/research-findings.md`
7. **Remaining Research Gaps:** `research/REMAINING-RESEARCH-GAPS.md`

**Note:** The NVIDIA manuals provide hardware specifications, power management APIs (NVML), and monitoring tools (DCGM), but **do not provide empirical power profiles** for inference workloads. 

**Validation Status:**
- ✅ **Steady-state inference power (250-280W)** has been validated from academic research
- ⚠️ **Phase transitions** are refined estimates inferred from workload characteristics
- ⚠️ **Idle power** is a refined estimate based on research (not directly measured)
- ❌ **Complete per-phase power profiles** still require empirical validation

**Current Status:** Power profiles are **refined estimates** with validated steady-state inference power. MLPerf and academic paper research is in progress to further validate and refine these estimates (see `docs/MLPERF-ACADEMIC-VALIDATION-PLAN.md`).

---

## Next Steps

### Immediate (In Progress)
1. ✅ **Refined power estimates** - Updated based on validated steady-state inference power
2. 🔄 **MLPerf + Academic Paper Research** - See `prompts/research/MLPERF-ACADEMIC-POWER-VALIDATION-PROMPT.md`
3. 🔄 **Update calculator** - Consider using refined estimate (0.2-0.25 kW) for more realistic modeling

### Short-Term (1-2 Weeks)
4. **Complete MLPerf data extraction** - Extract power data from MLPerf submissions
5. **Complete academic paper review** - Extract power measurements from research papers
6. **Synthesize findings** - Create data synthesis report
7. **Update power profiles** - Incorporate validated data from MLPerf/academic papers

### Long-Term (Post-Construction)
8. **Obtain hardware access** for H100 PCIe systems
9. **Deploy external power metering** (Yokogawa WT5000 or equivalent)
10. **Measure empirical power profiles** for all phases
11. **Final validation** - Update this document with direct measurements
12. **Refine calculator assumptions** based on complete empirical data

---

**Document Status:** Modeling profiles documented based on research and manufacturer specifications. Suitable for construction planning and partner selection. Empirical validation planned for post-construction validation phases.

