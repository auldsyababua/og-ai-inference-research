# BITCOIN MINER INTEGRATION MODEL

**Version:** 1.0  
**Last Updated:** 2025-12-02  
**Status:** Working prototype

---

## Purpose

Model Bitcoin miners as flexible, controllable load that can be shed to offset GPU power ramps in off-grid AI inference infrastructure. Miners help maintain stable generator loading by providing elastic load capacity.

---

## Quick Start Guide

### Step 1: Open Calculator
Open the CSV file in Excel, Google Sheets, or any spreadsheet application:
```
models/bitcoin-miner-integration/MinerIntegration-v1.csv
```

### Step 2: Configure Scenario

**GPU Ramp Configuration:**
- `GPU_Ramp_kW` - GPU power step (kW)
- `Ramp_Duration_s` - Time window for ramp (seconds)

**Miner Configuration:**
- `Miner_Model` - M60S or M50S++ (or custom)
- `Miner_Power_kW` - Power per miner unit (kW)
- `Containers_Available` - Number of mining containers
- `Container_Power_MW` - Power capacity per container (MW)

**Coordination Parameters:**
- `Shedding_Strategy` - Full/Partial/Staged
- `Response_Time_ms` - Miner shutdown response time (ms)
- `Opportunity_Cost_per_kWh` - Economic cost of downtime ($/kWh)

### Step 3: Review Outputs

**Coordination Outputs:**
- `Miner_Shed_Required_kW` - Power to shed (matches GPU ramp)
- `Units_to_Shed` - Number of miner units to shut down
- `Containers_to_Shed` - Number of containers (if full container shedding)
- `Response_Time_s` - Time to complete shedding (seconds)
- `Economic_Cost_per_Hour` - Cost of miner downtime ($/hour)

**Generator Impact:**
- `Net_Load_Change_kW` - Net change seen by generator (GPU ramp - miner shed)
- `Generator_Step_Fraction` - Net load change as % of generator capacity
- `Within_Generator_Limits` - TRUE if within generator step limits

---

## Miner Models

### Whatsminer M60S
- **Hashrate:** 184 TH/s (typical)
- **Power:** 3.3 kW per unit
- **Efficiency:** 18.5 J/TH
- **Container Capacity:** 300-600 units (1-2 MW)

### Whatsminer M50S++
- **Hashrate:** 160 TH/s (typical)
- **Power:** 3.3 kW per unit
- **Efficiency:** 22 J/TH
- **Container Capacity:** 300-600 units (1-2 MW)

**Note:** Both models have similar power consumption (~3.3 kW), so modeling treats them identically for power coordination purposes.

---

## Shedding Strategies

### Strategy 1: Full Container Shedding
- **Use Case:** Large GPU ramps (>500 kW)
- **Method:** Shut down entire containers (1-2 MW blocks)
- **Advantage:** Simple, fast coordination
- **Disadvantage:** Less granular control

### Strategy 2: Partial Container Shedding
- **Use Case:** Medium GPU ramps (100-500 kW)
- **Method:** Shut down specific units within containers
- **Advantage:** More precise matching to GPU ramp
- **Disadvantage:** Requires unit-level control

### Strategy 3: Staged Shedding
- **Use Case:** Very large ramps or multi-step sequences
- **Method:** Shed miners in stages matching generator ramp steps
- **Advantage:** Matches generator multi-step ramp capability
- **Disadvantage:** More complex coordination

---

## Example Scenarios

### Scenario 1: GPU Warmup with Miner Offset
- **GPU Ramp:** 500 kW over 10 seconds
- **Miner Shed:** 500 kW (150 units)
- **Response Time:** 100-500 ms
- **Net Load Change:** ~0 kW (perfect offset)
- **Economic Cost:** $50/hour while shed

### Scenario 2: Large GPU Cluster Startup
- **GPU Ramp:** 2000 kW over 60 seconds
- **Miner Shed:** 2000 kW (2 containers @ 1 MW each)
- **Response Time:** 500 ms
- **Net Load Change:** ~0 kW (perfect offset)
- **Economic Cost:** $200/hour while shed

### Scenario 3: Partial Offset (Limited Miners)
- **GPU Ramp:** 1000 kW
- **Miner Shed Available:** 500 kW (1 container)
- **Net Load Change:** 500 kW (50% offset)
- **Remaining:** 500 kW must be handled by generator/BESS

---

## Integration with Multi-Step Ramp Simulator

The miner integration model works with the multi-step ramp simulator:

1. **Calculate GPU Ramp:** Determine GPU power step and duration
2. **Calculate Miner Shed:** Determine how much miner load to shed
3. **Calculate Net Load:** GPU ramp - Miner shed = Net load change
4. **Feed to Ramp Simulator:** Use net load change as input to generator ramp model

**Example:**
- GPU wants to ramp: +500 kW
- Miners shed: -500 kW
- Net load change: 0 kW
- Generator sees: No change (perfect coordination)

---

## Limitations

**Current Version (v1) does NOT include:**
- Miner startup coordination (only shutdown/shedding)
- Partial unit control (assumes full unit shutdown)
- Network latency modeling
- Miner firmware variations
- Temperature-dependent power consumption
- Hashrate variation during operation

---

## References

- **Miner Specifications:** `data/miners/Whatsminer-Miner-Library.md`
- **Miner Manuals:** `docs/upstream-data-manuals/bitcoin-miners/`
- **Multi-Step Ramp Simulator:** `models/multistep-ramp-simulator/`
- **Generator Risk Calculator:** `models/generator-risk-calculator/`

---

**Last Updated:** 2025-12-02

