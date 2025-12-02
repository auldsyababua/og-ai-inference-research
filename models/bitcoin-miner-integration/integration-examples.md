# BITCOIN MINER INTEGRATION - EXAMPLES

**Version:** 1.0  
**Last Updated:** 2025-12-02

---

## Example 1: Perfect Offset - GPU Warmup with Miner Shedding

**Scenario:** GPU cluster warmup (500 kW ramp) with sufficient miner capacity

**Configuration:**
- **GPU Ramp:** 500 kW over 10 seconds
- **Miner Capacity:** 3 containers × 1 MW = 3 MW available
- **Miner Model:** M60S (3.3 kW per unit)
- **Generator:** CG260-16 (4300 kW rated)

**Coordination:**
1. **GPU Signals:** "Ramping up 500 kW in 10 seconds"
2. **Miner Controller:** "Shedding 500 kW (152 units)"
3. **Response Time:** 500 ms (miners shut down)
4. **GPU Ramp:** 500 kW over 10 seconds
5. **Net Load Change:** 500 kW - 500 kW = **0 kW**

**Result:**
- ✅ Generator sees **zero net change**
- ✅ No generator ramp required
- ✅ No BESS required for this ramp
- ✅ Economic cost: $0.14 per event (negligible)

**Generator Impact:**
- Step fraction: 0% (within all limits)
- Risk level: GREEN
- No frequency deviation
- No RoCoF

---

## Example 2: Large GPU Cluster Startup with Full Container Shedding

**Scenario:** Large GPU cluster startup (2000 kW ramp) using full container shedding

**Configuration:**
- **GPU Ramp:** 2000 kW over 60 seconds
- **Miner Capacity:** 3 containers × 1 MW = 3 MW available
- **Miner Model:** M60S (3.3 kW per unit)
- **Generator:** CG260-16 (4300 kW rated)

**Coordination:**
1. **GPU Signals:** "Ramping up 2000 kW in 60 seconds"
2. **Miner Controller:** "Shedding 2 full containers (2 MW)"
3. **Response Time:** 500 ms (containers shut down)
4. **GPU Ramp:** 2000 kW over 60 seconds
5. **Net Load Change:** 2000 kW - 2000 kW = **0 kW**

**Result:**
- ✅ Generator sees **zero net change**
- ✅ No generator ramp required
- ✅ No BESS required for this ramp
- ✅ Economic cost: $0.56 per event (still negligible)

**Generator Impact:**
- Step fraction: 0% (within all limits)
- Risk level: GREEN
- No frequency deviation
- No RoCoF

---

## Example 3: Partial Offset - Limited Miner Capacity

**Scenario:** GPU ramp exceeds available miner capacity

**Configuration:**
- **GPU Ramp:** 1000 kW over 30 seconds
- **Miner Capacity:** 1 container × 1 MW = 1 MW available
- **Miner Model:** M60S (3.3 kW per unit)
- **Generator:** CG260-16 (4300 kW rated)

**Coordination:**
1. **GPU Signals:** "Ramping up 1000 kW in 30 seconds"
2. **Miner Controller:** "Shedding 1 full container (1 MW) - maximum available"
3. **Response Time:** 500 ms (container shuts down)
4. **GPU Ramp:** 1000 kW over 30 seconds
5. **Net Load Change:** 1000 kW - 1000 kW = **500 kW** (partial offset)

**Result:**
- ⚠️ Generator sees **500 kW net increase** (23% of rated)
- ⚠️ Requires generator ramp (within CG260 16% first step limit - **RED**)
- ⚠️ May require BESS buffering for first step
- ✅ Economic cost: $0.28 per event

**Generator Impact:**
- Step fraction: 11.6% (500 kW / 4300 kW)
- Risk level: **YELLOW** (within 16% limit but high)
- Frequency deviation: ~-0.58 Hz (at 5% droop)
- RoCoF: ~-0.12 Hz/s

**Mitigation Options:**
1. **Stagger GPU Ramp:** Split 1000 kW into two 500 kW ramps (10s apart)
2. **Add BESS:** Use BESS to buffer the 500 kW net step
3. **Add More Miners:** Increase miner capacity to 2 MW

---

## Example 4: Multi-Step Generator Ramp with Staged Miner Shedding

**Scenario:** Large GPU ramp coordinated with CG260 multi-step ramp sequence

**Configuration:**
- **GPU Ramp:** 2000 kW total (wants immediate)
- **Miner Capacity:** 3 containers × 1 MW = 3 MW available
- **Generator:** CG260-16 (requires multi-step ramp: 16% → 13% → 10% → ...)

**Coordination Strategy:**
1. **Pre-Ramp:** Shed 2000 kW of miners (2 containers)
2. **Generator Step 1:** Generator ramps 16% (688 kW) over 10s
   - Miners already shed, generator picks up 688 kW
   - Net: 0 kW change (miners offset)
3. **Generator Step 2:** Generator ramps 13% (559 kW) over 10s
   - Generator picks up additional 559 kW
   - Net: 0 kW change (miners still offset)
4. **Continue:** Generator continues multi-step sequence
   - Miners remain shed until generator reaches full load
5. **Post-Ramp:** Miners can restart after generator stabilizes

**Result:**
- ✅ Generator sees **zero net change** at each step
- ✅ Multi-step ramp proceeds normally
- ✅ No BESS required for coordination
- ✅ Economic cost: $0.56 per event

**Generator Impact:**
- Each step: 0% net change (perfect offset)
- Risk level: GREEN
- No frequency deviation
- No RoCoF

---

## Example 5: Small GPU Step - No Miner Coordination Needed

**Scenario:** Small GPU step within generator single-step capability

**Configuration:**
- **GPU Ramp:** 100 kW over 5 seconds
- **Miner Capacity:** Available but not needed
- **Generator:** CG260-16 (16% first step = 688 kW limit)

**Coordination:**
- **Decision:** No miner shedding needed
- **Reason:** 100 kW is only 2.3% of generator capacity (well within 16% limit)
- **GPU Ramp:** 100 kW directly to generator
- **Net Load Change:** 100 kW

**Result:**
- ✅ Generator handles directly (no coordination needed)
- ✅ Step fraction: 2.3% (well within limits)
- ✅ Risk level: GREEN
- ✅ No economic cost (miners continue running)

**Generator Impact:**
- Step fraction: 2.3% (within all limits)
- Risk level: GREEN
- Frequency deviation: ~-0.12 Hz (at 5% droop)
- RoCoF: ~-0.02 Hz/s

---

## Key Insights

1. **Perfect Coordination:** When miner shed = GPU ramp, generator sees zero net change
2. **Economic Cost:** Negligible ($0.10-$0.50 per event) compared to BESS costs
3. **Response Time:** 100-500ms acceptable for multi-second ramps (>1s)
4. **Partial Offset:** Even partial miner shedding reduces generator step requirements
5. **Multi-Step Coordination:** Miners can remain shed during entire generator ramp sequence

---

## Integration with Multi-Step Ramp Simulator

**Workflow:**
1. **Calculate GPU Ramp:** Determine GPU power step and duration
2. **Calculate Miner Shed:** Determine available miner capacity and shedding strategy
3. **Calculate Net Load:** GPU ramp - Miner shed = Net load change
4. **Feed to Ramp Simulator:** Use net load change as input
5. **Result:** Generator ramp requirements (if any) after miner coordination

**Example Integration:**
```
GPU Ramp: 500 kW
Miner Shed: 500 kW
Net Load: 0 kW
→ Feed 0 kW to ramp simulator
→ Result: No generator ramp needed
```

---

## References

- `MinerIntegration-v1.csv` - Calculator spreadsheet
- `formulas.md` - Detailed calculation formulas
- `models/multistep-ramp-simulator/` - Generator ramp simulator
- `data/miners/Whatsminer-Miner-Library.md` - Miner specifications

---

**Last Updated:** 2025-12-02

