# GPU-TO-GENERATOR COMPATIBILITY MATRIX

**Version:** 1.0  
**Last Updated:** 2025-12-02  
**Status:** Working prototype

---

## Purpose

Quick reference guide mapping GPU cluster configurations to compatible generator models. Provides risk classifications and BESS requirements for each combination to enable rapid deployment planning and generator selection.

---

## Quick Start Guide

### Step 1: Identify Your GPU Configuration
- **GPU Count:** Number of GPUs in cluster
- **GPU Type:** H100 PCIe, H100 SXM, or A100 PCIe
- **Cluster Power:** Total power rating (GPU_Count × GPU_Power_per_Unit_kW)

### Step 2: Find Compatible Generators
Search the matrix for your GPU configuration and review compatible generator options.

### Step 3: Review Risk Classification
- **GREEN:** Safe operation - Generator can handle GPU load step
- **YELLOW:** Marginal - Close to limits, BESS recommended
- **RED:** Unsafe - Generator cannot handle GPU load step, BESS required

### Step 4: Check BESS Requirements
- **No-BESS:** Only viable for small clusters (≤4 GPUs) with fast-response generators
- **Buffer BESS:** 50-100 kW for ride-through and transient support
- **Grid-Forming BESS:** 400-600 kW for islanded operation or when generator cannot handle step

---

## Risk Level Interpretation

| Level | Meaning | Action |
|-------|---------|--------|
| **GREEN** | Safe operation | Generator can handle GPU load step. Proceed with configuration. Buffer BESS optional for ride-through. |
| **YELLOW** | Marginal - may require mitigation | Generator close to limits. Grid-forming BESS recommended for safety margin. |
| **RED** | Unsafe - exceeds limits | Generator cannot handle GPU load step. Grid-forming BESS required. |

---

## GPU Power Specifications

### H100 PCIe
- **Power per Unit:** 3.5 kW (350W TDP)
- **Typical Use:** Standard servers, air-cooled
- **Power Step:** 0.2-0.3 kW (idle to warmup)

### H100 SXM
- **Power per Unit:** 7.0 kW (700W TDP)
- **Typical Use:** High-throughput workloads, liquid-cooled
- **Power Step:** 0.4-0.6 kW (idle to warmup)

### A100 PCIe
- **Power per Unit:** 2.5 kW (250W TDP)
- **Typical Use:** Legacy/alternative option
- **Power Step:** 0.15-0.2 kW (idle to warmup)

**Source:** `data/gpu-profiles/GPU-Power-Profiles.md`

---

## Generator Load Acceptance Capabilities

### Natural Gas Generators

| Generator Type | Load Acceptance | Notes |
|----------------|-----------------|-------|
| **Fast-Response (G3520)** | 100% block load | Designed for data centers, 10s start-to-load |
| **CG260 Series** | 16% first step, then 13%, 10%, 9%... | Multi-step ramp, 10s recovery per step |
| **CG170 Series** | 10-20% per step | Ramped loading, 15s recovery |
| **Standard Natural Gas** | 25-35% | Conservative estimate, varies by model |
| **Lean-Burn** | 25-30% | Most restrictive |
| **Rich-Burn** | 40-50% | Better than lean-burn |

### Diesel Generators

| Generator Type | Load Acceptance | Notes |
|----------------|-----------------|-------|
| **Standard Diesel** | 50-80% | Use 70% for conservative design |
| **High-Performance Diesel** | 80-100% | Block load capable |

**Source:** `data/generators/caterpillar/Caterpillar-Technical-Analysis.md`

---

## Example Scenarios

### Scenario 1: Small Cluster (4 H100 PCIe)
- **Cluster Power:** 14 kW
- **Compatible Generators:**
  - ✅ G3520 Fast Response (2500 kW) - **GREEN** - No-BESS viable
  - ✅ G3516C Island Mode (1660 kW) - **GREEN** - Buffer BESS recommended
- **Recommendation:** Fast-response generator with proper controls. No-BESS viable.

### Scenario 2: Medium Cluster (16 H100 PCIe)
- **Cluster Power:** 56 kW
- **Compatible Generators:**
  - ✅ G3520 Fast Response (2500 kW) - **GREEN** - Buffer BESS
  - ✅ CG170-16 (1560 kW) - **GREEN** - Buffer BESS
- **Recommendation:** Multiple options available. Buffer BESS (50 kW) sufficient.

### Scenario 3: Large Cluster (64 H100 PCIe)
- **Cluster Power:** 224 kW
- **Compatible Generators:**
  - ✅ G3520 Fast Response (2500 kW) - **GREEN** - Buffer BESS
  - ✅ CG260-16 (4300 kW) - **GREEN** - Grid-Forming BESS (islanded)
  - ⚠️ CG170-16 (1560 kW) - **YELLOW** - Close to limits
- **Recommendation:** Fast-response generator preferred. Grid-forming BESS if islanded.

### Scenario 4: Very Large Cluster (142 H100 PCIe)
- **Cluster Power:** 497 kW
- **Compatible Generators:**
  - ✅ G3520 Fast Response (2500 kW) - **GREEN** - Buffer BESS
  - ⚠️ CG260-16 (4300 kW) - **YELLOW** - Multi-step required
  - ❌ CG170-16 (1560 kW) - **RED** - Cannot handle step
  - ❌ Standard Natural Gas (1000 kW) - **RED** - Cannot handle step
- **Recommendation:** Fast-response generator or CG260 with grid-forming BESS.

### Scenario 5: Massive Cluster (571 H100 PCIe)
- **Cluster Power:** 1998.5 kW
- **Compatible Generators:**
  - ⚠️ G3520 Fast Response (2500 kW) - **YELLOW** - Close to limits
  - ❌ CG260-16 (4300 kW) - **RED** - Cannot handle step
- **Recommendation:** Multiple generators in parallel or larger generator model. Grid-forming BESS required.

---

## BESS Requirements Summary

### No-BESS
- **When:** Small clusters (≤4 GPUs) with fast-response generators
- **Requirements:** Experienced control systems engineering team, high risk tolerance
- **Cost:** $0 (but engineering costs $68,000-$143,000)

### Buffer BESS (50-100 kW)
- **When:** Generator can handle GPU load step, or load sequencing available
- **Power:** 50-100 kW (20-40% of GPU cluster)
- **Energy:** 50-100 kWh (1-2 hours at power rating)
- **Cost:** $30,000-$60,000 installed
- **Vendor:** BYD Battery-Box LVL

### Grid-Forming BESS (400-600 kW)
- **When:** Generator cannot handle GPU load step, or islanded operation required
- **Power:** 400-600 kW (80-120% of load step gap)
- **Energy:** 100-200 kWh (sufficient for transient support)
- **Cost:** $350,000-$500,000 installed
- **Vendors:** Schneider Electric EcoStruxure, SMA Sunny Island, Dynapower MPS-125

**Source:** `models/bess-sizing/BESS-Sizing-v1.csv` and `research/bess-decision-analysis/BESS-DECISION-CONSOLIDATED-ANALYSIS.md`

---

## Limitations

**Current Version (v1) does NOT include:**
- Multi-generator parallel configurations
- Load sequencing effectiveness modeling
- Correlation factor variations (assumes worst-case C=1.0)
- Voltage dynamics (only power/frequency considered)
- Economic modeling (TCO, break-even analysis)
- Generator derating factors (altitude, temperature, fuel quality)
- MTU Series 4000, Cummins QSK, INNIO Jenbacher models (pending library expansion)

See: `docs/GAP_ANALYSIS.md` for planned enhancements

---

## Troubleshooting

### Common Issues

**Issue: Matrix shows RED but generator seems large enough**
- **Cause:** Check load acceptance percentage - this is critical parameter
- **Solution:** CG260 has only 16% first-step acceptance despite large rating. Multi-step ramp required.

**Issue: Matrix shows different results than BESS sizing calculator**
- **Cause:** Matrix uses conservative worst-case assumptions (C=1.0 correlation)
- **Solution:** Use BESS sizing calculator for detailed analysis with actual correlation factors.

**Issue: Generator model not in matrix**
- **Cause:** Matrix includes primary Caterpillar models. Other manufacturers pending.
- **Solution:** Use generator risk calculator (`models/generator-risk-calculator/`) for custom analysis.

### Getting Help

- **Generator Specs:** See `data/generators/caterpillar/` for complete generator data
- **GPU Profiles:** See `data/gpu-profiles/GPU-Power-Profiles.md` for GPU power characteristics
- **BESS Sizing:** See `models/bess-sizing/` for detailed BESS sizing calculator
- **Generator Risk:** See `models/generator-risk-calculator/` for detailed compatibility analysis
- **Gap Analysis:** See `docs/GAP_ANALYSIS.md` for known limitations

---

## References

- `docs/PRD.md` - Calculator requirements
- `data/generators/caterpillar/Caterpillar-Technical-Analysis.md` - Generator specifications
- `data/gpu-profiles/GPU-Power-Profiles.md` - GPU power characteristics
- `models/bess-sizing/BESS-Sizing-v1.csv` - BESS sizing calculator
- `models/generator-risk-calculator/GeneratorRisk-v1.csv` - Generator risk calculator
- `research/bess-decision-analysis/BESS-DECISION-CONSOLIDATED-ANALYSIS.md` - Decision framework
- `docs/GAP_ANALYSIS.md` - Known limitations
- `docs/GLOSSARY.md` - Standardized terminology

---

## Future Enhancements

Planned additions for v2:
- MTU Series 4000 models
- Cummins QSK series
- INNIO Jenbacher J-series
- PSI generator models
- Multi-generator parallel configurations
- Load sequencing effectiveness modeling
- Correlation factor variations
- Economic modeling (TCO comparison)
- Generator derating factors

