# Generator Risk Calculator - Test Scenarios

**Version:** 1.0  
**Last Updated:** 2025-12-02  
**Purpose:** Comprehensive test scenarios covering GREEN, YELLOW, and RED boundary conditions

---

## Overview

This test scenario suite expands the original 4 scenarios to **30+ scenarios** covering:
- ✅ **GREEN scenarios** - Safe operation (baseline and refined estimates)
- ⚠️ **YELLOW scenarios** - Marginal/caution zone (50-90% of max step)
- 🔴 **RED scenarios** - Unsafe/overload conditions (exceeds limits)
- **Edge cases** - Worst-case correlation, fast ramps, temperature derating, coordination failures

---

## Scenario Categories

### 1. Baseline Scenarios (GREEN)
**Purpose:** Validate existing scenarios and establish reference points

| Scenario | GPUs | Generator | Step % | Result |
|----------|------|-----------|--------|--------|
| Existing_G3520_FR_2x_GPU_Warmup | 1024 | G3520 FR (4000kW) | 12.3% | GREEN |
| Existing_CG260_16_GPU_Warmup | 1024 | CG260 (4300kW) | 11.4% | GREEN |
| Existing_CG260_16_BTC_Container | 5000 | CG260 (4300kW) | 10.5% | GREEN |
| Existing_G3516_1x_MidCluster | 256 | G3516 (1500kW) | 7.2% | GREEN |

---

### 2. YELLOW Scenarios (Marginal/Caution Zone)
**Purpose:** Test boundary conditions at 50-90% of generator's max step capability

**CG260-16 (16% max step):**
- `YELLOW_CG260_50pct_MaxStep` - 8% step (50% of limit)
- `YELLOW_CG260_75pct_MaxStep` - 12% step (75% of limit)
- `YELLOW_CG260_90pct_MaxStep` - 14.4% step (90% of limit)

**CG170-16 (20% max step):**
- `YELLOW_CG170_50pct_MaxStep` - 10% step (50% of limit)
- `YELLOW_CG170_90pct_MaxStep` - 18% step (90% of limit)

**G3520 FR (100% max step):**
- `YELLOW_G3520_50pct_MaxStep` - 50% step (50% of limit)
- `YELLOW_G3520_90pct_MaxStep` - 90% step (90% of limit)

**G3516 (100% max step):**
- `YELLOW_G3516_50pct_MaxStep` - 40% step (50% of limit)

**Other YELLOW scenarios:**
- `FastRamp_HighRoCoF` - Fast ramp (0.1s) creates high RoCoF
- `TemperatureDerating_CG260` - Generator derated to 90% capacity
- `MultiplePhaseTransitions` - Warmup spike (0.35kW) scenario
- `VeryLargeCluster_G3520` - 8192 GPUs on G3520 (30.7% step)

---

### 3. RED Scenarios (Overload/Unsafe)
**Purpose:** Test conditions that exceed generator limits

**CG260-16 Overloads:**
- `RED_CG260_Overload_110pct` - 17.6% step (110% of 16% limit)
- `RED_CG260_Overload_150pct` - 24% step (150% of 16% limit)
- `RED_CG260_2000_GPU_Sync` - 2000 GPUs with C=1.0 (exceeds 16%)
- `WorstCase_Correlation_C1_CG260` - Exactly at 16% limit with C=1.0
- `LargeCluster_CG260_Overload` - 4096 GPUs exceeds 16% limit
- `VeryLargeCluster_CG260_Impossible` - 8192 GPUs impossible without staggering

**CG170-16 Overloads:**
- `RED_CG170_Overload_110pct` - 22% step (110% of 20% limit)
- `WorstCase_Correlation_C1_CG170` - Exactly at 20% limit with C=1.0

**G3520 FR Overloads:**
- `RED_G3520_Overload_110pct` - 110% step (exceeds 100% rating)
- `RED_G3520_Overload_150pct` - 150% step (severe overload)

**G3516 Overloads:**
- `RED_G3516_Overload_110pct` - 110% step (exceeds 100% rating)

**Coordination Failures:**
- `BitcoinMiner_GPU_Coordination_Failed` - Miner shedding failed, high correlation

---

### 4. Refined Estimate Scenarios (GREEN)
**Purpose:** Validate refined power estimates from GPU phase research

| Scenario | GPUs | ΔP_GPU | Correlation | Step % | Result |
|----------|------|--------|-------------|--------|--------|
| RefinedEstimate_Realistic | 1024 | 0.225kW | 0.6 | 3.2% | GREEN |
| RefinedEstimate_HighCorrelation | 1024 | 0.225kW | 0.8 | 4.3% | GREEN |

**Note:** Refined estimates show 62.5% lower power steps than conservative estimates, indicating significant safety margin.

---

### 5. Edge Cases and Special Scenarios

**Ramp Rate Variations:**
- `FastRamp_HighRoCoF` - 0.1s ramp (high RoCoF, may trigger protection)
- `SlowRamp_LowRoCoF` - 10s ramp (low RoCoF, well within limits)

**Coordination Scenarios:**
- `BitcoinMiner_GPU_Coordination` - Successful coordination (low correlation, slow ramp)
- `BitcoinMiner_GPU_Coordination_Failed` - Failed coordination (high correlation, fast ramp)

**Cluster Size Variations:**
- `SmallCluster_CG170` - 128 GPUs (small cluster)
- `LargeCluster_G3520` - 4096 GPUs (large cluster)
- `VeryLargeCluster_G3520` - 8192 GPUs (very large cluster)

**Environmental Factors:**
- `TemperatureDerating_CG260` - Generator derated to 90% for high temperature

**Workload Variations:**
- `MultiplePhaseTransitions` - Warmup spike scenario (0.35kW per GPU)

---

## Risk Level Thresholds

**Formula:**
```
if StepFraction × 100 < MaxStep_pct × 0.5:
    RiskLevel = GREEN
elif StepFraction × 100 < MaxStep_pct:
    RiskLevel = YELLOW
else:
    RiskLevel = RED
```

**Interpretation:**
- **GREEN:** Step < 50% of generator's max step capability
- **YELLOW:** Step between 50-100% of generator's max step capability
- **RED:** Step exceeds generator's max step capability

---

## Generator Specifications Used

| Generator | Rated Power (kW) | Max Step (%) | H_eff (s) | R_eff (pu) |
|-----------|-----------------|--------------|-----------|------------|
| **CG260-16** | 4300 | 16% | 5 | 0.05 |
| **CG170-16** | 1560 | 20% | 4 | 0.04 |
| **G3520 FR** | 4000 | 100% | 3 | 0.04 |
| **G3516** | 1500 | 100% | 4 | 0.04 |

---

## Power Profile Assumptions

**Conservative Estimates (Original):**
- ΔP_GPU: 0.6 kW (worst-case)
- Correlation: 0.8 (worst-case synchronous)

**Refined Estimates (Validated):**
- ΔP_GPU: 0.2-0.25 kW (validated from GPU phase research)
- Correlation: 0.3-0.7 (typical operation range)

**Scenarios use both estimates:**
- Conservative (0.6 kW, C=0.8) for worst-case planning
- Refined (0.225 kW, C=0.6-0.8) for realistic modeling

---

## Usage

### Import into Calculator

1. Open `GeneratorRisk-v1.csv` in Excel/Sheets
2. Copy scenarios from `test-scenarios/scenarios.csv`
3. Paste into calculator (starting at row 2)
4. Review calculated outputs

### Validate Formulas

All scenarios include calculated outputs. Verify:
- `DeltaP_cluster_kW` = N_GPUs × DeltaP_GPU_kW × Correlation_C
- `RampRate_kW_per_s` = DeltaP_cluster_kW / DeltaT_event_s
- `StepFraction` = DeltaP_cluster_kW / P_rated_gen_kW
- `RiskLevel` matches expected result

---

## Expected Results Summary

| Risk Level | Count | Purpose |
|------------|-------|---------|
| **GREEN** | 15 scenarios | Baseline, refined estimates, safe operation |
| **YELLOW** | 9 scenarios | Boundary testing, marginal conditions |
| **RED** | 11 scenarios | Overload testing, failure modes |

**Total:** 35 scenarios

---

## Key Insights from Test Scenarios

1. **CG260-16 is most constrained:** Only 16% max step makes it vulnerable to overload
2. **G3520 FR is most flexible:** 100% block load capability handles large clusters
3. **Correlation matters:** C=1.0 (worst-case) can push scenarios from GREEN to RED
4. **Ramp rate matters:** Fast ramps (0.1s) create high RoCoF even if step size is acceptable
5. **Refined estimates show safety margin:** 0.225kW vs 0.6kW provides 62.5% reduction

---

## References

- `../formulas.md` - Calculator formulas
- `../README.md` - Calculator documentation
- `data/generators/caterpillar/` - Generator specifications
- `research/gpu-phase-research/CONSOLIDATED-SUMMARY.md` - Validated GPU power profiles

---

**Last Updated:** 2025-12-02

