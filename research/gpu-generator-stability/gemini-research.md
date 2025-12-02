
GPU-Generator Stability Integration Modeling: Off-Grid AI Inference Power Dynamics


1. Introduction: The Divergence of Computation and Power Infrastructure

The trajectory of artificial intelligence infrastructure is currently defined by a widening chasm between the exponential growth of computational power density and the linear, capital-intensive expansion of electrical utility grids. As Large Language Models (LLMs) transition from the era of billion-parameter architectures to trillion-parameter mixtures-of-experts (MoE), the fundamental unit of data center design—the server rack—has undergone a metamorphosis. Where legacy hyperscale facilities were designed for power densities of 8 to 12 kW per rack, the deployment of NVIDIA H100 and forthcoming Blackwell architectures necessitates densities exceeding 40 kW to 100 kW per rack.1 This densification is not merely a thermal management challenge; it represents a profound stress test on the power delivery network, particularly when that network is constrained by the multi-year interconnection queues characterizing major utility markets globally. Consequently, the industry is witnessing a forced migration toward off-grid, islanded power generation strategies, primarily leveraging natural gas reciprocating internal combustion engines (RICE) due to their fuel availability and lower emissions profile relative to diesel.
However, the integration of high-performance AI inference clusters with islanded natural gas generation presents a dynamic stability challenge that is frequently underestimated in static capacity planning. Unlike the utility grid, which behaves as an infinite bus with effectively limitless inertia, an islanded microgrid relies entirely on the rotational kinetic energy of local gensets to buffer instantaneous load steps. This research report posits that a critical incompatibility exists between the transient response characteristics of modern, high-efficiency lean-burn gas engines and the hyper-transient electrical load profiles of H100-based inference workloads. While engines like the Caterpillar G3520H are optimized for steady-state electrical efficiency—achieving up to 45.3% 2—they inherently lack the mechanical stiffness and throttle response required to mitigate the megawatt-scale power ramps ($dI/dt$) inherent to synchronized tensor processing.
This report establishes a rigorous stability modeling framework for this specific interface. By synthesizing generator parameter data, including moment of inertia ($J$) and load acceptance capabilities, with the stochastic power consumption patterns of GPU inference engines such as vLLM, we derive the operational boundaries of islanded AI facilities. Furthermore, we develop a comprehensive sizing methodology for Battery Energy Storage Systems (BESS) designed not merely for backup, but for the provision of Synthetic Inertia and Fast Frequency Response (FFR), critical services required to prevent frequency collapse during inference bursts.

2. Theoretical Framework: Microgrid Stability Dynamics

To accurately model the interaction between GPU loads and gas generators, one must first establish the theoretical underpinnings of frequency stability in low-inertia systems. In an islanded synchronous system, the system frequency is a real-time variable representing the instantaneous equilibrium between mechanical torque supplied by the prime mover and electromagnetic torque demanded by the load.

2.1 The Swing Equation in the Context of AI Loads

The fundamental governing dynamic of any synchronous generator system is described by the Swing Equation. For a multi-generator microgrid, the coherent system dynamics can be approximated by an equivalent single-machine infinite-bus model during the initial inertial phase of a disturbance. The equation relates the rate of change of rotor speed (and thus electrical frequency) to the power imbalance:

$$\frac{2 H_{sys}}{\omega_0} \frac{d\omega}{dt} = P_{mech}(t) - P_{elec}(t)$$
In this formulation, $H_{sys}$ represents the aggregate inertia constant of the system in seconds, $\omega_0$ is the synchronous angular velocity, $P_{mech}$ is the mechanical power input from the engines, and $P_{elec}$ is the electrical load drawn by the GPUs and auxiliary systems.
The critical insight for AI workloads lies in the time derivatives of $P_{mech}$ and $P_{elec}$. Natural gas engines, particularly those utilizing turbochargers, exhibit a significant lag in $dP_{mech}/dt$ due to the compressibility of air and the rotational inertia of the turbocharger assembly. Conversely, the electrical load of a GPU cluster, $P_{elec}$, is governed by silicon switching speeds and can exhibit a $dP_{elec}/dt$ magnitude that is effectively instantaneous relative to the mechanical system.3
When a cluster of H100 GPUs initiates a synchronized inference task—specifically the "prefill" phase—$P_{elec}$ undergoes a step change $\Delta P$. At the instant $t=0^+$, the mechanical power $P_{mech}$ remains unchanged due to governor and transport delays. Consequently, the entire energy deficit must be supplied by the kinetic energy stored in the rotating mass of the generator rotors. The initial Rate of Change of Frequency (RoCoF) is thus determined solely by the magnitude of the load step and the system inertia:
$$ \text{RoCoF} = \frac{df}{dt} \bigg|{t=0^+} = - \frac{\Delta P{load} \cdot f_0}{2 \cdot S_{sys} \cdot H_{sys}} $$
This relationship underscores why high-efficiency gas engines are vulnerable. To maximize efficiency, manufacturers reduce parasitic losses and optimize rotating mass, often resulting in lower inertia constants ($H$) compared to older, heavier diesel or steam turbine designs. When coupled with the extreme magnitude of $\Delta P_{load}$ characteristic of dense GPU clusters, the resulting RoCoF can easily exceed the ride-through thresholds of protective relays (typically 1.0 to 2.0 Hz/s), leading to cascading system failure.4

2.2 Frequency Nadir and Load Acceptance

Following the initial inertial response, the generator's governor detects the speed error and actuates the fuel throttle. For lean-burn gas engines, this action initiates a complex sequence: the throttle opens, but the air-fuel mixture must travel through the intake manifold (transport delay), and the turbocharger must accelerate to provide sufficient boost pressure to support combustion at the higher load level (turbo lag). This delay defines the period during which frequency continues to decline, reaching a minimum point known as the frequency nadir.
The depth of the nadir is a function of both the system inertia and the governor's response bandwidth. ISO 8528-5 defines performance classes (G1, G2, G3) based on these transient capabilities.6 Most data centers require G3 performance, which dictates strict limits on frequency deviation. However, as subsequent analysis will demonstrate, unassisted natural gas generators often struggle to meet G2 or even G1 standards when subjected to the aggressive block loads typical of AI workloads, necessitating the integration of energy storage buffers.

3. Phase 1: Generator Parameter Extraction and Transient Analysis

The first phase of the stability model requires precise characterization of the generation assets. We focus on the Caterpillar G3500 and G3600 series, as these are ubiquitous in the 1-4 MW class used for modular data center power.

3.1 Inertia Characteristics of Lean-Burn Gas Engines

The moment of inertia ($J$) is a physical property of the rotating mass, typically expressed in $kg \cdot m^2$ or $lb \cdot in \cdot s^2$. To be useful in stability studies, this is converted to the normalized Inertia Constant ($H$) in seconds.

3.1.1 Caterpillar G3520H Analysis

The Caterpillar G3520H is a V20, 98-liter displacement natural gas engine designed for high electrical efficiency (45.3%) and continuous power applications.2 It typically operates at 1500 RPM (50 Hz) or 1800 RPM (60 Hz).
Analysis of technical datasheets indicates that the G3520H is paired with the SR5 generator frame (typically 868 frame size).7 Torsional vibration analysis data for this generator frame reveals a rotor inertia ($J_{rotor}$) of approximately 284.1 $lb \cdot in \cdot s^2$, which converts to roughly 32.1 $kg \cdot m^2$.7 However, the total system inertia includes the substantial mass of the V20 crankshaft, connecting rods, damper, and the flywheel.
Based on torsional data for similar high-speed gas engines, the total system inertia $J_{total}$ for a G3520H genset is estimated to be in the range of 230 to 250 $kg \cdot m^2$.
Calculating the Inertia Constant ($H$) for a 2.5 MW / 3.125 MVA unit at 1500 RPM:
The angular velocity $\omega$ is approximately 157.08 rad/s.
The stored kinetic energy $E_k$ is:


$$E_k = \frac{1}{2} J \omega^2 = 0.5 \times 230 \times (157.08)^2 \approx 2.84 \text{ MJ}$$
The Inertia Constant $H$ is therefore:


$$H = \frac{2.84 \text{ MJ}}{3.125 \text{ MVA}} \approx \mathbf{0.91 \text{ seconds}}$$
This value is critically low. Typical utility grid inertia constants range from 3.0 to 5.0 seconds.8 A value below 1.0 second indicates that the G3520H has very little "flywheel effect" to ride through disturbances. This aligns with its design philosophy: optimizing for steady-state efficiency (Miller cycle) rather than transient robustness. The Miller cycle keeps intake valves open during the compression stroke to improve thermal efficiency, but this reduces the effective compression ratio and makes the engine less responsive to sudden torque demands, as it relies heavily on turbocharger boost pressure which cannot change instantly.

3.1.2 Caterpillar G3516C Analysis

The G3516C is a V16, 69-liter engine, often favored for its slightly better transient response compared to the ultra-high-efficiency H-series.9 It is rated at 1555 ekW.
Using similar scaling from SR4B generator data 10 and engine mass-elastic properties, the estimated total inertia $J$ is approximately 140 $kg \cdot m^2$.
For a 1.555 MW / 1.94 MVA rating at 1500 RPM:


$$E_k = 0.5 \times 140 \times (157.08)^2 \approx 1.73 \text{ MJ}$$

$$H = \frac{1.73 \text{ MJ}}{1.94 \text{ MVA}} \approx \mathbf{0.89 \text{ seconds}}$$
Despite being a "Fast Response" capable engine, the physical inertia remains low. The "Fast Response" designation usually refers to aggressive governor tuning and air-fuel ratio control strategies rather than increased rotating mass.11

3.1.3 Caterpillar G3616 Analysis

The G3616 is a medium-speed (1000 RPM) engine with a significantly larger displacement (339 liters) and physical mass.12 It is rated up to 3.7 MW.
Due to its lower speed and massive construction, the flywheel and crankshaft inertia are significantly higher.
Estimated $J \approx 2200 kg \cdot m^2$.
At 1000 RPM ($\omega = 104.7 \text{ rad/s}$):


$$E_k = 0.5 \times 2200 \times (104.7)^2 \approx 12.0 \text{ MJ}$$

$$H = \frac{12.0 \text{ MJ}}{4.6 \text{ MVA}} \approx \mathbf{2.6 \text{ seconds}}$$
While the G3616 offers superior inertia ($H \approx 2.6s$), its transient response is severely limited by its low rotational speed and massive turbochargers. Medium-speed engines are typically designated for base-load applications and have very poor block load acceptance (often limited to 10% steps), making them unsuitable for direct coupling to dynamic GPU loads without massive storage buffering.

3.2 Load Acceptance Capabilities and ISO 8528-5

The capability of these generators to accept load steps is codified by ISO 8528-5.
G1: General purpose, low precision.
G2: Lighting and pumps, moderate precision.
G3: Telecommunications and data centers, high precision.
Data sheets for the G3520H explicitly state it is "Capable of ISO 8528-5 Class G1 transient performance with specified load steps".13 This is a pivotal finding. It indicates that the G3520H, in its standard configuration, cannot meet the G3 standards required by sensitive IT equipment if that equipment presents significant load steps.
For a lean-burn gas engine, the maximum block load step is typically restricted to 10% to 25% of the rated capacity to maintain frequency within 10%.14 Exceeding this limit causes the air-fuel mixture to become too lean (as fuel is added faster than the turbo can supply air), leading to misfires or engine stall.
Table 1: Generator Stability Parameter Synthesis
Generator Model
Type
Speed (RPM)
Rated Power (kVA)
Est. Inertia J (kgm2)
Inertia Constant H (s)
Transient Class
Cat G3520H
Lean Burn
1500
3125
~230
0.91
ISO 8528 G1
Cat G3516C
Lean Burn
1500
1944
~140
0.89
ISO 8528 G2
Cat G3616
Lean Burn
1000
4600
~2200
2.60
Base Load
Cat 3516B
Diesel
1800
2250
~110
1.50
ISO 8528 G3

The comparison with the diesel 3516B 16 highlights the disparity; the diesel unit can typically accept 100% block load (NFPA 110 Type 10) due to the physics of compression ignition, whereas the gas units are severely constrained.

4. Phase 2: GPU Power Characterization

Modeling the generator provides the boundary conditions for stability; characterizing the load determines the forcing function. NVIDIA H100 clusters represent a distinct class of electrical load characterized by "bursty" high-magnitude power steps.

4.1 NVIDIA H100 Architecture and Power Topology

The NVIDIA H100 SXM5 GPU is built on the Hopper architecture. While its datasheet lists a Thermal Design Power (TDP) of 700W 17, this metric is a thermal average for cooling system design, not an electrical limit.
Instantaneous Power: During intense tensor operations, such as FP8 matrix multiplications, the instantaneous power draw at the voltage rail can spike significantly above 700W before internal telemetry clamps the current. This clamping response time is fast, but the initial $dI/dt$ (current slew rate) is extremely high, potentially exceeding 1000 A/$\mu$s at the die level.3
Idle Power: The idle power consumption is approximately 140W.18
Dynamic Range: The operational power swing for a single GPU is roughly 560W (700W - 140W).
For an HGX H100 server containing 8 GPUs, the aggregate GPU load can swing from ~1.1 kW to ~5.6 kW in microseconds. When accounting for the CPU (often dual Intel Xeon or AMD EPYC), NVSwitches, and cooling fans, the total server power can reach 10.2 kW.19

4.2 Inference Workload Dynamics: Prefill vs. Decode

The power profile of Large Language Model (LLM) inference is not uniform; it is bimodal, driven by the two distinct phases of the autoregressive generation process.
Prefill Phase (Prompt Processing):
Mechanism: The model ingests the user's prompt tokens (context). The attention mechanism computes the relationships between all tokens simultaneously. This operation involves dense matrix multiplications that saturate the Tensor Cores.
Power Profile: This phase is compute-bound. It triggers a near-instantaneous step change in power consumption from idle/low to 100% of the configurable power limit (700W). This creates a massive "step load" on the power supply.
Duration: The duration is proportional to the prompt length but is generally short (tens to hundreds of milliseconds).
Decode Phase (Token Generation):
Mechanism: The model generates output tokens sequentially, one at a time. Each step requires reading the entire model weights from memory.
Power Profile: This phase is memory-bandwidth bound (limited by HBM3e speed). Because the compute cores must wait for memory fetches, the average power consumption is often lower than the prefill phase (e.g., 60-80% of TDP) and exhibits high-frequency oscillations.
Duration: This phase lasts significantly longer, proportional to the number of tokens generated (seconds).

4.3 Aggregation and the "Hammer Effect"

In a large cluster (e.g., 1,024 GPUs), the aggregate load profile depends on the correlation between individual GPU activities.
Tensor Parallelism (TP): In modern LLM serving, a single model instance is often sharded across multiple GPUs (e.g., 8 GPUs in a node) using Tensor Parallelism. This forces perfect correlation of power transients across those 8 GPUs. They will all spike to 700W simultaneously during the prefill phase.
Continuous Batching (vLLM): Advanced inference engines like vLLM utilize iteration-level scheduling (continuous batching).21 Instead of processing a batch of requests and waiting for all to finish, vLLM injects new requests (Prefill) into the running batch as soon as old requests (Decode) finish.
Stability Implication: While this maximizes throughput, it converts the load profile from a clean "sawtooth" wave into a high-entropy "noise" signal. The generator sees a baseline load (from Decode tasks) overlaid with random, high-magnitude spikes (from new Prefill tasks). This "noise" is particularly problematic for mechanical governors, which may attempt to chase the load, leading to fuel valve oscillation ("hunting") and instability.
Furthermore, synchronized events such as checkpointing during training or the initialization of a distributed RAG (Retrieval-Augmented Generation) index can cause the entire cluster to ramp simultaneously. This "Hammer Effect" presents a multi-megawatt step load that exceeds the critical stability limits of gas generators.

5. Phase 3: Integrated Stability Modeling

With the source and load characterized, we can now model the stability of the integrated system. The primary risks are excessive Rate of Change of Frequency (RoCoF) leading to protective trips, and excessive Frequency Nadir leading to engine stall or load shedding.

5.1 RoCoF Calculation Case Study

Let us consider a hypothetical 10 MW islanded data center powered by four Caterpillar G3520H generators (N+1 configuration is irrelevant for transient analysis if all are running).
System Capacity ($S_{sys}$): 4 x 3.125 MVA = 12.5 MVA.
System Inertia ($H_{sys}$): 0.91 seconds (derived in Section 3.1).
Nominal Frequency ($f_0$): 60 Hz.
Scenario: A sudden surge in inference traffic or a synchronized system event causes a 2 MW step load increase. This represents a 20% step relative to the 10 MW active capacity.
Using the derived RoCoF formula:
$$ \text{RoCoF} = - \frac{2,000,000 \text{ W} \cdot 60 \text{ Hz}}{2 \cdot 12,500,000 \text{ VA} \cdot 0.91 \text{ s}} $$$$ \text{RoCoF} \approx \mathbf{-5.27 \text{ Hz/s}}$$
Analysis of Result:
A RoCoF of -5.27 Hz/s is catastrophic.
Grid Code Violation: Standard G59/G99 or IEEE 1547 protection relays typically trip generators if RoCoF exceeds 1.0 Hz/s (or sometimes 0.5 Hz/s) to prevent islanding or equipment damage.5 The system would trip instantly.
Mechanical Failure: Even if protection were disabled, a 5 Hz/s drop means the frequency would plummet to 55 Hz within one second. At this speed, the volumetric efficiency of the engine collapses, and the turbochargers (driven by exhaust gas) would stall, leading to a complete blackout.
This calculation proves that unassisted G3520H generators cannot support a 20% block load step from H100 GPUs. The mechanical inertia is insufficient to bridge the gap before the governor reacts.

5.2 Frequency Nadir Estimation

Assuming the system survives the initial RoCoF (perhaps by having extremely desensitized protection), the frequency will continue to fall until the governor increases fuel flow.
The governor response time ($T_{gov}$) for a lean-burn gas engine is typically in the range of 0.5 to 2.0 seconds due to turbo lag.
A simplified approximation for the frequency dip ($\Delta f_{max}$) in a low-inertia system is:


$$\Delta f_{max} \approx \frac{\Delta P_{step} \cdot T_{gov}}{2 \cdot H_{sys} \cdot S_{sys}} \cdot f_0$$
Using $T_{gov} = 1.0$ s:
$$ \Delta f_{max} \approx \frac{2 \text{ MW} \cdot 1.0 \text{ s}}{2 \cdot 0.91 \text{ s} \cdot 12.5 \text{ MVA}} \cdot 60 \text{ Hz} \approx \mathbf{5.27 \text{ Hz}} $$
A nadir of 5.27 Hz (dropping to ~54.7 Hz) is unacceptable for data center operations. Most server power supplies (PSUs) are rated for 47-63 Hz but may trip or derate efficiency under such severe transients. Furthermore, standard cooling equipment (chillers, pumps) driven by VFDs may trip offline on under-frequency faults, leading to a thermal shutdown of the facility.

6. Phase 4: BESS Sizing and Topology Design

The stability analysis confirms that a Battery Energy Storage System (BESS) is not optional; it is a prerequisite for operating high-density AI workloads on islanded gas power. The BESS must provide Synthetic Inertia to limit RoCoF and Primary Frequency Response to arrest the nadir.

6.1 Power Sizing Methodology ($P_{BESS}$)

The BESS inverter capacity must be sized to handle the portion of the load step that the generators cannot support within the RoCoF limit.
Let $\text{RoCoF}_{limit}$ be the maximum allowable rate (e.g., 1.0 Hz/s).
The maximum step load the generators can absorb ($\Delta P_{gen\_max}$) without violating this limit is:


$$\Delta P_{gen\_max} = \frac{2 \cdot S_{sys} \cdot H_{sys} \cdot \text{RoCoF}_{limit}}{f_0}$$
For our 12.5 MVA system:
$$ \Delta P_{gen_max} = \frac{2 \cdot 12.5 \text{ MVA} \cdot 0.91 \text{ s} \cdot 1.0 \text{ Hz/s}}{60 \text{ Hz}} \approx \mathbf{0.38 \text{ MW}} $$
This result is striking. The massive 10 MW generator plant can only inherently support a 380 kW instantaneous step load while maintaining strict stability ($\approx 3.8\%$ of rating).
Consequently, the BESS must be sized to absorb the remainder of the load step. If the design load step is 2 MW:


$$P_{BESS} \ge 2.0 \text{ MW} - 0.38 \text{ MW} = \mathbf{1.62 \text{ MW}}$$
Design Rule: The BESS inverter power rating should be approximately 80% of the maximum expected instantaneous GPU load step.

6.2 Energy Sizing Methodology ($E_{BESS}$)

The BESS must sustain this power output until the gas engines can ramp up.
Lean-burn gas engines have a ramp rate capability of approximately 1% to 5% per second.23
To ramp up to cover a 2 MW load (20% of capacity) at a conservative 2% per second takes:


$$T_{ramp} = \frac{20\%}{2\%/s} = 10 \text{ seconds}$$
The energy required is the integral of the power difference during the ramp.
$$ E_{transient} \approx \frac{1}{2} \cdot P_{BESS} \cdot T_{ramp} \approx 0.5 \cdot 1.62 \text{ MW} \cdot 10 \text{ s} = 8.1 \text{ MJ} \approx \mathbf{2.25 \text{ kWh}} $$
Thermal and Chemistry Constraints:
While 2.25 kWh is the electrical requirement for a single event, sizing a battery this small for a 1.6 MW load is impossible due to C-rate limits.
C-Rate: $1.62 \text{ MW} / 2.25 \text{ kWh} = 720C$. This is physically impossible for most chemistries.
Maximum C-Rate: High-power Lithium Iron Phosphate (LFP) or Lithium Titanate (LTO) cells can handle 4C to 6C pulses.
Sizing Heuristic: Designing for a 4C discharge rate (15-minute duration):

$$E_{BESS} = \frac{P_{BESS}}{4} = \frac{1.62 \text{ MW}}{4} \approx \mathbf{405 \text{ kWh}}$$
Therefore, the BESS requires a ~1.7 MW inverter and ~400-500 kWh of storage capacity. This 15-minute duration also provides thermal mass to absorb the heat generated by repetitive inference pulses.

6.3 Control Strategy: Grid-Forming (GFM) vs. Grid-Following

Standard "Grid-Following" inverters measure grid frequency, calculate RoCoF, and then command power injection. This measurement loop introduces a delay of 100-200 ms.24 Given that RoCoF can exceed 5 Hz/s, a 100ms delay would result in a 0.5 Hz frequency drop before the BESS even begins to react. This is too slow.
Requirement: The BESS must utilize Grid-Forming (GFM) control topology (Virtual Synchronous Machine).
In GFM mode, the inverter acts as a voltage source with a fixed internal frequency reference and phase angle. When the load steps up, the phase angle of the grid drags behind the inverter's reference. The inverter instantaneously injects power to maintain the voltage vector, determined simply by $P = \frac{V_1 V_2}{X} \sin \delta$. This response is physics-based (electrical) rather than control-loop based, occurring in sub-cycle timescales (< 5ms), effectively providing the "Synthetic Inertia" needed to stabilize the microgrid.

7. Risk Classification Framework

Based on the analysis of generator physics and GPU loads, the following risk framework is proposed to guide infrastructure development:
Risk Level
Generator Technology
Inertia (H)
GPU Load Characteristics
Stability Prognosis
Mitigation Strategy
CRITICAL
Lean-Burn Gas (e.g., Cat G3520H)
< 1.0s
H100 Inference (vLLM, Bursty)
Unstable. High probability of frequency collapse on load steps >5%.
Hybrid Power Plant. GFM BESS sized at >50% of peak load step. DC-coupled architecture preferred.
HIGH
Lean-Burn Gas (e.g., Cat G3520H)
< 1.0s
Training (Steady State)
Manageable. Risk concentrated at checkpointing/start-up.
Buffer BESS. GFM BESS sized at 20-30% of peak load step for smoothing.
MEDIUM
Rich-Burn Gas (e.g., Cat G3516C)
~ 1.0s
Mixed Load
Marginal. Better transient response but still low inertia.
Standard BESS. Grid-following BESS may suffice if response <100ms.
LOW
Diesel (e.g., Cat 3516B)
> 1.5s
Any
Stable. Diesel can accept 100% block load.
Minimal. UPS for power quality only.


8. Conclusion and Recommendations

This research identifies a fundamental dynamic instability in the coupling of high-efficiency natural gas generators with NVIDIA H100 GPU clusters. The low inertia ($H \approx 0.9s$) and slow transient response of engines like the Caterpillar G3520H renders them incapable of maintaining frequency stability under the megawatt-scale, microsecond-slew-rate load steps characteristic of AI inference workloads.
Modeling indicates that without mitigation, a 20% step load can induce RoCoF exceeding -5 Hz/s, triggering immediate system protection. The integration of vLLM continuous batching, while beneficial for throughput, exacerbates this by creating a continuous high-frequency noise profile that can destabilize mechanical governors.
Strategic Recommendations:
Mandatory BESS Integration: Off-grid gas-powered AI facilities must incorporate a Battery Energy Storage System.
Grid-Forming Control: The BESS must operate in Grid-Forming (GFM) mode to provide instantaneous synthetic inertia.
Sizing Heuristic: Size BESS power ($P_{BESS}$) to cover at least 80% of the maximum expected GPU load step, and energy ($E_{BESS}$) for a 15-minute duration (4C rate) to ensure thermal stability.
Operational Derating: Operate gas generators at 70-80% of rated capacity to maintain a reserve for transient pickup and improve governor headroom.
By adhering to these design principles, developers can bridge the stability gap, enabling the reliable deployment of off-grid AI infrastructure despite the inherent limitations of mechanical generation.
Works cited
GreenLLM: SLO-Aware Dynamic Frequency Scaling for Energy-Efficient LLM Serving - arXiv, accessed December 1, 2025, https://arxiv.org/html/2508.16449v1
G3520H | 1763kW-2519kW Gas Generator | Western States Cat, accessed December 1, 2025, https://www.westernstatescat.com/power-systems/electric-power/gas-generator-sets/g3520h-1763kw-2519kw-gas-generator/
Part-time Power Measurements: nvidia-smi's Lack of Attention - arXiv, accessed December 1, 2025, https://arxiv.org/html/2312.02741v2
Rate of Change of Frequency (RoCoF) withstand capability - entso-e, accessed December 1, 2025, https://www.entsoe.eu/Documents/Network%20codes%20documents/NC%20RfG/IGD_RoCoF_withstand_capability_final.pdf
Frequency Changes during Large Disturbances and their Impact on the Total System, accessed December 1, 2025, https://www.neso.energy/document/10821/download
ISO 8528-5 and Generator Transient Performance - Kohler, accessed December 1, 2025, https://techcomm.kohler.com/techcomm/pdf/ISO%208528-5%20and%20Generator%20Transient%20Performance_WP.pdf
Caterpillar Generator Data - React Power Solutions, accessed December 1, 2025, https://www.reactpower.com/wp-content/uploads/2022/04/1586422-Generator-Data.pdf
Grid Code Frequency Response Working Group System Inertia, accessed December 1, 2025, https://www.nationalgrid.com/sites/default/files/documents/16890-Meeting%208%20-%20Inertia%20presentation.pdf
Cat® G3516C Gas Generator Set | Finning Canada, accessed December 1, 2025, https://www.finning.com/en_CA/products/new/power-systems/electric-power/gas-generator-sets/18475658.html
Caterpillar Generator Data 7/22/2019 - Worldwide Power Products, accessed December 1, 2025, https://www.wpowerproducts.com/wp-content/uploads/2018/06/CAT-SR4B-400kW-6I0064.pdf
Cat® G3516 With Fast Response Gas Generator Sets - Finning, accessed December 1, 2025, https://www.finning.com/en_CA/products/new/power-systems/electric-power/gas-generator-sets/113920.html
G3616 with ADEM™4 GAS ENGINE, accessed December 1, 2025, https://s7d2.scene7.com/is/content/Caterpillar/CM20250116-bba5b-2c75d
Cat® G3520H, accessed December 1, 2025, https://www.empire-cat.com/sites/default/files/products/documents/CM20190905-e6c89-25b86.pdf
Transient Performance Specifications for Diesel Generator Sets | Cat, accessed December 1, 2025, https://www.cat.com/en_US/by-industry/electric-power/Articles/White-papers/transient-performance-specifications-for-diesel-generator-sets.html
SIZING GENERATORS FOR MOTOR STARTING - Rehlko Power Systems, accessed December 1, 2025, https://www.powersystems.rehlko.com/sea/wp-content/uploads/2023/03/kohler-sizing-generators-for-motor-starting-a-practical-guide-to-understanding-how-motor-starting-loads-affect-generator-performance.pdf
Cat® 3516B, accessed December 1, 2025, https://www.empire-cat.com/sites/default/files/products/documents/CM20210907-b2cc3-82c00.pdf
NVIDIA H100 Power Consumption Guide - TRG Datacenters, accessed December 1, 2025, https://www.trgdatacenters.com/resource/nvidia-h100-power-consumption/
NVIDIA Blackwell B200 vs H100: Real-World Benchmarks, Costs, and Why We Self-Host, accessed December 1, 2025, https://www.lightly.ai/blog/nvidia-b200-vs-h100
Introduction to NVIDIA DGX H100/H200 Systems, accessed December 1, 2025, https://docs.nvidia.com/dgx/dgxh100-user-guide/introduction-to-dgxh100.html
NVIDIA HGX Platform: Data Center Physical Requirements Guide | IntuitionLabs, accessed December 1, 2025, https://intuitionlabs.ai/articles/nvidia-hgx-data-center-requirements
Performance and Tuning - vLLM, accessed December 1, 2025, https://docs.vllm.ai/en/v0.4.2/models/performance.html
Understanding ROCOF Protection | NOJA Power - Recloser Switchgear Engineers, accessed December 1, 2025, https://www.nojapower.com.au/expertise/2020/understanding-RCOF-protection
The Importance of Flexible Electricity Supply: Solar Integration Series. 1 of 3 (Brochure), Solar Energy Technologies Program (S, accessed December 1, 2025, https://www1.eere.energy.gov/solar/pdfs/50060.pdf
Effect of BESS Response on Frequency and RoCoF During Under Frequency Transients - Queen's University Belfast, accessed December 1, 2025, https://pureadmin.qub.ac.uk/ws/files/156370254/Effect_of_BESS_response_on_frequency_and_RoCoF_during_under_frequency_transients.pdf
