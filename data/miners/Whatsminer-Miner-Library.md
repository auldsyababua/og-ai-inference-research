# WHATSMINER BITCOIN MINER LIBRARY

**Project:** Off-Grid AI Inference Research  
**Date:** 2025-12-02  
**Source:** MicroBT Electronics Technology Co., Ltd. Product Manuals (October 2024)

---

## Executive Summary

This library documents specifications for Whatsminer Bitcoin mining equipment used as flexible load in off-grid AI inference infrastructure. Miners serve as controllable, elastic load that can be shed to offset GPU power ramps, helping maintain stable generator loading.

**Primary Models:**
- **Whatsminer M60S** - 184 TH/s (typical)
- **Whatsminer M50S++** - 160 TH/s (typical)

---

## Model Specifications

### **Whatsminer M60S**

**Typical Configuration:** 184 TH/s (within manufacturer range)

| Parameter | Value | Notes |
|-----------|-------|-------|
| **Hashrate** | 170-186 TH/s ±5% | Typical: 184 TH/s |
| **Power Consumption** | 3145-3441 W ±10% | At wall, AC input |
| **Power Efficiency** | 18.5 J/TH ±5% @ 25°C | Power ratio |
| **Input Voltage** | AC 220-240 V | Single phase |
| **Input Current** | ~15-16 A | At 220V |
| **Power Cable** | IEC C19, ≥ 16 A | Standard connector |
| **Net Weight** | 11.5 kg | Without packaging |
| **Gross Weight** | 12.6 kg | With packaging |
| **Dimensions (L×W×H)** | 430 × 155 × 226 mm | Without package |
| **Noise Level** | ~75 dB | Typical for air-cooled |
| **Operating Temperature** | -5°C to +35°C | Ambient |
| **Air Flow** | 350 CFM | Cooling requirement |
| **Network** | Ethernet (RJ45) | 10/100M |
| **Release Date** | October 2024 | Product manual date |

**Power Modeling:**
- **Typical Power:** ~3.3 kW per unit (mid-range of 3145-3441W)
- **Power per TH/s:** ~18 W/TH (at 184 TH/s, 3.3 kW)
- **Container Capacity:** ~300-600 units per container (1-2 MW typical)

---

### **Whatsminer M50S++**

**Typical Configuration:** 160 TH/s (within manufacturer range)

| Parameter | Value | Notes |
|-----------|-------|-------|
| **Hashrate** | 138-158 TH/s ±5% | Typical: 160 TH/s |
| **Power Consumption** | 3036-3476 W ±10% | At wall, AC input |
| **Power Efficiency** | 22 J/TH ±5% @ 25°C | Power ratio |
| **Input Voltage** | AC 220-240 V | Single phase |
| **Input Current** | ~14-16 A | At 220V |
| **Power Cable** | IEC C19, ≥ 16 A | Standard connector |
| **Net Weight** | 11.5 kg | Without packaging |
| **Gross Weight** | 12.6 kg | With packaging |
| **Dimensions (L×W×H)** | 430 × 155 × 226 mm | Without package |
| **Noise Level** | ~75 dB | Typical for air-cooled |
| **Operating Temperature** | -5°C to +35°C | Ambient |
| **Air Flow** | 350 CFM | Cooling requirement |
| **Network** | Ethernet (RJ45) | 10/100M |
| **Release Date** | October 2024 | Product manual date |

**Power Modeling:**
- **Typical Power:** ~3.3 kW per unit (mid-range of 3036-3476W)
- **Power per TH/s:** ~20.6 W/TH (at 160 TH/s, 3.3 kW)
- **Container Capacity:** ~300-600 units per container (1-2 MW typical)

---

## Container Configurations

### Typical Mining Container Setup

**Standard Container:**
- **Container Size:** 20-40 ft shipping container
- **Power Capacity:** 1-2 MW (typical)
- **Miner Units:** 300-600 units (M60S or M50S++)
- **Cooling:** Air-cooled (350 CFM per unit)
- **Power Distribution:** 220-240V AC, 16A circuits

**Power Density:**
- **Per Unit:** ~3.3 kW
- **Per Container (1 MW):** ~300 units
- **Per Container (2 MW):** ~600 units

---

## Flexible Load Characteristics

### Response Time

**Miner Shutdown Response:**
- **Software Command:** <100 ms (API call to miner)
- **Physical Shutdown:** 100-500 ms (power down sequence)
- **Total Response:** ~100-500 ms (multi-second timescale)

**Miner Startup Response:**
- **Power On:** 1-5 seconds
- **Boot Sequence:** 10-30 seconds
- **Hashrate Ramp:** 30-60 seconds to full hashrate
- **Total Startup:** ~1-2 minutes

### Shedding Granularity

**Minimum Shedding Increment:**
- **Per Unit:** 3.3 kW (one miner)
- **Per Container:** 1-2 MW (entire container)
- **Partial Container:** 100-500 kW blocks (30-150 units)

**Practical Shedding Blocks:**
- **Small Block:** 10-50 kW (3-15 units)
- **Medium Block:** 50-200 kW (15-60 units)
- **Large Block:** 200-1000 kW (60-300 units)
- **Full Container:** 1-2 MW (300-600 units)

---

## Economic Modeling

### Opportunity Cost

**Miner Downtime Value:**
- **Revenue Loss:** Based on Bitcoin price and network difficulty
- **Typical Range:** $0.05-$0.15 per kWh of downtime (varies with BTC price)
- **Example:** At $0.10/kWh opportunity cost, shedding 1 MW for 1 hour = $100 lost revenue

**Cost per kW Shed:**
- **Per Unit:** 3.3 kW × $0.10/kWh = $0.33/hour per unit
- **Per Container (1 MW):** $100/hour
- **Per Container (2 MW):** $200/hour

---

## Integration with GPU Ramp Control

### Use Case: Offset GPU Power Steps

**Scenario:** GPU cluster ramping up 500 kW
- **Miner Shedding Required:** 500 kW
- **Units to Shed:** ~150 units (M60S or M50S++)
- **Response Time:** 100-500 ms (acceptable for multi-second ramps)
- **Economic Cost:** $50/hour while shed (at $0.10/kWh)

**Coordination Strategy:**
1. **Pre-Ramp:** Signal miners to shed 500 kW (150 units)
2. **Ramp Window:** GPUs ramp up over 10-60 seconds
3. **Post-Ramp:** Miners can restart after generator stabilizes
4. **Net Load:** Generator sees minimal net change

---

## References

- **M60S Manual:** `docs/upstream-data-manuals/bitcoin-miners/WhatsMinerM60S_1760948331396.pdf`
- **M50S++ Manual:** `docs/upstream-data-manuals/bitcoin-miners/WhatsMinerM50S++_1760947002245.pdf`
- **Manufacturer:** Shenzhen MicroBT Electronics Technology Co., Ltd.
- **Website:** www.whatsminer.com

---

## Notes

- **Prototype Data:** Manuals note "Prototype data for reference only"
- **Power Variation:** Power consumption varies ±10% with ambient temperature
- **Firmware Updates:** Specifications may change with firmware updates
- **Modeling Assumption:** Using typical values (184T for M60S, 160T for M50S++) for planning

---

**Last Updated:** 2025-12-02

