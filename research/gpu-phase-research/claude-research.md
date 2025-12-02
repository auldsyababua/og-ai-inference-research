# H100 PCIe Power Profile Validation for LLM Inference Workloads

**NVIDIA H100 PCIe GPUs draw 200-280W during LLM inference—well below their 350W TDP rating**—with idle power at 50-70W. This represents a validated foundation for off-grid generator stability modeling, though critical gaps remain in power ramp rate and multi-GPU correlation data.

Research across Hugging Face benchmarks, MLPerf submissions, academic papers, and technical documentation converges on a consistent finding: LLM inference is memory-bandwidth-bound, causing GPUs to operate at **60-80% of TDP** rather than near maximum. This contradicts TDP-based energy estimations, which can overestimate consumption by up to **4.1x** according to the ML.ENERGY benchmark study.

---

## Validated power parameters with high confidence

Empirical measurements from multiple independent sources provide strong validation for several target parameters. The table below synthesizes findings across Brookhaven National Laboratory PDU measurements, ServeTheHome hands-on testing, Scaleway production deployments, and academic power profiling studies.

| Parameter | Your Target | Validated Range | Confidence | Key Sources |
|-----------|-------------|-----------------|------------|-------------|
| **TDP (Max)** | 350W | 350W (310W config available) | ✅ HIGH | NVIDIA spec PB-11133-001 |
| **Idle Power** | 60-80W | **50-70W** | ✅ HIGH | ServeTheHome (68-70W), Scaleway (51W) |
| **Steady-State Inference** | 250-280W | **200-280W** | ✅ HIGH | ML.ENERGY, ServeTheHome CFD tests |
| **Model Loading** | 170-200W | **~150-200W (estimated)** | ⚠️ MEDIUM | Inferred from phase behavior |
| **Warmup** | 250-280W | **220-280W** | ✅ MEDIUM-HIGH | Consistent with prefill phase |
| **Peak Power** | ~350W | **310-350W** | ✅ HIGH | Approaches TDP only under stress |
| **Power Step (Idle→Inference)** | 0.2-0.25 kW | **0.15-0.23 kW** | ✅ HIGH | Measured deltas across sources |

The **idle power** target of 60-80W is slightly conservative. ServeTheHome measured **68-70W** during normal idle, while Scaleway documented **51W** with no active processes—suggesting actual idle draw may be **10-20% lower** than assumed. For generator sizing, using **60-70W idle** provides appropriate margin.

**Steady-state inference** at 250-280W aligns well with empirical data. ServeTheHome's CFD benchmarks showed **217W (FP32), 257W (FP16S), and 277W (FP16C)**—all within or slightly below the target range. The ML.ENERGY benchmark confirms LLM decoding operates at **40-70% of TDP** due to memory-bandwidth bottlenecks, while prefill phases briefly reach **70-85% of TDP**.

---

## Critical finding on measurement methodology

The nvidia-smi power reporting interface has significant limitations that affect power profiling accuracy. Research from the University of Oxford (arXiv:2312.02741) testing 10 H100 GPUs reveals a critical constraint: **nvidia-smi only samples 25% of GPU runtime**—capturing a 25ms window every 100ms. This means **75% of power activity goes unmeasured**, potentially missing transient spikes during phase transitions.

| nvidia-smi Parameter | Value | Implication |
|---------------------|-------|-------------|
| Averaging window (instant) | 25ms | Cannot capture sub-25ms transients |
| Update period | 100ms | Limits temporal resolution |
| Runtime sampled | **25%** | Misses majority of power events |
| Proportional error | ±5% | ±17.5W for 350W TDP |
| Rise time to steady-state | ~250ms | Phase transitions require this duration |

For generator stability modeling requiring accurate transient capture, **external power meters (PDU-level or Yokogawa-class analyzers) are strongly recommended** over nvidia-smi. The Brookhaven National Laboratory study used DCIM PDU metering and achieved consistent, validated measurements across 8-GPU nodes.

---

## Power ramp rates require reassessment

Your target of **3-4 kW/s per GPU** appears significantly higher than empirically measured rates. Based on the documented 250ms rise time (10-90% power transition), an H100 PCIe transitioning from 60W idle to 280W inference represents approximately:

**Calculated ramp rate:** (280W - 60W) ÷ 0.25s = **0.88 kW/s per GPU**

This is roughly **4x slower** than your assumed 3-4 kW/s. However, three factors may explain the discrepancy:

- **Multi-GPU synchronization:** When 8 GPUs start simultaneously, the aggregate ramp is 8× individual rate, creating **~7 kW/s for an 8-GPU system**
- **Transient spikes:** nvidia-smi's 25% sampling may miss instantaneous current inrush
- **Cold start vs warm transitions:** Initial power-on may exhibit faster ramps than workload transitions

For conservative generator design, maintain the **3-4 kW/s assumption** as a safety margin for synchronized multi-GPU startup scenarios, while recognizing typical operational ramps are closer to **0.8-1.5 kW/s per GPU**.

---

## Multi-GPU correlation data remains insufficient

No academic source provided direct measurements of power correlation coefficients (C) for H100 clusters. Your target range of **0.3-0.7** cannot be empirically validated. However, qualitative findings inform the estimate:

**Factors increasing correlation (toward 0.7+):**
- Tensor parallelism creates synchronized compute phases across GPUs
- Batch processing synchronizes memory access patterns
- Training workloads show "highly correlated power swings" per Microsoft Research

**Factors decreasing correlation (toward 0.3):**
- Pipeline parallelism introduces phase offsets between GPUs
- vLLM continuous batching creates asynchronous token generation
- Thermal throttling variations between GPUs

The Microsoft POLCA study notes that inference workloads show lower power correlation than training, suggesting **0.4-0.6 may be appropriate for LLM inference** while training clusters may reach 0.7-0.8. Without direct measurement data, this remains a **LOW confidence estimate**.

---

## LLM inference versus training power characteristics

A consistent finding across sources: LLM inference consumes **significantly less power than training**—typically **10-20% lower** for equivalent models. This stems from the memory-bound nature of autoregressive decoding.

| Workload Type | Typical Power (% of TDP) | Behavior |
|---------------|-------------------------|----------|
| LLM prefill (prompt processing) | 70-85% | Compute-intensive, higher power |
| LLM decode (token generation) | 40-70% | Memory-bound, lower sustained power |
| Diffusion models | 85-95% | Compute-intensive throughout |
| Training | 75-95% | Sustained high compute utilization |

The ML.ENERGY benchmark found that using TDP for energy estimation can cause **worst-case overestimation by 4.1×** (CodeGemma 2B on H100). For generator sizing, steady-state inference should be modeled at **70-80% of TDP**, not full TDP.

Brookhaven National Laboratory's 8-GPU H100 HGX node measurements showed maximum power draw of **8.48 kW**—only **83% of the rated 10.2 kW** even under 100% GPU utilization stress tests. This consistent "TDP headroom" pattern should factor into generator sizing calculations.

---

## Model and framework effects on power consumption

Power consumption varies meaningfully by inference framework and model architecture. The GitHub LLM-Inference-Engine-Benchmark (HotCarbon '25) documented the following for 8×H100 systems:

| Framework | Energy/Token | Peak Power (8-GPU) | Efficiency Ranking |
|-----------|--------------|-------------------|-------------------|
| **vLLM** | 37 mJ | 1382W | Most efficient |
| TensorRT-LLM | 91 mJ | 1003W | Lower peak, higher energy |
| DeepSpeed | 356 mJ | 1063W | Moderate |
| Transformers | 711 mJ | 1063W | Least efficient |

Higher peak power with vLLM correlates with better energy efficiency—the GPU runs at higher utilization for shorter duration. For generator stability, **vLLM workloads may produce larger but shorter power spikes** compared to less efficient frameworks.

Model architecture also matters: Llama-3 8B with Grouped Query Attention (GQA) achieves better **performance per watt** than Llama-2 7B with Multi-Head Self-Attention, despite similar model sizes.

---

## Refined power profile recommendations

Based on cross-validated findings, the following refined power profile is recommended for H100 PCIe LLM inference workloads:

| Phase | Original Estimate | Refined Estimate | Validation Status |
|-------|-------------------|------------------|-------------------|
| **Idle** | 60-80W | **55-70W** | VALIDATED (lower end) |
| **Model Loading** | 170-200W | **150-200W** | PARTIALLY VALIDATED |
| **Warmup/Prefill** | 250-280W | **240-300W** | VALIDATED (brief spikes) |
| **Steady-State Decode** | 250-280W | **200-260W** | VALIDATED |
| **Peak Transients** | — | **310-350W** | VALIDATED |
| **Power Step (Idle→Inference)** | 0.2-0.25 kW | **0.15-0.21 kW** | VALIDATED (slightly lower) |
| **Ramp Rate (per GPU)** | 3-4 kW/s | **0.8-1.5 kW/s typical; 3-4 kW/s burst** | NEEDS REVISION |
| **Correlation Coefficient** | 0.3-0.7 | **0.4-0.6 (inference)** | LOW CONFIDENCE |

---

## Generator sizing implications

For off-grid generator stability modeling with H100 PCIe inference clusters:

**Per-GPU power budgeting:**
- Minimum: 280W continuous capacity (80% of TDP)
- Recommended: 320W capacity for headroom
- Peak reserve: 350W for startup/burst events

**System-level considerations:**
- CPU, memory, cooling overhead: Add **200-400W per server**
- PSU efficiency losses: Apply **85-92% efficiency factor**
- 4×H100 PCIe server: Budget **2.0-2.5 kW** sustained, **3.0-3.5 kW** peak

**Transient response requirements:**
- Phase transition duration: **250-500ms**
- Synchronized startup (worst case): Prepare for **multi-kW/s ramps** at cluster scale
- Consider capacitive buffering or soft-start sequencing for generator protection

---

## Conclusion

This validation effort confirms your H100 PCIe power profile assumptions are **directionally correct with minor refinements needed**. Idle power runs slightly lower than assumed (50-70W vs 60-80W), steady-state inference is validated at 200-280W, and TDP specifications are accurate. The most significant revision involves **power ramp rates**, where per-GPU rates of 0.8-1.5 kW/s are more typical than the assumed 3-4 kW/s—though multi-GPU synchronization can still create high aggregate ramps requiring the conservative assumption.

Three gaps remain: (1) **direct model loading phase measurements** are unavailable, (2) **multi-GPU correlation coefficients** lack empirical validation, and (3) **nvidia-smi sampling limitations** may mask sub-25ms transients critical for generator protection. For highest-fidelity modeling, external PDU-level power monitoring during actual inference workloads would provide the definitive dataset.