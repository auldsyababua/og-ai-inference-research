# MULTI-STEP RAMP SIMULATOR

**Version:** 1.0  
**Last Updated:** 2025-12-01  
**Status:** Working prototype

---

## Purpose

Simulate multi-step load ramping sequences for generators with constrained load acceptance (e.g., CG260-16). Models time-series behavior including recovery periods between steps, frequency response, and BESS energy requirements.

---

## Quick Start Guide

### Step 1: Open Simulator
Open the CSV file in Excel, Google Sheets, or any spreadsheet application:
```
models/multistep-ramp-simulator/MultiStepRamp-v1.csv
```

### Step 2: Configure Scenario

**Load Target:**
- `TargetLoad_kW` - Desired final load (kW)
- `TargetLoad_pct` - Desired final load (% of rated)

**Generator Configuration:**
- `P_rated_gen_kW` - Generator rated power (kW)
- `H_eff_s` - Effective inertia constant (seconds)
- `R_eff_pu` - Governor droop (per unit, e.g., 0.05 = 5%)
- `f_nom_Hz` - Nominal frequency (50 or 60 Hz)

**Initial Conditions:**
- `InitialLoad_kW` - Starting load (kW) - typically 0 for cold start
- `InitialLoad_pct` - Starting load (% of rated)

### Step 3: Review Outputs

**Summary Outputs:**
- `TotalRampTime_s` - Total time to reach target load (seconds)
- `NumberOfSteps` - Number of discrete steps required
- `BESS_EnergyRequired_kWh` - Minimum BESS energy capacity needed
- `BESS_PowerRequired_kW` - Minimum BESS power rating needed
- `MaxFrequencyDeviation_Hz` - Maximum frequency dip during ramp
- `MaxRoCoF_Hz_per_s` - Maximum rate of change of frequency

**Time-Series Output:**
- See `TimeSeries` sheet/tab for step-by-step simulation results

---

## CG260-16 Load Step Sequence

The CG260-16 requires a specific multi-step ramp sequence:

| Step | Load Range (% of Rated) | Step Size (%) | Recovery Time (s) | Speed Drop (%) |
|------|------------------------|---------------|-------------------|----------------|
| 1    | 0% → 16%               | 16%           | 10                | 8%             |
| 2    | 16% → 29%               | 13%           | 10                | 8%             |
| 3    | 29% → 39%               | 10%           | 10                | 8%             |
| 4    | 39% → 48%               | 9%            | 10                | 8%             |
| 5    | 48% → 57%               | 9%            | 10                | 8%             |
| 6    | 57% → 66%               | 9%            | 10                | 8%             |
| 7    | 66% → 75%               | 9%            | 10                | 8%             |
| 8    | 75% → 84%               | 9%            | 10                | 8%             |
| 9    | 84% → 91%               | 7%            | 10                | 8%             |
| 10   | 91% → 100%              | 9%            | 10                | 8%             |

**Note:** Recovery time is the stabilization period required before the next step can be applied.

---

## Example Scenarios

### Scenario 1: CG260 Cold Start to 50% Load
- Target: 2150 kW (50% of 4300 kW)
- Result: Requires 4 steps, ~40 seconds total ramp time
- BESS must carry full load for first 10 seconds

### Scenario 2: CG260 Cold Start to 100% Load
- Target: 4300 kW (100% of 4300 kW)
- Result: Requires 10 steps, ~100 seconds total ramp time
- BESS must carry full load during entire ramp sequence

### Scenario 3: CG260 Partial Ramp (25% → 75%)
- Initial: 1075 kW (25%)
- Target: 3225 kW (75%)
- Result: Requires 5 steps starting from Step 3, ~50 seconds

---

## BESS Sizing Logic

The simulator calculates BESS requirements based on:

1. **Power Rating:** Must cover the difference between target load and generator's current output during each step
2. **Energy Capacity:** Must provide energy for the duration of the ramp sequence

**Formula:**
```
BESS_EnergyRequired = ∫(TargetLoad - GeneratorOutput(t)) dt
```

Where integration is over the entire ramp duration.

---

## Limitations

**Current Version (v1) does NOT include:**
- Voltage dynamics (only frequency)
- Generator governor response time (assumes instantaneous)
- BESS discharge efficiency losses
- Temperature effects on generator performance
- Partial load efficiency curves

---

## References

- `data/generators/caterpillar/Caterpillar-Technical-Analysis.md` - CG260 load step table
- `models/generator-risk-calculator/formulas.md` - Frequency response formulas
- `docs/GLOSSARY.md` - Standardized terminology

