# H100 Economics Research - Consolidated Bibliography

**Purpose**: Master reference list consolidating all sources from 4 H100 economics research reports
**Date**: 2025-12-01
**Total Unique Sources**: 62 (55 from ECONOMICS-Q4 + 9 unique from PRICING-DOCX + 3 newly added: MLPerf [56], Argonne LLM-Inference-Bench [57], Meta TCO [58])

---

## Source Attribution by Document

- **ECONOMICS-Q4**: H100-PCIe-vs-SXM-Economics-Q4-2025.md [55 citations]
- **PRICING-DOCX**: H100-PCIe-vs-SXM-Pricing-Q4-2025.docx [58 citations → 9 unique sources with multiple citation numbers]
- **PRICING-PUZZLE**: GPU Inference Economics: The PCIe vs SXM H100 Pricing Puzzle.md [No citations]
- **STRATEGIC**: Strategic-Infrastructure-Analysis-H100.md [No citations]

---

## Category A: Hardware Specifications & Benchmarks

### GPU Architecture & Specifications
[1] Clarifai - NVIDIA H100: Price, Specs, Benchmarks & Decision Guide
https://www.clarifai.com/blog/nvidia-h100
**Used by**: PRICING-DOCX [citations 14, 28, 29, 50, 52, 58]

[2] Hyperstack - Comparing NVIDIA H100 PCIe vs SXM Performance, Use Cases and More
https://www.hyperstack.cloud/technical-resources/performance-benchmarks/comparing-nvidia-h100-pcie-vs-sxm-performance-use-cases-and-more
**Used by**: ECONOMICS-Q4 [citation 2]

[8] Arc Compute - NVIDIA H100 PCIe vs SXM5 Form Factors
https://www.arccompute.io/arc-blog/nvidia-h100-pcie-vs-sxm5-form-factors-which-gpu-is-right-for-your-company
**Used by**: ECONOMICS-Q4 [citation 8]

[22] NVIDIA Official - H100 Tensor Core GPU
https://www.nvidia.com/en-us/data-center/h100/
**Used by**: ECONOMICS-Q4 [citation 22]

[23] AceCloud - NVIDIA B200 vs H200, H100, A100
https://acecloud.ai/blog/nvidia-b200-vs-h200-h100-a100/
**Used by**: ECONOMICS-Q4 [citation 23]

[34] RunPod - H100 PCIe vs H100 SXM GPU Comparison
https://www.runpod.io/gpu-compare/h100-pcie-vs-h100-sxm
**Used by**: ECONOMICS-Q4 [citation 34], PRICING-DOCX [citations 19, 20, 24, 25]

[38] Verda - PCIe and SXM5 Comparison
https://verda.com/blog/pcie-and-sxm5-comparison
**Used by**: ECONOMICS-Q4 [citation 38]

### Performance Benchmarks
[3] Cudo Compute - Real-World GPU Benchmarks
https://www.cudocompute.com/blog/real-world-gpu-benchmarks
**Used by**: ECONOMICS-Q4 [citation 3]

[35] GitHub - llama.cpp Discussion: H100 PCIe vs SXM Performance
https://github.com/ggml-org/llama.cpp/discussions/8511
**Used by**: ECONOMICS-Q4 [citation 35], PRICING-DOCX [citations 21, 26, 47]

[36] Lambda Labs - NVIDIA H100 GPU Deep Learning Performance Analysis
https://lambda.ai/blog/nvidia-h100-gpu-deep-learning-performance-analysis
**Used by**: ECONOMICS-Q4 [citation 36]

[37] Hyperstack - NVLink vs PCIe: What's the Difference for AI Workloads
https://www.hyperstack.cloud/blog/case-study/nvlink-vs-pcie-whats-the-difference-for-ai-workloads
**Used by**: ECONOMICS-Q4 [citation 37]

[39] NVIDIA Forums - Computation vs Memory Bound Inference Workloads
https://forums.developer.nvidia.com/t/how-to-accurately-determine-if-a-deep-learning-inference-workload-is-computation-bound-or-memory-bound-on-an-nvidia-gpu/342690
**Used by**: ECONOMICS-Q4 [citation 39]

[40] Hyperstack - LLM Inference Benchmark: A100 NVLink vs H100 SXM
https://www.hyperstack.cloud/technical-resources/performance-benchmarks/llm-inference-benchmark-comparing-nvidia-a100-nvlink-vs-nvidia-h100-sxm
**Used by**: ECONOMICS-Q4 [citation 40]

[41] Baseten - Double Inference Speed with NVIDIA H100 GPUs
https://www.baseten.co/resources/changelog/double-inference-speed-and-throughput-with-nvidia-h100-gpus/
**Used by**: ECONOMICS-Q4 [citation 41]

[56] MLCommons - MLPerf Inference Benchmark Results
https://mlcommons.org/en/inference-datacenter/
**Used by**: PRICING-PUZZLE (cited for 2.6x multi-GPU advantage on Llama 2 70B)
**Note**: Official MLPerf Inference benchmark results showing H100 SXM vs PCIe performance on Llama 2 70B. Results available in v5.0 and v5.1 rounds. Specific 2.6x claim referenced by multiple documents but exact submission page pending verification.

[57] Argonne National Laboratory - LLM-Inference-Bench
https://github.com/argonne-lcf/LLM-Inference-Bench
**Used by**: PRICING-PUZZLE (cited for 39x batch scaling improvement on Llama 3 70B)
**Note**: Comprehensive benchmarking suite evaluating LLM inference performance across diverse AI accelerators. Documents H100's 39x throughput improvement when batch size increases from 1 to 64 on Llama-3-70B, compared to 3x improvement on A100.

### GPU Comparisons (H100 vs A100)
[22] OpenMetal - Comparing NVIDIA H100 vs A100 GPUs for AI Workloads
https://openmetal.io/resources/blog/nvidia-h100-vs-a100-gpu-comparison/
**Used by**: PRICING-DOCX [citations 22, 23, 30]

[37] Ori - Choosing between NVIDIA H100 vs A100 - Performance and Costs
https://www.ori.co/blog/choosing-between-nvidia-h100-vs-a100-performance-and-costs-considerations
**Used by**: PRICING-DOCX [citation 37]

[52] Northflank - H100 vs H200
https://northflank.com/blog/h100-vs-h200
**Used by**: ECONOMICS-Q4 [citation 52]

### Interconnect Technology
[24] Exxact Corp - SXM vs PCIe: GPUs Best for Training LLMs
https://www.exxactcorp.com/blog/deep-learning/sxm-vs-pcie-gpus-best-for-training-llms-like-gpt-4
**Used by**: ECONOMICS-Q4 [citation 24], PRICING-DOCX [citations 6, 13, 31, 32, 48, 49, 55]

[25] NVIDIA Official - NVLink Technology
https://www.nvidia.com/en-us/data-center/nvlink/
**Used by**: ECONOMICS-Q4 [citation 25]

[26] Intuition Labs - NVIDIA NVLink GPU Interconnect
https://intuitionlabs.ai/articles/nvidia-nvlink-gpu-interconnect
**Used by**: ECONOMICS-Q4 [citation 26]

---

## Category B: Pricing & Market Analysis

### GPU Purchase Costs & Pricing Trends
[4] Jarvislabs.ai - H100 Price Guide 2025
https://docs.jarvislabs.ai/blog/h100-price
**Used by**: ECONOMICS-Q4 [citation 4], PRICING-DOCX [citations 4, 5, 7, 8, 9, 10, 11, 12, 15, 16, 17, 18, 27, 38, 39, 40, 41, 42, 51, 53, 54, 56, 57]

[5] Northflank - How Much Does an NVIDIA H100 GPU Cost?
https://northflank.com/blog/how-much-does-an-nvidia-h100-gpu-cost
**Used by**: ECONOMICS-Q4 [citation 5], PRICING-DOCX [citations 1, 2, 3, 44, 45, 46]

[6] Cyfuture Cloud - NVIDIA H100 Server Price 2025: Updated Cost Breakdown
https://cyfuture.cloud/kb/gpu/nvidia-h100-server-price-2025-updated-cost-breakdown
**Used by**: ECONOMICS-Q4 [citation 6]

[7] GMI Cloud - How Much Does the NVIDIA H100 GPU Cost in 2025? Buy vs Rent Analysis
https://www.gmicloud.ai/blog/how-much-does-the-nvidia-h100-gpu-cost-in-2025-buy-vs-rent-analysis
**Used by**: ECONOMICS-Q4 [citation 7]

### Cloud GPU Provider Pricing
[9] Lambda Labs - Pricing
https://lambda.ai/pricing
**Used by**: ECONOMICS-Q4 [citation 9]

[10] Thunder Compute - CoreWeave GPU Pricing Review
https://www.thundercompute.com/blog/coreweave-gpu-pricing-review
**Used by**: ECONOMICS-Q4 [citation 10]

[11] Hyperstack - Best Cloud GPU Providers for AI
https://www.hyperstack.cloud/blog/case-study/best-cloud-gpu-providers-for-ai
**Used by**: ECONOMICS-Q4 [citation 11]

[12] Uvation - CoreWeave H100 Pricing: How Does It Stack Up?
https://uvation.com/articles/coreweave-h100-pricing-how-does-it-stack-up-against-other-cloud-gpu-providers
**Used by**: ECONOMICS-Q4 [citation 12]

[13] Intuition Labs - H100 Rental Prices: A Cloud Cost Comparison (Nov 2025)
https://intuitionlabs.ai/pdfs/h100-rental-prices-a-cloud-cost-comparison-nov-2025.pdf
**Used by**: ECONOMICS-Q4 [citation 13]

[33] Thunder Compute - NVIDIA H100 Pricing (September 2025): Cheapest On-Demand Cloud GPU Rates
https://www.thundercompute.com/blog/nvidia-h100-pricing
**Used by**: PRICING-DOCX [citations 33, 34, 35, 36, 43]

[42] Hyperbolic - GPU Cloud Pricing
https://www.hyperbolic.ai/blog/gpu-cloud-pricing
**Used by**: ECONOMICS-Q4 [citation 42]

[43] GetDeploying - Lambda Labs Review
https://getdeploying.com/lambda-labs
**Used by**: ECONOMICS-Q4 [citation 43]

[44] RunPod - Top Cloud GPU Providers
https://www.runpod.io/articles/guides/top-cloud-gpu-providers
**Used by**: ECONOMICS-Q4 [citation 44]

[45] GetDeploying - CoreWeave Review
https://getdeploying.com/coreweave
**Used by**: ECONOMICS-Q4 [citation 45]

[46] Fireworks.ai - Pricing
https://fireworks.ai/pricing
**Used by**: ECONOMICS-Q4 [citation 46]

[47] DeepInfra - Pricing
https://deepinfra.com/pricing
**Used by**: ECONOMICS-Q4 [citation 47]

[48] Codingscape - Best AI Cloud Providers for LLMs Apps Compute
https://codingscape.com/blog/best-ai-cloud-providers-for-llms-apps-compute
**Used by**: ECONOMICS-Q4 [citation 48]

### Neo-Cloud Market Analysis
[14] SemiAnalysis - Neo-Clouds Tag
https://semianalysis.com/tag/neoclouds/
**Used by**: ECONOMICS-Q4 [citation 14]

[15] dstack.ai - State of Cloud GPU 2025
https://dstack.ai/blog/state-of-cloud-gpu-2025/
**Used by**: ECONOMICS-Q4 [citation 15]

[16] SemiAnalysis Newsletter - GPU Cloud ClusterMAX Rating System
https://newsletter.semianalysis.com/p/the-gpu-cloud-clustermax-rating-system-how-to-rent-gpus
**Used by**: ECONOMICS-Q4 [citation 16]

[17] McKinsey - The Evolution of Neoclouds and Their Next Moves
https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/the-evolution-of-neoclouds-and-their-next-moves
**Used by**: ECONOMICS-Q4 [citation 17]

[18] Thunder Compute - Neoclouds: The New GPU Clouds Changing AI Infrastructure
https://www.thundercompute.com/blog/neoclouds-the-new-gpu-clouds-changing-ai-infrastructure
**Used by**: ECONOMICS-Q4 [citation 18]

[19] SemiAnalysis Newsletter - GPU Cloud Economics Explained
https://newsletter.semianalysis.com/p/gpu-cloud-economics-explained-the
**Used by**: ECONOMICS-Q4 [citation 19]

[20] SemiAnalysis Newsletter - ClusterMAX 2.0: The Industry Standard
https://newsletter.semianalysis.com/p/clustermax-20-the-industry-standard
**Used by**: ECONOMICS-Q4 [citation 20]

[21] Tech Gov Intelligence - Observations About LLM Inference Pricing
https://techgov.intelligence.org/blog/observations-about-llm-inference-pricing
**Used by**: ECONOMICS-Q4 [citation 21]

[27] SemiAnalysis Newsletter - AI Neocloud Playbook and Anatomy
https://newsletter.semianalysis.com/p/ai-neocloud-playbook-and-anatomy
**Used by**: ECONOMICS-Q4 [citation 27]

---

## Category C: Infrastructure & Operations

### Data Center Infrastructure
[28] Data Center Knowledge - Data Center Cooling Methods: Costs vs Efficiency vs Sustainability
https://www.datacenterknowledge.com/cooling/data-center-cooling-methods-costs-vs-efficiency-vs-sustainability
**Used by**: ECONOMICS-Q4 [citation 28]

[29] Creative Endeavor B2B - Data Center Cooling Special Report
https://creative.endeavorb2b.com/ClientMarketing/processing/DCF-5789_HYPERTEC-002-Special-Report_FINAL.pdf
**Used by**: ECONOMICS-Q4 [citation 29]

[30] Lawrence Berkeley National Laboratory - United States Data Center Energy Usage Report (2024)
https://eta-publications.lbl.gov/sites/default/files/2024-12/lbnl-2024-united-states-data-center-energy-usage-report_1.pdf
**Used by**: ECONOMICS-Q4 [citation 30]

[31] Solar Tech Online - How Much Electricity Do Data Centers Use?
https://solartechonline.com/blog/how-much-electricity-data-center-use-guide/
**Used by**: ECONOMICS-Q4 [citation 31]

[53] Bloomberg - Data Centers Cut Energy Use by Submerging Servers in Liquid
https://www.bloomberg.com/news/features/2025-06-18/data-centers-cut-energy-use-by-submerging-servers-in-liquid
**Used by**: ECONOMICS-Q4 [citation 53]

### Energy & Power Considerations
[54] Trellis - Data Center Demand: Electricity Prices Soaring
https://trellis.net/article/data-center-demand-electricity-prices-soaring/
**Used by**: ECONOMICS-Q4 [citation 54]

[55] Secure Solar Futures - Data Centers Really Do Raise Energy Prices
https://securesolarfutures.com/data-centers-really-do-raise-energy-prices/
**Used by**: ECONOMICS-Q4 [citation 55]

---

## Category D: Total Cost of Ownership & Lifecycle

### TCO Analysis & Methodology
[32] ANSYS - Understanding Total Cost of Ownership for HPC/AI Systems
https://www.ansys.com/blog/understanding-total-cost-ownership-hpc-ai-systems
**Used by**: ECONOMICS-Q4 [citation 32]

[33] WhiteFiber - Understanding GPU Lifecycle
https://www.whitefiber.com/blog/understanding-gpu-lifecycle
**Used by**: ECONOMICS-Q4 [citation 33]

[58] Meta AI Infrastructure TCO Analysis (Referenced)
**Primary Source**: Pending verification
**Cited by**: PRICING-PUZZLE (references Meta's 24,576 GPU infrastructure analysis)
**Claim**: $1.49-$1.70/GPU-hour TCO over 4-year lifecycle for hyperscale deployment
**Note**: This analysis is referenced in PRICING-PUZZLE but the primary source (Meta engineering blog, investor presentation, or technical publication) has not been located. May be from Meta's internal infrastructure documentation, SemiAnalysis coverage of Meta deployments, or Meta earnings calls discussing GPU economics. Requires further research to locate exact source.

### GPU Depreciation & Lifespan
[49] Tom's Hardware - Datacenter GPU Service Life Can Be Surprisingly Short
https://www.tomshardware.com/pc-components/gpus/datacenter-gpu-service-life-can-be-surprisingly-short-only-one-to-three-years-is-expected-according-to-unnamed-google-architect
**Used by**: ECONOMICS-Q4 [citation 49]

[50] LinkedIn Post - Average Useful Lifespan of NVIDIA GPU
https://www.linkedin.com/posts/richjester_the-average-useful-lifespan-of-an-nvidia-activity-7394892794613362688-TJiQ
**Used by**: ECONOMICS-Q4 [citation 50]

[51] Business Insider - AI Bubble Argument Wrong: GPUs NVIDIA Depreciation Data Centers
https://www.businessinsider.com/ai-bubble-argument-wrong-gpus-nvidia-depreciation-data-centers-crusoe-2025-11
**Used by**: ECONOMICS-Q4 [citation 51]

---

## Coverage Analysis by Category

| Category | ECONOMICS-Q4 | PRICING-DOCX | Overlap | Total Unique |
|----------|-------------|-------------|---------|--------------|
| Hardware Specs & Benchmarks | 18 sources | 5 sources | 3 sources | 20 |
| Pricing & Market Analysis | 24 sources | 3 sources | 2 sources | 25 |
| Infrastructure & Operations | 7 sources | 0 sources | 0 sources | 7 |
| TCO & Lifecycle | 6 sources | 1 source | 0 sources | 7 |
| **TOTAL** | **55** | **9** | **5** | **59 unique** |

---

## Source Quality Assessment

### Primary Sources (First-Party Data)
- NVIDIA Official Documentation [citations 22, 25]
- Lambda Labs Pricing [citation 9]
- Cloud Provider Pricing Pages [citations 42, 46, 47]

### Industry Analysis (High Authority)
- SemiAnalysis Newsletter [citations 14, 16, 19, 20, 27]
- McKinsey Analysis [citation 17]
- Lawrence Berkeley National Lab Energy Report [citation 30]
- Bloomberg Reporting [citation 53]

### Technical Benchmarks (Empirical Data)
- Lambda Labs Performance Analysis [citation 36]
- Hyperstack Benchmarks [citations 2, 37, 40]
- Baseten Performance Data [citation 41]
- Cudo Compute Benchmarks [citation 3]
- GitHub Community Benchmarks [citation 35]

### Cloud Provider Comparisons (Aggregated Data)
- Intuition Labs Cost Comparison [citation 13]
- Thunder Compute Reviews [citations 10, 18, 33]
- Jarvislabs.ai Price Guide [citation 4]
- Northflank Cost Analysis [citation 5]
- RunPod Comparisons [citations 34, 44]

### Technical Explainers (Educational)
- Clarifai H100 Guide [citation 1]
- Exxact Corp SXM vs PCIe [citation 24]
- Arc Compute Form Factors [citation 8]
- Verda Comparison [citation 38]
- Intuition Labs NVLink [citation 26]

---

## Citation Coverage by Topic in Consolidated Report

### Section 1: Perfect Agreements
- **Hardware Specifications**: Verified by [1, 2, 8, 22, 34, 38] + PRICING-DOCX sources
- **Acquisition Costs**: Verified by [4, 5, 6, 7] + PRICING-DOCX sources
- **Operational Costs**: Verified by [28, 29, 30, 31]
- **Market Pricing**: Verified by [9, 10, 11, 12, 13, 14, 15, 42, 43, 44, 45, 46, 47, 48] + PRICING-DOCX sources
- **Performance**: Verified by [3, 35, 36, 37, 39, 40, 41] + PRICING-DOCX benchmarks
- **TCO**: Verified by [32, 33, 49, 50, 51]

### Section 3: Critical Disagreements
- **Break-even utilization**: SemiAnalysis [14, 16, 19, 20] vs case studies [PRICING-DOCX]
- **Multi-GPU advantage**: MLPerf claims vs community benchmarks [35, 40]
- **Cost floor**: Meta analysis vs mid-scale TCO [4, 5, 6, 7, 32]

### Section 6: Data Gaps
- **Power conditioning**: No sources address off-grid generator integration
- **Fuel logistics**: No sources model natural gas fuel costs
- **Thermal management**: [28, 29, 53] address data center cooling, not off-grid containers
- **Network latency**: No sources address Starlink impact on inference serving

---

## Recommended Additional Sources (Not in Original Documents)

For completing off-grid AI inference research, the following source types are needed:

1. **Generator-Grid Stability**:
   - IEEE standards for frequency regulation
   - Caterpillar technical manuals (in project data/)
   - Power systems engineering textbooks (droop control, RoCoF)

2. **Battery Energy Storage Systems**:
   - BESS manufacturers' technical specs
   - Grid-scale battery response time data
   - BESS cost per kWh and per kW ratings

3. **Natural Gas Infrastructure**:
   - Industrial natural gas pricing data
   - Fuel logistics cost models
   - Pipeline vs LNG delivery economics

4. **Edge Computing**:
   - Starlink latency profiles for inference serving
   - Edge data center thermal management case studies
   - Container-based GPU deployment guides

5. **GPU Power Characterization**:
   - NVIDIA power management documentation
   - Empirical GPU cluster power draw traces
   - Correlation studies of multi-GPU power consumption

---

## Document Metadata

**Created**: 2025-12-01
**Purpose**: Consolidated bibliography for H100 economics research
**Status**: Complete for existing documents; additional sources needed for off-grid integration
**Next Action**: Extract Caterpillar generator citations from technical library documents

**Total Sources Documented**: 62 unique sources (59 original + 3 newly added)
**Citation Count**: 113 total citations (with duplicates)
**Coverage**: Hardware (34%), Economics (42%), Infrastructure (12%), TCO (12%)
