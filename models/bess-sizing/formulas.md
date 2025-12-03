# BESS SIZING CALCULATOR - FORMULAS

**Version:** 1.0  
**Last Updated:** 2025-12-02

---

## Input Parameters

| Symbol | Name | Units | Description |
|--------|------|-------|-------------|
| P_gen | Generator_Power_kW | kW | Generator rated power |
| η_accept | Generator_Load_Acceptance_pct | % | Maximum safe load step as % of rated power |
| N_gpu | GPU_Count | count | Number of GPUs in cluster |
| P_gpu | GPU_Power_per_Unit_kW | kW | Per-GPU power rating |
| Island | Islanded_Operation | TRUE/FALSE | Whether site operates in island mode |
| BlackStart | Black_Start_Required | TRUE/FALSE | Whether black-start capability required |
| Sequencing | Load_Sequencing_Available | TRUE/FALSE | Whether load sequencing available |

---

## Calculated Outputs

### 1. GPU Cluster Power

```
GPU_Cluster_Power_kW = N_gpu × P_gpu
```

**Interpretation:** Total power rating of GPU cluster.

**Example:**
- 142 GPUs × 3.5 kW = 497 kW

---

### 2. Maximum Load Step

```
Max_Load_Step_kW = GPU_Cluster_Power_kW
```

**Assumption:** Worst-case scenario assumes entire cluster transitions simultaneously.

**Note:** In practice, correlation factor (C) from generator risk calculator may reduce this, but BESS sizing uses conservative worst-case.

**Example:**
- 497 kW (entire cluster)

---

### 3. Generator Load Acceptance Capability

```
Generator_Load_Acceptance_kW = P_gen × (η_accept / 100)
```

**Interpretation:** Maximum load step generator can safely accept.

**Example:**
- 1000 kW × (30 / 100) = 300 kW

---

### 4. Load Step Magnitude (Gap Analysis)

```
Load_Step_Magnitude_kW = Max_Load_Step_kW - Generator_Load_Acceptance_kW
```

**Interpretation:** 
- **Positive value:** Generator cannot handle step, BESS required
- **Zero or negative:** Generator can handle step, Buffer BESS optional

**Example:**
- 497 kW - 300 kW = 197 kW gap (BESS required)

---

### 5. BESS Type Decision Logic

#### Rule 1: No-BESS Check

```
if (N_gpu ≤ 4) AND (Generator_Type = "Natural_Gas_Fast_Response" OR "Rich_Burn") AND (NOT Island) AND (Risk_Tolerance = "High"):
    BESS_Type = "No_BESS"
```

**Conditions:** All must be true:
- GPU count ≤4 units
- Fast-response or rich-burn generator
- Not islanded operation
- High risk tolerance

---

#### Rule 2: Buffer BESS Check

```
if (Load_Step_Magnitude_kW ≤ 0) OR (Load_Step_Magnitude_kW < 200 AND Sequencing = TRUE):
    BESS_Type = "Buffer"
```

**Conditions:** Either:
- Generator can handle step (gap ≤ 0), OR
- Gap < 200 kW AND load sequencing available

**Configuration:**
- **Power:** 50-100 kW (20-40% of GPU cluster)
- **Energy:** 50-100 kWh (1-2 hours at power rating)
- **Cost:** $30,000-$60,000

---

#### Rule 3: Grid-Forming BESS (Default)

```
if (Load_Step_Magnitude_kW > 0) AND (Island = TRUE OR BlackStart = TRUE):
    BESS_Type = "Grid_Forming"
```

**Conditions:** 
- Generator cannot handle step (gap > 0), AND
- Islanded operation OR black-start required

**Configuration:**
- **Power:** 400-600 kW (80-120% of gap, with safety margin)
- **Energy:** 100-200 kWh (sufficient for transient support)
- **Cost:** $350,000-$500,000

---

### 6. BESS Power Sizing

#### Buffer BESS

```
BESS_Power_kW = MAX(50, MIN(100, GPU_Cluster_Power_kW × 0.3))
```

**Interpretation:** 20-40% of GPU cluster rating, clamped to 50-100 kW range.

**Example:**
- MIN(100, 497 × 0.3) = 100 kW (clamped to 100 kW max)

---

#### Grid-Forming BESS

```
BESS_Power_kW = MAX(400, Load_Step_Magnitude_kW × 1.2)
```

**Where:**
- 1.2 = Safety margin factor (20% overhead)
- Minimum 400 kW for grid-forming capability

**Interpretation:** BESS must cover load step gap plus safety margin.

**Example:**
- MAX(400, 197 × 1.2) = 400 kW (meets minimum)

**Alternative Formula (for large gaps):**
```
BESS_Power_kW = MIN(600, MAX(400, Load_Step_Magnitude_kW × 1.2))
```

Clamps to 400-600 kW range (typical grid-forming BESS sizes).

---

### 7. BESS Energy Sizing

#### Buffer BESS

```
BESS_Energy_kWh = BESS_Power_kW × 1.0
```

**Interpretation:** 1 hour at power rating (1:1 ratio).

**Example:**
- 75 kW × 1.0 = 75 kWh

---

#### Grid-Forming BESS

```
BESS_Energy_kWh = MAX(100, BESS_Power_kW × 0.25)
```

**Interpretation:** 0.25 hours (15 minutes) at power rating, minimum 100 kWh.

**Example:**
- MAX(100, 400 × 0.25) = 100 kWh

**Rationale:** Grid-forming BESS primarily provides power (not energy). Energy capacity sufficient for transient support and synthetic inertia.

---

### 8. BESS Cost Estimation

#### Buffer BESS

```
BESS_Cost_USD = 30000 + (BESS_Power_kW - 50) × 500
```

**Interpretation:** Linear cost model: $30,000 base + $500/kW above 50 kW.

**Example:**
- 30,000 + (75 - 50) × 500 = $42,500

**Range:** $30,000-$60,000 (for 50-100 kW range)

---

#### Grid-Forming BESS

```
BESS_Cost_USD = 350000 + (BESS_Power_kW - 400) × 750
```

**Interpretation:** Linear cost model: $350,000 base + $750/kW above 400 kW.

**Example:**
- 350,000 + (500 - 400) × 750 = $425,000

**Range:** $350,000-$500,000 (for 400-600 kW range)

**Note:** Costs are 2025 USD estimates. Actual costs vary based on:
- Site-specific factors (installation complexity)
- Regional pricing variations
- Vendor negotiations
- Component availability

---

## Decision Rationale Generation

### Buffer BESS Rationale

```
if (Load_Step_Magnitude_kW ≤ 0):
    Rationale = "[Generator type] generator ([acceptance]% acceptance) can handle [step]kW GPU step. Buffer BESS for ride-through only."
else:
    Rationale = "Load sequencing reduces effective step to <200kW. Buffer BESS sufficient for transient support."
```

---

### Grid-Forming BESS Rationale

```
if (Generator_Type contains "CG260"):
    Rationale = "[Generator model] ([acceptance]% first step) cannot handle [step]kW step. Grid-forming BESS required."
else:
    Rationale = "[Generator type] generator ([acceptance]% acceptance) cannot handle [step]kW GPU step. Grid-forming BESS required for islanded operation."
```

---

### No-BESS Rationale

```
Rationale = "Small cluster (≤4 GPUs) with fast-response generator. No-BESS viable with proper controls."
```

---

## Assumptions & Limitations

1. **Worst-Case Load Step:** Assumes entire GPU cluster transitions simultaneously (correlation C = 1.0). In practice, correlation may be lower (0.5-0.8), reducing effective step.

2. **Generator Acceptance:** Uses conservative estimates from manufacturer specifications. Actual performance may vary based on:
   - Operating conditions (temperature, altitude)
   - Fuel quality (methane number, Wobbe index)
   - Maintenance status
   - Governor tuning

3. **Load Sequencing:** Assumes sequencing can reduce effective step by 50-70%. Actual reduction depends on:
   - Sequencing algorithm sophistication
   - GPU workload characteristics
   - Control system response time

4. **Cost Estimates:** Based on 2025 market pricing. Costs may vary:
   - Regional pricing differences
   - Vendor-specific pricing
   - Installation complexity
   - Component availability

5. **No Multi-Step Modeling:** Does not model CG260 multi-step ramp sequences in detail. Uses first-step acceptance (16%) as conservative estimate.

6. **No Voltage Dynamics:** Only considers power/frequency. Voltage dip/recovery not modeled.

7. **No Economic Modeling:** Does not include:
   - TCO analysis
   - Break-even calculations
   - Battery degradation costs
   - Operational cost differences

---

## References

- ISO 8528-5: Performance classes for generator sets
- `research/bess-decision-analysis/BESS-DECISION-CONSOLIDATED-ANALYSIS.md` - Decision framework
- `research/bess-discrepancy-reports/BESS-DISCREPANCY-CONSOLIDATED-ANALYSIS.md` - Technical analysis
- Caterpillar application guides
- Power system dynamics textbooks (Kundur, Anderson & Fouad)

---

## Future Enhancements

Planned additions for v2:
- Multi-step generator ramp sequences (CG260 detailed modeling)
- Voltage dip calculations
- Economic modeling (TCO, break-even analysis)
- Battery degradation and lifecycle costs
- Multi-generator configurations
- Load sequencing effectiveness modeling
- Correlation factor integration from generator risk calculator

