# BITCOIN MINER INTEGRATION - FORMULAS

**Version:** 1.0  
**Last Updated:** 2025-12-02

---

## Input Parameters

| Symbol | Name | Units | Description |
|--------|------|-------|-------------|
| P_gpu | GPU_Ramp_kW | kW | GPU power step/ramp |
| Δt | Ramp_Duration_s | s | Time window for GPU ramp |
| P_miner | Miner_Power_kW | kW | Power per miner unit |
| N_containers | Containers_Available | count | Number of mining containers |
| P_container | Container_Power_MW | MW | Power capacity per container |
| t_response | Response_Time_ms | ms | Miner shutdown response time |
| C_opp | Opportunity_Cost_per_kWh | $/kWh | Economic cost of downtime |

---

## Coordination Calculations

### 1. Miner Shedding Required

```
P_shed = P_gpu
```

**Interpretation:** Shed miner load equal to GPU ramp to maintain net load constant.

**Example:**
- GPU ramp: 500 kW
- Miner shed: 500 kW

---

### 2. Units to Shed

```
N_units = P_shed / P_miner
```

**Units:** count

**Interpretation:** Number of miner units to shut down.

**Example:**
- Shed required: 500 kW
- Power per unit: 3.3 kW
- Units to shed: 500 / 3.3 = 152 units

---

### 3. Containers to Shed (Partial)

```
N_containers_partial = N_units / N_units_per_container
```

Where:
```
N_units_per_container = P_container × 1000 / P_miner
```

**Example:**
- Units to shed: 152
- Units per container: 1 MW / 3.3 kW = 303 units
- Containers (partial): 152 / 303 = 0.51 containers

---

### 4. Containers to Shed (Full Container Strategy)

```
N_containers_full = ceil(P_shed / P_container)
```

**Units:** count (rounded up)

**Interpretation:** Number of full containers to shut down.

**Example:**
- Shed required: 500 kW = 0.5 MW
- Container capacity: 1 MW
- Containers (full): ceil(0.5 / 1) = 1 container

---

### 5. Response Time

```
t_response_s = t_response_ms / 1000
```

**Units:** seconds

**Interpretation:** Time to complete miner shutdown.

**Example:**
- Response time: 500 ms
- Response time (s): 0.5 seconds

---

### 6. Economic Cost per Hour

```
Cost_per_hour = P_shed × C_opp
```

**Units:** $/hour

**Interpretation:** Cost of miner downtime per hour.

**Example:**
- Shed: 500 kW
- Opportunity cost: $0.10/kWh
- Cost per hour: 500 × 0.10 = $50/hour

---

### 7. Economic Cost per Ramp Event

```
Cost_per_ramp = Cost_per_hour × (Δt / 3600)
```

**Units:** $

**Interpretation:** Total cost for a single ramp event.

**Example:**
- Cost per hour: $50/hour
- Ramp duration: 10 seconds
- Cost per ramp: 50 × (10 / 3600) = $0.14

---

## Generator Impact Calculations

### 8. Net Load Change

```
ΔP_net = P_gpu - P_shed
```

**Units:** kW

**Interpretation:** Net change in generator load after coordination.

**Example:**
- GPU ramp: 500 kW
- Miner shed: 500 kW
- Net load change: 500 - 500 = 0 kW (perfect offset)

---

### 9. Generator Step Fraction

```
StepFraction = ΔP_net / P_rated_gen
```

**Units:** per unit (dimensionless)

**Interpretation:** Net load change as fraction of generator capacity.

**Example:**
- Net load change: 0 kW
- Generator rated: 4300 kW (CG260-16)
- Step fraction: 0 / 4300 = 0 (no step required)

---

### 10. Within Generator Limits Check

```
WithinLimits = (StepFraction × 100 < MaxStep_pct)
```

**Result:** TRUE or FALSE

**Example:**
- Step fraction: 0 (0%)
- Max step: 16% (CG260-16)
- Within limits: TRUE

---

## Shedding Strategy Logic

### Strategy 1: Perfect Offset (Default)

```
if P_shed <= N_containers × P_container:
    P_shed_actual = P_shed
    ΔP_net = P_gpu - P_shed_actual
else:
    P_shed_actual = N_containers × P_container  # Limited by available miners
    ΔP_net = P_gpu - P_shed_actual  # Partial offset
```

**Interpretation:** Shed as much as possible to offset GPU ramp, up to available miner capacity.

---

### Strategy 2: Full Container Shedding

```
N_containers_shed = ceil(P_shed / P_container)
P_shed_actual = min(N_containers_shed × P_container, N_containers × P_container)
```

**Interpretation:** Shut down full containers only, rounded up to nearest container.

---

### Strategy 3: Staged Shedding (Multi-Step)

For multi-step generator ramps (e.g., CG260), match miner shedding to generator steps:

```
for each generator_step in ramp_sequence:
    P_shed_step = generator_step.load_increase
    Shed miners: P_shed_step kW
    Wait: generator_step.recovery_time
```

**Interpretation:** Coordinate miner shedding with generator multi-step ramp sequence.

---

## Integration with Multi-Step Ramp Simulator

### Combined Calculation

```
# From GPU ramp:
P_gpu_step = GPU power step (kW)

# From miner coordination:
P_shed = Miner shed (kW)

# Net load for generator:
ΔP_net = P_gpu_step - P_shed

# Feed to ramp simulator:
Generator sees: ΔP_net kW step
```

**Example:**
- GPU wants: +500 kW
- Miners shed: -500 kW
- Generator sees: 0 kW (no ramp needed)

---

## Assumptions & Limitations

1. **Instantaneous Shedding:** Assumes miners can shed instantly (actual: 100-500ms)
2. **Full Unit Shutdown:** Assumes entire miner unit shuts down (no partial unit control)
3. **Constant Power:** Assumes miner power constant (actual: varies ±10% with temperature)
4. **Perfect Coordination:** Assumes perfect matching of GPU ramp and miner shed
5. **No Startup Coordination:** Only models shutdown/shedding, not startup
6. **Economic Model:** Simple opportunity cost model (doesn't account for BTC price volatility)

---

## References

- `data/miners/Whatsminer-Miner-Library.md` - Miner specifications
- `models/multistep-ramp-simulator/formulas.md` - Generator ramp formulas
- `models/generator-risk-calculator/formulas.md` - Generator risk formulas
- `docs/upstream-data-manuals/bitcoin-miners/` - Manufacturer manuals

---

**Last Updated:** 2025-12-02

