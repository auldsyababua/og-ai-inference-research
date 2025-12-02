# GPU-ASIC-Generator Operational Model

**Version:** 1.0  
**Date:** 2025-12-02  
**Status:** Core Operational Model

---

## Executive Summary

This document describes the operational model for a 1 MW natural gas generator powering 500 kW of Bitcoin miners (ASICs) and 500 kW of H100 GPUs. The model demonstrates how **shaped ramps** (small GPU steps) and **optional miner shedding** can keep net load changes within generator tolerances, making BESS **optional rather than required** for GPU ramp control.

**Key Principle:** Small steps are effectively free. By bringing GPUs online in small batches and optionally shedding equivalent ASIC load, the generator only ever sees small, controlled changes in net kW.

---

## 1. System Setup

### 1.1 Hardware Configuration

**Generator:**
- **Rated Power:** P_rated = 1000 kW (1 MW)
- **Type:** Natural gas genset
- **Constraints:**
  - Max safe step: ~20-30% of rating (200-300 kW)
  - Max ramp rate: kW/s (model-dependent)
  - **Key insight:** Small steps are fine, big sudden steps are bad

**Bitcoin Miners (ASICs):**
- **Target Steady-State:** 500 kW
- **Role:** Flexible ballast load
- **Control:** Can be turned off/on in kW chunks
- **Response Time:** Seconds (not milliseconds)

**H100 GPUs:**
- **Target Steady-State:** 500 kW of GPU load
- **Example:** H100 SXM5 at ~700 W each → ~714 GPUs for 500 kW
- **Power Phases:**
  - Preload/model-load: Moderate power (~30% of full)
  - Full compute: High power (~100% of full)

### 1.2 System Architecture

We manage two big controllable loads (miners + GPUs) behind one 1 MW machine.

**Total Capacity:** 1000 kW
- **ASICs:** Up to 500 kW (flexible)
- **GPUs:** Up to 500 kW (phased power)
- **Other Loads:** Small or fixed (assumed negligible for this model)

---

## 2. Control Goals

The control strategy has three primary objectives:

### 2.1 Keep Generator in Comfort Zone
- **No giant instantaneous steps:** Don't go from 500 → 900 kW in 100 ms
- **Respect max ramp rate:** |ΔP_gen / Δt| within engine/governor capabilities
- **Stay within step limits:** |ΔP_gen| ≤ Step_max over short Δt

### 2.2 Bring GPUs Up/Down Without Tripping
- Start big jobs safely
- Move from preload → full-power phase
- Shut down cleanly
- All without big shocks to the genset

### 2.3 Use Miners as Flexible Buffer (Optional)
- Miners can be dropped when extra headroom is needed quickly
- If patient, can avoid touching miners and just ramp GPUs within generator's natural tolerance
- **Key:** Miners are optional, not mandatory

---

## 3. State Variables

At any moment, we track:

### 3.1 Power Variables

- **P_gen(t)** – Generator output (kW), between 0 and 1000 kW
- **P_gpu(t)** – Total GPU power draw (kW), between 0 and 500 kW
- **P_miner(t)** – Total miner power draw (kW), between 0 and 500 kW
- **P_other(t)** – Any other site load (kW), assumed small or fixed

### 3.2 Power Balance Constraint

```
P_gen(t) ≈ P_gpu(t) + P_miner(t) + P_other(t)
```

(ignoring losses)

### 3.3 Generator Constraints

```
P_gen(t) ≤ 1000 kW
|ΔP_gen| ≤ Step_max over short Δt (e.g., no >200-300 kW jump in one shot)
|ΔP_gen / Δt| ≤ Ramp_max (kW/s)
```

We design the scheduler and miner control so that the net load the generator sees always respects these constraints.

---

## 4. Baseline Operating Point

### 4.1 Initial State: "Boring Steady Mining Mode"

- **P_gen = 500 kW**
- **P_miner = 500 kW**
- **P_gpu = 0 kW**
- **P_other ≈ 0 kW**

All 500 kW is going to miners. No GPUs running yet.

### 4.2 Target State: "Half ASIC / Half GPU"

- **P_gen = 1000 kW** (full load)
- **P_gpu ≈ 500 kW** (batch job fully up)
- **P_miner = 500 kW** (or adjusted based on spare capacity)
- **P_other ≈ 0 kW**

Generator between 500-1000 kW depending on desired operating point.

---

## 5. Step 1: Bringing GPUs Online from Zero

### 5.1 Core Principle: Tiny Steps Are Effectively Free

**Key Insight:** A single H100 at ~700 W is **0.07%** of a 1 MW generator.

- Turning on **1 GPU:** 0.7 kW step → trivial
- Turning on **10 GPUs:** 7 kW step → still trivial

These are tiny relative to:
- The generator rating (1000 kW)
- Typical allowed load steps (hundreds of kW)

**Model Assumption:**
- You can always bring up 1-N GPUs at a time (where N is small)
- Let the generator pick up that tiny extra load with no drama
- You have two levers:
  1. **Generator ramp:** Let P_gen rise to cover new GPUs
  2. **Miner shedding (optional):** Turn down miners by same kW to keep P_gen flat

### 5.2 Path A: "No Miner Changes, Genset Ramps Up Slowly"

**Strategy:** Let the generator ramp up naturally as GPUs come online.

**Initial State:**
- P_gen = 500 kW
- P_miner = 500 kW
- P_gpu = 0 kW

**Process:**
1. Turn on 1 GPU (700 W)
   - New load = 500.7 kW
   - Generator sees 0.7 kW step → trivial
   - Let governor ramp P_gen from 500 → 500.7 kW over ~1 second

2. Repeat:
   - Turn on another GPU → 501.4 kW
   - Continue in small increments

3. As long as we respect generator ramp spec (e.g., 20 kW/s), we're fine

**Timing Options:**
- 1 GPU every X seconds
- 5 GPUs every Y seconds
- As slowly as needed

**End State Example:**
- P_gen = 750 kW
- P_miner = 500 kW
- P_gpu = 250 kW

**Full Ramp:**
- Continue until P_gpu = 500 kW
- Final: P_gen = 1000 kW, P_miner = 500 kW, P_gpu = 500 kW
- Ramp from 500 → 1000 kW over minutes via small increments

**Key Point:** In this path, you never touch the miners. You simply let the generator ramp up as you bring more GPUs online in tiny steps. **No BESS required.**

### 5.3 Path B: "Keep Generator Flat, Use Miners as Ballast"

**Strategy:** Keep generator at fixed power (e.g., 1000 kW) and swap miners for GPUs.

**Control Law:**
- Set P_gen_target = 1000 kW (run gen at full output)
- Maintain: P_miner + P_gpu ≈ 1000 kW

**Initial State:**
- P_gen = 1000 kW
- P_miner = 1000 kW
- P_gpu = 0 kW

**Process:**
1. Turn on 1 GPU (0.7 kW)
2. Immediately drop 0.7 kW of miners (turn off ASICs totaling ~0.7 kW)
3. Net load seen by generator stays ~1000 kW
4. Electrically, it's almost a wash: 0.7 kW miners vanish, 0.7 kW GPUs appear

**Repeat:**
- Every time you add X kW of GPUs, shed X kW of miners
- Generator sees almost zero step load (ideally exactly zero if coordinated perfectly)

**End State:**
- P_gpu = 500 kW
- P_miner = 500 kW
- P_gen = 1000 kW

**Key Point:** In this path, the generator barely feels anything. You're just swapping one type of load (miners) for another (GPUs) in equal chunks. **No BESS required; just control.**

---

## 6. Step 2: Within a Job - Preload → Full-Power Phase

### 6.1 The Phase Transition Problem

Inside a job, GPUs have a phase change:

- **Phase A:** Preload/model load – ~30% of full power
- **Phase B:** Full inference/training – ~100% of full power

**Naive Behavior (Problematic):**
If all 250 GPUs at 30% jump to 100% simultaneously:
- 250 GPUs × (0.7 kW × 0.7 extra) ≈ 122.5 kW step
- This is a meaningful step that could strain the generator if instantaneous

### 6.2 Solution: Power-Aware Job Design

**We don't accept "slam everything from 30% → 100% instantly" as valid behavior.**

Instead, design the job pipeline:

#### 6.2.1 Preload Phase Finishes
- GPUs sitting at lower power, ready to start main compute

#### 6.2.2 Checkpoint / Hold
- Scheduler or firmware inserts a brief pause
- No new work yet
- Just existing preload state

#### 6.2.3 Controlled Ramp-Up
- Ramp GPU power caps from 30% → 100% in steps
- Example:
  - First 10 GPUs ramp over 0.5 s
  - Then next 10 GPUs
  - Continue in batches

#### 6.2.4 Parallel Actions
In parallel, either:
- Let the generator ramp (Path A), or
- Shed miners in chunks to keep P_gen constant (Path B), or
- Mix of both

#### 6.2.5 Start Heavy Compute
- Only after cluster reaches new steady GPU power
- Start the heavy, throughput-sensitive part of the job

**Result:** Generator always sees either:
- A small net step, or
- Almost no net step at all (if compensated with miner shedding)

**Again: No BESS required for this, just software control and respecting the gen's ramp spec.**

---

## 7. Edge Cases & Tolerances

### 7.1 You Never Have Literally Zero Margin

- Even when "using all 500 kW" in miners, there's natural tolerance
- Turning on 1 GPU (0.7 kW) doesn't instantly explode anything
- Generator can momentarily carry 500.7 kW and adjust

### 7.2 Generator Is Not Infinitely Picky

- A 1 MW machine will barely notice a 1-5 kW change
- Control loops, inertia, and voltage regulation tolerate small wobbles

### 7.3 You Control How Big Each Step Is

- **Heart of this model:** You never let 100 kW appear out of nowhere
- Stage things in small increments well below troublesome threshold (<10-20 kW steps)

### 7.4 Miners Are Optional, Not Mandatory

If okay with slower bring-up, you can do everything by:
- Ramping the generator
- Shaping GPU admission

If you want faster job start or to keep gen near fixed efficient load:
- Miners give you extra knobs
- Shed 50 kW of miners as you ramp 50 kW of GPUs over a few seconds

---

## 8. Where BESS Fits in This Model

### 8.1 BESS Is Not Strictly Required

In the 1 MW / 0.5 MW ASIC / 0.5 MW GPU model:

**We've shown that you can safely:**
- Bring GPUs online
- Move from preload → full power

**By:**
- Limiting how many GPUs change state at once (small batches)
- Staying inside generator's step and ramp limits
- Optionally shedding miners to keep net load flat

**In this theoretical control regime, a BESS is not strictly required for ramp management.** The generator's inertia + shaped ramps + miner flexibility are enough.

### 8.2 Why a BESS Might Still Be Worth Having

Even if we can engineer a no-BESS control scheme, a **small BESS may still be the more practical solution:**

#### 8.2.1 Easier to Build and Tune

**Control-only designs require:**
- More complex software
- Tighter integration between power and job schedulers
- More careful testing and edge-case handling

**Small BESS provides:**
- Forgiving buffer
- Control logic doesn't have to be perfect from day one

#### 8.2.2 Easier to Operate and Maintain

**With BESS smoothing fast edges:**
- Operating staff less exposed to "close to the limit" ramp conditions
- Less risk of nasty interactions between GPU scheduling and miner control
- System more tolerant of:
  - Minor misconfigurations
  - Unusual workloads
  - Firmware updates that change GPU power behavior

#### 8.2.3 Can Be Small and Still Very Useful

**Because we're already shaping ramps in software:**
- BESS doesn't need to carry minutes of full-site load
- A few seconds to tens of seconds of buffer at some fraction of site power (e.g., 50-200 kW) can:
  - Absorb mis-timed ramps
  - Ride through small faults or engine hiccups
  - Cover bootstrap for "first wave" of GPUs with zero drama

#### 8.2.4 Can Be Recharged with "GPU Budget"

**During periods when GPUs are idle or underutilized:**
- The "GPU slice" of generator capacity (0.5 MW) can recharge BESS
- BESS is mostly a burst-capacity device, not big energy store
- Topped up opportunistically without extra fuel beyond preferred generator range

#### 8.2.5 Might Be Cheaper in Total System Cost

**Even if BESS hardware costs upfront, it can:**
- Reduce required engineering time and complexity for control stack
- Reduce risk (and cost) of outages or equipment trips
- Potentially allow looser constraints on workloads

**It's plausible that:** "Small BESS + simpler controls" is cheaper and safer than "No BESS + very clever, brittle controls" once all capex + engineering + ops are accounted for.

### 8.3 Open Question for Future Work

**Current Stance:**

We have shown **feasibility of a no-BESS control model:**
- Shaped GPU ramps
- Respecting generator limits
- Optional miner shedding

**But we explicitly leave open the question:**

> "Is a small BESS actually the better, cheaper, more reliable design in practice?"

**Future Research/Modeling Should:**

**Compare scenarios:**
- **Scenario A:** No BESS, tight ramp scheduling + miner orchestration
- **Scenario B:** Small BESS (seconds of cover), simpler controls

**Quantify:**
- Capex difference (BESS + inverter vs extra engineering + complexity)
- Operational risk and failure modes
- Fuel/efficiency impacts
- Sensitivity to weird workloads

**For Now:**

BESS should be treated as:
- **Not strictly required** to make the 1 MW / 0.5 MW ASIC / 0.5 MW GPU design work
- **But a likely practical component** that could:
  - Make the system easier to build
  - More forgiving in operation
  - Potentially cheaper in full lifecycle cost

---

## 9. The "One Sentence" Description

> **We run a 1 MW gas generator feeding up to 500 kW of ASIC miners and 500 kW of H100 GPUs; we bring GPUs online in small batches and, when needed, shed equivalent ASIC load so the generator only ever sees small, controlled changes in net kW — making a BESS optional rather than fundamental to safe operation.**

---

## 10. Implications for BESS Sizing

### 10.1 If Using This Operational Model

**BESS sizing can be much smaller** than the 400-600 kW recommended in the BESS discrepancy reports because:

1. **Load steps are controlled:** Maximum step size is bounded by scheduler policy (e.g., <50-100 kW)
2. **Generator can handle small steps:** Steps of 50-100 kW are within generator's 25-40% acceptance capability
3. **Miner shedding provides additional buffer:** Can swap miners for GPUs to keep net load flat
4. **BESS role is different:** Not for handling 500 kW instantaneous steps, but for:
   - Absorbing mis-timed ramps
   - Riding through small faults
   - Covering bootstrap for first wave of GPUs
   - Providing grid-forming capability during startup

### 10.2 Revised BESS Sizing Logic

**With this operational model:**

**Minimum BESS Size:**
- Based on maximum allowed scheduler step (e.g., 50-100 kW)
- Plus safety margin (1.2-1.5×)
- **Result:** 60-150 kW minimum

**Recommended BESS Size:**
- 100-200 kW grid-forming BESS
- 50-200 kWh energy capacity (seconds to minutes of buffer)
- **Cost:** $80,000-$200,000 (vs $350,000-$500,000 for 400-600 kW)

**This aligns with the "Alternative Path" recommendations in the BESS discrepancy reports:**
- Report 1 & 3: 150-200 kW grid-forming BESS + load sequencing ($80-120k)
- Report 2 & 4: 50-100 kW + aggressive software throttling

### 10.3 Key Difference from BESS Reports

**BESS Reports Assumed:**
- Unmanaged worst-case steps (400-500 kW instantaneous)
- No load sequencing
- No miner coordination
- Natural gas generator must handle large steps alone

**This Operational Model Assumes:**
- Managed steps (50-100 kW maximum)
- Load sequencing via scheduler
- Optional miner coordination
- Generator sees only small, controlled changes

**Result:** BESS can be 3-5× smaller (100-200 kW vs 400-600 kW) with proper operational controls.

---

## 11. Implementation Considerations

### 11.1 Scheduler Requirements

**The scheduler must:**
- Enforce maximum GPU steps per time window
- Coordinate GPU phase transitions
- Optionally coordinate with miner control
- Respect generator ramp rate limits

**Example Policy:**
- Maximum 10 GPUs can change state per second
- Maximum 50 kW step per 1-second window
- Preload → full-power transitions must be staggered (e.g., 10 GPUs every 0.5 seconds)

### 11.2 Miner Control Integration

**If using Path B (miner shedding):**
- Real-time coordination between GPU scheduler and miner control
- Fast response time (seconds, not milliseconds)
- Ability to shed/add miners in kW chunks

### 11.3 Monitoring and Safety

**Required monitoring:**
- Real-time P_gen, P_gpu, P_miner
- Generator frequency and voltage
- Step size and ramp rate tracking
- BESS state of charge (if present)

**Safety interlocks:**
- Maximum step size limits
- Maximum ramp rate limits
- Frequency/voltage protection
- Automatic load shedding if limits exceeded

---

## 12. References

- **BESS Discrepancy Reports:** `research/bess-discrepancy-reports/`
- **Off-Grid Compute Modeling Challenges:** `research/gpu-compute/Off-Grid-Compute-Modeling-Challenges.md`
- **Multi-Step Ramp Simulator:** `models/multistep-ramp-simulator/`
- **Bitcoin Miner Integration:** `models/bitcoin-miner-integration/`

---

**Last Updated:** 2025-12-02  
**Version:** 1.0  
**Status:** Core Operational Model

