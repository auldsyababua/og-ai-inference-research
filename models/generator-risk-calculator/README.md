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
  - **Current scenarios use:** 0.6 kW (conservative estimate)
  - **Refined estimate:** 0.2-0.25 kW (more realistic, based on validated inference power)
  - **Recommendation:** Use 0.6 kW for worst-case planning, 0.2-0.25 kW for realistic modeling
  - See `data/gpu-profiles/GPU-Power-Profiles.md` for details
- `Correlation_C` - Fraction transitioning together (0.0-1.0)
  - **Current scenarios use:** 0.8 (worst-case synchronous warmup)
  - **Refined estimate:** 0.3-0.7 (typical operation range)
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

**Note:** Refined estimates show 62.5% lower power steps, indicating current conservative estimates provide significant safety margin but may lead to over-engineering. See `docs/POWER-PROFILE-UPDATE-SUMMARY.md` for details.

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
