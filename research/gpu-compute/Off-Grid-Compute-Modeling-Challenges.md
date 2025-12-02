# **Off-Grid Compute – Open Modeling Challenges**

## **1\. GPU Cluster Ramp Rates (kW/s)**

### **What the issue is**

GPU jobs don’t just “turn on” once. They move through phases:

* Preload / model load (moderate power)

* Warmup / steady compute (high power)

* Tear-down (dropping back to lower power)

Each transition is a **power step per GPU**, and when many GPUs change phase together, the cluster presents a **kW step** to the generator. Over some time window Δt, that becomes a ramp rate in **kW/s**.

### **What we’ve established**

* The **raw physics** are simple: if one GPU jumps by ΔP\_gpu watts, then C·N GPUs doing that together make a total step  
   ΔP\_cluster \= C · N · ΔP\_gpu  
   and a ramp \= ΔP\_cluster / Δt.

* A **single GPU** (even a 700 W H100) is basically a rounding error to a **1 MW generator**. The generator’s inertia can easily absorb that instantaneous step without blinking.

* The danger is **not** one GPU; it’s **many GPUs moving together** and producing big net steps.

* We are **not forced** to let all GPUs jump at once:

  * We can ramp them in batches (e.g. 1–5 GPUs at a time).

  * We can stretch that ramp over seconds to keep **cluster-level ΔP/Δt** inside generator limits.

### **New decision: “shaped ramps by design”**

For this project, we’ll assume:

* GPU power phases are **software-controllable** at the cluster level:

  * We can choose how many GPUs enter a new phase per second.

  * We can slow the ramp intentionally (e.g. 50 GPUs over 10 seconds, not all in 10 ms).

* Worst-case ramps for modeling are therefore **bounded by scheduler policies**, not by “all GPUs slam on at once.”

### **Why it matters**

Generator constraints (max step %, ramp rate, RoCoF) are hard limits. We can’t change the engine physics, but we *can* change how many GPUs move at once. Modeling worst-case ramps with **scheduler-imposed limits** is the bridge between “what GPUs want” and “what the generator can survive.”

---

## **2\. Correlation Dynamics (Synchronous vs Staggered GPUs)**

### **What the issue is**

**Correlation** \= how many GPUs change state in the same short time window.

* High correlation: big instantaneous cluster step.

* Low correlation: same total work, but spread out in time.

At large N, correlation is the difference between “fine” and “instant blackout.”

### **What we’ve established**

* Full synchronization (C ≈ 1\) on a large cluster is **both avoidable and undesirable** off-grid.

* We can **intentionally de-correlate**:

  * Only allow a max number of GPUs per second to enter a new phase.

  * Add jitter to job launches so no big “start everything at t=0” events.

* Inference/training workloads we care about **do not need hard real-time behavior**:

  * For batch or offline jobs, an extra second to stagger GPUs is acceptable.

  * Real-time, sub-100ms latency workloads (e.g. live video) are **out of scope** for OG sites.

### **New decision: correlation is a controlled parameter**

For this calculator and system design, we will:

* Treat correlation as a **scheduler-controlled knob**, not a “given of the universe.”

* Explicitly assume:

  * **High-correlation events are disallowed** by design (e.g. “no more than X GPUs can change phase per second”).

  * Workloads admitted to the site are those that tolerate this behavior (batch/offline, not tight real-time).

### **Why it matters**

This turns “correlation risk” from a scary unknown into a **design constraint**:

* We don’t model “1000 GPUs all flip at once” as acceptable behavior.

* We instead model: “Scheduler guarantees no more than X kW of cluster step per second,” and check that against generator limits.

---

## **3\. Generator Dynamic Limits (What the Genset Actually Sees)**

### **What the issue is**

A natural-gas generator has finite dynamic capability:

* Can only accept a **max step** (e.g. 20–30% of rated kW) without ugly frequency dips.

* Has a finite **ramp rate** (kW/s).

* Has inertia (H) and governor droop (R) that set how much the frequency moves for a given step.

The GPU cluster plus miners must present a **net load profile** that stays inside that envelope.

### **What we’ve established from the chat**

1. **From the generator’s perspective, everything is just load.**  
    If we:

   * Turn off miners

   * Turn on GPUs  
      with coordinated timing, the generator only “sees” the **net difference**. Electrically, dropping 100 kW of miners and adding 100 kW of GPUs at the same instant is almost a wash.

2. **Small steps are free, big steps are not.**

   * A single 700 W GPU on a 1 MW gen is trivial.

   * Ten GPUs (7 kW) still trivial.

   * Hundreds of GPUs moving in lockstep becomes a material step (tens or hundreds of kW) and must be shaped.

3. **You never have exactly zero tolerance.**

   * Even if you’re “at 500 kW,” the system has a bit of slack; small deviations are absorbed by inertia and control loops.

   * You don’t need to turn off one miner *before* you can power one GPU. The generator can cover that first tiny step while controls adjust.

4. **We can bootstrap slowly.**

   * If you’re okay with time, you can bring GPUs up **one at a time** and let the generator catch up between each step – in theory never touching miners at all.

   * The real constraints are:

     * How quickly you *want* the cluster up.

     * The generator’s ramp spec in kW/s and max step %.

### **New decision: model the genset vs a shaped, not worst-case, ramp**

For modeling:

* We will not assume “all GPUs slam from 0 → full” as a valid operating mode.

* Instead, we:

  * Define a **max cluster step** and **max ramp** the scheduler is allowed to produce.

  * Compare those to the genset’s **max\_step\_pct** and plausible ramp capabilities.

* We also acknowledge that:

  * Miners can **help flatten net steps** by being shed as GPUs ramp (see next section).

  * But **sub-second transients** (faults, short spikes) still require traditional buffers (UPS/BESS).

### **Why it matters**

This squares the engineering circle:

* We respect gas engine limits (no fantasy transients).

* We rely on scheduler control plus miners/BESS, not on magical engine behavior.

---

## **4\. Control Strategies for Ramp Shaping**

### **4.1 Scheduler & Power-Aware Job Design**

**Key insight:** For the workloads we care about (batch inference, training, simulations), we *do* have the freedom to tweak when exactly jobs move between phases.

What we’ve established:

* Jobs typically have a **preload / model-load phase** (lower/moderate power) followed by a **high-power compute phase**.

* The naive behavior is “once preload is finished, immediately slam to 100% utilization.”

* We can change that:

  * Insert a **checkpoint after preload**.

  * Use that checkpoint to:

    * Ramp GPU power up gradually (in steps or ramped caps).

    * Shed miners or let the genset ramp.

  * Only then start the “heavy” phase.

### **New decision: power-aware phases are required**

For off-grid sites, we will:

* Restrict to workloads that **can tolerate**:

  * A pause between preload and full-power compute (hundreds of ms to a few seconds).

  * Staggered ramping of GPU groups.

* Treat “instant 30% → 100% jump with no opportunity to pause” as **out-of-scope** behavior for admitted jobs.

If a workload insists on hard real-time behavior (true live video, ultra-low-latency serving), it’s either:

* Not a fit for this architecture, or

* Requires separate, more traditional power infrastructure.

### **4.2 BESS / UPS: What’s Still Needed**

We also clarified an important nuance:

* GPUs themselves react on **millisecond timescales**.

* Generators and miner control are **slower** (hundreds of ms to seconds).

* So:

  * For **sub-second** events (faults, very sharp edges), you still want some form of **electronic buffer**:

    * UPS, flywheel, small BESS, or capacitor bank.

  * But it doesn’t have to be a massive multi-minute battery; it can be **just big enough to cover the first “kick”** for a small batch of GPUs.

We are *not* replacing UPS/BESS entirely; we’re using control plus miners to minimize the required size/energy.

### **4.3 Bitcoin Miners as Flexible Load**

We refined our view of miners:

**What miners can do:**

* Act as a **controllable, elastic load**:

  * Shed tens or hundreds of kW in response to planned GPU ramps.

  * Help keep the **generator’s net load more constant**, improving efficiency and reducing wear.

* Respond quickly enough (on human+software timescales, \~100ms+ to seconds) to be useful for multi-second ramp shaping.

**What miners cannot do:**

* Replace a **sub-second buffer** (they don’t act in milliseconds like a capacitor or UPS).

* Guarantee perfectly smooth real-time compensation for tiny transients.

* Magically make “all GPUs slam instantly to full power” safe; you still need scheduling discipline.

**New decision on miners:**

* In the modeling:

  * We treat miners as an **optional flexible load block** that:

    * Can be shed in kW chunks.

    * Helps shape **multi-second** ramps and steady-state loading.

  * We do **not** count miners as a replacement for:

    * UPS for ride-through.

    * Small BESS for the first, sharp edges of ramps.

* Miners are an *economic and multi-second control knob*, not a hard transient-protection device.

---

## **5\. Data Logistics (Starlink, Sneakernet, Fiber) – No Big Change, Just Context**

This part hasn’t changed much from the chat, but for completeness:

* We still model:

  * **Starlink**: always-on, limited TB/month, good for control plane \+ moderate data.

  * **Sneakernet**: drives in trucks, great for huge batched TB but high latency.

  * **Fiber**: expensive upfront, best for sustained large flow.

The chat didn’t really alter the structure, just reinforced an important meta-point:

* It’s the same story as power:

  * You want to **shape flows** and pick modes that match your workload.

  * Use Starlink for control \+ small deltas.

  * Use sneakernet for bulk if fiber is not yet justified.

  * Use fiber when volume and horizon make it worth the capex.

---

## **6\. Scope & Modeling Assumptions (Pulled Together)**

Based on this conversation, here are the **explicit assumptions** we’ll bake into the modeling toolkit:

1. **Workload Scope**

   * We focus on **batch / offline / training / simulation** workloads that:

     * Can tolerate seconds of ramp/pause between phases.

     * Do not require hard real-time response.

   * Truly latency-sensitive, live-stream inference is **out-of-scope** unless separately engineered.

2. **GPU Ramp Control**

   * Cluster-level power ramps are **deliberately shaped**:

     * Max GPUs-per-second starting a phase.

     * Option to pause after preload to ramp power.

   * We do **not** treat “instant all-GPU 0→100%” as normal behavior.

3. **Generator Modeling**

   * We compare **shaped ramps** (post-scheduler) to:

     * Rated power (kW).

     * Max step %.

     * Plausible ramp rate (kW/s).

     * Inertia/droop estimates.

   * We assume small, single-GPU steps are negligible vs MW-scale gensets.

4. **Flexible Load (Miners)**

   * Modeled as a **controllable load**:

     * Shed or add in kW blocks on 100ms–seconds timescales.

   * Used to:

     * Keep the generator near a “sweet spot” of loading.

     * Smooth multi-second ramps as GPUs move through phases.

5. **Buffers**

   * A **small UPS/BESS/capacitor bank** is still assumed for:

     * Sub-second events.

     * The very first little jumps in GPU power before slower controls react.

   * But we explicitly **minimize the required size** by:

     * Using scheduler control.

     * Using miners as multi-second balancing load.

