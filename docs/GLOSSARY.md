# TERMINOLOGY GLOSSARY
**Off-Grid AI Inference Research Project**

**Version:** 1.0
**Last Updated:** 2025-12-01
**Purpose:** Standardized terminology for all project documents

---

## How to Use This Glossary

**When writing or updating documents:**
1. Use the **Standardized Term** (column 1)
2. Avoid deprecated aliases unless in quotes
3. Include units where specified
4. Link to this glossary in document headers

**Symbol Convention:**
- **Bold** = Primary standardized term
- *Italic* = Acceptable alternative
- ~~Strikethrough~~ = Deprecated, do not use

---

## A. GENERATOR & POWER SYSTEM TERMS

### Generator Types & Classifications

| Term | Symbol | Units | Definition | Usage Notes |
|------|--------|-------|------------|-------------|
| **Generator** | - | - | Engine + synchronous alternator producing electrical power | Preferred over "genset" in technical docs |
| **Genset** | - | - | Generator set (engine + alternator + controls + enclosure) | Acceptable in informal contexts |
| **Prime Power** | - | kW | Rated continuous power for base-load operation | Typically 10% lower than standby |
| **Standby Power** | - | kW | Emergency backup power rating (limited hours/year) | Typical emergency rating |
| **Continuous Power** | P_cont | kW | Maximum power for unlimited runtime at rated conditions | Most conservative rating |

### Generator Performance Classes

| Term | Symbol | Units | Definition | Usage Notes |
|------|--------|-------|------------|-------------|
| **ISO 8528-5 Class** | - | - | International standard defining generator transient performance | G1 (lenient) to G3 (strict) |
| **Class G1** | - | - | General purpose, relaxed frequency/voltage tolerances | High-efficiency engines |
| **Class G2** | - | - | Standard industrial loads, moderate tolerances | Typical gas generators |
| **Class G3** | - | - | Mission-critical applications, strict tolerances | Data centers, hospitals |
| **NFPA 110 Type 10** | - | - | US code: generator ready in ≤10 seconds | Data center emergency standard |

### Dynamic Parameters

| Term | Symbol | Units | Definition | Usage Notes |
|------|--------|-------|------------|-------------|
| **Inertia Constant** | H or H_eff | seconds | Stored kinetic energy per unit MVA rating | **Always use seconds**, not kg⋅m² |
| **Mass Moment of Inertia** | J | kg⋅m² | Rotational inertia of generator rotor + flywheel | Convert to H for modeling |
| **Governor Droop** | R or R_eff | p.u. or % | Steady-state speed change per unit load change | Express as 0.04 (4%) not "4" |
| **Rate of Change of Frequency** | **RoCoF** | Hz/s | Speed at which frequency changes during transient | **Never** "ROCOF" or "df/dt" alone |
| **Frequency Deviation** | ΔF | Hz or p.u. | Change from nominal frequency (50 or 60 Hz) | Specify units: "ΔF = -0.3 Hz" or "-0.005 p.u." |
| **Voltage Dip** | ΔV | % or p.u. | Temporary voltage sag during load application | Express as percentage: "ΔV = 8%" |
| **Recovery Time** | t_recovery | seconds | Time to return to ±1% of rated after transient | **Never** "settling time" or "t_f,in" |
| **Transient Response** | - | - | Generator behavior during load changes | Encompasses frequency & voltage dynamics |

### Load Step Parameters

| Term | Symbol | Units | Definition | Usage Notes |
|------|--------|-------|------------|-------------|
| **Load Step** | ΔP | kW or % | Instantaneous change in electrical load | Prefer "load step" over "power step" |
| **Step Fraction** | - | p.u. or % | Load step as fraction of generator rating | ΔP / P_rated |
| **Max Step Load** | MaxStep | % | Maximum allowable instantaneous load increase | Manufacturer-specified limit |
| **Ramp Rate** | dP/dt | **kW/s** | Rate of load change over time | **Always kW/s**, never kW/min |
| **Block Load** | - | % | Sudden application of a large load percentage | "100% block load" = instant full load |
| **Load Acceptance** | - | - | Generator's ability to handle load steps | Generic term for dynamic capability |

### Fuel & Efficiency

| Term | Symbol | Units | Definition | Usage Notes |
|------|--------|-------|------------|-------------|
| **Electrical Efficiency** | η_e | % | Electrical output / fuel input (LHV basis) | **Primary metric** for comparison |
| **Thermal Efficiency** | η_th | % | Heat recovered / fuel input | For CHP applications |
| **Total Efficiency** | η_total | % | (Electrical + thermal) / fuel input | CHP systems only |
| **Lower Heating Value** | LHV | MJ/m³ | Fuel energy excluding water vapor condensation | Natural gas standard |
| **Methane Number** | MN | - | Fuel's resistance to knock (like octane for gasoline) | MN 70-80 typical for pipeline gas |
| **Wobbe Index** | WI | MJ/Nm³ | LHV / √(specific gravity) | Fuel interchangeability metric |

---

## B. GPU & COMPUTE CLUSTER TERMS

### GPU Hardware

| Term | Symbol | Units | Definition | Usage Notes |
|------|--------|-------|------------|-------------|
| **GPU** | - | - | Graphics Processing Unit (compute accelerator) | H100, H200, A100, etc. |
| **GPU Cluster** | - | - | Multiple GPUs managed as a single compute resource | Typically in data center context |
| **Node** | - | - | Single server containing 1-8 GPUs | Physical hardware unit |
| **Rack** | - | - | Standard 42U cabinet containing multiple nodes | Physical organization unit |
| **TDP** | - | W | Thermal Design Power (max continuous power) | GPU manufacturer spec |

### GPU Power Dynamics

| Term | Symbol | Units | Definition | Usage Notes |
|------|--------|-------|------------|-------------|
| **GPU Power Phase** | - | - | Distinct operational state with characteristic power draw | E.g., idle, loading, inference |
| **Idle Power** | P_idle | W | GPU power when not processing workloads | Baseline consumption |
| **Per-GPU Power Step** | ΔP_gpu | W or kW | Power change for a single GPU during phase transition | Individual GPU delta |
| **Cluster Power Step** | ΔP_cluster | kW | Total power change when multiple GPUs transition | **= C × N × ΔP_gpu** |
| **Correlation** | C or C_factor | 0-1 | Fraction of GPUs transitioning simultaneously | **0 = none, 1 = perfect sync** |
| **Transition Time** | Δt_event | seconds | Time window during which GPUs change phase | Used for ramp rate calculation |
| **Synchronous Event** | - | - | Many GPUs changing state at same time (high correlation) | Avoid unless controlled |

### GPU Workload Phases

| Term | Symbol | Units | Definition | Usage Notes |
|------|--------|-------|------------|-------------|
| **Launch** | - | - | Job initialization and resource allocation | Moderate power |
| **Model Load** | - | - | Loading neural network weights into GPU memory | Variable duration |
| **Warmup** | - | - | Initial inference passes to stabilize performance | High power ramp |
| **Steady-State Inference** | - | - | Continuous inference at full utilization | Maximum sustained power |
| **Cleanup** | - | - | De-allocation of resources after job completion | Power ramp down |
| **Teardown** | - | - | Final shutdown and memory clearing | Return to idle |

### Workload Types

| Term | Symbol | Units | Definition | Usage Notes |
|------|--------|-------|------------|-------------|
| **Batch Inference** | - | - | Processing multiple inputs in parallel | Tolerates ramp delays |
| **Online Inference** | - | - | Real-time, low-latency serving (< 100ms) | Requires instant response |
| **Training** | - | - | Model weight optimization via gradient descent | Very high sustained power |
| **Fine-Tuning** | - | - | Training from pre-existing model checkpoint | Lower power than training |

---

## C. CONTROL & MITIGATION TERMS

### Scheduling & Control

| Term | Symbol | Units | Definition | Usage Notes |
|------|--------|-------|------------|-------------|
| **Ramp Shaping** | - | - | Deliberate control of load change rate to stay within limits | **Core mitigation strategy** |
| **Staggering** | - | - | Spreading GPU transitions over time to reduce correlation | Reduces peak step |
| **Scheduler** | - | - | Software system controlling when GPUs enter phases | Cluster orchestrator |
| **Power-Aware Scheduling** | - | - | Job scheduling that considers electrical constraints | Off-grid requirement |
| **Max GPUs-per-Second** | - | GPUs/s | Scheduler limit on phase transitions | Ramp shaping parameter |

### Energy Storage

| Term | Symbol | Units | Definition | Usage Notes |
|------|--------|-------|------------|-------------|
| **BESS** | - | - | Battery Energy Storage System | **Preferred term** |
| **UPS** | - | - | Uninterruptible Power Supply | For short-term ride-through |
| **Energy Capacity** | E | kWh | Total stored energy | BESS sizing parameter |
| **Discharge Rate** | P_discharge | kW | Maximum power output rate | BESS power capability |
| **Ride-Through** | - | seconds | Duration BESS can support load during outage | Typically 10-30s for transients |

### Flexible Load

| Term | Symbol | Units | Definition | Usage Notes |
|------|--------|-------|------------|-------------|
| **Flexible Load** | - | - | Controllable electrical load used for load shaping | Generic term |
| **Bitcoin Miner** | - | - | Cryptocurrency mining hardware (flexible load) | Off-grid use case |
| **Miner Shedding** | - | - | Turning off miners to free generator capacity for GPUs | Load coordination strategy |
| **Miner Container** | - | - | Modular unit containing multiple mining ASICs | Typical deployment unit |
| **Response Time** | t_response | ms or s | Time from control signal to load change | Miner: ~100ms, Generator: seconds |

---

## D. MODELING & CALCULATION TERMS

### Risk Assessment

| Term | Symbol | Units | Definition | Usage Notes |
|------|--------|-------|------------|-------------|
| **Risk Level** | - | - | Safety classification: GREEN, YELLOW, RED | Calculator output |
| **GREEN** | - | - | Safe operation, within all limits | < 50% of max step |
| **YELLOW** | - | - | Marginal, may require mitigation | 50-100% of max step |
| **RED** | - | - | Unsafe, exceeds generator capability | > max step limit |
| **Step Within Limit** | - | boolean | TRUE if load step < generator max step | Calculator check |

### Calculator Parameters

| Term | Symbol | Units | Definition | Usage Notes |
|------|--------|-------|------------|-------------|
| **Nominal Frequency** | f_nom | Hz | Standard grid frequency (50 or 60 Hz) | Regional standard |
| **Rated Power** | P_rated | kW or MW | Generator nameplate capacity | At rated conditions |
| **Base Power** | S_base or P_base | MVA or MW | Reference power for per-unit calculations | Often = P_rated |
| **Per Unit** | p.u. | - | Normalized value (actual / base) | Dimensionless |

---

## E. SITE & INFRASTRUCTURE TERMS

### Site Architecture

| Term | Symbol | Units | Definition | Usage Notes |
|------|--------|-------|------------|-------------|
| **Off-Grid Site** | - | - | Facility operating without utility grid connection | Project focus |
| **Island Mode** | - | - | Generator operating standalone (not grid-connected) | Synonym for off-grid |
| **Microgrid** | - | - | Localized grid with distributed generation | Can be grid-connected or islanded |
| **Grid-Forming** | - | - | Generator establishing voltage and frequency reference | Primary source in microgrid |
| **Grid-Following** | - | - | Generator synchronizing to existing grid | Secondary source |

### Data Connectivity

| Term | Symbol | Units | Definition | Usage Notes |
|------|--------|-------|------------|-------------|
| **Starlink** | - | - | Satellite internet connectivity | Always-on, limited bandwidth |
| **Sneakernet** | - | - | Physical transport of storage media (drives in trucks) | High latency, high capacity |
| **Fiber** | - | - | Optical fiber internet connection | High CapEx, low OpEx |
| **TB/month** | - | TB/mo | Data transfer volume per month | Connectivity sizing metric |
| **Cost/TB** | - | $/TB | Cost per terabyte transferred | Economic comparison metric |

---

## F. ECONOMIC & FINANCIAL TERMS

### Capital Costs

| Term | Symbol | Units | Definition | Usage Notes |
|------|--------|-------|------------|-------------|
| **CapEx** | - | $ | Capital Expenditure (upfront equipment costs) | One-time investment |
| **OpEx** | - | $/year | Operating Expenditure (ongoing costs) | Annual recurring cost |
| **Levelized Cost** | LCOE | $/kWh | Total lifetime cost per kWh produced | Includes CapEx + OpEx |
| **NPV** | - | $ | Net Present Value | Discounted cash flow metric |
| **IRR** | - | % | Internal Rate of Return | Investment return metric |

### Operational Costs

| Term | Symbol | Units | Definition | Usage Notes |
|------|--------|-------|------------|-------------|
| **Fuel Cost** | - | $/kWh | Cost of natural gas per kWh electrical output | Depends on efficiency |
| **Maintenance Interval** | - | hours | Time between scheduled maintenance | E.g., 4,000h first service |
| **Overhaul Interval** | - | hours | Time between major rebuilds | E.g., 64,000-80,000h |
| **Lifecycle Cost** | - | $/kWh | Total cost of ownership over asset life | CapEx + OpEx + fuel |

---

## G. INDUSTRY STANDARDS & COMPLIANCE

| Term | Acronym | Full Name | Description |
|------|---------|-----------|-------------|
| **ISO 8528-5** | - | Generator Set Performance Classes | International transient performance standard |
| **NFPA 110** | - | Emergency & Standby Power Systems | US code for backup generators |
| **EPA NSPS** | - | Environmental Protection Agency New Source Performance Standards | US emissions regulations |
| **IEC 61000** | - | Electromagnetic Compatibility | Power quality standards |
| **ASHRAE** | - | American Society of Heating, Refrigerating and Air-Conditioning Engineers | Data center design standards |

---

## H. COMMON ABBREVIATIONS

| Abbreviation | Meaning | Usage Notes |
|--------------|---------|-------------|
| **AVR** | Automatic Voltage Regulator | Generator voltage control system |
| **CHP** | Combined Heat and Power | Co-generation system |
| **BESS** | Battery Energy Storage System | **Preferred over "battery" or "storage"** |
| **UPS** | Uninterruptible Power Supply | Short-term backup |
| **THD** | Total Harmonic Distortion | Power quality metric |
| **PF** | Power Factor | Real power / apparent power |
| **LHV** | Lower Heating Value | Fuel energy content standard |
| **HHV** | Higher Heating Value | Alternative fuel energy basis |
| **RoCoF** | Rate of Change of Frequency | **Use this spelling, not ROCOF** |
| **TDP** | Thermal Design Power | GPU power rating |
| **AI** | Artificial Intelligence | Machine learning inference/training |
| **ML** | Machine Learning | Subset of AI |
| **LLM** | Large Language Model | Type of AI model (GPT, Claude, etc.) |

---

## I. UNIT CONVENTIONS

### Standard Units to Use

| Quantity | Preferred Unit | Alternative | Notes |
|----------|----------------|-------------|-------|
| Power | **kW** | MW (for large systems) | Avoid "W" for generators |
| Energy | **kWh** | MWh | Never "kW" for energy |
| Frequency | **Hz** | - | 50 or 60 Hz |
| Time | **seconds (s)** | ms, minutes | Specify clearly |
| Inertia | **seconds (H)** | kg⋅m² (J) | Convert J to H for modeling |
| Efficiency | **% (percent)** | p.u. | 43.5%, not 0.435 |
| Droop | **p.u. or %** | - | 0.04 or 4%, never ambiguous |
| Rate | **kW/s** | MW/s | Never kW/min |
| Temperature | **°C** | K | Celsius for engineering |

### Per Unit (p.u.) System

**Definition:** Normalized value = (Actual Value) / (Base Value)

**Example:**
- Rated power: 4000 kW
- Load step: 500 kW
- Step fraction: 500 / 4000 = 0.125 p.u. (or 12.5%)

---

## J. CROSS-REFERENCE INDEX

### Where Terms Appear

| Term | Primary Reference | Also Discussed In |
|------|------------------|-------------------|
| Inertia Constant (H) | docs/GAP_ANALYSIS.md §3.2 | data/generators/caterpillar/Caterpillar-Technical-Analysis.md §2.3 |
| Governor Droop (R) | models/generator-risk-calculator/formulas.md | docs/PRD.md §4.1 |
| Correlation (C) | research/gpu-compute/Off-Grid-Compute-Modeling-Challenges.md §2 | models/generator-risk-calculator/README.md |
| Ramp Shaping | research/gpu-compute/Off-Grid-Compute-Modeling-Challenges.md §4.1 | docs/PRD.md §3.4 |
| BESS | docs/GAP_ANALYSIS.md §5.3 | research/gpu-compute/Off-Grid-Compute-Modeling-Challenges.md §4.2 |
| ISO 8528-5 | data/generators/caterpillar/Caterpillar-Phase1-Library.md | data/generators/caterpillar/Caterpillar-Technical-Analysis.md §2.2 |

---

## K. DEPRECATED TERMS (DO NOT USE)

| Deprecated Term | Use Instead | Reason |
|-----------------|-------------|--------|
| ~~"Power step"~~ | **Load step** | Ambiguous (power can mean many things) |
| ~~"Settling time"~~ | **Recovery time** | Not standard in ISO 8528 |
| ~~"t_f,in"~~ | **Recovery time (t_recovery)** | Obscure notation |
| ~~"ROCOF"~~ | **RoCoF** | Incorrect capitalization |
| ~~"df/dt" (alone)~~ | **RoCoF (Hz/s)** | Needs units |
| ~~"Battery"~~ | **BESS** or **UPS** | Too generic |
| ~~"Storage"~~ | **BESS** | Ambiguous (could be data storage) |
| ~~"Fast buffers"~~ | **BESS or UPS** | Colloquial |
| ~~"Transient"~~ | **Transient response** or **Load step** | Too generic |
| ~~"Genset"~~ | **Generator** | Use in technical docs |

---

## L. USAGE EXAMPLES

### Correct Usage ✓

```
"The CG260-16 generator has an inertia constant H = 5 seconds and governor
droop R = 4% (0.04 p.u.). When a cluster of 1024 GPUs with correlation C = 0.8
transitions at ΔP_gpu = 0.6 kW per GPU, the cluster power step is:

ΔP_cluster = 0.8 × 1024 × 0.6 = 491.52 kW

This represents a step fraction of 491.52 kW / 4300 kW = 11.4%, which is
within the CG260's max step limit of 16% for the first load step."
```

### Incorrect Usage ✗

```
"The genset has inertia of 710 kg⋅m² and 4 droop. When GPUs ramp at 0.6W each
with 80% synchronization, the power step is 491kW. This is a 11% transient
which causes frequency dip."
```

**Problems:**
- ✗ "genset" (use "generator")
- ✗ Inertia in kg⋅m² not converted to H (seconds)
- ✗ "4 droop" (missing units: 4% or 0.04 p.u.)
- ✗ "80% synchronization" (use "correlation C = 0.8")
- ✗ "0.6W" (should be "0.6 kW")
- ✗ "491kW" (space needed: "491 kW")
- ✗ "transient" (use "load step" or "step fraction")
- ✗ "frequency dip" (use "frequency deviation ΔF")

---

## M. GLOSSARY MAINTENANCE

**Update This Glossary When:**
1. New technical terms are introduced
2. Abbreviations become ambiguous
3. Cross-references need updating
4. Standards are revised (e.g., ISO 8528 updated)

**Approval Required For:**
- Changes to standardized terms
- Addition of deprecated terms
- Unit convention changes

**Version History:**
- v1.0 (2025-12-01): Initial glossary created

---

**Next Steps:**
1. Review all research documents
2. Update non-compliant terminology
3. Add glossary references to document headers
4. Train team on standardized usage

---

*This glossary is a living document. Propose updates via project issues or pull requests.*
