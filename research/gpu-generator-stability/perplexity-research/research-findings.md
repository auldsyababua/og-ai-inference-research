# GPU–Generator Stability Integration: Initial Research Findings

## 1. Scope and Status

This initial document summarizes early findings for:
- Phase 1: **Generator parameter extraction** (focus of this iteration)
- Phase 2: **GPU power characterization – high-level** (literature signals only)

It is intended as a working draft to validate methods, identify gaps, and tune assumptions before full model and sizing work.

---

## 2. Generator Parameters – Current Best Estimates

### 2.1 Methodology for Inertia Constant \(H\)

For each genset, the inertia constant \(H\) in seconds is approximated from rotor inertia \(J\) using the standard relationship for synchronous machines:
\[ H = \frac{J \omega^2}{2 S_\text{base}} \]

Where:
- \(J\): mass moment of inertia \(\text{kg·m}^2\)
- \(\omega\): mechanical angular speed (rad/s) at synchronous speed
- \(S_\text{base}\): MVA rating (approximately equal to MW at pf = 1.0)

Synchronous speed and pole count are inferred from rated frequency and rpm. This is consistent with utility references on inertia constants and per-unit formulation.[44][45][51][149]

### 2.2 Caterpillar CG170‑16 (Natural Gas)

**Known nameplate data**
- Continuous rating: **1560 ekW @ 1.0 pf** (50/60 Hz)[9][13][19][25][118]
- Speed: **1500 rpm** at 50 Hz (4‑pole machine)[9][13][19]
- Fuel: Natural gas / biogas / coal gas[9][19]
- Typical electrical efficiency: **≈43.3%**[9][12][19]
- Dry genset mass: **≈14,900 kg**[19]

**Inertia input (from prior internal table)**
- Mass moment of inertia: **\(J \approx 44.6\, \text{kg·m}^2\)** (likely rotor-only, lower bound)
- Confidence: **65%** (internal estimate, not found in public spec PDFs)

**Derived quantities (50 Hz operation)**
- Poles: **4** → pole pairs \(p = 2\)
- Electrical frequency: \(f = 50\,\text{Hz}\)
- Mechanical angular velocity: \(\omega = 2 \pi f / p \approx 157.1\,\text{rad/s}\)
- Base apparent power: \(S_\text{base} \approx 1.56\,\text{MVA}\)

**Estimated inertia constant**
- Using the equation above and \(J = 44.6\,\text{kg·m}^2\):
  - \(H \approx 0.35\,\text{s}\)
- **Confidence**: **50–65%**
  - Value is a *lower bound* (likely excludes engine/flywheel inertia, and may exclude full alternator inertia)
  - Typical synchronous generators in this size range have **H ≈ 2–7 s**,[44][45][149] so total system \(H_\text{eff}\) will need to be *assumed* significantly higher than 0.35 s for stability studies.

**Interim modeling recommendation**
- Treat 0.35 s as a **rotor-only lower bound** and use a **conservative engineering estimate of \(H_\text{eff} = 3.0–4.0 s\)** (65% confidence) for bulk-frequency stability work, pending better OEM data.

### 2.3 Caterpillar CG260‑16 (Natural Gas)

**Known nameplate data**
- Continuous rating: **4000–4300 ekW @ 1.0 pf** (50/60 Hz)[17][20][119][121][126]
- Speed: **1000 rpm @ 50 Hz** (6‑pole machine) or 900 rpm @ 50 Hz variant[17][20][121][126]
- Fuel: Natural gas, biogas, coal gas, associated gas, synthesis gas, H2 blend up to 25%[17][20][119]
- Maximum electrical efficiency: **≈44.1–44.6%**[17][20][119][124][127]
- Dry genset mass: **≈53,300 kg**[17][121][126]

**Inertia input (from prior internal table)**
- Mass moment of inertia: **\(J \approx 710\, \text{kg·m}^2\)** (likely rotor-only)
- Confidence: **65%** (internal, not yet corroborated by public CG260 rotor data)

**Derived quantities (assume 1000 rpm / 50 Hz)**
- Poles: **6** → pole pairs \(p = 3\)
- Electrical frequency: \(f = 50\,\text{Hz}\)
- Mechanical angular velocity: \(\omega = 2 \pi f / p \approx 104.7\,\text{rad/s}\)
- Base apparent power: \(S_\text{base} \approx 4.3\,\text{MVA}\)

**Estimated inertia constant**
- With \(J = 710\,\text{kg·m}^2\):
  - \(H \approx 0.91\,\text{s}\)
- **Confidence**: **50–65%**
  - As with CG170‑16, this is almost certainly **below** the true electromechanical \(H_\text{eff}\) observed in grid studies for machines of this size (where 2–7 s is typical).[44][45][149]

**Interim modeling recommendation**
- Use **\(H_\text{eff} = 3.5–5.0 s\)** for bulk RoCoF calculations (65% confidence), with sensitivity runs down to 2 s (worst-case) and up to 6 s (best-case).

### 2.4 Caterpillar G3516C (Natural Gas)

**Known nameplate data**
- Continuous rating: **≈1555–1660 ekW @ 0.8 pf** (50/60 Hz variants)[15][18][24][75][82]
- Speed: **1500 / 1800 rpm** (4‑pole machine at 1500 rpm)[15][18][24]
- Fuel: Natural gas / coal mine methane / biogas variants[18][24][75][82]
- Maximum electrical efficiency: **≈37.7–40%** for gas versions[18][24][75][82]

**Inertia input (internal estimate)**
- Mass moment of inertia: **\(J \approx 150\, \text{kg·m}^2\)** (rough estimate based on 3500‑series mechanical size)
- Confidence: **50%** (engineering guess; no OEM inertia data located yet)

**Derived quantities (50 Hz natural‑gas configuration)**
- Poles: **4** → pole pairs \(p = 2\)
- Electrical frequency: \(f = 50\,\text{Hz}\)
- Mechanical angular velocity: \(\omega \approx 157.1\,\text{rad/s}\)
- Base apparent power: \(S_\text{base} \approx 1.56\,\text{MVA}\)

**Estimated inertia constant**
- With \(J = 150\,\text{kg·m}^2\):
  - \(H \approx 1.19\,\text{s}\)
- **Confidence**: **50%**

**Interim modeling recommendation**
- For initial studies, assume **\(H_\text{eff} = 3.0–4.0 s\)** with sensitivity over 2–6 s, consistent with typical utility ranges for gas machines.[44][45][51][149]

### 2.5 Typical Ranges and Sanity Checks

Multiple grid-operator and academic references give characteristic inertia constant ranges:
\[ H_\text{typ} \approx 2\text{–}7\,\text{s} \]
for conventional synchronous generators.[44][45][51][149]

Given the very low \(H\) values produced when using rotor-only \(J\) on machine MVA base, it is highly probable that:
- Vendor \(J\) values used so far exclude significant **prime mover and flywheel inertia**.
- The true **electromechanical inertia seen by the grid** is closer to the 2–7 s range.

**Modeling stance**:
- Use literature ranges (2–7 s) as **primary priors** (75–85% confidence).[44][45][51][149]
- Treat calculated \(H\) from partial \(J\) as **lower‑bound checks** (50–65% confidence).
- Perform **sensitivity analyses** with \(H\) at 2, 3, 4, 5, and 7 s for each genset.

### 2.6 Governor Droop (\(R_\text{eff}\))

General engine–generator and governor literature, as well as Caterpillar and third‑party application guides, consistently state that **speed droop is normally in the 3–5% range** for generator governors used in parallel operation and load sharing.[76][132][136][138]

- Typical droop: **3–5%** (0.03–0.05 p.u. on frequency).
- This range is also consistent with broader generator/governor practice.[76][132][136]

Caterpillar application documents for ADEM A4‑governed gensets (e.g., C15, C32, C175‑16) specify ADEM A4 as an **electronic governor** suitable for both isochronous and droop operation, with external load‑sharing modules able to impose droop for paralleling.[100][147][148][150][152]

**Current working assumptions** (per model, off‑grid islanded operation):
- **Single‑genset island, no paralleling**: ADEM A4 or TEM EVO often run **isochronous** (effective \(R_\text{eff} \approx 0\)) for tight frequency regulation.[132][150][151]
- **Multi‑genset island**: droop usually set **3–5%** for stable load sharing.

For bulk frequency‑deviation estimates where pure isochronous data is not available, a **conservative default of 5% droop (\(R_\text{eff} = 0.05\))** is recommended (75% confidence), unless specific site settings are known.

### 2.7 RoCoF and Frequency Deviation Limits

There is no public evidence that Caterpillar publishes **per-model RoCoF ride-through limits**. Instead, limits are typically defined by **grid codes, interconnection standards, and protection relay settings**, with gensets tested to those requirements.[52][55][61][117][120][122][128]

Representative system-level RoCoF limits and ride-through requirements:
- Many grids historically used **0.125–0.5 Hz/s** as anti-islanding thresholds for small generators.[52][61][122]
- ENTSO‑E and related guidance often treat **1 Hz/s (over 500 ms)** as a practical upper bound for *safe* system RoCoF; emergency controls may not prevent blackouts if exceeded.[52][55][61][117][120]
- IEEE 1547‑2018 DER ride-through categories:
  - Category I: ride through for RoCoF \(\le 0.5\,\text{Hz/s}\).
  - Category II: \(\le 2.0\,\text{Hz/s}\).
  - Category III: \(\le 3.0\,\text{Hz/s}\).[120]

Caterpillar’s own microgrid and ECS control documentation confirms support for **RoCoF (81R) functions** in supervisory controls but does not disclose numeric limits in public datasheets; those are typically site-configurable.[123][128]

**Working design limits for this project (islanded off-grid gensets)**
- **Conservative “no-trip” RoCoF design target**: \(|\text{RoCoF}| \le 0.5\,\text{Hz/s}\) (high safety margin vs many codes).[52][55][61][117][120]
- **Absolute worst-case threshold for short events**: \(|\text{RoCoF}| \le 1.0\,\text{Hz/s}\) over 500 ms (aligned with modern RoCoF ride-through capability expectations).[52][55][61][117]

For **frequency deviation**, many technical data sheets and ISO 8528‑5 guidance indicate that well-tuned gas gensets can recover from **block loads of 20–25% of rating** while keeping frequency within about **±5% transient, ±1–2% steady-state**.[131][132][135]

**Working steady-state \(\Delta f\) limits for modeling**
- Nominal frequency: **50 or 60 Hz** (deployment dependent).
- **Tight limit** (GREEN zone target): \(|\Delta f| \le 0.5\,\text{Hz}\).
- **Upper bound for YELLOW**: \(|\Delta f| \le 1.0\,\text{Hz}\).
- **RED**: events that risk exceeding 1.0 Hz deviation or trigger underfrequency protections per site settings.

These values should be cross-checked against any site-specific relay settings in the final deployment.

---

## 3. GPU Power Characterization – Early External Signals

Detailed, phase-resolved power profiles for **H100 PCIe** under *inference* are not yet available in open literature at the required granularity (idle vs model-load vs burst vs sustained). However, several recent studies and industry reports give useful constraints:

### 3.1 H100 PCIe Nameplate and Card-Level Parameters

- NVIDIA H100 PCIe card:
  - TDP (Total board power): **350 W** default and maximum in standard PCIe 16-pin 450–600 W power mode.[172][174]
  - Supported power modes allow down-rating to 310 W in 300 W sense-pin mode.[172]
- Industry providers (e.g., Hyperstack) and cloud benchmarking sites confirm:
  - H100 PCIe **max power consumption up to 350 W** per GPU under heavy workloads.[174][175]

These align with the project’s existing assumptions for PCIe H100 TDP.

### 3.2 Measured Node-Level Power for H100 HGX Training

Recent measurement work on **8-GPU H100 HGX nodes** during *training* provides the clearest empirical data so far:[154][156][164]
- Node TDP rating: **≈10.2 kW** (8 × 700 W H100 SXM plus CPUs, memory, networking).[154][164][176]
- Measured maximum node draw under ResNet and Llama2‑13B training: **≈8.4 kW**, about **18–24% below TDP**.[154][156][164]
- Average operation in realistic training workloads: **≈76% of rated node TDP**.[155][156][164]

While this is training, not inference, it suggests a general pattern: **real workloads rarely sustain 100% of TDP** over long windows.

### 3.3 Measurement Caveats (nvidia‑smi / NVML)

Multiple detailed studies of NVIDIA’s internal power sensors show that **nvidia-smi under-samples power** on recent GPUs including A100 and H100:[95][161]
- On A100 and H100, only **25% of runtime is sampled for power**; the remaining 75% is unobserved, and reported power is an average over a 25 ms window every 100 ms.[95][161]
- This can significantly distort **fast transients** (exactly the regime of interest for RoCoF) and lead to under- or over-estimation of instantaneous power draw.[95][161]

**Implication for this project**
- Any future empirical measurements using nvidia-smi must:
  - Use **phase-shifting and micro-benchmarking techniques** recommended in these papers to recover more accurate short-term statistics.[95][161]
  - Not be treated as authoritative for **sub-100 ms transients** relevant to generator stability.

### 3.4 Inference Power and Variability – System-Level Signals

Several recent system-level and TCO/energy studies highlight key qualitative patterns for **LLM inference** on GPU clusters:[168][176][178][183]

- **Inference vs training utilization**:
  - Inference clusters tend to operate at **sub-TDP average power** with significant headroom; measured average GPU power is often **50–80% of TDP** depending on utilization and batching.[168][176]
- **Fast, large power swings**:
  - AI data-center studies note that large GPU clusters can cause **“power fluctuations of hundreds of megawatts within only seconds”** for grid-scale campuses.[178]
  - Within a single facility, per-rack power can range from **30 to 100+ kW**, with abrupt changes driven by workload scheduling.[176][178]
- **Bursty behavior for LLM inference**:
  - Workloads are **bursty and hard to predict**, especially in interactive inference (chatbots, on-demand APIs).[167][168][178]

These observations support the project’s assumption that worst-case step events can legitimately occur on 1–10 s windows and potentially faster.

### 3.5 Correlation of GPU Power in Clusters

There is not yet an H100-specific, open-literature study directly reporting a **correlation coefficient \(C\)** for GPU-to-GPU power draw under LLM inference. However, several recent works on AI cluster power behavior provide indirect evidence:[160][167][168][176][178][183]

- **Schedulers often co-schedule similar work on many GPUs** (e.g., multi-GPU tensor parallelism, data parallel replicas, batched inference jobs), which tends to **increase correlation** of power demand.
- At the same time, **queueing effects, cooling-aware scheduling, and oversubscription strategies** can desynchronize activity across nodes and racks.[163][167][168][183]
- System-level power-flexibility work (load shaping, demand response) assumes that *without specific mitigation*, large **correlated ramps** are realistic, motivating explicit control.

**Working correlation assumptions** (to be refined when empirical H100 inference data becomes available):
- **Worst-case design**: \(C = 1.0\) (perfect synchronization across the cluster) – used for all **RED-line** stability and BESS sizing.
- **Typical cluster operation** (well-mixed inference requests, no special coordination): **\(C \approx 0.5\)** with a plausible range **0.3–0.7** (50–65% confidence) based on qualitative scheduling analyses.[160][167][168][176][178][183]

These values will be revisited once direct GPU-level correlation measurements are obtained in the empirical validation phase.

### 3.6 Initial Power Step Scenarios for PCIe H100 Inference

Given the lack of fine-grained inference-only traces, conservative but structured scenarios are recommended for first-pass stability analysis:

1. **Single-cluster step (100 PCIe H100 GPUs)**
   - Nameplate per-GPU max: **350 W**.[172][174]
   - Idle power: industry anecdotal evidence for H100-class GPUs suggests **idle draw on the order of 100–150 W**, with some measurements for similar accelerators reporting **≈140 W idle** for next-gen devices.[181]
   - For modeling, treat **idle → full-load step** as **\(\Delta P_\text{gpu} \approx 250\,\text{W}\)** (100 → 350 W) with 50–65% confidence until direct H100 PCIe measurements are available.
   - Cluster step: \(\Delta P_\text{cluster} = 100 \times 0.25\,\text{kW} = 25\,\text{kW}\) for \(C = 1.0\).

2. **Sustained inference load level**
   - Training measurements on H100 HGX show **≈76% of node TDP** under heavy workload.[155][156][164]
   - Translating this to PCIe inference is non-trivial, but as a conservative initial estimate, assume **sustained inference at 70–80% of 350 W**, i.e. **245–280 W per GPU**.[155][156][164][168][176]

3. **Burst behavior and ramp times**
   - Node-level studies for AI hardware and SoCs stress that **peak current draw and power can vary on µs–ms scales**, especially across layer boundaries and changing batch sizes.[159]
   - For generator-level modeling (RoCoF over 100–500 ms windows), it is defensible to treat **model-load or workload-start events as near-step changes over 100–500 ms**, i.e. effectively instantaneous compared with the mechanical time constants of gas engines.

**Explicit data gaps (to be filled in later phases or via measurement)**
- Direct **H100 PCIe inference** power traces with phase separation:
  - Idle, model loading, KV-cache warm-up, steady decode, bursty prompt arrival.
- GPU-to-GPU power **correlation statistics** for single- and multi-node H100 inference clusters.
- Quantified **ramp rates (kW/s)** for realistic orchestration events (autoscaling, job admission bursts, failover, etc.).

---

## 4. Data Gaps and Assumptions (Current Snapshot)

### 4.1 Generator Side

**Missing / low-confidence parameters**
- Exact **rotor + engine + flywheel inertia** for all six target gensets (only partial \(J\) data inferred for CG170‑16 and CG260‑16; none found for G3520-family gas sets in public PDFs).[94][115][124][127][132][133][137]
- Model-specific default **governor droop settings** (3–5% range is well-supported generically, but not tied to each Caterpillar model).[76][132][136][147][148][150]
- Explicit OEM **RoCoF ride-through limits** in Hz/s for each machine (grid codes and DER standards provide system-level guidance, not per-genset numbers).[52][55][61][117][120][122][125][128]

**Current conservative assumptions**
- \(H_\text{eff}\) per genset initially drawn from **2–7 s** typical range; specific working bands (e.g., 3–4 s, 3.5–5 s) chosen per model for sensitivity studies.
- Governor droop **\(R_\text{eff} = 0.05\)** (5%) when droop-based load sharing is assumed, with an alternative **isochronous case (\(R_\text{eff} \approx 0\))** for single-unit microgrids.
- RoCoF design limits **0.5–1.0 Hz/s** based on grid-code practice and RoCoF protection studies.[52][55][61][117][120][122]

### 4.2 GPU / Cluster Side

**Missing / low-confidence parameters**
- Direct **H100 PCIe inference-only** power profiles by phase (idle vs model load vs inference vs batch changes), and **ramp rates**.
- Measured **correlation coefficients** of per-GPU power draw in realistic inference clusters.
- Time-resolved (**≤100 ms**) power traces for cluster-level orchestration events (e.g., many jobs admitted simultaneously, or failover).

**Current conservative assumptions**
- Per H100 PCIe GPU:
  - TDP / max board power: **350 W** (95% confidence).[172][174]
  - Idle: **100–150 W** (50–65% confidence; extrapolated from similar-class measurements and initial H100 anecdotal reports).[176][181]
  - Sustained inference: **245–280 W (70–80% of TDP)** (50–75% confidence, guided by training utilization evidence and TCO studies).[155][156][164][168][176]
- Correlation coefficient **\(C\)**:
  - Worst-case design: **1.0** (perfect correlation).
  - Typical: **0.5** with range **0.3–0.7** (50–65% confidence) subject to empirical refinement.[160][167][168][176][178][183]
- Event time window **\(\Delta t_\text{event}\)** for worst-case step events (e.g., large cluster enabling):
  - Treated as **≈0.1–1.0 s** versus generator mechanical dynamics (i.e., essentially a step from the genset’s perspective), consistent with SoC-level peak-power studies.[159][178]

---

## 5. Example Stability Calculations – Structure (No Final Numbers Yet)

Once final \(H_\text{eff}\), \(R_\text{eff}\), RoCoF limits and GPU power-step parameters are approved, the stability calculations will follow the framework already defined in the project spec:

1. **Cluster step power**:
\[ \Delta P_\text{cluster} = C \cdot N \cdot \Delta P_\text{gpu} \]

2. **RoCoF estimate** (per generator):
\[ \text{RoCoF} = - \frac{\Delta P_\text{cluster}}{2 H_\text{eff} S_\text{base}} \]

3. **Steady-state frequency deviation** (droop mode):
\[ \frac{\Delta f}{f_\text{nom}} \approx - R_\text{eff} \cdot \frac{\Delta P_\text{cluster}}{P_\text{rated}} \]

These will be run across:
- Each genset model (CG170‑16, CG260‑16, G3516C, G3520 variants, G3520H, G3616 A4).
- A grid of GPU counts per generator (e.g., 50, 100, 200, …).
- Correlation factors (e.g., \(C = 0.3, 0.5, 0.7, 1.0\)).
- Multiple \(H_\text{eff}\) scenarios (2, 3, 4, 5, 7 s).

The outputs will feed directly into the **GREEN/YELLOW/RED** risk classification in later phases once all required parameters are locked or bracketed.

---

## 6. Confidence Assessment (High-Level)

### 6.1 High Confidence (≥85–95%)

- **Inertia constant formulation** and its relationship to rotor inertia and MVA base.[44][45][51][149]
- **Typical \(H\) ranges** for conventional synchronous generators (2–7 s).[44][45][51][149]
- **Governor droop typical range 3–5%** and its role in load sharing and frequency droop.[76][132][136][138]
- **H100 PCIe TDP = 350 W** and SXM TDP = 700 W.[172][174]
- **Limitations of nvidia-smi power telemetry** on A100/H100 and need for careful measurement techniques.[95][161]

### 6.2 Medium Confidence (65–75%)

- Proposed **RoCoF design and absolute limits** (0.5–1.0 Hz/s) based on grid-code and DER ride-through guidance.[52][55][61][117][120][122][125][128]
- Use of **70–80% of TDP as typical sustained power** for heavy AI workloads on H100-class hardware.[155][156][164][168][176]
- Assumption that **cluster power events on 0.1–1 s horizons** can be approximated as step changes for genset-level modeling.[159][178]

### 6.3 Low–Medium Confidence (50–65%)

- Rotor inertia \(J\) figures used for CG170‑16, CG260‑16, G3516C, and derived \(H\) values (very few public OEM data).[94][115][124][127][132][133][137]
- Idle and sustained-inference power ranges for **H100 PCIe** (currently inferred from analogues and higher-level studies, not direct measurements).[176][181]
- Cluster-level **correlation coefficient \(C\)** for GPU power draw (no direct H100 inference measurements yet).[160][167][168][176][178][183]

---

## 7. Recommended Next Steps

1. **OEM / channel outreach for generator inertia and controls data**
   - Request **full mechanical inertia breakdowns** (engine, alternator, flywheel) and, if possible, **direct \(H\) in seconds** for CG170‑16, CG260‑16, G3516C, G3520 (standard & Fast Response), G3520H, and G3616 A4.
   - Request **factory default droop settings, governor modes, and recommended RoCoF limits** for islanded operation.

2. **Targeted literature / app-guide scan for 3500-series gas gensets**
   - Focus on transient performance and block-load acceptance (especially for **G3520 Fast Response** and **G3520H**), including any ISO 8528‑5 class declarations and example transient plots.[71][79][81][84][132]

3. **Design empirical measurement campaign for H100 PCIe inference**
   - Instrument a **multi-GPU H100 PCIe node** with:
     - High-rate **external power metering** at the rack / node level.
     - GPU-local telemetry via NVML plus **sampling-phase correction** per recent sensor studies.[95][161]
   - Collect time-series power data for:
     - Idle, model load, prompt bursts, steady decode, batch-size changes, and model switching.
   - Compute:
     - Per-GPU and node-level **ramp rates (kW/s)**.
     - Empirical **correlation coefficients C** across GPUs and across nodes for both training and inference patterns.

4. **Formalize parameter bands for Phase 3 modeling**
   - For each generator, define **primary, optimistic, and pessimistic \(H_\text{eff}\)** bands.
   - For GPUs, lock **\(\Delta P_\text{gpu}\)** and event timing bands pending measurement (e.g., best guess + conservative margins).

These steps will raise confidence on key parameters into the 75–95% range needed for final stability modeling and BESS sizing.
