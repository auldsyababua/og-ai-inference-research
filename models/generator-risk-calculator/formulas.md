# GENERATOR RISK CALCULATOR - FORMULAS

**Version:** 1.0
**Last Updated:** 2025-12-01

---

## Input Parameters

| Symbol | Name | Units | Description |
|--------|------|-------|-------------|
| N | N_GPUs | count | Number of GPUs in cluster |
| ΔP_gpu | DeltaP_GPU_kW | kW | Per-GPU power step |
| C | Correlation_C | 0-1 | Fraction of GPUs transitioning together |
| Δt | DeltaT_event_s | s | Time window of transition |
| P_rated | P_rated_gen_kW | kW | Generator rated power |
| H | H_eff_s | s | Effective inertia constant |
| R | R_eff_pu | p.u. | Governor droop (per unit) |
| f_nom | f_nom_Hz | Hz | Nominal frequency |
| MaxStep | MaxStep_pct | % | Maximum safe load step |

---

## Calculated Outputs

### 1. Cluster Power Step
```
ΔP_cluster = C × N × ΔP_gpu
```

**Interpretation:** Total power change when the specified fraction of GPUs transition.

**Example:**
- 1024 GPUs × 0.6 kW × 0.8 correlation = 491.52 kW

---

### 2. Ramp Rate
```
RampRate = ΔP_cluster / Δt
```

**Units:** kW/s

**Interpretation:** Rate at which the cluster load changes.

**Example:**
- 491.52 kW ÷ 1 s = 491.52 kW/s

---

### 3. Step Fraction
```
StepFraction = ΔP_cluster / P_rated
```

**Units:** per unit (dimensionless)

**Interpretation:** Load step as a fraction of generator capacity.

**Example:**
- 491.52 kW ÷ 4000 kW = 0.12288 (12.3%)

---

### 4. Steady-State Frequency Deviation
```
ΔF / F_nom ≈ -R × StepFraction
```

**Units:** per unit (or Hz if multiplied by f_nom)

**Derivation:** From governor droop characteristic:
- Droop = (Δf / f_nom) / (ΔP / P_rated)
- Rearranging: Δf / f_nom = -R × (ΔP / P_rated)

**Example:**
- -(0.04) × 0.12288 = -0.0049152 p.u. (or -0.295 Hz at 60 Hz)

---

### 5. Rate of Change of Frequency (RoCoF)
```
df/dt ≈ -ΔP_cluster / (2 × H × S_base)
```

Where:
- S_base = P_rated (assuming unity power factor)
- H = inertia constant (seconds)

**Units:** Hz/s

**Derivation:** From swing equation for synchronous machines.

**Example:**
- -491.52 kW ÷ (2 × 3 s × 4000 kW) = -0.02048 p.u./s
- At 60 Hz: -0.02048 × 60 = -1.229 Hz/s

**Note:** This is the *initial* rate of change before governor response.

---

### 6. Step Within Limit Check
```
StepWithinLimit = (StepFraction × 100 < MaxStep_pct)
```

**Result:** TRUE or FALSE

**Example:**
- 12.3% < 100% → TRUE

---

### 7. Risk Level Classification

```
if StepFraction × 100 < MaxStep_pct × 0.5:
    RiskLevel = GREEN
elif StepFraction × 100 < MaxStep_pct:
    RiskLevel = YELLOW
else:
    RiskLevel = RED
```

**Thresholds:**
- **GREEN:** Less than 50% of generator's max step
- **YELLOW:** Between 50% and 100% of max step
- **RED:** Exceeds generator's max step capability

---

## Assumptions & Limitations

1. **Linear Scaling:** Assumes all GPUs transition with same ΔP
2. **Single Step:** Does not model multi-step sequences
3. **Simplified Dynamics:** Uses first-order approximations
4. **No Voltage:** Only models frequency response
5. **No BESS:** Does not include energy storage buffering
6. **Steady State:** Governor droop formula assumes steady-state

---

## References

- ISO 8528-5: Performance classes for generator sets
- Power system dynamics textbooks (Kundur, Anderson & Fouad)
- Caterpillar application guides

---

## Future Enhancements

Planned additions for v2:
- Multi-phase GPU modeling
- Multi-step ramp sequences
- Voltage dip calculations
- BESS sizing integration
- Time-series simulation output
