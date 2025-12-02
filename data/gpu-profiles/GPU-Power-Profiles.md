# GPU POWER PROFILES - DOCUMENTATION

**Version:** 1.0  
**Last Updated:** 2025-12-01  
**Status:** Modeling profiles based on research and manufacturer specifications

---

## Purpose

This document consolidates GPU power characteristics for H100 (PCIe and SXM) based on research findings and manufacturer specifications. **These are modeling assumptions** suitable for construction planning and partner selection. Empirical validation with real-world measurements is planned for future phases but is not required for current planning purposes.

---

## H100 PCIe Power Specifications

### Manufacturer Specifications

| Parameter | Value | Source |
|-----------|-------|--------|
| **TDP (Total Board Power)** | 350 W (default/maximum) | NVIDIA official specs |
| **Power Mode (300W sense-pin)** | 310 W (down-rated) | NVIDIA official specs |
| **Memory** | 80GB HBM2e | NVIDIA official specs |
| **Memory Bandwidth** | 2.0 TB/s | NVIDIA official specs |

### Power Profile (Inference Workloads) - Modeling Assumptions

**Status:** ✅ **MODELING ASSUMPTIONS** - Based on manufacturer specs and research literature, suitable for planning purposes

| Phase | Estimated Power | Duration | Notes |
|-------|----------------|----------|-------|
| **Idle** | 30-60 W | Continuous | Estimated from SXM scaling; needs measurement |
| **Launch** | 100-150 W | 1-5 s | Job initialization, resource allocation |
| **Model Load** | 200-300 W | 10-60 s | Loading neural network weights into GPU memory |
| **Warmup** | 300-350 W | 5-30 s | Initial inference passes to stabilize performance |
| **Steady-State Inference** | 250-350 W | Continuous | Sustained inference at full utilization |
| **Cleanup** | 150-200 W | 1-5 s | De-allocation of resources |
| **Teardown** | 50-100 W | 1-3 s | Final shutdown, return to idle |

### Power Step Estimates

| Transition | ΔP (per GPU) | Transition Time | Notes |
|-----------|--------------|-----------------|-------|
| Idle → Launch | 50-120 W | 50-500 ms | Sharp step |
| Launch → Model Load | 100-200 W | 1-10 s | Gradual ramp |
| Model Load → Warmup | 50-100 W | 1-5 s | Moderate step |
| Warmup → Inference | 0-50 W | 1-10 s | Stabilization |
| Inference → Cleanup | -100 to -200 W | 50-500 ms | Sharp drop |
| Cleanup → Idle | -50 to -150 W | 50-500 ms | Moderate drop |

**Key Assumption:** Per-GPU power step during warmup phase: **0.6 kW** (used in calculator scenarios)

---

## H100 SXM Power Specifications

### Manufacturer Specifications

| Parameter | Value | Source |
|-----------|-------|--------|
| **TDP (Total Board Power)** | 700 W (maximum) | NVIDIA official specs |
| **Memory** | 80GB HBM3 | NVIDIA official specs |
| **Memory Bandwidth** | 3.35 TB/s | NVIDIA official specs |

### Power Profile (Inference Workloads) - Modeling Assumptions

**Status:** ✅ **MODELING ASSUMPTIONS** - Based on PCIe estimates scaled by TDP ratio (2:1), suitable for planning

| Phase | Estimated Power | Duration | Notes |
|-------|----------------|----------|-------|
| **Idle** | 60-120 W | Continuous | Estimated (2× PCIe idle) |
| **Launch** | 200-300 W | 1-5 s | Job initialization |
| **Model Load** | 400-600 W | 10-60 s | Loading weights |
| **Warmup** | 600-700 W | 5-30 s | Initial inference passes |
| **Steady-State Inference** | 500-700 W | Continuous | Sustained inference |
| **Cleanup** | 300-400 W | 1-5 s | De-allocation |
| **Teardown** | 100-200 W | 1-3 s | Final shutdown |

### Power Step Estimates

| Transition | ΔP (per GPU) | Transition Time | Notes |
|-----------|--------------|-----------------|-------|
| Idle → Launch | 100-240 W | 50-500 ms | Sharp step |
| Launch → Model Load | 200-400 W | 1-10 s | Gradual ramp |
| Model Load → Warmup | 100-200 W | 1-5 s | Moderate step |
| Warmup → Inference | 0-100 W | 1-10 s | Stabilization |
| Inference → Cleanup | -200 to -400 W | 50-500 ms | Sharp drop |
| Cleanup → Idle | -100 to -300 W | 50-500 ms | Moderate drop |

**Key Assumption:** Per-GPU power step during warmup phase: **1.2 kW** (2× PCIe, used in calculator scenarios)

---

## Cluster-Level Power Dynamics

### Correlation Coefficients

**Status:** ✅ **MODELING ASSUMPTIONS** - Based on research findings, suitable for planning and risk assessment

| Scenario | Estimated Correlation (C) | Notes |
|----------|--------------------------|-------|
| **Synchronous Warmup** | 0.7-0.9 | Many GPUs starting simultaneously (worst case) |
| **Staggered Launch** | 0.3-0.5 | Scheduler spreads transitions over time |
| **Random Workloads** | 0.1-0.3 | Independent job scheduling |
| **Batch Inference** | 0.5-0.7 | Similar workloads scheduled together |

**Current Calculator Assumption:** C = 0.8 for worst-case scenarios

### Cluster Power Step Calculation

```
ΔP_cluster = C × N × ΔP_gpu
```

**Example:**
- 1024 GPUs × 0.6 kW × 0.8 correlation = **491.52 kW** cluster step

### Ramp Rate Calculation

```
RampRate = ΔP_cluster / Δt_event
```

**Example:**
- 491.52 kW ÷ 1 s = **491.52 kW/s** ramp rate

---

## Measurement Limitations

### nvidia-smi / NVML Limitations

**Critical Finding:** nvidia-smi under-samples power on A100 and H100 GPUs:

- **Sampling Rate:** Only 25% of runtime is sampled
- **Sampling Window:** 25 ms window every 100 ms
- **Impact:** Fast transients (<100 ms) are not accurately captured
- **Implication:** Cannot rely on nvidia-smi for sub-second power transients relevant to generator stability

### Recommended Measurement Approach

**For accurate power profiling:**
1. **External Power Meter:** Yokogawa WT5000 or similar (<10 ms sampling)
2. **Phase-Shifting Techniques:** Micro-benchmarking to recover accurate short-term statistics
3. **Multiple Measurement Points:** Node-level, rack-level, and cluster-level monitoring
4. **Validation:** Cross-reference with nvidia-smi for steady-state values only

---

## Research Findings Summary

### From GPU-Generator Stability Research

1. **Training vs Inference:**
   - Training workloads: ~76% of rated node TDP on average
   - Inference workloads: Estimated 50-80% of TDP depending on utilization
   - **Pattern:** Real workloads rarely sustain 100% of TDP over long windows

2. **Power Fluctuations:**
   - Large GPU clusters can cause "power fluctuations of hundreds of megawatts within only seconds"
   - Per-rack power can range from 30 to 100+ kW with abrupt changes
   - Workloads are bursty and hard to predict, especially in interactive inference

3. **Scheduler Impact:**
   - Schedulers often co-schedule similar work on many GPUs (increases correlation)
   - Queueing effects and cooling-aware scheduling can desynchronize activity
   - Without mitigation, large correlated ramps are realistic

---

## Future Validation (Post-Construction)

### Planned Empirical Validation

**Note:** These measurements are planned for future validation phases after construction. Current modeling assumptions are sufficient for planning and partner selection.

| Parameter | Current Modeling Assumption | Future Validation Method |
|-----------|----------------------------|-------------------------|
| **H100 PCIe idle power** | 30-60W (estimated) | External power meter (Yokogawa WT5000) |
| **H100 PCIe power step** | 0.6 kW (estimated) | Characterize actual idle→full load transition |
| **Model loading power transient** | 200-300W (estimated) | Characterize specific models (Llama, Mistral, etc.) |
| **Multi-GPU correlation** | 0.3-0.7 (estimated) | Measure cluster-level power during inference |
| **Ramp rates (kW/s)** | 3-4 kW/s per GPU (estimated) | External metering with <10ms sampling |

### Future Measurement Plan

1. **Deploy external power metering** on H100 systems post-construction
2. **Measure power profiles** for:
   - Idle state
   - Model load phase
   - KV-cache warmup
   - Steady decode
   - Batch-size changes
3. **Compute empirical correlation coefficients** across GPUs and nodes
4. **Validate nvidia-smi limitations** with external metering
5. **Refine modeling assumptions** based on empirical data

---

## Usage in Calculator

### Current Calculator Assumptions

The generator risk calculator uses these estimated values:

| Parameter | Value Used | Source |
|-----------|-----------|--------|
| **ΔP_gpu (PCIe)** | 0.6 kW | Estimated warmup power step |
| **ΔP_gpu (SXM)** | 1.2 kW | Estimated warmup power step (2× PCIe) |
| **Correlation (C)** | 0.8 | Worst-case synchronous warmup |
| **Transition Time (Δt)** | 1-30 s | Varies by scenario |

### Calculator Scenarios

**Scenario 1: G3520 Fast Response + GPU Warmup**
- 1024 GPUs × 0.6 kW × 0.8 correlation = 491.52 kW
- G3520 (4000 kW, 100% block load capable)
- Result: **GREEN** - 12.3% step, well within limits

**Scenario 2: CG260-16 + GPU Warmup**
- Same GPU configuration (491.52 kW)
- CG260 (4300 kW, 16% max first step)
- Result: **GREEN** - 11.4% step, within first step limit

---

## References

1. **NVIDIA H100 Specifications:** Official NVIDIA datasheets
2. **GPU-Generator Stability Research:** `research/gpu-generator-stability/GPU-GENERATOR-STABILITY-CONSOLIDATED-ANALYSIS.md`
3. **Perplexity Research Findings:** `research/gpu-generator-stability/perplexity-research/research-findings.md`
4. **Remaining Research Gaps:** `research/REMAINING-RESEARCH-GAPS.md`

---

## Next Steps

1. **Obtain hardware access** for H100 PCIe systems
2. **Deploy external power metering** (Yokogawa WT5000 or equivalent)
3. **Measure empirical power profiles** for all phases
4. **Update this document** with validated measurements
5. **Refine calculator assumptions** based on empirical data

---

**Document Status:** Modeling profiles documented based on research and manufacturer specifications. Suitable for construction planning and partner selection. Empirical validation planned for post-construction validation phases.

