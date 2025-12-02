# MULTI-STEP RAMP SIMULATOR - FORMULAS

**Version:** 1.0  
**Last Updated:** 2025-12-01

---

## Input Parameters

| Symbol | Name | Units | Description |
|--------|------|-------|-------------|
| P_rated | P_rated_gen_kW | kW | Generator rated power |
| H | H_eff_s | s | Effective inertia constant |
| R | R_eff_pu | p.u. | Governor droop (per unit) |
| f_nom | f_nom_Hz | Hz | Nominal frequency |
| P_init | InitialLoad_kW | kW | Starting load |
| P_target | TargetLoad_kW | kW | Target load |

---

## Step Sequence Logic

### 1. Determine Starting Step

```
if InitialLoad_pct < 16%:
    StartStep = 1
elif InitialLoad_pct < 29%:
    StartStep = 2
elif InitialLoad_pct < 39%:
    StartStep = 3
elif InitialLoad_pct < 48%:
    StartStep = 4
elif InitialLoad_pct < 57%:
    StartStep = 5
elif InitialLoad_pct < 66%:
    StartStep = 6
elif InitialLoad_pct < 75%:
    StartStep = 7
elif InitialLoad_pct < 84%:
    StartStep = 8
elif InitialLoad_pct < 91%:
    StartStep = 9
else:
    StartStep = 10
```

### 2. Determine Number of Steps Required

```
StepsNeeded = 0
CurrentLoad_pct = InitialLoad_pct

for step in range(StartStep, 11):
    if CurrentLoad_pct >= TargetLoad_pct:
        break
    if LoadEnd_pct[step] <= TargetLoad_pct:
        StepsNeeded += 1
        CurrentLoad_pct = LoadEnd_pct[step]
    else:
        StepsNeeded += 1  # Partial step to target
        break
```

---

## Time-Series Calculations

### 3. Time at Each Step

```
Time_StepStart[0] = 0
Time_StepEnd[i] = Time_StepStart[i] + RecoveryTime[i]
Time_StepStart[i+1] = Time_StepEnd[i]
```

**Example:**
- Step 1 starts: t = 0 s
- Step 1 ends: t = 10 s (recovery complete)
- Step 2 starts: t = 10 s
- Step 2 ends: t = 20 s

### 4. Load at Each Step

```
Load_kW[i] = LoadEnd_pct[i] × P_rated / 100
```

### 5. Generator Output

**During Step Application (t = StepStart):**
```
GeneratorOutput_kW(t) = LoadStart_pct[i] × P_rated / 100
```

**After Recovery (t = StepEnd):**
```
GeneratorOutput_kW(t) = LoadEnd_pct[i] × P_rated / 100
```

**During Recovery (interpolated):**
```
GeneratorOutput_kW(t) = LoadStart_kW + (LoadEnd_kW - LoadStart_kW) × (t - StepStart) / RecoveryTime
```

---

## Frequency Response

### 6. Frequency Deviation (Per Step)

**Immediate Response (Speed Drop):**
```
DeltaF_Hz = -SpeedDrop_pct × f_nom / 100
```

**Steady-State Deviation (After Governor Response):**
```
DeltaF_over_F = -R × StepFraction
DeltaF_Hz = DeltaF_over_F × f_nom
```

Where:
```
StepFraction = StepSize_pct / 100
```

### 7. Rate of Change of Frequency (RoCoF)

**Initial RoCoF (Before Governor Response):**
```
RoCoF_Hz_per_s = -DeltaP_step / (2 × H × P_rated × f_nom)
```

Where:
```
DeltaP_step = StepSize_pct × P_rated / 100
```

**Example:**
- Step 1: 16% of 4300 kW = 688 kW
- RoCoF = -688 / (2 × 5 × 4300 × 60) = -0.000267 Hz/s
- At 60 Hz: -0.000267 × 60 = -0.016 Hz/s

**Note:** This is simplified. Actual RoCoF depends on generator dynamics and governor response time.

---

## BESS Sizing

### 8. Load Deficit

**At any time t:**
```
LoadDeficit_kW(t) = max(0, TargetLoad_kW - GeneratorOutput_kW(t))
```

### 9. BESS Energy Requirement

**Total Energy Required:**
```
BESS_Energy_kWh = ∫[t=0 to t=TotalRampTime] LoadDeficit_kW(t) dt
```

**Discrete Calculation (Trapezoidal Rule):**
```
BESS_Energy_kWh = Σ[i=0 to n-1] (LoadDeficit[i] + LoadDeficit[i+1]) / 2 × Δt[i]
```

### 10. BESS Power Rating

```
BESS_PowerRequired_kW = max(LoadDeficit_kW(t)) for all t
```

---

## Summary Outputs

### 11. Total Ramp Time

```
TotalRampTime_s = Σ[i=StartStep to EndStep] RecoveryTime[i]
```

### 12. Maximum Frequency Deviation

```
MaxFrequencyDeviation_Hz = min(DeltaF_Hz[i]) for all steps
```

### 13. Maximum RoCoF

```
MaxRoCoF_Hz_per_s = max(|RoCoF_Hz_per_s[i]|) for all steps
```

---

## Assumptions & Limitations

1. **Instantaneous Step Application:** Assumes load step is applied instantly at step start time
2. **Linear Recovery:** Generator output increases linearly during recovery period
3. **Simplified Frequency Response:** Uses first-order approximations; actual dynamics are more complex
4. **No Voltage Dynamics:** Only models frequency, not voltage dips
5. **Constant Inertia:** Assumes H remains constant (may vary with load)
6. **No Governor Delay:** Assumes instantaneous governor response (actual delay ~0.5-2s)
7. **No BESS Efficiency Losses:** Assumes 100% round-trip efficiency

---

## References

- `models/generator-risk-calculator/formulas.md` - Single-step formulas
- `data/generators/caterpillar/Caterpillar-Technical-Analysis.md` - CG260 specifications
- ISO 8528-5: Performance classes for generator sets
- Power system dynamics textbooks (Kundur, Anderson & Fouad)

