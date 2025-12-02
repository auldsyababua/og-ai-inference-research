# PSI POWER SOLUTIONS INTERNATIONAL NATURAL-GAS GENERATOR LIBRARY

## Project Overview

**Project:** Structured Natural-Gas Generator Library for Data Centers & Microgrids  
**Phase:** Phase 2 - PSI Engine Integration  
**Generated:** 2025-12-01  
**Scope:** 4 engine families (4.5L, 6.7L, 10L, 13L), multiple variants, power range 35-350 kW per unit  
**Source:** PSI Operations & Maintenance Manuals (7610061, 7610041-3, 7610034-2)

---

## Executive Summary

This library consolidates **PSI Power Solutions International natural-gas generator engines** extracted from official operations and maintenance manuals. These engines are commonly used in bitcoin mining generator applications and can be adapted for GPU-housed data center applications. Primary focus: mechanical engine parameters, with electrical generator set parameters to be confirmed with manufacturer for complete genset specifications.

### Key Metrics

| Metric | Value |
|--------|-------|
| **Total Engine Families** | 4 (4.5L, 6.7L, 10L, 13L) |
| **Total Variants** | 7+ (including turbocharged variants) |
| **Power Range (Estimated Gensets)** | 35-350 kW per unit |
| **Fuel Types** | Natural Gas, LPG (Liquid Propane Gas) |
| **Typical Applications** | Bitcoin Mining, Industrial Prime Power, Standby Power |
| **Manufacturer** | Power Solutions International (PSI), Wood Dale, IL |

### Important Notes

⚠️ **Data Status:** These manuals contain **engine-only specifications**. Complete generator set (genset) power outputs, electrical efficiency, and dynamic response parameters require manufacturer datasheets or application engineering consultation.

✅ **Application Context:** These engines are proven in bitcoin mining applications. The manufacturer can create GPU-housed versions using the same engine platforms.

---

## Detailed Model Summaries

### **PSI 4.5L SERIES**
*Small-Scale Prime Power & Standby*

**Family Overview:**
- **Engine Type:** 4.5L Naturally Aspirated, 4-cylinder
- **Displacement:** 4.5 liters
- **Estimated Power Range:** 35-45 kW (genset output, varies by generator head)
- **Typical Applications:** Small-scale bitcoin mining, standby power, distributed generation
- **Fuel Types:** Natural Gas, LPG

#### 4.5L NA (Naturally Aspirated)
- **Engine Configuration:** 4-cylinder, naturally aspirated
- **Displacement:** 4.5 L
- **Estimated Genset Power:** 35-41 kW @ 50 Hz, 40-45 kW @ 60 Hz
- **Rated Speed:** See nameplate (typically 1500 RPM @ 50 Hz, 1800 RPM @ 60 Hz)
- **Fuel:** Natural Gas, LPG
- **Key Note:** Entry-level engine for smaller mining operations or distributed generation

---

### **PSI 6.7L SERIES**
*Mid-Range Prime Power*

**Family Overview:**
- **Engine Type:** 6.7L Naturally Aspirated and Turbocharged variants
- **Displacement:** 6.7 liters
- **Estimated Power Range:** 87-150+ kW (genset output, varies by configuration)
- **Typical Applications:** Medium-scale bitcoin mining, industrial prime power
- **Fuel Types:** Natural Gas, LPG

#### 6.7L NA (Naturally Aspirated)
- **Engine Configuration:** 6-cylinder (inferred), naturally aspirated
- **Displacement:** 6.7 L
- **Estimated Genset Power:** ~87 kW
- **Rated Speed:** See nameplate
- **Fuel:** Natural Gas, LPG
- **Key Note:** Standard naturally aspirated configuration

#### 6.7L Turbocharged (6.7LT)
- **Engine Configuration:** 6-cylinder (inferred), turbocharged
- **Displacement:** 6.7 L
- **Estimated Genset Power:** Higher than NA variant (TBD - manufacturer data required)
- **Rated Speed:** See nameplate
- **Fuel:** Natural Gas, LPG
- **Key Note:** Turbocharged variant for increased power density

---

### **PSI 10L SERIES**
*Large Mid-Range Prime Power*

**Family Overview:**
- **Engine Type:** 10L Naturally Aspirated and Turbocharged variants
- **Displacement:** 10 liters
- **Estimated Power Range:** 130-236 kW (genset output, varies by configuration)
- **Typical Applications:** Large-scale bitcoin mining, industrial prime power, microgrids
- **Fuel Types:** Natural Gas, LPG

#### 10L NA (Naturally Aspirated)
- **Engine Configuration:** 6-cylinder (inferred), naturally aspirated
- **Displacement:** 10 L
- **Estimated Genset Power:** ~130 kW
- **Rated Speed:** See nameplate
- **Fire Order:** 1-5-3-6-2-4
- **Rotation:** CCW viewed on flywheel
- **Fuel:** Natural Gas, LPG
- **Key Note:** Standard naturally aspirated configuration

#### 10L Turbocharged (10LT)
- **Engine Configuration:** 6-cylinder (inferred), turbocharged
- **Displacement:** 10 L
- **Estimated Genset Power:** ~236 kW
- **Rated Speed:** See nameplate
- **Fuel:** Natural Gas, LPG
- **Key Note:** Turbocharged variant provides ~80% more power than NA version

---

### **PSI 13L SERIES**
*Large-Scale Prime Power*

**Family Overview:**
- **Engine Type:** 13L Turbocharged variants
- **Displacement:** 13 liters
- **Estimated Power Range:** 350+ kW (genset output)
- **Typical Applications:** Large-scale bitcoin mining operations, industrial prime power, microgrids
- **Fuel Types:** Natural Gas, LPG

#### 13L Turbocharged (13LT / 13LTHO)
- **Engine Configuration:** V-configuration (inferred), turbocharged
- **Displacement:** 13 L
- **Estimated Genset Power:** ~350 kW
- **Rated Speed:** See nameplate
- **Fuel:** Natural Gas, LPG
- **Key Note:** Highest power output in PSI lineup, suitable for large-scale operations

---

## Data Gaps & Required Information

### Critical Missing Data (Requires Manufacturer Consultation)

1. **Electrical Parameters:**
   - Rated electrical power output (ekW) for complete gensets
   - Electrical efficiency at rated load
   - Power factor capability
   - Voltage options (typically 0.48 kV, 4.16 kV, 13.8 kV)

2. **Dynamic Response Parameters:**
   - Maximum step load capability (% of rating)
   - Start time (seconds from start signal to ready-for-load)
   - Generator inertia (kg⋅m²)
   - ISO 8528 performance class (G1/G2/G3/G4)
   - Governor/control system type

3. **Generator Set Specifications:**
   - Generator head manufacturer and model
   - Complete genset efficiency (electrical + mechanical)
   - Load acceptance profiles
   - Frequency response characteristics

4. **Application-Specific Data:**
   - Bitcoin mining generator configurations
   - GPU-housed generator configurations (if available)
   - Containerized system specifications

---

## Structured Data Table

| Manufacturer | Model Variant | Application Tags | Estimated Power (ekW) | Displacement (L) | Cylinders | Aspiration | Fuel Types | Data Status |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **PSI** | **4.5L NA** | Bitcoin Mining, Standby | 35-45 | 4.5 | 4 | Naturally Aspirated | NG, LPG | Engine Only |
| **PSI** | **6.7L NA** | Bitcoin Mining, Prime | ~87 | 6.7 | 6 (est.) | Naturally Aspirated | NG, LPG | Engine Only |
| **PSI** | **6.7L Turbo** | Bitcoin Mining, Prime | TBD | 6.7 | 6 (est.) | Turbocharged | NG, LPG | Engine Only |
| **PSI** | **10L NA** | Bitcoin Mining, Prime | ~130 | 10 | 6 (est.) | Naturally Aspirated | NG, LPG | Engine Only |
| **PSI** | **10L Turbo** | Bitcoin Mining, Prime | ~236 | 10 | 6 (est.) | Turbocharged | NG, LPG | Engine Only |
| **PSI** | **13L Turbo** | Bitcoin Mining, Prime | ~350 | 13 | V-config (est.) | Turbocharged | NG, LPG | Engine Only |

**Legend:**
- **Data Status:** "Engine Only" = Manuals contain engine specs only; genset electrical parameters require manufacturer datasheets
- **Estimated Power:** Based on web research; actual values vary by generator head pairing and application

---

## Source References

1. **PSI Operations & Maintenance Manual 7610061-2** (5/08/2024)
   - Covers: 4.5L, 6.7L, 10L, 13L engines
   - Content: Operations, maintenance, engine specifications

2. **PSI 13L Owners Manual 7610041-3** (02/20/2023)
   - Covers: 13L Turbocharged engine
   - Content: Operations, maintenance, engine specifications

3. **PSI 6.7L Turbo Service Manual 7610034-2** (06/06/2022)
   - Covers: 6.7L Turbocharged engine
   - Content: Service procedures, disassembly/assembly

4. **PSI Diagnostic Manual 7610037-1** (04/21/2021)
   - Covers: 4.5L, 6.7L, 10L, 13L engines
   - Content: Diagnostic procedures, trouble codes

---

## Next Steps

1. **Contact PSI Application Engineering** for complete genset specifications:
   - Electrical power outputs for each engine variant
   - Generator head options and pairings
   - Electrical efficiency data
   - Dynamic response characteristics
   - ISO 8528 performance classifications

2. **Request GPU-Housed Generator Configurations:**
   - Specifications for GPU-optimized generator sets
   - Power output ratings
   - Efficiency characteristics
   - Containerized system options

3. **Validate Power Outputs:**
   - Confirm web-researched power ratings with manufacturer
   - Obtain official datasheets for each variant
   - Clarify power ratings for different generator head pairings

4. **Complete Data Integration:**
   - Add electrical parameters once obtained
   - Add dynamic response parameters
   - Update consolidated generator library
   - Add to generator risk calculator

---

## Notes for GPU Application

These PSI engines are proven in bitcoin mining applications, which share similar power characteristics with GPU compute loads:
- **Continuous duty operation**
- **High power density requirements**
- **Natural gas fuel availability**
- **Containerized deployment**

The manufacturer can create GPU-housed versions using the same engine platforms, potentially optimizing:
- Generator head selection for GPU power profiles
- Control systems for GPU load characteristics
- Containerization for GPU server integration
- Cooling systems for combined generator + GPU heat rejection

---

**Document Status:** Initial draft - Engine specifications extracted from manuals. Electrical/genset parameters require manufacturer consultation.

**Last Updated:** 2025-12-01

