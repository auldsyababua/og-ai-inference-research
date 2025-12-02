# research-findings.md

## Section 1: GPU Power Ramp Analysis (Phase 2 Deliverable)

### 1.1 Overview
This section quantifies worst-case and mitigated GPU power ramp rates during inference phase transitions for off-grid H100 PCIe clusters. These ramp rates are critical to generator stability modeling. Ramp scenarios are structured by cluster size and power correlation, using consistent formulas.

---

### 1.2 Assumptions and Input Parameters

| Parameter                     | Value                         | Notes                                               |
|------------------------------|-------------------------------|-----------------------------------------------------|
| GPU Model                    | NVIDIA H100 PCIe              | 350W nominal TDP                                    |
| Per-GPU Power Step (\u0394P_gpu)  | 0.35 kW                      | From idle to active (model load/warmup/inference)   |
| Cluster Sizes (N)            | 32, 256, 1024 GPUs            | Representative of pod/rack/multi-rack scale         |
| Correlation Coefficients (C) | 1.0, 0.5, 0.03\u20130.1           | Full sync, partial sync, staggered                  |
| Time Windows (\u0394t)             | 1s, 5s, 30s                   | Duration of ramp (correlated vs staggered)          |

---

### 1.3 Ramp Rate Equations

- **Total cluster step load:** \u0394P_cluster = C \u00d7 N \u00d7 \u0394P_gpu
- **Ramp rate:** Ramp_rate = \u0394P_cluster / \u0394t

---

### 1.4 Ramp Scenarios and Outputs

#### Table 1: 100% Correlated Ramp (C = 1.0, \u0394t = 1s)

| Cluster Size | \u0394P_cluster (kW) | Ramp Rate (kW/s) |
|--------------|-------------------|------------------|
| 32 GPUs      | 11.2              | 11.2             |
| 256 GPUs     | 89.6              | 89.6             |
| 1024 GPUs    | 358.4             | 358.4            |

#### Table 2: 50% Correlated Ramp (C = 0.5 sync, 0.5 over 5s)

| Cluster Size | Initial Step (kW) | Sustained Ramp (kW/s over 5s) |
|--------------|-------------------|-------------------------------|
| 32 GPUs      | 5.6               | 1.12                          |
| 256 GPUs     | 44.8              | 8.96                          |
| 1024 GPUs    | 179.2             | 35.84                         |

#### Table 3: Staggered Ramp (C \u2248 0.03\u20130.1, \u0394t = 30s)

| Cluster Size | Total \u0394P (kW) | Avg Ramp Rate (kW/s over 30s) |
|--------------|------------------|-------------------------------|
| 32 GPUs      | 11.2             | 0.37                          |
| 256 GPUs     | 89.6             | 2.99                          |
| 1024 GPUs    | 358.4            | 11.95                         |

---

### 1.5 Key Findings

- Ramp rates scale **linearly with GPU count**, but can be shaped by controlling correlation.
- **100% correlation (C=1.0)** leads to dangerous spikes (e.g. ~358 kW/s for 1024 GPUs).
- **Scheduler shaping** (e.g. spreading ramp over 30s) reduces ramp rate by ~30x.
- **Ramp shaping is a design requirement**: All modeling assumes that fully synchronized ramps are disallowed unless buffered.

---

## Section 2: Status Tracking (Phase 2)

### 2.1 ✅ Completed
- Ramp formulas defined and applied.
- Ramp rates computed for 32, 256, 1024 GPUs across 3 correlation scenarios.
- Ramp tables included with kW and kW/s values.

### 2.2 🔜 Next (Pending)
- Validate \u0394P_gpu empirically for H100 PCIe (model load, inference burst).
- Validate real-world C (correlation coefficient) via literature or telemetry.
- Populate generator-matching results in Phase 3.

### 2.3 ❓ Open Questions
1. Should we express ramp rates as % of generator rated power?
2. Should we include H100 SXM (700W) ramp scenarios now or defer?
3. Include coordinated miner shedding in ramp shaping now or in Phase 3?

---

## Section 3: Deliverable Integration

This file is structured to feed directly into:
- `stability-model.md` for mapping ramps to generator response
- `bess-sizing.md` for calculating buffer size and discharge rates
- `parameter-database.csv` for structured lookup of ramp parameters

All ramp rates are computed using transparent equations with clear inputs, matching Compute Refinery Modeling PRD Section 3.1 and 3.2【50†source】.

---

## Confidence Assessment (Phase 2 Scope)

| Parameter        | Value         | Source                         | Confidence |
|------------------|---------------|--------------------------------|------------|
| \u0394P_gpu (PCIe)   | 0.35 kW       | Assumed from spec range        | 65%        |
| Correlation C    | 0.03\u20131.0     | Conservative scheduler model   | 75%        |
| Time window \u0394t   | 1s / 5s / 30s | Based on modeling assumptions  | 85%        |

---

## Recommendations

- Begin Phase 2.1 literature review for empirical power traces.
- Confirm C ranges using telemetry or NVIDIA scheduler behavior.
- Prepare GPU ramp + generator overlay plots for Phase 3.

This document is ready for internal review and expansion into final deliverables upon validation of power and correlation assumptions.

