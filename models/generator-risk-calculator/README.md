# GENERATOR RISK CALCULATOR

**Version:** 1.0
**Last Updated:** 2025-12-01
**Status:** Working prototype

---

## Purpose

Calculate GPU cluster power ramp rates and assess compatibility with natural gas generator constraints. Determines if a given GPU cluster configuration will operate safely on a specific generator model.

---

## Quick Start Guide

### Step 1: Open Calculator
Open the CSV file in Excel, Google Sheets, or any spreadsheet application:
```
models/generator-risk-calculator/GeneratorRisk-v1.csv
```

### Step 2: Edit Input Parameters (Yellow Cells)

**Cluster Configuration:**
- `N_GPUs` - Number of GPUs in cluster
- `DeltaP_GPU_kW` - Per-GPU power step (kW)
  - **Conservative estimate:** 0.6 kW (worst-case planning)
  - **✅ Validated estimate:** 0.2-0.25 kW (idle to inference: 60-80W → 220-260W = 140-200W step)
  - **Warmup step:** 0.24-0.29 kW (idle to warmup: 60-80W → 300-350W = 240-290W step)
  - **Recommendation:** Use 0.25-0.30 kW for warmup phase (most critical), 0.2-0.25 kW for inference
  - **Source:** `research/gpu-phase-research/CONSOLIDATED-SUMMARY.md` - Validated from 4 independent research efforts
  - See `data/gpu-profiles/GPU-Power-Profiles.md` for details
- `Correlation_C` - Fraction transitioning together (0.0-1.0)
  - **Conservative:** 0.9-1.0 (Tensor Parallelism worst-case)
  - **✅ Validated typical:** 0.5-0.7 (General Inference)
  - **Best-case:** 0.3-0.5 (Data Parallelism)
  - **Current scenarios use:** 0.8 (worst-case synchronous warmup)
  - **Recommendation:** Use 0.9 for conservative generator design, 0.5-0.7 for typical operation
  - **Source:** `research/gpu-phase-research/CONSOLIDATED-SUMMARY.md`
- `DeltaT_event_s` - Transition time window (seconds)

**Generator Configuration:**
- `P_rated_gen_kW` - Generator rated power (kW)
- `H_eff_s` - Effective inertia constant (seconds)
- `R_eff_pu` - Governor droop (per unit, e.g., 0.04 = 4%)
- `f_nom_Hz` - Nominal frequency (50 or 60 Hz)
- `MaxStep_pct` - Maximum safe load step (% of rated)

### Step 3: Review Calculated Outputs (Green Cells)

- `DeltaP_cluster_kW` - Total cluster power step
- `RampRate_kW_per_s` - Power change rate
- `StepFraction` - Load step as fraction of generator capacity
- `DeltaF_over_F_pu` - Frequency deviation (per unit)
- `RoCoF_Hz_per_s` - Rate of change of frequency
- `StepWithinLimit` - TRUE if within generator limits
- `RiskLevel` - GREEN (safe) / YELLOW (caution) / RED (unsafe)

---

## Risk Level Interpretation

| Level | Meaning | Action |
|-------|---------|--------|
| **GREEN** | Safe operation | Proceed with configuration |
| **YELLOW** | Marginal - may require mitigation | Add BESS buffer or reduce correlation |
| **RED** | Unsafe - exceeds limits | Reconfigure or use different generator |

---

## Example Scenarios

### Scenario 1: G3520 Fast Response + GPU Warmup (Conservative Estimate)
- 1024 GPUs × 0.6 kW × 0.8 correlation = 491.52 kW
- G3520 (4000 kW, 100% block load capable)
- Result: **GREEN** - 12.3% step, well within limits

### Scenario 1 (Refined Estimate - More Realistic):
- 1024 GPUs × 0.225 kW × 0.8 correlation = 184.32 kW
- G3520 (4000 kW, 100% block load capable)
- Result: **GREEN** - 4.6% step, well within limits (more realistic)

### Scenario 2: CG260-16 + GPU Warmup (Conservative Estimate)
- Same GPU configuration (491.52 kW)
- CG260 (4300 kW, 16% max first step)
- Result: **GREEN** - 11.4% step, within first step limit

### Scenario 2 (Refined Estimate - More Realistic):
- 1024 GPUs × 0.225 kW × 0.8 correlation = 184.32 kW
- CG260 (4300 kW, 16% max first step)
- Result: **GREEN** - 4.3% step, well within limits (more realistic)

**Note:** ✅ **Validated estimates** show 58-67% lower power steps than conservative estimates (0.2-0.25 kW vs 0.6 kW), indicating conservative estimates provide significant safety margin but may lead to over-engineering. 

**⚠️ Critical Finding:** Warmup phase is "hidden danger" with 300-350W sustained (86-100% of TDP) for 10-60 seconds - most likely phase to trigger generator overload. Use 0.25-0.30 kW for warmup step calculations.

**Source:** `research/gpu-phase-research/CONSOLIDATED-SUMMARY.md` - Validated from 4 independent research efforts

### Scenario 3: CG260 + Bitcoin Container
- 5000 GPUs × 0.3 kW × 0.3 correlation over 30s
- Result: **GREEN** - slow ramp (15 kW/s) easily handled

---

## Formulas

See: `formulas.md` for detailed formula documentation

---

## Test Scenarios

Pre-configured test cases available in:
```
models/generator-risk-calculator/test-scenarios/scenarios.csv
```

---

## Limitations

**Current Version (v1) does NOT include:**
- Multi-phase GPU power modeling
- Multi-step generator ramp sequences (CG260)
- BESS sizing calculations
- Bitcoin miner coordination
- Voltage dynamics
- Economic modeling

See: `docs/GAP_ANALYSIS.md` for planned enhancements

---

## Troubleshooting

### Common Issues

**Issue: Risk Level shows RED but StepWithinLimit is TRUE**
- **Cause:** Risk level uses conservative thresholds (50% of max step for GREEN)
- **Solution:** Review the step fraction - YELLOW is acceptable for many applications

**Issue: RoCoF value seems very high**
- **Cause:** RoCoF is the initial rate before governor response
- **Solution:** This is expected - governor will respond within 0.5-2 seconds to stabilize frequency

**Issue: Calculator shows different results than expected**
- **Cause:** Check that all input parameters match your generator model
- **Solution:** Verify generator parameters from `data/generators/caterpillar/Caterpillar-Phase1-Library.md`

### Getting Help

- **Formulas:** See `formulas.md` for detailed formula documentation
- **Generator Specs:** See `data/generators/caterpillar/` for complete generator data
- **Gap Analysis:** See `docs/GAP_ANALYSIS.md` for known limitations

---

## References

- `docs/PRD.md` - Calculator requirements
- `data/generators/caterpillar/` - Generator specifications
- `data/gpu-profiles/GPU-Power-Profiles.md` - GPU power characteristics
- `docs/GAP_ANALYSIS.md` - Known limitations
- `docs/GLOSSARY.md` - Standardized terminology
