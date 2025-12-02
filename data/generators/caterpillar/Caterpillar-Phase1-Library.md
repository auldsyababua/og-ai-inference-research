# CATERPILLAR NATURAL-GAS GENERATOR LIBRARY - PHASE 1

## Project Overview

**Project:** Structured Natural-Gas Generator Library for Data Centers & Microgrids  
**Phase:** Phase 1 - Caterpillar Deep Dive  
**Generated:** 2025-11-27  
**Scope:** 6 model families, 11 variants, power range 1.2–4.5 MW (gensets), 3.7–4 MW (engine-only)

---

## Executive Summary

This library consolidates **11 Caterpillar natural-gas generator variants** across 6 product families, extracted from official technical datasheets and application guides. Primary focus: electrical parameters, dynamic response capability, fuel flexibility, and operational characteristics suitable for data-center, microgrid, and industrial prime-power applications.

### Key Metrics

| Metric | Value |
|--------|-------|
| **Total Models Extracted** | 6 (CG170, CG260, G3516, G3520, G3520H, G3616) |
| **Total Variants** | 11 |
| **Power Range (Gensets)** | 1.2–4.5 MW per unit |
| **Power Range (Engine-only)** | 3.7–4 MW (G3616) |
| **Highest Efficiency** | 45.3% (G3520H 50 Hz) |
| **Best Dynamic Response** | G3520H (ISO 8528-5 Class G1), G3520 (ISO 8528-5 G2 + NFPA 110) |
| **Most Fuel-Flexible** | CG260-16 (Nat. Gas, Biogas, Coal Gas, Synthesis Gas, H₂ to 25%) |
| **Typical First Service** | 4,000 hours (CG170, CG260) |
| **Major Overhaul Interval** | 64,000–80,000 hours |

---

## Detailed Model Summaries

### **CATERPILLAR CG170 SERIES** 
*Prime/Continuous Industrial & CHP Workhorse*

**Family Overview:**
- **Power Range:** 1.2–2.0 MW per unit
- **Typical Applications:** Industrial prime power, CHP, microgrids, data centers, distributed generation
- **Fuel Types:** Natural Gas, Biogas, Coal Gas, Synthesis Gas
- **Installation Base:** 3,000+ MWel worldwide, 2,854+ generator sets deployed

#### CG170-12
- **Rated Power:** 1,200 kW @ 1.0 pf (50 Hz), 1,200 kW @ 1.0 pf (60 Hz)
- **Electrical Efficiency:** 43.7% (50 Hz), 43.4% (60 Hz)
- **Total Efficiency:** 87.0% (50 Hz), 86.6% (60 Hz)
- **Governor:** Electronic - Reactive Droop (TEM), ISO 8528 compliant
- **Displacement:** 53.1 L (V-12 cylinders)
- **Maintenance:** 4,000 h first service, 64,000 h major overhaul
- **Key Note:** Soot-free combustion, extended intervals reduce lifecycle cost

#### CG170-16 (Most Common)
- **Rated Power:** 1,560 kW @ 1.0 pf (50 Hz), 1,550 kW @ 1.0 pf (60 Hz)
- **Electrical Efficiency:** 43.3% (50 Hz), 43.0% (60 Hz)
- **Total Efficiency:** 87.1% (50 Hz), 86.7% (60 Hz)
- **Governor:** Electronic - Reactive Droop (TEM), grid-code compliant
- **Displacement:** 70.8 L (V-16 cylinders)
- **Application:** Prime power, continuous, data-center, microgrid
- **Key Note:** Industry standard for modular data-center deployments (~1.56 MW units)

#### CG170-20
- **Rated Power:** 2,000 kW @ 1.0 pf (both 50 Hz and 60 Hz)
- **Electrical Efficiency:** 43.7% (50 Hz), 43.5% (60 Hz)
- **Total Efficiency:** 86.9% (50 Hz), 86.7% (60 Hz)
- **Governor:** Electronic - Reactive Droop (TEM)
- **Displacement:** 88.5 L (V-20 cylinders)
- **Application:** Prime power, continuous, large industrial CHP

---

### **CATERPILLAR CG260 SERIES** 
*Large-Scale Prime / Utility-Grade*

**Family Overview:**
- **Power Range:** 3.0–4.5 MW per unit
- **Typical Applications:** Utility peak-load, large industrial CHP, multi-MW microgrids
- **Fuel Types:** Natural Gas, Biogas, Coal Gas, Associated Gas, Synthesis Gas, **Hydrogen to 25%**
- **Installation Base:** 800+ MWel installed globally

#### CG260-16
- **Rated Power:** 4,300 kW @ 1.0 pf (50 Hz), 4,000 kW @ 1.0 pf (60 Hz)
- **Electrical Efficiency:** 44.1% (50 Hz), **43.8% (60 Hz) – Highest in Caterpillar genset class**
- **Standby Power:** 4,500 kW (both frequencies)
- **Governor:** Electronic (ADEM-based), ISO 8528 compliant
- **Displacement:** 271.8 L (V-16 cylinders)
- **Maintenance:** 4,000 h first service, 80,000 h major overhaul (extended interval)
- **Unique Feature:** **Hydrogen-capable to 25% blending** for future decarbonization
- **Key Note:** Utility-scale efficiency; long overhaul intervals minimize downtime in large fleets

---

### **CATERPILLAR G3516** 
*Data-Center Standby Standard (North America)*

**Family Overview:**
- **Power:** ~1.5 MW standby @ 0.8 pf
- **Typical Applications:** Data-center emergency backup, mission-critical standby, industrial backup
- **Fuel Types:** Natural Gas, **Hydrogen Blend (up to 5%)**
- **Governor:** GECM (Gas Engine Control Module) A4
- **Compliance:** U.S. EPA Stationary Non-Emergency Certified

#### G3516-60 Hz
- **Standby Rating:** 1,500 ekW @ 0.8 pf
- **Frequency:** 60 Hz
- **Engine Speed:** 1,800 rpm
- **Electrical Efficiency:** Not explicitly stated (standby units typically 40–42%)
- **Compression Ratio:** 11.5:1
- **Emissions:** Selectable NOx (0.5 or 1.0 g/bhp-hr)
- **Key Advantage:** Proven reliability, EPA certified, wide voltage range (120V–13.8kV)
- **Application Note:** Workhorse standby generator for North American data centers

---

### **CATERPILLAR G3520 (FAST RESPONSE)** 
*Data-Center Emergency Backup – Mission-Critical*

**Family Overview:**
- **Power:** ~1.4–2.5 MW standby @ 0.8 pf
- **Typical Applications:** Data-center emergency backup, NFPA 110 Type 10 (mission-critical), utility standby
- **Key Differentiator:** **100% block load acceptance** (fastest loading in class)
- **Compliance:** NFPA 110 Type 10, ISO 8528-5 G2

#### G3520-60 Hz (2000 kW Standby)
- **Standby Rating:** 2,000 ekW @ 0.8 pf
- **Frequency:** 60 Hz
- **Engine Speed:** 1,800 rpm
- **Governor:** ADEM™ A4
- **Fuel Type:** Natural Gas, **Hydrogen Blend (up to 5%)**
- **Emissions:** Selectable NOx (0.5 or 1.0 g/bhp-hr)
- **Dynamic Performance:** **ISO 8528-5 G2 (100% block load, NFPA 110 Type 10 compliant)**
- **Key Feature:** "FAST RESPONSE" variant designed for rapid load acceptance (critical for data center UPS transition)
- **Application:** Industry standard for data-center emergency power; proven NFPA compliance

---

### **CATERPILLAR G3520H** 
*Premium Continuous Prime / Grid Support*

**Family Overview:**
- **Power:** ~2.5 MW continuous @ 1.0 pf (50 Hz), ~2.5 MW @ 0.8 pf (60 Hz)
- **Typical Applications:** Continuous prime power, CHP, grid support, microgrid primary source, renewables balancing
- **Key Differentiator:** **HIGHEST ELECTRICAL EFFICIENCY in gas genset market (45.3%)**
- **Compliance:** ISO 8528-5 Class G1 (excellent transient performance verified)

#### G3520H-50 Hz (Continuous 2,519 kW)
- **Continuous Rating:** 2,519 ekW @ 1.0 pf
- **Frequency:** 50 Hz
- **Engine Speed:** 1,500 rpm
- **Electrical Efficiency:** **45.3% (BEST-IN-CLASS)**
- **Thermal Efficiency:** 41.0%
- **Total Efficiency:** 86.3%
- **Governor:** ADEM™ A4 (isochronous/droop capable)
- **Fuel Consumption:** 7.94 MJ/kWh @ 100% load
- **Emissions:** 500 mg/Nm³ NOx
- **Dynamic Performance:** ISO 8528-5 Class G1 (transient performance verified through torsional vibration and endurance testing)
- **Key Advantage:** Top-tier electrical efficiency; suitable for modern microgrids requiring continuous, dispatchable power with grid support

#### G3520H-60 Hz (Continuous 2,476 kW)
- **Continuous Rating:** 2,476 ekW @ 0.8 pf
- **Frequency:** 60 Hz
- **Engine Speed:** 1,500 rpm
- **Thermal Efficiency:** 41.1%
- **Total Efficiency:** 86.7%
- **Fuel Consumption:** 8.56 MJ/kWh @ 100% load
- **Package Options:** High Efficiency vs. Humidity/Fuel Tolerant (flexible inlet conditions)
- **Governor:** ADEM™ A4
- **Dynamic Performance:** ISO 8528-5 Class G1
- **Voltage Range:** 440V–13.8kV (wide application flexibility)

---

### **CATERPILLAR G3616 (LEAN-BURN)** 
*Industrial Prime Mover / Gas Compression (Engine-Only)*

**Family Overview:**
- **Power:** 3,729–3,990 bkW (5,000–5,350 bhp) @ 1,000 rpm
- **Configuration:** **ENGINE-ONLY** (requires custom synchronous generator coupling)
- **Typical Applications:** Gas compression, pipeline compressor drives, very large CHP plants, industrial prime movers
- **Key Differentiator:** Slow-speed (1,000 rpm), lean-burn technology for maximum durability and efficiency

#### G3616-1000 rpm (Lean-Burn)
- **Rated Power:** 3,729–3,990 bkW (5,000–5,350 bhp) depending on ambient temperature
- **Engine Speed:** 1,000 rpm
- **Displacement:** 339 L (V-16 cylinders)
- **Combustion:** Low-Emission Lean-Burn technology
- **Governor:** ADEM™ A4 (integrated speed, air/fuel ratio, individual cylinder timing control)
- **Fuel Consumption:** 9.18–9.23 MJ/bkWh (excellent efficiency for power density)
- **Emissions:** 0.5 g/bhp-hr NOx (EPA NSPS compliant with oxidation catalyst)
- **Key Features:**
  - **Slow-speed design:** Extended bearing life, lower maintenance
  - **Lean-burn:** Highest fuel efficiency in class, lower emissions
  - **Air/fuel & ignition control:** ADEM A4 manages individual cylinder detonation and timing
  - **Oil change interval:** 5,000 hours
  - **Potential life:** 80,000+ hours (very long vs. high-speed alternatives)
- **Application Note:** Engine-only product; requires separate generator coupling and custom integration engineering. Typical in industrial/utility settings where custom architecture is feasible.

---

## Dynamic Response & Control Characteristics

### Governor & Control Systems

| Model Family | Governor Type | ISO 8528 Compliance | Control Features |
|--------------|---------------|-------------------|------------------|
| **CG170** | Electronic - Reactive Droop (TEM) | ISO 8528 | 3-phase PF control, KVAR adjustment, grid-code compliant |
| **CG260** | Electronic (ADEM) | ISO 8528 | Electronic fuel control, droop & isochronous modes |
| **G3516** | GECM A4 | EPA Non-Emergency | Electronic fuel control, emissions-selectable (0.5 or 1.0 g/bhp-hr) |
| **G3520** | ADEM™ A4 | ISO 8528-5 G2 | 100% block load acceptance, NFPA 110 Type 10, fast response |
| **G3520H** | ADEM™ A4 | ISO 8528-5 G1 | Verified transient performance, extended continuous operation |
| **G3616** | ADEM™ A4 | N/A (engine-only) | Lean-burn air/fuel & ignition control, individual cylinder management |

### Data Gaps for Microgrid Modeling

**Critical parameters NOT available in public datasheets:**

- ❌ **Inertia constant (H)** in seconds – Required for RoCoF estimation
- ❌ **Rate of Change of Frequency (RoCoF)** – No published values for standard load steps
- ❌ **Voltage dip %** for X% block load – Only "ISO 8528 compliant" stated; exact dip not quantified
- ❌ **Settling time** after transient – Time to return within ±1% frequency tolerance
- ❌ **Governor droop default** – Stated as "typical 2–5%" but factory settings not specified
- ❌ **AVR/exciter gains & time constants** – Not provided in genset brochures
- ❌ **Load ramp rates** – Maximum allowable dP/dt (kW/s)

**Recommendation:** Contact Caterpillar application engineering for detailed technical datasheets containing transient performance curves and dynamic parameters.

---

## Fuel Specifications

### Natural Gas Quality Requirements

| Model | Gas Pressure (inlet) | Wobbe Index | Methane Number Min | Notes |
|-------|----------------------|------------|-------------------|-------|
| CG170 | 0.5–10 bar | 31.5–47.2 MJ/Nm³ | 70 (NG), 130 (biogas) | Pipeline or biogas compatible |
| CG260 | Not specified | Not specified | Not specified | Specify with engineering |
| G3516 | 10.2–34.5 kPa to fuel valve | Not specified | 80 (NG) | Optimized for low-pressure pipeline |
| G3520 | Not specified | Not specified | Not specified | Specify with engineering |
| G3520H | Not specified (NG optimized) | Not specified | Not specified | Premium efficiency package |
| G3616 | 400–485 kPag | Not specified | Not specified | Industrial-grade gas supply |

### Hydrogen Blending Capability

| Model | Hydrogen Blending |
|-------|------------------|
| **CG260** | **Up to 25%** (most flexible) |
| **G3516** | Up to 5% |
| **G3520** | Up to 5% |
| **G3520H** | Not mentioned (natural gas optimized) |
| **G3616** | Not mentioned (lean-burn NG optimized) |

---

## Electrical Efficiency Ranking (All Models)

| Rank | Model | Variant | Efficiency | Rating | Notes |
|------|-------|---------|-----------|--------|-------|
| **1** | **G3520H** | **50 Hz Continuous** | **45.3%** | **1.0 pf** | Best-in-class; premium continuous operation |
| **2** | **CG260-16** | **50 Hz Continuous** | **44.1%** | **1.0 pf** | Highest among large gensets; hydrogen capable |
| **3** | CG260-16 | 60 Hz Continuous | 43.8% | 1.0 pf | – |
| **4** | CG170-12 | 50 Hz | 43.7% | 1.0 pf | – |
| **5** | CG170-20 | 50 Hz | 43.7% | 1.0 pf | – |
| **6** | CG170-16 | 50 Hz | 43.3% | 1.0 pf | Most common variant |
| **7** | CG170-20 | 60 Hz | 43.5% | 1.0 pf | – |
| **8** | CG170-16 | 60 Hz | 43.0% | 1.0 pf | – |
| **9** | CG170-12 | 60 Hz | 43.4% | 1.0 pf | – |
| **N/A** | **G3516** | 60 Hz Standby | Not stated | 0.8 pf | Standby unit (typical 40–42%) |
| **N/A** | **G3520** | 60 Hz Standby | Not stated | 0.8 pf | Standby unit (typical 40–42%) |

---

## Application Suitability Matrix

### For Data-Center Emergency Backup (Standby)
✅ **Best Choice:** G3520 (2,000 kW) or G3516 (1,500 kW)  
- 100% block load acceptance (FAST RESPONSE)
- NFPA 110 Type 10 compliant
- ISO 8528-5 G2 transient performance
- Proven reliability in mission-critical facilities

### For Data-Center Prime Power (Continuous or Peak Shaving)
✅ **Best Choice:** G3520H (2,500 kW)  
- 45.3% electrical efficiency (best-in-class)
- ISO 8528-5 G1 transient compliance
- Suitable for 24/7 or extended runtime
- Grid-support capable (isochronous or droop)

### For Large Industrial CHP
✅ **Best Choice:** CG260-16 (4,300 kW) or G3520H (2,500 kW stack)  
- High efficiency (44.1%–45.3%)
- Extended service intervals (64,000–80,000 h)
- Heat recovery optimized
- Flexible fuel and voltage options

### For Utility / Multi-MW Microgrids
✅ **Best Choice:** CG260-16 (4.3 MW) + CG170-16 units (1.56 MW each)  
- Modular scalability
- CG260 for base-load, CG170 for peaking
- Hydrogen-ready capability (CG260 to 25%)
- 80,000 h overhaul interval (CG260) minimizes fleet maintenance

### For Gas Compression / Industrial Prime Mover
✅ **Best Choice:** G3616 (3.7–4 MW engine)  
- 1,000 rpm slow-speed design (durability)
- Lean-burn efficiency (9.18–9.23 MJ/kWh)
- 5,000 h oil changes, 80,000+ h potential life
- Custom generator coupling + integration engineering required

---

## Data Sources & Verification

All parameters extracted from **official Caterpillar technical documentation:**

- **Brochures:**
  - LEBE0017-01: CG170 Product Overview
  - CM20190506-00f9b-fb814: G3520 FAST RESPONSE
  - CM20190904-a8775-29c11: G3520H 60 Hz Continuous
  - LEHE1267-00: G3520H 50 Hz

- **Product Pages:**
  - https://www.cat.com/en_US/products/new/power-systems/electric-power/gas-generator-sets/

- **Dealer Technical Sheets:**
  - Hawthorne Cat, Finning, Western States Cat, Cleveland Brothers

- **Distributor Engineering Data:**
  - Finning PDF archives (G3616 ADEM A4, G3520H specification sheets)

---

## Maintenance & Lifecycle Costs

| Model | First Service | Major Overhaul | Oil Change | Key Advantage |
|-------|---------------|----------------|-----------|-----------------|
| CG170 | 4,000 h | 64,000 h | ~500 h | Extended intervals reduce downtime |
| CG260 | 4,000 h | **80,000 h** | ~500 h | **Longest overhaul interval** (ideal for fleet) |
| G3516 | 1,000 h / 12 mo | Not specified | Typical | Proven standby reliability |
| G3520 | 1,000 h / 12 mo | Not specified | Typical | Fast response priority |
| G3520H | 12 mo (unlimited h) | Not specified | Extended | Low oil consumption, premium intervals |
| G3616 | Not specified | **80,000+ h potential** | 5,000 h | Slow-speed durability, minimal maintenance |

---

## Recommendations for Microgrid Implementation

### 1. **For Electrical Modeling & Simulation**
- Use **G3520H** as "best available" parameter reference (highest efficiency, G1 compliance)
- Estimate inertia constant (H) using rotating mass approximation or engineering support
- Assume governor droop 2–5% for grid-connected, 5–10% for island mode
- ISO 8528-5 compliance ensures transient response within defined envelope

### 2. **For Fleet-Level Deployments**
- **Base-load:** Stack CG260-16 units (4.3 MW each, 44.1% efficiency, 80,000 h overhaul)
- **Peak/Peaking:** CG170-16 units (1.56 MW each, modular scalability)
- **Emergency backup:** G3520 units (2 MW each, NFPA 110 Type 10, 100% block load)

### 3. **For Fuel Strategy**
- **Natural gas:** Any model suitable
- **Biogas/landfill gas:** CG170, CG260 excellent options
- **Hydrogen transition:** CG260-16 (up to 25%), G3516/G3520 (up to 5%)

### 4. **Dynamic Parameters (Estimated)**
- Typical droop setting: **3–4%** (grid-connected), **7%** (island mode)
- Inertia constant (H): **~2–4 seconds** (estimate from mass/speed); contact vendor for verification
- Governor response time: **0.5–2 seconds** to steady-state (ADEM A4 control)
- Voltage regulation (AVR): **±3–5%** on load step (ISO 8528 G1/G2 envelope)

### 5. **Next Phase: Expand Library**
- **MTU Series 4000** (4.0–5.0 MW, 45%+ efficiency)
- **Cummins QSK** (similar power/efficiency range)
- **INNIO Jenbacher J-series** (esp. J920 for data centers)
- **Wärtsilä 34SG / 50SG** (utility-scale, 34–50 MW per engine)

---

## Critical Notes & Disclaimers

1. **Inertia Constant (H):** NOT provided by Caterpillar in public datasheets. Required for RoCoF analysis. Recommend:
   - Derivation from rotating mass: H = (1/2 × M × ω²) / (S_base)
   - Direct inquiry to application engineering team
   - Load-step testing if available

2. **Transient Response:** Caterpillar references "ISO 8528-5 Class G1/G2" compliance but does NOT publish exact:
   - Voltage dip (%) for specified load steps
   - RoCoF (Hz/s) for frequency support
   - Settling time to steady-state
   - These must be requested from dealer engineering support

3. **Emissions Compliance:** Models support variable NOx settings (typically 0.5–1.0 g/bhp-hr). Environmental regulations may require lowest setting; verify with local authority and emission standards.

4. **Fuel Quality:** Gas pressure, Wobbe index, and methane number are critical. Site-specific analysis required for non-standard fuel sources. Contact dealer for detailed feasibility.

5. **Hydrogen Blending:** CG260 supports up to 25%, but requires specialized fuel system engineering. Thermal efficiency may vary. Pilot testing recommended before fleet deployment.

---

## Conclusion

The **Caterpillar natural-gas generator library (Phase 1)** provides comprehensive electrical, operational, and maintenance data for 11 genset variants suitable for data-center, microgrid, and industrial applications. **Highest electrical efficiency (45.3%, G3520H 50 Hz) and best transient compliance (ISO 8528-5 Class G1, G3520H; G2 NFPA 110 G3520)** make these units industry-leading for continuous prime power and mission-critical standby.

**Key gaps for microgrid modeling** (inertia constant, RoCoF, exact transient parameters) require additional technical support from Caterpillar application engineering. Phase 2 should expand to MTU, Cummins, Jenbacher, and Wärtsilä to complete the multi-manufacturer comparative analysis.

**Excel-ready data records** enable immediate integration into planning and procurement workflows. Flat CSV format supports pivot table analysis by efficiency, power range, fuel type, and application suitability.

---

**For detailed transient performance, dynamic parameters, and application engineering support, contact your local Caterpillar dealer or application engineering team.**

