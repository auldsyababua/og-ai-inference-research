# Operational Model Validation Gaps

**Date:** 2025-12-02  
**Status:** Critical Validation Questions  
**Related Model:** `models/integrated-model/GPU-ASIC-GENERATOR-OPERATIONAL-MODEL.md`

---

## Executive Summary

The operational model demonstrates **feasibility** of a no-BESS control scheme using shaped ramps and optional miner shedding. However, several **critical validation questions** remain unanswered that could affect system reliability, performance, and cost. This document identifies gaps that should be addressed before finalizing the design.

**Recommendation:** **Yes, targeted research is needed** to validate key assumptions, but **not a full re-run** of all previous research. Focus on specific validation questions identified below.

---

## 1. Generator Response to Many Small Steps (HIGH PRIORITY)

### 1.1 The Question

**Model Assumption:** Small steps (0.7-7 kW) are "effectively free" and can be repeated continuously.

**Validation Needed:**

1. **Cumulative Frequency Deviation:**
   - If you do 100 small steps (0.7 kW each) over 100 seconds, does frequency deviation accumulate?
   - Or does the governor recover fully between steps?
   - What's the maximum frequency deviation during a long ramp sequence?

2. **RoCoF from Rapid Small Steps:**
   - What's the RoCoF if you do 10 steps of 7 kW each over 10 seconds?
   - Does it exceed 0.5-1.0 Hz/s protection limits?
   - How does this compare to one 70 kW step?

3. **Governor Response Time:**
   - What's the actual response time for a 0.7 kW step on a 1 MW generator?
   - What's the minimum time between steps before governor is ready for next step?
   - Does governor "get tired" or have reduced response after many steps?

4. **Generator Efficiency Impact:**
   - Does continuous small-step ramping affect generator efficiency?
   - Does it cause increased wear compared to steady-state operation?
   - What's the fuel penalty (if any)?

### 1.2 What We Know

- **Single small steps:** Research confirms 0.7 kW is trivial for 1 MW generator
- **RoCoF formula:** `RoCoF = -ΔP / (2 × H × S_base)` - but this assumes single step
- **CG260 multi-step table:** Shows discrete steps with 10s recovery time, but doesn't address many tiny steps

### 1.3 Research Needed

**Priority:** HIGH  
**Type:** Analytical modeling + literature review  
**Questions:**
- Can we model cumulative effects using existing formulas?
- Are there studies on generator response to many small steps vs one large step?
- What do generator manufacturers say about continuous small-step ramping?

---

## 2. GPU Power Phase Control Feasibility (HIGH PRIORITY)

### 2.1 The Question

**Model Assumption:** We can control GPU power caps in real-time to ramp from 30% → 100% in batches.

**Validation Needed:**

1. **Power Cap Control:**
   - Can NVIDIA GPUs actually be power-capped dynamically during inference?
   - What's the response time for power cap changes?
   - Does power capping affect inference performance/accuracy?

2. **Preload Phase Power Profile:**
   - What's the actual power during preload/model-load phase?
   - Is it really ~30% of full power, or does it vary?
   - How long does preload actually take?

3. **Checkpoint/Hold Feasibility:**
   - Can we insert a checkpoint after preload without affecting job?
   - What's the overhead of checkpointing?
   - Can GPUs hold at preload power indefinitely?

4. **Staggered Ramp Control:**
   - Can we ramp 10 GPUs every 0.5 seconds reliably?
   - What's the coordination complexity?
   - What happens if one GPU fails to ramp?

### 2.2 What We Know

- **GPU power phases:** We have estimated profiles (idle → launch → model load → warmup → inference)
- **Power capping:** NVIDIA GPUs support power limits via NVML API (`nvmlDeviceSetPowerManagementLimit()`)
  - **Reference:** `docs/nvidia-manuals/NVML-API-Reference-Guide.pdf`
  - NVML provides APIs for dynamic power limit adjustment during runtime
  - Power limit constraints available via `nvmlDeviceGetPowerManagementLimitConstraints()`
  - However, dynamic control **during active inference** (not just idle/preload) needs validation
- **Preload power:** Estimated at 200-300W for PCIe, 400-600W for SXM (30-40% of TDP)
- **Monitoring:** DCGM can be used to monitor power-aware scheduler behavior
  - **Reference:** `docs/nvidia-manuals/NVIDIA-DCGM-User-Guide.md`

### 2.3 Research Needed

**Priority:** HIGH  
**Type:** Technical documentation review + empirical testing  
**Questions:**
- ✅ NVIDIA documentation on power capping APIs: `docs/nvidia-manuals/NVML-API-Reference-Guide.pdf` (collected)
- ❓ Dynamic power capping **during active inference** (not just idle/preload) - needs empirical validation
- MLPerf or other benchmarks showing preload power profiles
- Feasibility of checkpoint/hold in common inference frameworks

**Available Resources:**
- NVML API Reference Guide provides power management APIs (`nvmlDeviceSetPowerManagementLimit()`, `nvmlDeviceGetPowerManagementLimitConstraints()`)
- DCGM User Guide provides monitoring tools for power-aware scheduler behavior
- **Gap:** Manuals provide APIs but do not provide empirical power profiles or validation of dynamic power capping during inference workloads

---

## 3. Miner Response Time and Coordination (MEDIUM PRIORITY)

### 3.1 The Question

**Model Assumption:** Miners can respond in seconds and can be shed in kW chunks to match GPU ramps.

**Validation Needed:**

1. **Miner Response Time:**
   - What's the actual response time for miner shedding?
   - Can miners respond fast enough (seconds) for Path B coordination?
   - What's the granularity of miner control (can we shed exactly 0.7 kW)?

2. **Coordination Complexity:**
   - How complex is real-time coordination between GPU scheduler and miner control?
   - What's the latency in the control loop?
   - What happens if coordination fails (miners don't shed when needed)?

3. **Partial Shedding:**
   - Can miners be partially shed (e.g., reduce hash rate by 50%)?
   - Or must they be fully on/off?
   - What's the impact on miner efficiency?

### 3.2 What We Know

- **Miner control:** Bitcoin miners can be controlled via API
- **Response time:** Estimated at seconds (not milliseconds)
- **Flexible load:** Miners are treated as controllable load in the model

### 3.3 Research Needed

**Priority:** MEDIUM  
**Type:** Technical documentation + vendor consultation  
**Questions:**
- Miner API documentation (response times, control granularity)
- Real-world miner control systems (how fast can they respond?)
- Feasibility of partial hash rate reduction vs full on/off

---

## 4. Failure Modes and Edge Cases (HIGH PRIORITY)

### 4.1 The Question

**Model Assumption:** Sequencing and coordination work reliably.

**Validation Needed:**

1. **Sequencing Failure:**
   - What happens if GPU sequencing fails and 100 GPUs start simultaneously?
   - What are the protection mechanisms?
   - How do we detect and recover from sequencing failures?

2. **Concurrent Events:**
   - What if multiple jobs start simultaneously?
   - What if generator has a hiccup during ramp?
   - What if miners fail to shed when needed?

3. **Network/Control Failures:**
   - What happens if control network fails?
   - What happens if GPU scheduler loses communication?
   - What are the fallback modes?

4. **Generator Hiccups:**
   - What if generator governor malfunctions during ramp?
   - What if fuel supply has momentary interruption?
   - How does BESS (if present) help vs hurt in these scenarios?

### 4.2 What We Know

- **Failure modes mentioned:** Some research mentions "bugs or misconfigurations could dispatch large load step"
- **BESS as buffer:** Small BESS can absorb mis-timed ramps
- **Protection systems:** Generator has under-frequency protection

### 4.3 Research Needed

**Priority:** HIGH  
**Type:** System design analysis + failure mode analysis  
**Questions:**
- What are the failure modes of GPU schedulers?
- What are the failure modes of miner control systems?
- What protection systems are needed?
- How does small BESS help vs complicate failure scenarios?

---

## 5. BESS Grid-Forming Minimum Size (MEDIUM PRIORITY)

### 5.1 The Question

**Model Assumption:** A 50-200 kW BESS can provide grid-forming capability for a 1 MW system.

**Validation Needed:**

1. **Grid-Forming Authority:**
   - Can a 50-100 kW BESS actually form the grid for a 1 MW system?
   - What's the minimum size for effective grid-forming?
   - What happens if BESS is too small (does it lose control)?

2. **Black-Start Capability:**
   - Can a small BESS initiate black-start for the generator?
   - What's the minimum size for black-start?
   - What's the sequence (BESS starts → generator starts → BESS transitions)?

3. **Droop Settings:**
   - What droop settings are needed for small BESS in large system?
   - Does very soft droop reduce grid-forming effectiveness?
   - How does this affect frequency stability?

### 5.2 What We Know

- **Grid-forming is control mode:** Reports confirm grid-forming is software, not hardware
- **Small GFM products exist:** 75-100 kW grid-forming BESS are deployed
- **Current limiting:** Reports note that small inverters hit current limits on large steps

### 5.3 Research Needed

**Priority:** MEDIUM  
**Type:** Literature review + vendor consultation  
**Questions:**
- Case studies of small grid-forming BESS in larger systems
- Minimum size recommendations from vendors
- Droop settings for small BESS in large microgrids

---

## 6. Frequency Stability During Long Ramps (MEDIUM PRIORITY)

### 6.1 The Question

**Model Assumption:** Generator can handle long ramp sequences (e.g., 500 kW over minutes) without frequency issues.

**Validation Needed:**

1. **Cumulative Frequency Deviation:**
   - During a 10-minute ramp from 500 → 1000 kW, what's the frequency profile?
   - Does frequency stay within acceptable bounds throughout?
   - What's the maximum deviation during the ramp?

2. **RoCoF During Ramp:**
   - What's the RoCoF during continuous small steps?
   - Does it exceed protection limits?
   - How does it compare to single large step?

3. **Governor Stability:**
   - Does governor remain stable during long ramps?
   - Any risk of governor hunting or oscillation?
   - What's the recovery time after ramp completes?

### 6.2 What We Know

- **RoCoF formula:** We have formulas for single steps
- **CG260 multi-step:** Shows discrete steps with recovery, but not continuous small steps
- **Frequency limits:** ±5% transient, ±1-2% steady-state typical

### 6.3 Research Needed

**Priority:** MEDIUM  
**Type:** Simulation/modeling  
**Questions:**
- Can we simulate long ramp sequences using existing generator models?
- Are there studies on frequency stability during long ramps?
- What are the limits for continuous ramping?

---

## 7. Energy Capacity Requirements (LOW PRIORITY)

### 7.1 The Question

**Model Assumption:** BESS needs 50-200 kWh (seconds to minutes of buffer).

**Validation Needed:**

1. **Extended Ramp Scenarios:**
   - What if generator takes longer than expected to ramp?
   - What if multiple ramps happen sequentially?
   - How much energy is needed for worst-case scenarios?

2. **BESS Recharge:**
   - How long does it take to recharge BESS using "GPU budget"?
   - What if GPUs are always busy (no recharge opportunity)?
   - What's the minimum SoC for reliable operation?

### 7.2 What We Know

- **Energy for inertia:** Reports show <1 kWh needed for synthetic inertia
- **Ride-through:** Depends on use case (seconds vs minutes)
- **Recharge strategy:** Model mentions using GPU capacity when idle

### 7.3 Research Needed

**Priority:** LOW  
**Type:** Scenario analysis  
**Questions:**
- Worst-case energy scenarios
- Recharge time calculations
- Minimum SoC requirements

---

## 8. Scheduler Complexity and Integration (MEDIUM PRIORITY)

### 8.1 The Question

**Model Assumption:** Scheduler can enforce step limits and coordinate with miner control.

**Validation Needed:**

1. **Scheduler Complexity:**
   - How complex is the software to enforce step limits?
   - What's the integration effort with GPU schedulers (Kubernetes/Slurm)?
   - What's the performance overhead?

2. **Coordination Latency:**
   - What's the latency in GPU scheduler → miner control loop?
   - Can coordination be fast enough for Path B (miner shedding)?
   - What's the jitter/variance in response times?

3. **Testing and Validation:**
   - How do you test sequencing logic?
   - How do you validate it works correctly?
   - What's the risk of bugs causing large steps?

### 8.2 What We Know

- **Scheduler requirements:** Model defines policy (max 10 GPUs/second, max 50 kW/1s)
- **Complexity mentioned:** Research notes "more complex software" for control-only designs
- **Failure modes:** Research mentions "bugs or misconfigurations could dispatch large load step"

### 8.3 Research Needed

**Priority:** MEDIUM  
**Type:** System design + implementation planning  
**Questions:**
- Scheduler integration examples (Kubernetes power-aware scheduling)
- Control system architecture options
- Testing strategies for sequencing logic

---

## Research Recommendations

### Immediate (Before Final Design)

1. **Generator Response to Many Small Steps** (HIGH)
   - Analytical modeling of cumulative effects
   - Literature review on continuous small-step ramping
   - Generator manufacturer consultation

2. **GPU Power Phase Control Feasibility** (HIGH)
   - NVIDIA documentation review
   - Empirical testing if possible
   - Framework compatibility check

3. **Failure Modes Analysis** (HIGH)
   - System failure mode analysis
   - Protection system design
   - Fallback mode definition

### Short-Term (During Design Phase)

4. **Miner Response Time** (MEDIUM)
   - Miner API documentation
   - Vendor consultation
   - Control system design

5. **Frequency Stability During Ramps** (MEDIUM)
   - Simulation of long ramp sequences
   - Frequency profile analysis
   - RoCoF validation

6. **BESS Grid-Forming Minimum Size** (MEDIUM)
   - Case study review
   - Vendor consultation
   - Droop setting analysis

### Long-Term (During Implementation)

7. **Scheduler Complexity** (MEDIUM)
   - Implementation planning
   - Integration architecture
   - Testing strategy

8. **Energy Capacity** (LOW)
   - Scenario analysis
   - Recharge calculations

---

## Conclusion

**Do we need to rerun deep research?** 

**No, not a full re-run.** However, **targeted validation research is needed** on:

1. **Generator response to many small steps** (cumulative effects, RoCoF, governor response)
2. **GPU power phase control feasibility** (can we actually do this?)
3. **Failure modes and edge cases** (what can go wrong?)

These are **critical validation questions** that could affect system reliability. The operational model is **theoretically sound** but needs **practical validation** of key assumptions.

**Recommended Approach:**
- Start with analytical modeling and literature review (quick, low-cost)
- Follow with targeted vendor consultations (medium cost, high value)
- Consider empirical testing for GPU power control (higher cost, but definitive)

The model provides a **solid foundation** but these validations will determine if it's **practically implementable** vs **theoretically possible**.

---

**Last Updated:** 2025-12-02  
**Status:** Validation Gaps Identified - Research Needed

