# **Compute Refinery Modeling PRD (Working Draft)**

## **1\. Overview**

This document serves as an evolving specification for a calculator and modeling toolkit that captures the behavior, constraints, and economics of off-grid compute sites powered by variable or constrained energy sources. It tracks open questions, completed clarifications, definitions, and modeling requirements.

The immediate focus is GPU power/load dynamics and data logistics, but this PRD will expand as understanding deepens.

---

## **2\. What We Have Covered So Far**

### **2.1 GPU Batch Inference Power Phases**

A lifecycle model for a typical batch inference job, capturing per-GPU power behavior from idle to load to teardown. These phases include idling, launch, model loading, warmup, steady-state inference, and cleanup. Each phase has typical power deltas and timing behavior.

### **2.2 Linear Scaling of Power Ramps**

Power steps scale linearly with GPU count *if* all devices transition at the same moment. Practical risk and mitigation strategies change at larger scales even though the raw step physics are linear.

### **2.3 Nonlinear Operational Complexity at Scale**

Although physics scale cleanly, correlation risk grows with cluster size. This drives more complex scheduling, staggering, and load-shaping strategies.

---

## **3\. What We Still Need to Cover**

### **3.1 Quantifying Worst-Case kW/s Ramps at Cluster Scale**

* Define per-GPU power step sizes and timing for each phase (launch, model load, warmup, steady-state, teardown).

* Define correlation profiles (high, medium, low) and how they affect aggregate ramps.

* Express worst-case ramps in kW/s for different cluster sizes (e.g., 10, 100, 1000+ GPUs).

* Identify which phases dominate worst-case behavior.

### **3.2 Correlation Dynamics**

* Formalize “correlation” as a parameter: fraction of GPUs transitioning within a given time window.

* Model high-correlation (synchronous start/stop) vs low-correlation (staggered) scenarios.

* Define how correlation affects:

  * Peak power step (kW)

  * Ramp rate (kW/s)

  * Event frequency (how often big steps occur)

### **3.3 Mapping Ramps to Generator and Power System Constraints**

* Include generator nameplate size (kW or MW) as a core input.

* Include generator dynamic parameters (inertia, governor droop, response time, allowable step load, THD limits).

* Use simplified dynamic models to estimate:

  * Frequency deviation for a given step load.

  * Voltage sag/overshoot risk.

  * Maximum safe step size and ramp rate.

* Map worst-case cluster ramps against these limits to classify risk (safe, warning, critical).

### **3.4 Control Strategies for Ramp Shaping**

* Scheduling policies:

  * Max GPUs-per-second admitted to a new phase.

  * Job start/stop staggering windows.

* Power capping strategies:

  * Per-GPU and per-node power caps during warmup.

  * Cluster-wide ramp-rate limiter.

* Optional fast buffers:

  * UPS/capacitor banks as "shock absorbers" for sub-second events.

* Express these as tunable parameters the calculator can simulate.

### **3.5 Data Logistics Modeling**

* Starlink parameters:

  * Terminals, effective bandwidth, cost per month.

  * Usable TB/month (after overhead) and cost/TB.

* Sneakernet parameters:

  * Vehicle cost per mile, distance, frequency of trips.

  * Effective TB/trip and cost/TB.

* Fiber build parameters:

  * Cost per mile, distance to POP, amortization period.

  * Ongoing OpEx.

* Workload-side parameters:

  * TB/month of inbound data (per workload type).

  * TB/month of outbound artifacts (weights, embeddings, etc.).

* Calculator outputs:

  * Cost/TB by mode.

  * Break-even points (when fiber beats trucks, when more Starlink beats more trips).

### **3.6 Full Calculator Architecture**

* Inputs:

  * Cluster size (GPUs, nodes, racks).

  * Per-GPU power profiles by phase.

  * Correlation assumptions.

  * Generator size and dynamic limits.

  * Connectivity options (Starlink, sneakernet, fiber) and their cost structures.

  * Workload mix (training vs inference, batch sizes, duty cycle).

* Outputs:

  * Worst-case and typical ramp rates (kW/s) and step sizes (kW).

  * Risk classification vs generator capabilities.

  * Recommended ramp-shaping parameters.

  * Data logistics cost curves and mode recommendations.

## **4\. Index of Terms (Working Glossary)**

---

## **4.1 Generator Modeling Plan (Natural Gas Focus)**

This tool models any site (0.5–500 MW) as an **equivalent natural-gas-based microgrid** composed of one or more generator units. The calculator does not simulate full power-system transients; instead, it uses simplified, engineering-relevant parameters derived from generator spec sheets and operational manuals.

**Core goals:**

* Provide realistic, defensible estimates of generator response to GPU-cluster load ramps.

* Use parameters consistently published by major OEMs (Caterpillar, Cummins, MTU, Jenbacher, Wärtsilä).

* Maintain transparency: show equations, inputs, and numeric substitution for every result.

**Generator inputs:**

* `P_rated` — Rated active power (MW). Supports 0.5–500 MW total site rating.

* `H_eff` — Effective inertia constant (seconds). Defaults provided by size class; override allowed.

* `R_eff` — Governor droop (per unit, typically 0.03–0.05). Defaults \+ override.

* `max_step_pct` — Maximum safe load step as a fraction of rated power (e.g., 20–30%).

* `voltage_recovery_spec` — Optional: OEM-specified recovery time after step load.

* `fuel_quality_constraints` — Optional: if OEM lists Wobbe index, methane number, etc.

**Cluster-side inputs:**

* `N` — Number of GPUs.

* `ΔP_gpu` — Per-GPU power step (W) for the phase being modeled.

* `C` — Correlation factor (fraction of GPUs transitioning together).

* `Δt_event` — Time window of GPU transition (s).

**Derived values:**

* Total cluster step: `ΔP_cluster = C · N · ΔP_gpu` (kW/MW).

* Ramp rate: `Ramp_rate = ΔP_cluster / Δt_event` (kW/s).

* Step fraction: `Step_fraction = ΔP_cluster / P_rated`.

* Steady-state frequency deviation via droop:  
   `Δf / f_nom ≈ -R_eff · Step_fraction`.

* Initial rate of change of frequency (RoCoF):  
   `df/dt ≈ -ΔP_cluster / (2 · H_eff · S_base · f_nom)`.

**Risk classification:**

* **Green:** Step\_fraction \< safe\_limit; Δf and RoCoF within comfortable bounds.

* **Yellow:** Between safe\_limit and hard\_limit; caution advised; ramp shaping recommended.

* **Red:** Exceeds typical OEM limits; configuration likely unstable without buffering/staggering.

**Design philosophy:**

* Model is intentionally *simple but honest*—good for design exploration and scenario planning.

* Always show equations and substituted values for transparency.

* Excel export required for engineering review and modification.

\--- (Working Glossary)

**Correlation (Power Load Context)**  
 The degree to which many GPUs or nodes change state at the same time. High correlation means more devices transition simultaneously, producing large aggregate power steps.

**Phase**  
 A distinct stage in an inference job's execution, each with characteristic power behavior.

**Ramp-Up / Ramp-Down**  
 The rate at which power consumption increases or decreases across GPUs or an entire cluster.

**Cluster-Scale Step**  
 A change in total power when many GPUs transition states together.

**Synchronous Event**  
 A tightly aligned moment when many GPUs or workers begin or end a phase simultaneously.

**Ramp Shaping**  
 The deliberate control of how quickly GPUs move between power states to limit instantaneous load changes.

---

## **5\. Notes / Future Directions**

This PRD will evolve to incorporate equations, example scenarios, and more detailed architectural constraints as the modeling becomes sharper.

---

## **6\. Note for Follow-On Research Agent**

This document is an evolving Product Requirements Draft for a **Compute Refinery Modeling & Planning Calculator**. The primary goal is to model GPU-cluster power dynamics, generator/microgrid response, and data-logistics economics for off-grid compute sites powered by stranded natural gas.

The next agent should be aware that:

* We will build a **generator preset library** from real natural-gas generator technical data (starting with Caterpillar models).

* The calculator must output **transparent math** (equations \+ substituted values) and allow **Excel file export** for engineering and executive review.

* Generator behavior is simplified using an **equivalent-machine model** with parameters such as rated power, inertia constant, droop, and step-load limits.

* GPU cluster dynamics are modeled using per-phase power steps, correlation factors, and ramp-rate calculations.

* The tool will be used internally for scenario testing and early-stage design validation—**not** for final electrical engineering sign-off.

This agent should consult this PRD for context and extend it only by adding factual data, extracted generator parameters, and structured datasets as needed.  
 This PRD will evolve to incorporate equations, example scenarios, and more detailed architectural constraints as the modeling becomes sharper.

