# BESS SIZING CALCULATOR

**Version:** 1.0  
**Last Updated:** 2025-12-02  
**Status:** Working prototype

---

## Purpose

Calculate Battery Energy Storage System (BESS) sizing requirements for off-grid GPU inference deployments. Determines whether Buffer BESS (50-100 kWh) or Grid-Forming BESS (400-600 kW) is required based on generator type, GPU cluster configuration, and operational requirements.

---

## Quick Start Guide

### Step 1: Open Calculator
Open the CSV file in Excel, Google Sheets, or any spreadsheet application:
```
models/bess-sizing/BESS-Sizing-v1.csv
```

### Step 2: Edit Input Parameters (Yellow Cells)

**Generator Configuration:**
- `Generator_Type` - Type of generator (Natural_Gas, Diesel, Natural_Gas_Fast_Response, Natural_Gas_CG260, Natural_Gas_Lean_Burn, Natural_Gas_Rich_Burn)
- `Generator_Power_kW` - Generator rated power (kW)
- `Generator_Load_Acceptance_pct` - Maximum safe load step as % of rated power
  - **Natural Gas (Standard):** 25-35% (use 30% for conservative design)
  - **Natural Gas (Fast Response):** 100% (block load capable)
  - **Natural Gas (CG260):** 16% first step, then 13%, 10%, 9%... (see multi-step ramp table)
  - **Natural Gas (Lean Burn):** 25-30% (most restrictive)
  - **Natural Gas (Rich Burn):** 40-50% (better than lean-burn)
  - **Diesel:** 50-80% (use 70% for conservative design)

**GPU Cluster Configuration:**
- `GPU_Count` - Number of GPUs in cluster
- `GPU_Type` - GPU model (H100_PCIe, H100_SXM, A100_PCIe)
- `GPU_Power_per_Unit_kW` - Per-GPU power rating (kW)
  - **H100 PCIe:** 3.5 kW (350W TDP)
  - **H100 SXM:** 7.0 kW (700W TDP)
  - **A100 PCIe:** 2.5 kW (250W TDP)
- `GPU_Cluster_Power_kW` - Total cluster power = GPU_Count × GPU_Power_per_Unit_kW
- `Max_Load_Step_kW` - Maximum expected load step (typically equals GPU_Cluster_Power_kW for worst-case)

**Operational Requirements:**
- `Islanded_Operation` - TRUE if site operates in island mode (off-grid)
- `Black_Start_Required` - TRUE if BESS must provide black-start capability
- `Load_Sequencing_Available` - TRUE if GPU load can be sequenced/staggered to reduce transients

### Step 3: Review Calculated Outputs (Green Cells)

**Generator Capabilities:**
- `Generator_Load_Acceptance_kW` - Maximum load step generator can accept = Generator_Power_kW × Generator_Load_Acceptance_pct / 100
- `Load_Step_Magnitude_kW` - Net load step after generator acceptance = Max_Load_Step_kW - Generator_Load_Acceptance_kW

**BESS Recommendation:**
- `BESS_Type` - Recommended BESS type (Buffer, Grid_Forming, No_BESS)
- `BESS_Power_kW` - Required BESS power rating (kW)
- `BESS_Energy_kWh` - Required BESS energy capacity (kWh)
- `BESS_Cost_USD` - Estimated installed cost (USD)
- `Decision_Rationale` - Explanation of recommendation

---

## Decision Logic

### Rule 1: Buffer BESS (50-100 kWh / 50-100 kW)

**Use Buffer BESS when:**
- ✅ Generator can accept the load step (Load_Step_Magnitude_kW ≤ 0)
- ✅ OR load sequencing reduces effective step to <200 kW
- ✅ Grid connection or generator provides primary frequency support
- ✅ Islanding is rare and tolerant of frequency swings
- ✅ Black start not required

**Configuration:**
- **Power:** 50-100 kW (20-40% of GPU cluster rating)
- **Energy:** 50-100 kWh (1-2 hours at power rating)
- **Cost:** $30,000-$60,000 installed
- **Vendor:** BYD Battery-Box LVL (optimal for this range)

### Rule 2: Grid-Forming BESS (400-600 kW / 100-200 kWh)

**Use Grid-Forming BESS when:**
- ✅ Generator cannot accept the load step (Load_Step_Magnitude_kW > 0)
- ✅ AND islanded operation required
- ✅ AND load sequencing not available or insufficient
- ✅ OR black start capability required
- ✅ OR multiple concurrent load events possible

**Configuration:**
- **Power:** 400-600 kW (80-120% of load step magnitude)
- **Energy:** 100-200 kWh (sufficient for transient support)
- **Cost:** $350,000-$500,000 installed
- **Vendor:** Schneider Electric EcoStruxure, SMA Sunny Island, Dynapower MPS-125

### Rule 3: No-BESS

**Use No-BESS only when ALL are true:**
- ✅ GPU count ≤4 units
- ✅ Rich-burn or fast-response natural gas engine available
- ✅ Experienced control systems engineering team available
- ✅ High risk tolerance (experimental/research deployment)
- ✅ Budget constraints preclude any BESS investment

**Requirements:**
- Custom PLC-based microgrid controller
- 3-6 months development time
- Rigorous testing program (200-500 test scenarios)
- Conservative ramp rate limits

---

## Example Scenarios

### Scenario 1: 1 MW Natural Gas + 0.5 MW GPU (Islanded)
- **Generator:** 1000 kW natural gas (30% acceptance = 300 kW)
- **GPU Cluster:** 142 H100 PCIe = 497 kW
- **Load Step:** 497 kW - 300 kW = 197 kW gap
- **Result:** **Grid-Forming BESS** (400 kW / 150 kWh) - $400,000
- **Rationale:** Natural gas generator cannot handle GPU step. Grid-forming BESS required for islanded operation.

### Scenario 2: 1 MW Natural Gas + 0.5 MW GPU (With Load Sequencing)
- **Generator:** 1000 kW natural gas (30% acceptance = 300 kW)
- **GPU Cluster:** 142 H100 PCIe = 497 kW
- **Load Sequencing:** Reduces effective step to <200 kW
- **Result:** **Buffer BESS** (75 kW / 75 kWh) - $45,000
- **Rationale:** Load sequencing reduces effective step. Buffer BESS sufficient for transient support.

### Scenario 3: 1 MW Diesel + 0.5 MW GPU
- **Generator:** 1000 kW diesel (70% acceptance = 700 kW)
- **GPU Cluster:** 142 H100 PCIe = 497 kW
- **Load Step:** 497 kW - 700 kW = 0 kW gap (generator can handle)
- **Result:** **Buffer BESS** (50 kW / 50 kWh) - $30,000
- **Rationale:** Diesel generator can handle GPU step. Buffer BESS for ride-through only.

### Scenario 4: 2 MW Fast-Response Natural Gas + 0.5 MW GPU
- **Generator:** 2000 kW fast-response natural gas (100% acceptance = 2000 kW)
- **GPU Cluster:** 142 H100 PCIe = 497 kW
- **Load Step:** 497 kW - 2000 kW = 0 kW gap (generator can handle)
- **Result:** **Buffer BESS** (50 kW / 50 kWh) - $30,000
- **Rationale:** Fast-response natural gas (100% block load) can handle step. Buffer BESS for ride-through.

### Scenario 5: 4 MW CG260 + 2 MW GPU Cluster
- **Generator:** 4300 kW CG260 (16% first step = 688 kW)
- **GPU Cluster:** 571 H100 PCIe = 1998.5 kW
- **Load Step:** 1998.5 kW - 688 kW = 1310.5 kW gap
- **Result:** **Grid-Forming BESS** (600 kW / 200 kWh) - $500,000
- **Rationale:** CG260 (16% first step) cannot handle 1998.5 kW step. Grid-forming BESS required.

---

## Formulas

See: `formulas.md` for detailed formula documentation

---

## Cost Estimates

### Buffer BESS (50-100 kWh)
- **Power Rating:** 50-100 kW
- **Energy Capacity:** 50-100 kWh
- **Installed Cost:** $30,000-$60,000
- **Vendor:** BYD Battery-Box LVL (optimal for this range)
- **Source:** Consolidated research from 4 independent sources

### Grid-Forming BESS (400-600 kW)
- **Power Rating:** 400-600 kW
- **Energy Capacity:** 100-200 kWh
- **Installed Cost:** $350,000-$500,000
- **Vendors:** Schneider Electric EcoStruxure, SMA Sunny Island, Dynapower MPS-125
- **Source:** Consolidated research from 4 independent sources

**Note:** Costs are 2025 USD estimates. Actual costs may vary based on site-specific factors, regional pricing, and vendor negotiations.

---

## Limitations

**Current Version (v1) does NOT include:**
- Multi-step generator ramp sequences (CG260 detailed modeling)
- Voltage dynamics (only frequency/power considered)
- Economic modeling (TCO, break-even analysis)
- Battery degradation and lifecycle costs
- Multi-generator configurations
- Renewable energy integration

See: `docs/GAP_ANALYSIS.md` for planned enhancements

---

## Troubleshooting

### Common Issues

**Issue: Calculator recommends Grid-Forming BESS but budget only allows Buffer**
- **Cause:** Generator cannot accept load step
- **Solution:** 
  1. Consider load sequencing to reduce effective step
  2. Upgrade to fast-response generator or diesel
  3. Reduce GPU cluster size
  4. Accept operational risk (not recommended for commercial deployments)

**Issue: Load_Step_Magnitude_kW is negative**
- **Cause:** Generator can accept more load than GPU cluster requires
- **Solution:** This is correct - generator can handle the step. Use Buffer BESS for ride-through.

**Issue: Calculator shows different results than expected**
- **Cause:** Check generator load acceptance percentage - this is critical parameter
- **Solution:** Verify generator parameters from `data/generators/caterpillar/Caterpillar-Technical-Analysis.md`

### Getting Help

- **Formulas:** See `formulas.md` for detailed formula documentation
- **Generator Specs:** See `data/generators/` for complete generator data
- **BESS Research:** See `research/bess-decision-analysis/BESS-DECISION-CONSOLIDATED-ANALYSIS.md` for decision framework
- **Gap Analysis:** See `docs/GAP_ANALYSIS.md` for known limitations

---

## References

- `docs/PRD.md` - Calculator requirements
- `data/generators/caterpillar/` - Generator specifications
- `data/gpu-profiles/GPU-Power-Profiles.md` - GPU power characteristics
- `research/bess-decision-analysis/BESS-DECISION-CONSOLIDATED-ANALYSIS.md` - Decision framework
- `research/bess-discrepancy-reports/BESS-DISCREPANCY-CONSOLIDATED-ANALYSIS.md` - Technical analysis
- `docs/GAP_ANALYSIS.md` - Known limitations
- `docs/GLOSSARY.md` - Standardized terminology

