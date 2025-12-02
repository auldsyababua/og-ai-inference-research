# Deep Research Prompt: Inference Workload Taxonomy & Market Analysis

**Project:** Off-Grid AI Inference Research  
**Date:** 2025-12-02  
**Purpose:** Comprehensive research on inference workload types, hardware requirements, latency classifications, and market sizing  
**Research Agent:** Deep research agent (Claude, GPT, Gemini, Perplexity)  
**Expected Output:** Detailed markdown report with citations

---

## Research Clarifications

### 1. Geographic Scope for Market Data

**Priority:** **Global market data** with **US focus** where regional breakdowns are available.

**Rationale:**
- Off-grid deployments can be located anywhere globally
- US market data is most readily available and serves as baseline
- Include regional variations (APAC, Europe) when data is available
- **Format:** Present as "Global: $X B, US: $Y B, APAC: $Z B" or similar

**Recommendation:** Prioritize global data, but include US-specific breakdowns when available. If global data unavailable, use US data and note as "US market, global estimate unavailable."

---

### 2. Hardware Vendor Focus

**Primary Focus:** **NVIDIA GPUs** (H100 PCIe, H100 SXM, A100, L4, T4, etc.)

**Secondary Coverage:** Include alternatives for completeness, but prioritize NVIDIA:
- **AMD:** MI300X, MI250X (if relevant data available)
- **Intel:** Gaudi 2, Gaudi 3 (if relevant data available)
- **Custom ASICs:** Google TPU, AWS Trainium/Inferentia (brief mention, not primary focus)

**Rationale:**
- Project is focused on NVIDIA H100 deployments (PCIe and SXM)
- NVIDIA dominates inference market (>90% market share)
- Alternative vendors can be mentioned but don't require deep analysis

**Recommendation:** Focus **80% on NVIDIA**, **20% on alternatives** (brief comparison where relevant). If alternative vendor data is sparse, that's acceptable - prioritize NVIDIA completeness.

---

### 3. Output Format

**Deliverables:**

1. **Primary Report:** `research-findings.md` (Markdown format)
   - Comprehensive analysis (40-60 pages)
   - All sections completed
   - Citations throughout
   - Embedded tables and matrices

2. **Hardware Requirement Matrix:** 
   - **Embedded in report** (Section 5)
   - **Standalone CSV:** `hardware-requirement-matrix.csv`
   - Columns: Workload, Latency, GPU Model, Interconnect, VRAM, Power, SXM Required?, NVLink Required?, Market Size (2025), CAGR, Market Size (2030)

3. **Market Summary:**
   - **Embedded in report** (Section 6)
   - **Standalone CSV:** `market-summary.csv` (optional, but preferred)
   - Columns: Workload Category, Market Size (2025), CAGR, Market Size (2030), Key Verticals, Growth Drivers

**File Structure:**
```
research/inference-workload-taxonomy/
├── research-findings.md          # Main report
├── hardware-requirement-matrix.csv
├── market-summary.csv            # Optional but preferred
└── README.md                     # Brief overview (optional)
```

**Recommendation:** Create markdown report with embedded tables, plus CSV exports for easy analysis. CSVs should be well-formatted with clear column headers.

---

### 4. Source Access Constraints

**Constraint:** **Publicly available data only** - no paid research subscriptions (Gartner, IDC, Forrester paid reports).

**Acceptable Sources:**
- ✅ **Public research summaries:** Free summaries, press releases, or excerpts from paid reports
- ✅ **Academic papers:** Open access papers, arXiv preprints
- ✅ **Vendor documentation:** NVIDIA, AMD, Intel official specs and documentation
- ✅ **Cloud provider documentation:** AWS, Azure, GCP public documentation
- ✅ **Industry reports:** Free industry reports, government reports, public filings
- ✅ **Benchmark data:** MLPerf, academic benchmarks (publicly available)
- ✅ **News articles:** Industry news, analysis articles
- ✅ **Public company filings:** SEC filings, earnings reports (if applicable)

**Unacceptable Sources:**
- ❌ **Paid Gartner/IDC/Forrester reports** (unless free summary available)
- ❌ **Paywalled academic papers** (unless preprint available)
- ❌ **Subscription-only content**

**Workaround Strategy:**
- If paid report data is needed, look for:
  - Free summaries or press releases
  - News articles citing the report
  - Public excerpts or blog posts
  - Alternative free sources covering same topic
- **Note data gaps:** If critical data only available in paid reports, note this clearly with confidence level "LOW - requires paid report access"

**Recommendation:** Use publicly available data, cite free summaries of paid reports when available, and clearly mark confidence levels. If market size data is unavailable from free sources, use estimation methods and note limitations.

---

## Research Objective

Create a comprehensive taxonomy of AI inference workloads, categorized by latency requirements and hardware needs, with market size and growth projections for each category. This research will inform hardware selection, workload prioritization, and market opportunity assessment for off-grid AI inference deployments.

**Key Questions to Answer:**
1. What are all the major types of AI inference workloads?
2. Which workloads require edge/low-latency (<100ms) vs batch/non-real-time (>1s)?
3. What hardware is required for each workload type (GPU model, interconnect, memory)?
4. What is the market size for each workload category?
5. What are the projected growth rates for each category?

---

## Research Structure

The final report should be organized into the following sections:

### Section 1: Executive Summary
- Overview of inference workload landscape
- Key findings on latency requirements
- Hardware requirement patterns
- Market size summary
- Growth projections summary

### Section 2: Low-Latency/Edge Inference Workloads (<100ms)
- Detailed analysis of each workload type
- Hardware requirements
- Market size and growth

### Section 3: Batch/Non-Real-Time Inference Workloads (>1s)
- Detailed analysis of each workload type
- Hardware requirements
- Market size and growth

### Section 4: Training vs Inference Hardware Requirements
- SXM vs PCIe distinctions
- NVLink requirements
- When training hardware is needed vs inference-only

### Section 5: Market Analysis Summary
- Total addressable market (TAM)
- Serviceable addressable market (SAM)
- Growth projections by category
- Regional variations

---

## Section 1: Low-Latency/Edge Inference Workloads (<100ms)

### Research Requirements

For each workload type identified, research and document:

1. **Workload Description:**
   - What is the workload?
   - What problem does it solve?
   - Typical use cases and applications

2. **Latency Requirements:**
   - Target latency (p50, p95, p99)
   - Maximum acceptable latency
   - Consequences of latency violations

3. **Hardware Requirements:**
   - **GPU Model:** **Primary focus on NVIDIA** (H100 PCIe, H100 SXM, A100, L4, T4, etc.)
     - **Secondary:** AMD (MI300X, MI250X), Intel (Gaudi 2/3) - brief mention if relevant
     - **Note:** NVIDIA is primary focus (80% of analysis), alternatives for completeness (20%)
   - **Interconnect:** PCIe, NVLink, InfiniBand (if multi-GPU)
   - **Memory:** VRAM requirements (GB)
   - **Compute:** TFLOPS requirements
   - **Power:** Typical power consumption (W)
   - **Special Requirements:** Any unique hardware needs

4. **Model Characteristics:**
   - Typical model size (parameters, GB)
   - Model architecture (Transformer, CNN, etc.)
   - Quantization requirements (FP32, FP16, INT8, INT4)
   - Batch size (typically 1 for real-time)

5. **Market Size:**
   - Current market size (USD, deployments, or compute hours)
   - Market growth rate (CAGR)
   - Projected market size (2026, 2027, 2030)
   - Key market segments/verticals

6. **Growth Drivers:**
   - What is driving growth?
   - Adoption barriers
   - Technology trends

### Workload Categories to Research

**1. Real-Time Language Model Inference**
- Chatbots, virtual assistants
- Code completion (GitHub Copilot, Cursor)
- Real-time translation
- Voice assistants (Alexa, Siri, Google Assistant)

**2. Autonomous Vehicle Perception**
- Object detection
- Lane detection
- Pedestrian detection
- Traffic sign recognition
- Sensor fusion

**3. Robotics & Industrial Automation**
- Robot vision
- Real-time control
- Pick-and-place operations
- Quality inspection

**4. Medical Imaging Real-Time**
- Real-time X-ray analysis
- Ultrasound interpretation
- Endoscopy analysis
- Surgical guidance

**5. Financial Trading**
- Algorithmic trading
- Fraud detection (real-time)
- Risk assessment (real-time)
- Market prediction

**6. Gaming & Entertainment**
- Real-time rendering
- NPC behavior
- Procedural generation
- Anti-cheat detection

**7. Security & Surveillance**
- Facial recognition (real-time)
- Object tracking
- Anomaly detection
- License plate recognition

**8. Augmented Reality (AR) / Virtual Reality (VR)**
- Object recognition
- Hand tracking
- Scene understanding
- Real-time rendering

**9. Edge IoT Applications**
- Smart cameras
- Edge sensors
- Real-time analytics
- Predictive maintenance

**10. Content Moderation (Real-Time)**
- Live stream moderation
- Real-time chat filtering
- Image/video content detection

---

## Section 2: Batch/Non-Real-Time Inference Workloads (>1s)

### Research Requirements

Same structure as Section 1, but focus on workloads that can tolerate higher latency.

### Workload Categories to Research

**1. Batch Language Model Inference**
- Document summarization
- Content generation (non-real-time)
- Batch translation
- Code generation (non-real-time)
- Text analysis

**2. Scientific Computing**
- Climate modeling
- Drug discovery
- Protein folding
- Molecular dynamics
- Astronomy data analysis

**3. Media Processing**
- Video editing/processing
- Image batch processing
- Content creation
- Style transfer
- Upscaling/restoration

**4. Data Analytics & Business Intelligence**
- Large-scale data analysis
- Business intelligence queries
- Predictive analytics (batch)
- Customer segmentation
- Recommendation systems (batch)

**5. Content Generation (Batch)**
- Image generation (DALL-E, Midjourney)
- Video generation
- Music generation
- 3D model generation

**6. Research & Development**
- Model evaluation
- Hyperparameter tuning
- Experimentation
- Research workloads

**7. Medical Imaging (Batch)**
- Batch radiology analysis
- Pathology analysis
- Medical research
- Drug discovery

**8. Financial Analysis (Batch)**
- Portfolio optimization
- Risk modeling (batch)
- Credit scoring (batch)
- Regulatory reporting

**9. Content Moderation (Batch)**
- Bulk content review
- Archive analysis
- Compliance checking

**10. Training Data Generation**
- Synthetic data generation
- Data augmentation
- Labeling assistance
- Quality control

---

## Section 3: Training vs Inference Hardware Requirements

### Critical Research Areas

**1. SXM vs PCIe Distinctions:**

Research and document:
- **H100 SXM5:**
  - Interconnect: NVLink 4.0 (900 GB/s per GPU)
  - Use cases: Training, multi-GPU inference
  - Power: 700W TDP
  - Form factor: Requires specialized servers (DGX, HGX)
  - When required: Multi-GPU training, high-bandwidth model parallelism

- **H100 PCIe:**
  - Interconnect: PCIe 5.0 (128 GB/s), NVLink 3.0 (600 GB/s with bridges)
  - Use cases: Single-GPU inference, small-scale training
  - Power: 350W TDP
  - Form factor: Standard PCIe slot
  - When required: Inference, single-GPU workloads, cost-sensitive deployments

**2. NVLink Requirements:**

Research:
- When is NVLink required vs optional?
- Training requirements: Is NVLink required for training?
- Inference requirements: When is NVLink needed for inference?
- Multi-GPU scaling: How does NVLink affect multi-GPU performance?
- Alternatives: Can PCIe-only systems do training? What are the limitations?

**3. Training Hardware Requirements:**

Research:
- **Model Training:**
  - Minimum hardware: SXM required? PCIe sufficient?
  - Multi-GPU requirements: NVLink vs InfiniBand
  - Memory requirements: VRAM needs for training
  - Power requirements: Training power consumption

- **Fine-Tuning:**
  - Hardware requirements: SXM vs PCIe
  - LoRA/QLoRA: Can fine-tuning be done on PCIe?
  - Memory-efficient training techniques

- **Distributed Training:**
  - Multi-node requirements
  - Interconnect needs (NVLink, InfiniBand)
  - Scaling limitations

**4. Inference Hardware Requirements:**

Research:
- **Single-GPU Inference:**
  - PCIe sufficient for most workloads?
  - When is SXM needed for inference?
  - Memory requirements

- **Multi-GPU Inference:**
  - When is NVLink needed?
  - Tensor parallelism requirements
  - Data parallelism (NVLink optional?)

**5. Hardware Selection Guidelines:**

Create decision matrix:
- **Training:** SXM required? PCIe sufficient for small models?
- **Fine-tuning:** SXM vs PCIe trade-offs
- **Inference (single-GPU):** PCIe sufficient?
- **Inference (multi-GPU):** NVLink required?
- **Cost considerations:** When is PCIe acceptable trade-off?

---

## Section 4: Market Analysis

### Market Size Research

For each workload category, research:

1. **Current Market Size (2025):**
   - Total Addressable Market (TAM) in USD
   - Serviceable Addressable Market (SAM) in USD
   - Number of deployments/users
   - Compute hours/demand

2. **Market Growth:**
   - Historical growth (2020-2025)
   - Projected CAGR (2025-2030)
   - Projected market size: 2026, 2027, 2030
   - Growth drivers and barriers

3. **Market Segmentation:**
   - By vertical (healthcare, finance, automotive, etc.)
   - By geography (US, Europe, Asia-Pacific)
   - By deployment type (cloud, edge, on-premise)
   - By model size (small, medium, large, XL)

4. **Key Players:**
   - Major providers/vendors
   - Market share
   - Competitive landscape

5. **Pricing Models:**
   - Per-request pricing
   - Per-hour pricing
   - Subscription models
   - Enterprise pricing

### Data Sources to Prioritize

1. **Industry Reports:**
   - Gartner, IDC, Forrester market research
   - AI/ML market reports
   - Edge computing market reports
   - Vertical-specific reports (healthcare AI, autonomous vehicles, etc.)

2. **Academic Research:**
   - Papers on inference workloads
   - Benchmark studies
   - Performance analysis

3. **Vendor Documentation:**
   - NVIDIA technical documentation
   - Cloud provider documentation (AWS, Azure, GCP)
   - Hardware vendor specifications

4. **Market Data:**
   - Public company filings (if applicable)
   - Industry association reports
   - Government reports (if available)

---

## Section 5: Hardware Requirement Matrix

### Create Comprehensive Matrix

For each workload type, create a matrix with:

| Workload | Latency Req | GPU Model | Interconnect | VRAM (GB) | Power (W) | SXM Required? | NVLink Required? | Market Size (2025) | CAGR | Market Size (2030) |
|----------|-------------|-----------|--------------|-----------|-----------|---------------|------------------|-------------------|------|-------------------|
| Real-time Chat | <100ms | H100 PCIe | PCIe | 80 | 350 | No | No | $X B (Global) | Y% | $Z B (Global) |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

**Note:** 
- **GPU Model:** Primary focus on NVIDIA (H100 PCIe, H100 SXM, A100, L4, T4). Include alternatives (AMD, Intel) only if significantly relevant.
- **Market Size:** Present as "Global: $X B" or "Global: $X B, US: $Y B" when regional breakdown available.

**Key Columns:**
- **Workload:** Name of workload type
- **Latency Req:** Target latency (ms or seconds)
- **GPU Model:** Recommended GPU (H100 PCIe, H100 SXM, A100, L4, etc.)
- **Interconnect:** PCIe, NVLink, InfiniBand
- **VRAM:** Minimum/recommended VRAM
- **Power:** Typical power consumption
- **SXM Required?:** Yes/No/Depends (with explanation)
- **NVLink Required?:** Yes/No/Depends (with explanation)
- **Market Size (2025):** Current market in USD or other metric
- **CAGR:** Compound annual growth rate
- **Market Size (2030):** Projected market size

---

## Section 6: Off-Grid Deployment Considerations

### Research Requirements

For each workload category, analyze:

1. **Off-Grid Suitability:**
   - Can this workload run off-grid?
   - Power requirements vs generator capacity
   - Data logistics requirements
   - Latency constraints (if edge deployment)

2. **Deployment Scenarios:**
   - Edge deployment (low latency, off-grid)
   - Batch processing (higher latency acceptable, off-grid)
   - Hybrid (edge + batch)

3. **Hardware Selection for Off-Grid:**
   - PCIe vs SXM trade-offs (power, cost)
   - Single-GPU vs multi-GPU (power, complexity)
   - Cooling requirements

4. **Market Opportunity:**
   - Which workloads are best suited for off-grid?
   - Market size for off-grid addressable workloads
   - Competitive advantages of off-grid deployment

---

## Research Methodology

### Phase 1: Workload Identification

1. **Comprehensive Literature Review:**
   - Search academic papers on inference workloads
   - Review industry reports on AI/ML applications
   - Analyze cloud provider documentation (AWS SageMaker, Azure ML, GCP AI)
   - Review NVIDIA documentation and case studies

2. **Workload Categorization:**
   - Group by latency requirements
   - Group by hardware requirements
   - Group by use case/vertical

### Phase 2: Hardware Requirements Research

1. **NVIDIA Documentation:**
   - H100 PCIe vs SXM specifications
   - NVLink documentation
   - Training vs inference guides
   - Performance benchmarks

2. **Academic Benchmarks:**
   - MLPerf Inference benchmarks
   - Training benchmarks
   - Hardware comparison studies

3. **Vendor Documentation:**
   - Cloud provider GPU offerings
   - Hardware vendor specifications
   - Performance data sheets

### Phase 3: Market Analysis

1. **Market Research Reports:**
   - Gartner, IDC, Forrester reports
   - Industry-specific reports
   - Edge computing market reports

2. **Public Data:**
   - Company filings (if public companies)
   - Government reports
   - Industry association data

3. **Estimation Methods:**
   - If direct data unavailable, use:
     - Number of deployments × average value
     - Compute hours × pricing
     - User base × adoption rate × pricing

---

## Output Format

### Report Structure

Create a comprehensive markdown report: `research-findings.md`

**Required Sections:**

1. **Executive Summary** (2-3 pages)
   - Key findings
   - Market overview
   - Hardware requirement patterns
   - Growth projections

2. **Low-Latency/Edge Inference Workloads** (10-15 pages)
   - Detailed analysis of each workload type
   - Hardware requirements matrix
   - Market analysis

3. **Batch/Non-Real-Time Inference Workloads** (10-15 pages)
   - Detailed analysis of each workload type
   - Hardware requirements matrix
   - Market analysis

4. **Training vs Inference Hardware Requirements** (5-8 pages)
   - SXM vs PCIe analysis
   - NVLink requirements
   - Decision guidelines

5. **Comprehensive Hardware Requirement Matrix** (2-3 pages)
   - Complete matrix for all workloads
   - Quick reference guide

6. **Market Analysis Summary** (3-5 pages)
   - Total market size
   - Growth projections
   - Regional variations
   - Key trends

7. **Off-Grid Deployment Considerations** (3-5 pages)
   - Suitability analysis
   - Market opportunity
   - Deployment scenarios

8. **Citations & Sources** (2-3 pages)
   - All sources cited
   - Links to reports, papers, documentation
   - Data sources

---

## Specific Research Questions

### Critical Questions to Answer

1. **Training Hardware:**
   - Is SXM required for training, or can PCIe work?
   - What are the limitations of PCIe-only training?
   - Can LoRA/QLoRA fine-tuning be done on PCIe?
   - What model sizes require SXM for training?

2. **Inference Hardware:**
   - When is SXM needed for inference vs PCIe sufficient?
   - When is NVLink required for multi-GPU inference?
   - Can large models (70B+) run on PCIe for inference?
   - What are the performance trade-offs?

3. **Market Sizing:**
   - What is the total inference market size?
   - What is the edge inference market size?
   - What is the batch inference market size?
   - What are the growth rates for each segment?

4. **Workload Classification:**
   - Which workloads absolutely require <100ms latency?
   - Which workloads can tolerate >1s latency?
   - Are there workloads in between (100ms-1s)?

---

## Data Quality Requirements

### Confidence Levels

For each data point, indicate confidence level:

- **HIGH:** Data from authoritative sources (NVIDIA specs, Gartner reports, official benchmarks)
- **MEDIUM:** Data from reputable sources (academic papers, industry analysis)
- **LOW:** Estimates, extrapolations, or limited data

### Source Attribution

- **Cite all sources** with URLs or references
- **Note data gaps** where information is unavailable
- **Indicate estimation methods** when direct data unavailable
- **Cross-reference** multiple sources when possible

---

## Deliverables

1. **Primary Report:** `research-findings.md` (40-60 pages)
   - Comprehensive analysis
   - All sections completed
   - Citations throughout

2. **Hardware Matrix:** Embedded in report + standalone CSV
   - Complete matrix for all workloads
   - Easy to reference

3. **Market Summary:** Embedded in report + standalone summary
   - Key market metrics
   - Growth projections
   - Quick reference

---

## Research Priorities

### High Priority (Must Complete)

1. ✅ Low-latency workload taxonomy (10+ workload types)
2. ✅ Batch workload taxonomy (10+ workload types)
3. ✅ SXM vs PCIe requirements (training vs inference)
4. ✅ NVLink requirements analysis
5. ✅ Market size for major workload categories (top 5-10)

### Medium Priority (Should Complete)

6. ⚠️ Market growth projections (CAGR, 2030 projections)
7. ⚠️ Hardware requirement matrix (all workloads)
8. ⚠️ Off-grid deployment considerations

### Low Priority (Nice to Have)

9. ⚠️ Regional market variations
10. ⚠️ Detailed competitive landscape
11. ⚠️ Pricing model analysis

---

## Research Sources to Prioritize

### Primary Sources

1. **NVIDIA Documentation:**
   - H100 Product Briefs (PCIe and SXM)
   - NVLink documentation
   - Training vs Inference guides
   - Performance benchmarks (MLPerf)
   - **Access:** Publicly available ✅

2. **Market Research (Public Sources Only):**
   - Gartner AI/ML market reports (free summaries, press releases)
   - IDC edge computing reports (free summaries, public excerpts)
   - Forrester AI market analysis (free summaries, blog posts)
   - Industry-specific reports (healthcare AI, autonomous vehicles, etc.) - free/public versions
   - **Note:** Use free summaries/excerpts only, not full paid reports

3. **Academic Research:**
   - MLPerf benchmark papers (publicly available)
   - Inference workload analysis papers (arXiv, open access)
   - Hardware comparison studies (publicly available)
   - Performance optimization papers (arXiv, open access)
   - **Access:** Open access papers, arXiv preprints ✅

4. **Cloud Provider Documentation:**
   - AWS SageMaker inference documentation (public)
   - Azure ML inference documentation (public)
   - GCP AI Platform documentation (public)
   - Workload examples and case studies (public)
   - **Access:** Publicly available ✅

5. **Industry Reports (Public/Free):**
   - Edge AI market reports (free industry reports)
   - Autonomous vehicle market reports (public sources)
   - Healthcare AI market reports (public sources)
   - Financial AI market reports (public sources)
   - Government reports (if available)
   - **Access:** Publicly available sources only ✅

6. **Alternative Sources if Paid Reports Unavailable:**
   - News articles citing market research
   - Industry association reports (public)
   - Public company filings (SEC filings, earnings reports)
   - Vendor press releases and announcements
   - Public benchmark data (MLPerf, academic benchmarks)

---

## Expected Research Challenges

### Anticipated Difficulties

1. **Market Size Data:**
   - May not be publicly available for all workload types
   - May need to estimate from multiple sources
   - Market definitions may vary

2. **Hardware Requirements:**
   - May need to infer from benchmarks
   - Vendor documentation may be incomplete
   - Real-world requirements may differ from specs

3. **Workload Classification:**
   - Some workloads may span categories
   - Latency requirements may vary by use case
   - Hardware requirements may be flexible

### Mitigation Strategies

1. **Use Multiple Sources:** Cross-reference data from multiple sources
2. **Indicate Confidence:** Clearly mark confidence levels
3. **Note Assumptions:** Document assumptions and estimation methods
4. **Provide Ranges:** Use ranges when exact data unavailable

---

## Success Criteria

The research is successful if it provides:

1. ✅ **Comprehensive Workload Taxonomy:** 20+ workload types identified and categorized
2. ✅ **Clear Hardware Requirements:** SXM vs PCIe, NVLink requirements clearly defined
3. ✅ **Market Sizing:** Market size for major workload categories (top 10+)
4. ✅ **Growth Projections:** CAGR and 2030 projections for major categories
5. ✅ **Actionable Insights:** Clear guidance on hardware selection and market opportunities

---

## Additional Notes

### Research Focus Areas

**Critical for Off-Grid Deployment:**
- Which workloads can run off-grid?
- Power requirements vs generator capacity
- Data logistics requirements
- Latency constraints

**Critical for Hardware Selection:**
- When is PCIe sufficient vs SXM required?
- When is NVLink required vs optional?
- Cost vs performance trade-offs

**Critical for Market Analysis:**
- Total addressable market
- Growth opportunities
- Competitive landscape
- Pricing models

---

## Research Timeline

**Estimated Research Time:** 8-12 hours

**Phase Breakdown:**
- Phase 1 (Workload Identification): 2-3 hours
- Phase 2 (Hardware Requirements): 2-3 hours
- Phase 3 (Market Analysis): 3-4 hours
- Phase 4 (Synthesis & Report): 1-2 hours

---

## Final Instructions

1. **Be Comprehensive:** Cover all major inference workload types
2. **Be Specific:** Provide concrete hardware requirements, not generalities
3. **Be Data-Driven:** Use market data, benchmarks, and authoritative sources
4. **Be Clear:** Organize findings clearly with tables, matrices, and summaries
5. **Be Honest:** Indicate confidence levels and data gaps
6. **Be Actionable:** Provide insights that inform hardware selection and market strategy

**Remember:** This research will inform critical decisions about hardware procurement, workload prioritization, and market strategy. Accuracy and comprehensiveness are essential.

---

**Research Prompt Version:** 1.1  
**Last Updated:** 2025-12-02  
**Status:** Ready for research agent  
**Clarifications Added:** Geographic scope, hardware vendor focus, output format, source access constraints

