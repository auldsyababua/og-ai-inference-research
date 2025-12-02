# MULTI-STEP RAMP SIMULATOR - EXAMPLE SCENARIOS

**Version:** 1.0  
**Last Updated:** 2025-12-01

---

## Scenario 1: CG260 Cold Start to 50% Load

**Configuration:**
- Generator: CG260-16 (4300 kW rated)
- Initial Load: 0 kW (0%)
- Target Load: 2150 kW (50%)

**Results:**
- **Steps Required:** 4 steps (Steps 1-4)
- **Total Ramp Time:** 40 seconds
- **BESS Energy Required:** ~3.87 kWh
- **BESS Power Required:** 688 kW (peak deficit at Step 1)
- **Max Frequency Deviation:** -2.4 Hz (at each step)
- **Max RoCoF:** -0.24 Hz/s

**Interpretation:**
- Generator can reach 50% load in 4 discrete steps
- BESS must carry full load deficit during ramp
- Frequency dips to 57.6 Hz at each step, recovers to 60 Hz during 10s recovery period

**Use Case:** Partial facility startup, staged GPU cluster activation

---

## Scenario 2: CG260 Cold Start to 100% Load

**Configuration:**
- Generator: CG260-16 (4300 kW rated)
- Initial Load: 0 kW (0%)
- Target Load: 4300 kW (100%)

**Results:**
- **Steps Required:** 10 steps (complete sequence)
- **Total Ramp Time:** 100 seconds (1 minute 40 seconds)
- **BESS Energy Required:** ~95 kWh (estimated)
- **BESS Power Required:** 688 kW (peak deficit at Step 1)
- **Max Frequency Deviation:** -2.4 Hz
- **Max RoCoF:** -0.24 Hz/s

**Interpretation:**
- Full ramp from cold start requires complete 10-step sequence
- BESS must carry full facility load for entire 100-second period
- This is the worst-case scenario for BESS sizing

**Use Case:** Complete facility blackout recovery, full capacity startup

---

## Scenario 3: CG260 Partial Ramp (25% → 75%)

**Configuration:**
- Generator: CG260-16 (4300 kW rated)
- Initial Load: 1075 kW (25%)
- Target Load: 3225 kW (75%)

**Results:**
- **Starting Step:** Step 3 (29% is closest step above 25%)
- **Steps Required:** 5 steps (Steps 3-7)
- **Total Ramp Time:** 50 seconds
- **BESS Energy Required:** ~25 kWh (estimated)
- **BESS Power Required:** 430 kW (peak deficit)
- **Max Frequency Deviation:** -2.4 Hz
- **Max RoCoF:** -0.15 Hz/s

**Interpretation:**
- Starting from partial load reduces BESS requirements
- Fewer steps needed than cold start
- Lower peak deficit since generator already at 25%

**Use Case:** Adding GPU capacity to partially loaded facility, load increase during operation

---

## Scenario 4: CG260 GPU Cluster Warmup (500 kW Step)

**Configuration:**
- Generator: CG260-16 (4300 kW rated)
- Initial Load: 2000 kW (46.5%)
- Target Load: 2500 kW (58.1%)
- **Load Step:** 500 kW (11.6% of rated)

**Results:**
- **Starting Step:** Step 4 (48% is closest step above 46.5%)
- **Steps Required:** 1 step (Step 5: 48% → 57%)
- **Total Ramp Time:** 10 seconds (single recovery period)
- **BESS Energy Required:** ~0.7 kWh
- **BESS Power Required:** 500 kW
- **Max Frequency Deviation:** -2.4 Hz
- **Max RoCoF:** -0.09 Hz/s

**Interpretation:**
- Small load step fits within single CG260 step capability
- Minimal BESS requirement
- Fast ramp (10 seconds)

**Use Case:** GPU cluster warmup during normal operation, incremental load addition

---

## Scenario 5: CG260 Bitcoin Miner Container Addition

**Configuration:**
- Generator: CG260-16 (4300 kW rated)
- Initial Load: 1500 kW (34.9%)
- Target Load: 3000 kW (69.8%)
- **Load Step:** 1500 kW (34.9% of rated)

**Results:**
- **Starting Step:** Step 3 (39% is closest step above 34.9%)
- **Steps Required:** 4 steps (Steps 3-6: 39% → 66%)
- **Total Ramp Time:** 40 seconds
- **BESS Energy Required:** ~17 kWh (estimated)
- **BESS Power Required:** 559 kW (peak deficit)
- **Max Frequency Deviation:** -2.4 Hz
- **Max RoCoF:** -0.15 Hz/s

**Interpretation:**
- Large load addition requires multiple steps
- BESS must buffer during ramp
- Moderate ramp time (40 seconds)

**Use Case:** Adding bitcoin miner container, large flexible load integration

---

## Key Insights

1. **Cold Start is Worst Case:** Full 0% → 100% ramp requires maximum BESS capacity (~95 kWh for 4300 kW generator)

2. **Partial Ramps Reduce Requirements:** Starting from non-zero load significantly reduces BESS energy needs

3. **Step Size Matters:** Load steps that fit within single CG260 step (≤16% for first step) minimize ramp time

4. **BESS Power Rating:** Peak deficit occurs at first step (688 kW for 4300 kW generator), regardless of target load

5. **Frequency Stability:** Each step causes 8% speed drop (2.4 Hz at 60 Hz), but recovers during 10s stabilization period

---

## Recommendations

**For Planning:**
- Size BESS for worst-case cold start scenario
- Consider staged facility startup to reduce BESS requirements
- Use flexible loads (bitcoin miners) to offset GPU ramps

**For Operations:**
- Pre-load generator to 25-50% before GPU cluster activation
- Coordinate GPU warmup with generator ramp sequence
- Monitor frequency during ramp sequences

---

## References

- `MultiStepRamp-v1.csv` - Simulator spreadsheet
- `formulas.md` - Detailed calculation formulas
- `CG260-Load-Step-Table.md` - Complete step sequence reference

