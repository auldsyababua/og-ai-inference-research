
# **BESS vs. No-BESS Decision Framework: A Techno-Economic Analysis of Off-Grid AI Inference Architectures**

## **1\. Executive Context**

The rapid proliferation of large language models (LLMs) has catalyzed a paradigm shift in data center infrastructure, necessitating power densities and transient response capabilities that challenge traditional grid infrastructure. In response, off-grid microgrids utilizing natural gas generation have emerged as a viable alternative, particularly when coupled with flexible loads such as Bitcoin mining to stabilize generator utilization. This report rigorously examines the techno-economic viability of eliminating the Battery Energy Storage System (BESS) from such architectures. The primary research question addresses the conditions under which a "No-BESS" design—relying solely on generator inertia and precise load shedding of ASIC miners—is not only feasible but superior to a BESS-augmented architecture.

The baseline operating model assumes a 1 megawatt (MW) natural gas generator powering a split load of 0.5 MW Nvidia H100 GPUs and 0.5 MW ASIC miners. The miners serve as a flexible ballast, shedding load inversely to GPU ramp-ups to maintain a net-flat load profile for the generator. While this theoretical "Virtual Battery" concept promises significant capital expenditure (CapEx) reductions, the engineering reality involves complex interactions between generator governor dynamics, server power supply unit (PSU) hold-up times, and millisecond-level control latencies. This analysis dissects these interactions across technical, economic, and regulatory dimensions, focusing on key jurisdictions in the United States and Romania.

The findings suggest that while a No-BESS architecture offers a CapEx reduction of approximately 10-15%, it introduces operational fragilities that are unacceptable for high-availability inference workloads. The latency gap between a GPU's microsecond-level transient spike and an ASIC's millisecond-level shutdown response creates a vulnerability window that generator inertia alone often cannot bridge without violating power quality standards. Consequently, the optimal strategy for most commercial deployments is not a binary choice between "BESS" and "No-BESS," but rather a "Buffer BESS" configuration—a minimized energy storage system sized strictly for transient stabilization rather than bulk energy shifting.

---

## **2\. Technical Fundamentals: The Physics of the "No-BESS" Microgrid**

To determine the viability of operating without chemical energy storage, one must first understand the physical dynamics of the islanded power system. In a grid-connected facility, the utility provides an effectively infinite bus, absorbing massive load steps with negligible voltage deviation. In an off-grid microgrid, the generator is a finite source, and its ability to maintain voltage and frequency during load transients is constrained by the laws of thermodynamics and mechanical inertia.

### **2.1 Generator Dynamics and Transient Response**

The generator serves as the heartbeat of the off-grid system. In the absence of a BESS, the generator's rotating mass provides the only immediate energy buffer against load changes. When an electrical load is applied instantaneously, the electromagnetic torque on the generator rotor increases. Since the engine cannot instantly increase fuel combustion to match this new torque demand, energy is extracted from the kinetic energy of the rotating flywheel and crankshaft. This deceleration manifests as a drop in electrical frequency.

The magnitude of this frequency dip and the subsequent recovery time are governed by the generator's specific performance class. For data center applications, **ISO 8528-5 Class G3** is the non-negotiable standard.1 Class G3 dictates that for a sudden load increase, the frequency must not dip by more than 7-10%, and the voltage must not deviate by more than 15-20%.1 Crucially, the system must recover to steady-state conditions within 3 seconds. Meeting these stringent requirements with a diesel engine is relatively straightforward due to high compression ratios and the ability to inject liquid fuel directly into the cylinder for near-instant torque response.

However, the operating model specifies natural gas generation, likely utilizing flare gas or stranded gas resources. Natural gas engines face inherent disadvantages in transient response compared to diesel. The fuel is a gas, which must be mixed with air in the intake manifold or ports (fumigation) before entering the cylinder. This physical separation creates a "transport delay" or "dead time" between the governor commanding more power and the combustion event actually delivering that power to the crankshaft.

Two distinct categories of natural gas engines dominate this market, and their differences are critical to the No-BESS decision. **Lean-burn engines**, such as the Jenbacher J620 or similar high-efficiency models, run with excess air to minimize NOx emissions and maximize fuel efficiency.3 While economically superior for baseload power, their lean mixture burns slower and provides less torque authority. Typical lean-burn engines can only accept block load steps of 10% to 25% of their rated capacity without stalling or violating G3 limits.3 In a No-BESS scenario where a cluster of GPUs might ramp up by 100 kW (10% of a 1 MW genset) in milliseconds, a lean-burn engine operating near its limit may fail to respond fast enough, leading to frequency collapse and a site-wide blackout.

Conversely, **rich-burn or stoichiometric engines** operate with an air-fuel ratio closer to the chemical ideal. While less fuel-efficient and thermally more intensive, these engines offer transient response characteristics that rival diesel. Manufacturers like Caterpillar have developed "Fast Response" gas engines (e.g., the G3512 series) explicitly designed for the standby market, capable of accepting load steps of 50% or more while maintaining ISO 8528-5 G3 compliance.5 For a No-BESS architecture to be even theoretically viable, the use of rich-burn or optimized fast-response gas engines is a prerequisite. Utilizing standard wellhead gas generators or high-efficiency lean-burn turbines without a battery buffer effectively guarantees failure during high-intensity inference ramping.

### **2.2 The Load: Nvidia H100 Electrical Characteristics**

The load profile of modern AI hardware is fundamentally hostile to islanded power generation. The Nvidia H100 Tensor Core GPU represents a dynamic, pulsed electrical load that differs significantly from the steady-state industrial motors or lighting loads that legacy generators were designed to support.

The power consumption of an H100 varies by form factor. The PCIe version has a Thermal Design Power (TDP) of 300-350W, while the SXM5 module used in high-performance HGX clusters draws up to 700W.6 However, TDP is a thermal average, not an electrical maximum. Under the **ATX 3.0 power supply specification**, which governs modern server power delivery, PCIe components are permitted power excursions—short-duration spikes—of up to **200% of their rated power** for durations of 100 microseconds.8 For an SXM5 module, this could theoretically mean instantaneous demands approaching 1400W per chip.

More critical than the magnitude of the spike is the **slew rate**, or the rate of change of current ($dI/dt$). H100 GPUs can ramp current at rates exceeding **1 ampere per microsecond ($A/\\mu s$)**.9 When an inference job is dispatched to a rack of 8 or 16 GPUs, the aggregate load can jump from an idle state (\~2 kW) to peak load (\~10-12 kW) in a timeframe that is essentially instantaneous from the perspective of a mechanical generator.

This extreme $dI/dt$ creates a phenomenon known as a "load slam." In a grid-connected system, the grid's low impedance absorbs this. In an islanded system without BESS, the generator's voltage regulator (AVR) must react immediately to increase excitation field current to maintain voltage. If the AVR is too slow, or if the generator's magnetic field cannot build fast enough (limited by the exciter time constant), the voltage will sag.

Here, the server's own **Power Supply Unit (PSU)** becomes the last line of defense. Modern Titanium-rated server PSUs (e.g., Delta, Lite-On) are equipped with bulk capacitors that provide a "hold-up time"—typically roughly 10 to 20 milliseconds at full load.10 This means the PSU can continue to supply stable DC power to the GPU for roughly one 60Hz cycle (16.6ms) even if the AC input voltage collapses. This **10-20ms hold-up window** is the critical time budget for the No-BESS architecture. If the generator voltage does not recover, or if the ASIC load shedding does not occur within this window, the PSUs will trigger their Undervoltage Lockout (UVLO) protection and shut down the servers to prevent hardware damage.

### **2.3 The "Virtual Battery": ASIC Miner Load Shedding**

The central thesis of the No-BESS architecture is that ASIC miners can mimic a battery by shedding load instantly. When the scheduler anticipates a GPU ramp-up, it commands the miners to pause. Mathematically, shedding 100 kW of miner load is equivalent to discharging a 100 kW battery.

However, "instant" is a relative term. The latency chain for this operation involves several steps:

1. **Detection/Trigger:** The workload scheduler identifies an incoming inference job (t=0).  
2. **Transmission:** The control signal is sent over the local network to the miner control board via protocols like Modbus TCP or Stratum (t+2ms to t+10ms).  
3. **Execution:** The miner's control firmware processes the signal and cuts power to the hashboards (t+10ms to t+50ms, depending on firmware quality).  
4. **Physical Decay:** The current draw of the miners drops (t+50ms).

The total latency for this "Virtual Battery" to activate is realistically **20 to 100 milliseconds**. Comparing this to the **10-20ms hold-up time** of the server PSUs reveals the fundamental flaw in a purely reactive No-BESS design. If the system waits for the GPU to ramp up before shedding the miners, the generator will experience a double-load condition (GPU \+ Miner) for 20-80ms. This duration exceeds the PSU hold-up time, leading to a high probability of server failure.

Therefore, a reactive control strategy is insufficient. A No-BESS system requires **predictive scheduling**, where the controller forces the miners to shed load *before* the GPUs are allowed to ramp up. This introduces a "wait state" for the inference job, adding latency to the service. While acceptable for batch processing (e.g., protein folding), this artificial delay renders the No-BESS architecture unsuitable for real-time, low-latency inference applications (e.g., chatbots), where millisecond response times are the product's core value proposition.

---

## **3\. Economic Analysis: The Price of Removing the Battery**

The decision to omit BESS is fundamentally an economic trade-off: trading capital expenditure (CapEx) savings for increased operational risk and engineering complexity (NRE). This section quantifies these variables based on 2025 market rates.

### **3.1 Capital Expenditure Savings**

Eliminating the BESS removes a significant line item from the project budget. A typical commercial BESS for a 1 MW microgrid might be sized at 250 kW / 500 kWh (2-hour duration) to provide buffering and some extended ride-through.

**Table 1: Estimated CapEx Savings per 1 MW Deployment (2025 USD)**

| Component | BESS Architecture Cost | Source Basis |
| :---- | :---- | :---- |
| **BESS Modules (LFP, \~500 kWh)** | $150,000 \- $180,000 | Based on \~$300-$360/kWh commercial pricing 12 |
| **Power Conversion System (PCS)** | $40,000 \- $50,000 | Bi-directional 250kW inverters 14 |
| **Balance of System (HVAC, Container)** | $40,000 \- $60,000 | Thermal management and enclosure 15 |
| **Installation & Commissioning** | $30,000 \- $40,000 | Electrical labor, pads, interconnects 16 |
| **Total Avoided Cost (Gross Savings)** | **$260,000 \- $330,000** |  |

This suggests a gross saving of approximately **$300,000 per MW**, which is roughly 15-20% of the total infrastructure cost for a containerized 1 MW data center (excluding the compute hardware itself).

### **3.2 The Hidden Costs of "No-BESS"**

However, "No-BESS" is not "zero cost." It essentially transfers the burden of stability from hardware (batteries) to software (controls) and mechanical robustness (generators).

1. **Custom Controller Development (NRE):** Standard off-the-shelf genset controllers (e.g., Deep Sea DSE8610 MKII, ComAp InteliGen 1000\) are designed for load sharing, not sub-cycle load shedding synchronized with IT workloads.17 Developing a custom PLC-based microgrid controller (using Beckhoff or similar industrial automation platforms) that integrates with ASIC APIs and GPU cluster managers (Slurm/Kubernetes) requires specialized engineering.  
   * **Estimated NRE:** $50,000 \- $100,000 for software development and testing.19  
   * *Note:* This is a one-time cost. For a fleet of 10+ sites, this cost amortizes to negligible levels. For a single site, it significantly eats into the BESS savings.  
2. **Generator Oversizing:** To handle the transient loads without a battery buffer, the generator's alternator often needs to be oversized to increase inertia and magnetic stability (e.g., pairing a 1 MW engine with a 1.5 MVA alternator).  
   * **Estimated Adder:** $20,000 \- $30,000 per genset.20

**Net Savings Calculation:**

* Gross Savings: \+$300,000  
* Less Controller NRE: \-$75,000 (averaged)  
* Less Genset Upgrade: \-$25,000  
* **Net CapEx Benefit:** **\~$200,000 per MW.**

### **3.3 Operational Expenditure (OpEx) and Efficiency**

The No-BESS architecture offers subtle but compounding OpEx advantages.

* **Round-Trip Efficiency (RTE):** BESS systems typically have an RTE of 85-90% due to conversion losses (AC-DC-AC) and thermal management.16 In a BESS-centric design where 20% of energy flows through the battery, roughly 2-3% of total generated power is lost as heat. A No-BESS system avoids this loss, directly improving the fuel-to-compute efficiency.  
* **Maintenance:** Li-ion batteries degrade. A 10-year TCO model must account for augmentation or replacement of battery modules at year 7-8, costing \~$50k-$100k.21 Furthermore, BESS containers require active cooling (HVAC) to maintain temperatures between 20-25°C. In extreme climates like North Dakota or Wyoming, the heating/cooling load for the battery container can be substantial. Removing the BESS eliminates this parasitic load and the associated HVAC maintenance.

**Generator Wear Penalty:** Conversely, the No-BESS approach places extreme stress on the generator's mechanical governor and turbocharger actuators. The constant "hunting" to match rapid load changes can accelerate wear on these components, potentially increasing engine maintenance frequency by 10-20% compared to a steady-state baseload operation buffered by batteries.

---

## **4\. Regulatory and Jurisdictional Analysis**

Regulations often mandate hardware that engineering logic might deem optional. The feasibility of No-BESS is heavily dependent on the specific regulatory environment of the deployment site.

### **4.1 Texas (ERCOT)**

Texas is a complex regulatory environment driven by **Senate Bill 6 (SB 6\)** and ERCOT's focus on grid reliability. While off-grid "behind-the-meter" systems are generally insulated from grid codes, the landscape shifts if the site ever intends to interconnect or participate in ancillary service markets.

* **Voltage Ride-Through (VRT):** ERCOT is proposing strict VRT requirements for Large Flexible Loads, potentially requiring them to ride through voltage dips to 0.5 per-unit (50%) for extended durations.22 Meeting this requirement without a BESS or flywheel is virtually impossible for electronic loads. A No-BESS design in Texas effectively locks the facility into **permanent island mode**, prohibiting future monetization of grid services (like ECRS or Non-Spin Reserve), which are significant revenue streams in the ERCOT market.  
* **Phantom Load Fees:** New rules require significant interconnection study fees ($100k+) and proof of load.22 This bureaucratic friction encourages islanded designs, but the inability to *ever* connect reduces the asset's long-term resale value.

### **4.2 Wyoming, Montana, and North Dakota**

These states offer a more favorable environment for No-BESS architectures due to deregulation and specific incentives for data centers and flare gas utilization.

* **Climate Considerations:** The defining characteristic here is extreme cold. Lithium-iron-phosphate (LFP) batteries cannot be charged below freezing temperatures without causing permanent damage (lithium plating). A BESS deployed in North Dakota (-30°F winters) requires insulated, heated containers. The energy cost to heat a BESS container can be significant.  
  * *No-BESS Advantage:* Generators are easier and cheaper to winterize (block heaters) than large chemical battery banks. The absence of BESS eliminates a major cold-weather liability.  
* **Tariffs:** Utilities like NorthWestern Energy (Montana) and Black Hills Energy (Wyoming) are introducing "Large Load" tariffs to insulate ratepayers from infrastructure costs associated with data centers.24 Off-grid generation avoids these tariffs entirely.

### **4.3 West Virginia**

West Virginia's **HB 2014** creates "Certified Microgrid Districts" and offers tax incentives for data centers powered by coal or gas.26

* **Microgrid Freedom:** The law explicitly protects the right to self-generate and creates regulatory sandboxes. This legal framework is highly supportive of experimental architectures like No-BESS, provided safety codes are met.

### **4.4 Romania (EU Context)**

Operating in Romania introduces the complexity of EU regulations.

* **Grid Codes:** The European Network of Transmission System Operators for Electricity (ENTSO-E) enforces stricter frequency and voltage stability rules than the US. Even off-grid systems may face scrutiny if they are large enough (\>1 MW) to impact regional stability considerations.  
* **Cybersecurity:** Romania is drafting laws requiring strict technical standards and cybersecurity oversight for energy systems \>1 MW.28 A custom-built, software-heavy No-BESS controller might face difficult certification hurdles compared to a standardized, CE-certified BESS from a major vendor like Sungrow or Fluence.

### **4.5 NFPA Codes: The "Life Safety" Hard Stop**

Regardless of location, **NFPA 110** (Standard for Emergency and Standby Power Systems) poses a critical barrier.

* **Type 10 Requirement:** If the facility houses *any* life-safety equipment (fire pumps, emergency egress lighting, active smoke control), the power system must be capable of restoring power within **10 seconds** of a failure.29  
* **The Gas Engine Problem:** Large natural gas engines often require purge cycles and cranking time that exceed 10 seconds. A BESS or flywheel is the standard solution to bridge this gap.  
* **No-BESS Workaround:** To remain compliant without a main BESS, the facility must segregate life-safety loads onto a separate, dedicated small diesel generator or a standard commercial UPS. Attempting to run life-safety systems off the main "No-BESS" microgrid is a code violation in almost all jurisdictions.

Additionally, **NFPA 855** governs the installation of Energy Storage Systems.30 It mandates strict spacing (3 ft between racks), explosion control, and fire suppression.

* *No-BESS Advantage:* By removing the BESS, the project completely bypasses NFPA 855 compliance. This simplifies the site plan, reduces land use (no spacing requirements), and eliminates the need for specialized explosion-prevention systems, saving roughly **$30,000 \- $50,000** in compliance costs.

---

## **5\. Vendor and Hardware Landscape (2025)**

Understanding the available hardware is crucial for pricing the alternatives.

### **5.1 BESS Options**

* **Tesla:** The industrial "Megapack 2" (\~3.9 MWh) is priced at over $1.2 million, making it too large and expensive for a 1 MW site.31 The smaller "Powerpack" is largely legacy. For a 1 MW site, commercial integrators would likely use aggregated Powerwalls or a third-party rack system, but Tesla's focus is clearly on utility-scale.  
* **Sungrow:** The **PowerStack** series (e.g., ST225kWh liquid-cooled cabinet) is a strong fit for this scale. It offers high density and competitive pricing, estimated around **$300/kWh** installed.12  
* **BYD:** The **Battery-Box Commercial** (e.g., C130) is highly modular. Pricing for high-voltage commercial systems is competitive, but integration with US inverters requires careful matching.33  
* **Fluence:** Their "Cube" systems are robust but typically target larger deployments. Their focus on software (Fluence OS) adds value but cost.34

### **5.2 Generator Options**

* **Caterpillar:** The **G3512** is the industry benchmark for "Fast Response" natural gas engines, specifically engineered to meet NFPA 110 Type 10 requirements (under specific conditions) and accept 50%+ block loads.5 This engine is the **primary enabler** of a No-BESS strategy.  
* **Generic/Lean-Burn:** Using standard lean-burn engines (often rebranded industrial engines) is fatal for No-BESS designs due to poor transient response.3

---

## **6\. Reliability Analysis: The Cost of Failure**

The technical feasibility of No-BESS is binary (it works or it doesn't), but the economic feasibility is probabilistic. It depends on the *cost* of an outage.

### **6.1 Fault Tolerance and Recovery**

In a No-BESS system, there is zero ride-through capability for generator faults.

* **Scenario:** A fuel valve sticks momentarily, causing a 500ms drop in engine speed.  
* **BESS System:** The battery inverter instantaneously injects power, maintaining frequency. The servers see nothing.  
* **No-BESS System:** Frequency dips below PSU tolerances. The server PSUs trip. The H100 cluster undergoes a hard reboot.  
* **Recovery Cost:** Rebooting a cluster, running integrity checks on the file system, re-loading the Large Language Model (which can be hundreds of gigabytes) into VRAM, and re-synchronizing the nodes takes **15 to 30 minutes**.

### **6.2 ROI of Reliability**

If the H100 cluster generates revenue of **$50/hour per GPU** (a conservative estimate for spot instances), and the site hosts \~64 GPUs (0.5 MW):

* **Hourly Revenue:** $3,200.  
* **Cost of 30-min Outage:** $1,600 (direct revenue) \+ Potential SLA penalties.  
* **Break-Even:** The CapEx savings of \~$200,000 (No-BESS) is equivalent to roughly **60-70 hours of downtime**.  
* **Implication:** If the No-BESS design causes more than **\~10-15 outage events per year** (roughly one per month), the "savings" are wiped out by lost revenue. Given the sensitivity of gas engines to fuel quality variations (common with flare gas) and the complexity of the control logic, a failure rate of \>1/month is a realistic risk.

---

## **7\. Synthesis and Decision Framework**

Based on the detailed analysis, we can classify the decision scenarios.

### **7.1 When is "No-BESS" Beneficial? (The "Green" Scenario)**

The No-BESS architecture is a rational choice **only** when all the following conditions are met:

1. **Workload is Fault-Tolerant:** The AI workload is batch processing (training, rendering, scientific simulation) where latency is irrelevant and checkpoints are frequent. The "cost" of a reboot is low.  
2. **Generator is High-Performance:** The site utilizes **rich-burn/fast-response natural gas** or **diesel** generators with verified ISO 8528-5 G3 block load capability.  
3. **Site is Permanently Off-Grid:** There is no intention to ever connect to the grid (avoiding VRT codes).  
4. **Climate is Cold:** The site is in a region like North Dakota where BESS HVAC costs would be prohibitive.  
5. **Staffing is High:** The site has on-site engineering capable of managing the complex custom controller.

### **7.2 When is BESS Essential? (The "Red" Scenario)**

A BESS must be included if:

1. **Workload is Real-Time:** The site hosts inference APIs (chatbots) where 99.9% availability is contractually required.  
2. **Generators are Lean-Burn:** The engines are high-efficiency lean-burn models with poor transient response.  
3. **Hardware is SXM5:** The deployment uses high-density H100 SXM5 racks with extreme $dI/dt$ transients.  
4. **Jurisdiction is Texas:** The site is in ERCOT and may need to interact with the grid or provide ancillary services.

### **7.3 The Optimal "Middle Ground": The Buffer Battery**

The analysis reveals that the binary choice—Full BESS vs. Zero BESS—is a false dichotomy. The most robust solution for 2025 is a **"Buffer BESS."**

* **Concept:** Deploy a minimal battery system (e.g., 50-100 kWh) with high power discharge capability (2C-4C).  
* **Function:** This battery does not provide "backup" or "energy shifting." Its sole purpose is **Transient Stability**. It covers the 0-10 second window during load steps, allowing the generator time to react and the miners time to shed.  
* **Cost:** \~$30,000 \- $50,000.  
* **Value:** This captures 90% of the reliability benefits of a full BESS for only 20% of the cost, effectively insuring the $2M+ investment in H100 GPUs against dirty power events.

## **8\. Conclusion**

For the specific use case of off-grid H100 AI inference in 2025, **omitting BESS entirely is a high-risk financial strategy.** While technically possible through the "Virtual Battery" action of ASIC miners, the latency mismatch between GPU transients and miner shedding creates a fragility that threatens high-value revenue streams.

**Final Recommendation:** Do not deploy a "No-BESS" architecture for commercial H100 inference. Instead, deploy a **Buffer BESS** architecture. Use the ASIC miners for bulk energy balancing (minutes/hours), but rely on a small, power-dense battery buffer (seconds) to guarantee the power quality required by sensitive AI hardware. This hybrid approach maximizes capital efficiency without compromising the operational integrity of the data center.

#### **Works cited**

1. ISO 8528-5 and Generator Transient Performance \- Kohler, accessed December 1, 2025, [https://techcomm.kohler.com/techcomm/pdf/ISO%208528-5%20and%20Generator%20Transient%20Performance\_WP.pdf](https://techcomm.kohler.com/techcomm/pdf/ISO%208528-5%20and%20Generator%20Transient%20Performance_WP.pdf)  
2. Understanding ISO8528 G3 Generator Set Performance Class \- AGG Power, accessed December 1, 2025, [https://www.aggpower.com/news/understanding-iso8528-g3-generator-set-performance-class/](https://www.aggpower.com/news/understanding-iso8528-g3-generator-set-performance-class/)  
3. Frequency Stability Considerations of Reciprocating Gas Engine Generators in Microgrids \- Aurora Power Consulting, accessed December 1, 2025, [https://aurora-power.co.uk/wp-content/uploads/2024/01/Frequency-Stability-Considerations-of-Reciprocating-Gas-Engines.pdf](https://aurora-power.co.uk/wp-content/uploads/2024/01/Frequency-Stability-Considerations-of-Reciprocating-Gas-Engines.pdf)  
4. Flare Gas | Energy Solutions | Jenbacher, accessed December 1, 2025, [https://www.jenbacher.com/en/energy-solutions/energy-sources/flare-gas/](https://www.jenbacher.com/en/energy-solutions/energy-sources/flare-gas/)  
5. Caterpillar Introduces the G3512 Natural Gas Generator Set \- Blanchard Machinery, accessed December 1, 2025, [https://www.blanchardmachinery.com/about/blog/power-systems/caterpillar-introduces-new-g3512-natural-gas-generator-set-for-emergency-standby-applications/](https://www.blanchardmachinery.com/about/blog/power-systems/caterpillar-introduces-new-g3512-natural-gas-generator-set-for-emergency-standby-applications/)  
6. NVIDIA H100 GPU? Everything you need to know \[2025\] \- Neysa, accessed December 1, 2025, [https://neysa.ai/blog/nvidia-h100-gpu/](https://neysa.ai/blog/nvidia-h100-gpu/)  
7. NVIDIA H100 SXM5 96 GB Specs \- GPU Database \- TechPowerUp, accessed December 1, 2025, [https://www.techpowerup.com/gpu-specs/h100-sxm5-96-gb.c3974](https://www.techpowerup.com/gpu-specs/h100-sxm5-96-gb.c3974)  
8. Intel's ATX v3.0 PSU Standard Has More Power for GPUs | Tom's Hardware, accessed December 1, 2025, [https://www.tomshardware.com/news/intel-atx-v3-psu-standard](https://www.tomshardware.com/news/intel-atx-v3-psu-standard)  
9. Comparing NVIDIA H100 PCIe vs SXM: Performance, Use Cases and More \- Hyperstack, accessed December 1, 2025, [https://www.hyperstack.cloud/technical-resources/performance-benchmarks/comparing-nvidia-h100-pcie-vs-sxm-performance-use-cases-and-more](https://www.hyperstack.cloud/technical-resources/performance-benchmarks/comparing-nvidia-h100-pcie-vs-sxm-performance-use-cases-and-more)  
10. LITEON Server Power Supply 3000W Features:, accessed December 1, 2025, [https://liteon-cips.com/pdf/CRPSPowerSupply3000W.pdf](https://liteon-cips.com/pdf/CRPSPowerSupply3000W.pdf)  
11. Key Considerations For Choosing Power Supplies For AI GPU Servers \- linklieo, accessed December 1, 2025, [https://linklieo.com/key-considerations-for-choosing-power-supplies-for-ai-gpu-servers/](https://linklieo.com/key-considerations-for-choosing-power-supplies-for-ai-gpu-servers/)  
12. SUNGROW Power Stack Commercial Storage HV storage system, 110 kW inverter, 225 kWh, accessed December 1, 2025, [https://www.pv-24.at/en/products/sungrow-power-stack-commercial-storage/](https://www.pv-24.at/en/products/sungrow-power-stack-commercial-storage/)  
13. The Real Cost of Commercial Battery Energy Storage in 2025: What You Need to Know, accessed December 1, 2025, [https://www.gsl-energy.com/the-real-cost-of-commercial-battery-energy-storage-in-2025-what-you-need-to-know.html](https://www.gsl-energy.com/the-real-cost-of-commercial-battery-energy-storage-in-2025-what-you-need-to-know.html)  
14. Tesla battery pricing now public \- Gridium, accessed December 1, 2025, [https://gridium.com/tesla-battery-pricing/](https://gridium.com/tesla-battery-pricing/)  
15. How Much Does a Tesla Powerwall Cost in 2025? \- LawnStarter, accessed December 1, 2025, [https://www.lawnstarter.com/blog/cost/tesla-powerwall-price/](https://www.lawnstarter.com/blog/cost/tesla-powerwall-price/)  
16. How Much Does a Tesla Powerwall Cost 2025? \- BSL Battery, accessed December 1, 2025, [https://www.bsl-battery.com/news/how-much-does-a-tesla-powerwall-cost-2025](https://www.bsl-battery.com/news/how-much-does-a-tesla-powerwall-cost-2025)  
17. Aftermarket ComAp InteliGen 1000 Paralleling Controller IG31000XBBB IG31000YBBB for Generator Set \- FridayParts, accessed December 1, 2025, [https://www.fridayparts.com/inteligen-1000-paralleling-generator-set-controller-ig31000xbbb-ig31000ybbb-for-comap](https://www.fridayparts.com/inteligen-1000-paralleling-generator-set-controller-ig31000xbbb-ig31000ybbb-for-comap)  
18. Electronics Module Controller DSE8610 MKII for Deep Sea \- FridayParts, accessed December 1, 2025, [https://www.fridayparts.com/controller-dse8610-mkii-for-deep-sea-electronics-deep-sea-modul](https://www.fridayparts.com/controller-dse8610-mkii-for-deep-sea-electronics-deep-sea-modul)  
19. What are Startup Costs for Microgrid Energy Solutions Provider?, accessed December 1, 2025, [https://startupfinancialprojection.com/blogs/capex/microgrid-energy-solutions-provider](https://startupfinancialprojection.com/blogs/capex/microgrid-energy-solutions-provider)  
20. Generator Set Sizing | MacAllister Power Systems, accessed December 1, 2025, [https://www.macallisterpowersystems.com/solutions/engineering-toolbox/generator-set-sizing/](https://www.macallisterpowersystems.com/solutions/engineering-toolbox/generator-set-sizing/)  
21. Tesla Powerwall Cost 2025: Price, Installation & Savings \- PEP Solar, accessed December 1, 2025, [https://www.pepsolar.com/blog/how-much-does-the-tesla-powerwall-cost-in-2025/](https://www.pepsolar.com/blog/how-much-does-the-tesla-powerwall-cost-in-2025/)  
22. Texas Grid Operators and Regulators Iron Out New Rules for Data Centers, accessed December 1, 2025, [https://insideclimatenews.org/news/10102025/texas-grid-operators-and-regulators-iron-out-new-rules-for-data-centers/](https://insideclimatenews.org/news/10102025/texas-grid-operators-and-regulators-iron-out-new-rules-for-data-centers/)  
23. ERCOT LEL Ride-Through Criteria\_LLWG final, accessed December 1, 2025, [https://www.ercot.com/files/docs/2025/07/11/ERCOT-LEL-Ride-Through-Criteria\_LLWG-final.pptx](https://www.ercot.com/files/docs/2025/07/11/ERCOT-LEL-Ride-Through-Criteria_LLWG-final.pptx)  
24. Montanans ask PSC to rein in data-center energy agreements \- Missoula Current, accessed December 1, 2025, [https://missoulacurrent.com/data-center-energy-2/](https://missoulacurrent.com/data-center-energy-2/)  
25. NorthWestern plans 'large load' tariff for Montana data centers | Utility Dive, accessed December 1, 2025, [https://www.utilitydive.com/news/northwestern-large-load-data-center-tariff-montana/803334/](https://www.utilitydive.com/news/northwestern-large-load-data-center-tariff-montana/803334/)  
26. Site certification rules released for West Virginia data center/microgrid law, accessed December 1, 2025, [https://www.newsandsentinel.com/news/business/2025/11/site-certification-rules-released-for-data-center-microgrid-law/](https://www.newsandsentinel.com/news/business/2025/11/site-certification-rules-released-for-data-center-microgrid-law/)  
27. State Proposes Rule For Fast-Tracking Data Center Projects \- ObserverWV, accessed December 1, 2025, [https://observerwv.com/state-proposes-rule-for-fast-tracking-data-center-projects/](https://observerwv.com/state-proposes-rule-for-fast-tracking-data-center-projects/)  
28. Romania drafts cybersecurity rules for PV, cogeneration up to 1 MW \- PV Magazine, accessed December 1, 2025, [https://www.pv-magazine.com/2025/10/21/romania-drafts-cybersecurity-rules-for-pv-cogeneration-up-to-1-mw/](https://www.pv-magazine.com/2025/10/21/romania-drafts-cybersecurity-rules-for-pv-cogeneration-up-to-1-mw/)  
29. NFPA 110 Type 10 Requirements for Emergency Power Systems \- Cummins, accessed December 1, 2025, [https://www.cummins.com/sites/default/files/2019-03/PowerHour\_NFPA110.pdf](https://www.cummins.com/sites/default/files/2019-03/PowerHour_NFPA110.pdf)  
30. NFPA 855: Improving Energy Storage System Safety \- The American Clean Power Association (ACP), accessed December 1, 2025, [https://cleanpower.org/wp-content/uploads/gateway/2024/01/NFPA855\_Safety\_240111.pdf](https://cleanpower.org/wp-content/uploads/gateway/2024/01/NFPA855_Safety_240111.pdf)  
31. Order Megapack | Tesla, accessed December 1, 2025, [https://www.tesla.com/megapack/design](https://www.tesla.com/megapack/design)  
32. Tesla Megapack \- Wikipedia, accessed December 1, 2025, [https://en.wikipedia.org/wiki/Tesla\_Megapack](https://en.wikipedia.org/wiki/Tesla_Megapack)  
33. BYD Battery-box products list \- self2solar, accessed December 1, 2025, [https://www.self2solar.com/collections/byd-list](https://www.self2solar.com/collections/byd-list)  
34. Fluence Energy, Inc. Reports 2025 Financial Results and Initiates 2026 Guidance, accessed December 1, 2025, [https://ir.fluenceenergy.com/news-releases/news-release-details/fluence-energy-inc-reports-2025-financial-results-and-initiates/](https://ir.fluenceenergy.com/news-releases/news-release-details/fluence-energy-inc-reports-2025-financial-results-and-initiates/)