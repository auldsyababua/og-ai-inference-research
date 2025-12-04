#!/usr/bin/env python3
"""
Data Logistics Documentation
Detailed documentation for data transfer cost calculations
"""

import streamlit as st
import os
import sys

st.set_page_config(
    page_title="Data Logistics - Documentation",
    page_icon="📡",
    layout="wide"
)

st.title("📡 Data Logistics Documentation")

st.markdown("""
This page provides detailed documentation for **Data Logistics** calculations, including
Starlink, Sneakernet, and Fiber cost comparisons.

## 🎯 Addressable Market Context

Data movement constraints are the **primary limiting factor** for off-grid AI inference viability.
Our market research identifies **$2-3B (2025) → $7-10B (2030)** addressable market for workloads
that meet specific data transfer thresholds.

### Data Movement Viability Thresholds

The **<1TB per job** threshold is the critical breakpoint between "strong" and "marginal" off-grid viability
across all market analyses:

| Scenario | Data Size | Transfer Method | Turnaround | Viability |
|----------|-----------|-----------------|-----------|-----------|
| **Starlink-only (ideal)** | <100GB | 100-200 Mbps satellite | 3-8 hours | ✅ STRONG |
| **Starlink-only (stretched)** | 100GB-1TB | 100-200 Mbps satellite | 8-30 hours | ✅ MODERATE |
| **Starlink + sneakernet** | 1-5TB | Satellite + occasional drive shipment | 1-3 days | ⚠️ MARGINAL |
| **Sneakernet-primary** | 5-50TB | Weekly/monthly drive shipments | 1-2 weeks | ⚠️ MARGINAL |
| **Sneakernet-only** | 50-500TB | Dedicated appliance logistics | 2-4 weeks | ❌ WEAK |
| **Not viable** | >500TB or multi-TB/day continuous | N/A | N/A | ❌ NOT VIABLE |

### Compute-Intensity Ratio (CIR)

**Definition:** CIR = GPU-hours required / TB of data transferred

**Viability threshold:** CIR > 10 (i.e., >10 GPU-hours per TB transferred)

**High-CIR Workloads (Viable):**
- **AlphaFold (1k proteins):** CIR ~500 (Input: <1GB, Compute: ~500 GPU-hours)
- **Batch LLM (1TB corpus):** CIR ~30 (Processing 1TB text = 30+ GPU-hours on 70B model)
- **Generative Images (10k images):** CIR ~100 (Prompts: 10MB, Compute: ~100 GPU-hours, Output: 100GB)
- **Synthetic Data (10TB output):** CIR ~200 (Seed: negligible, Compute: days, Output: 10TB)

**Low-CIR Workloads (Non-Viable):**
- **Video Post-Production (10TB raw):** CIR ~1 (Mostly file I/O with some GPU transforms)
- **Analytics/BI (scanning 10TB):** CIR ~0.5 (Dominated by data reading, minimal compute)
- **Medical Imaging (batch 1TB scans):** CIR ~5 (Significant I/O, moderate GPU inference)

### Top Viable Workloads

Based on consensus across four independent market analyses, these workloads represent 85-95% of the addressable market:

**Tier 1: Immediate Focus ($1.2-2.4B)**
1. **Batch LLM Inference** - $500M-1B opportunity
   - Typical data: 10GB-1TB per job
   - Latency tolerance: 24-48h
   - Example: Overnight document summarization, embeddings generation

2. **Generative Image/Video** - $400-800M opportunity
   - Typical data: Input KB-MB, Output 100GB-1TB
   - Latency tolerance: 24-48h
   - Example: Ad agency generating 10k creatives overnight

3. **Synthetic Data Generation** - $300-600M opportunity
   - Typical data: Output 1-10TB
   - Latency tolerance: Days-weeks
   - Example: Training data generation for AI model development

**Tier 2: Near-Term Expansion ($500M-1B)**
4. **AlphaFold/Protein Folding** - $200-400M opportunity
   - Typical data: Input <1GB, Output <10GB
   - Latency tolerance: 12-48h
   - Example: Pharma running 10k protein structure predictions weekly

5. **LoRA Fine-Tuning** - $200-400M opportunity
   - Typical data: 10-50GB
   - Latency tolerance: 1-3 days
   - Example: Custom model adaptation for enterprise applications

### Regulatory Blockers

These scenarios represent ~40-50% of potential batch inference market but are immediately disqualified:

**Non-Negotiable Barriers:**
- ❌ **HIPAA/PHI (Healthcare):** Patient imaging (CT, MRI, pathology), clinical diagnosis
- ❌ **Financial Services (SOX, PCI-DSS):** Tier-1 banking, credit card processing
- ❌ **Real-time/Interactive:** Latency requirements <1 second
- ❌ **Continuous Streaming:** Cannot tolerate batch windows

**Manageable Scenarios:**
- ✅ **GDPR (EU data):** Can be handled with proper data residency
- ✅ **Corporate IP:** Addressed via contractual protections, encryption
- ✅ **Light PII (LLM batch):** Acceptable with BAAs, encryption, anonymization
""")

# Navigation
st.markdown("---")
st.markdown("[← Back to Calculator](/unified-calculator-app)")
st.markdown("---")

# Load and display formulas
@st.cache_data
def load_formulas():
    """Load data logistics formulas markdown"""
    base_paths = [
        os.getcwd(),
        '/home/jovyan/work/og-ai-inference-research',
        '/srv/projects/og-ai-inference-research'
    ]
    
    for base_path in base_paths:
        formulas_path = os.path.join(base_path, 'models/data-logistics/formulas.md')
        if os.path.exists(formulas_path):
            with open(formulas_path, 'r') as f:
                return f.read()
    return None

formulas_content = load_formulas()

if formulas_content:
    st.markdown(formulas_content)
else:
    st.warning("Could not load formulas documentation. Using inline content.")
    
    st.header("Input Parameters")
    
    st.subheader("Inbound Data (TB/month)")
    st.markdown("""
    **Units:** TB/month  
    **Default:** 400.0 TB/month
    
    Monthly inbound data volume transferred to the site:
    - Model weights
    - Training datasets
    - Input data for inference
    
    **Example:** 400 TB/month = ~13 TB/day average
    """)
    
    st.subheader("Outbound Data (TB/month)")
    st.markdown("""
    **Units:** TB/month  
    **Default:** 50.0 TB/month
    
    Monthly outbound data volume transferred from the site:
    - Inference results
    - Embeddings
    - Output data
    
    **Example:** 50 TB/month = ~1.7 TB/day average
    """)
    
    st.subheader("Starlink Terminals")
    st.markdown("""
    **Units:** Count  
    **Default:** 15 terminals
    
    Number of Starlink satellite terminals.
    
    **Capacity per Terminal:**
    - Effective bandwidth: 100-150 Mbps (sustained)
    - Usable capacity: ~20-25 TB/month per terminal (with overhead)
    
    **2025 Pricing Model:**
    - $290/month per terminal (1TB priority data)
    - $540/month per terminal (2TB priority data)
    - $250/TB overage after priority data exhausted
    - **Note:** Post-cap throttling (1 Mbps) makes high-volume transfer impractical
    """)
    
    st.subheader("Sneakernet Distance (miles)")
    st.markdown("""
    **Units:** miles  
    **Default:** 200.0 miles
    
    One-way distance to site for physical data transport.
    
    **Cost Calculation:**
    - Vehicle cost: $0.70/mile (IRS standard rate)
    - Driver labor: $0.30-$0.50/mile
    - Total: $1.00-$1.20/mile (round trip)
    
    **Capacity per Trip:**
    - Typical: 120 TB per trip (6× 20TB drives with RAID-Z2)
    """)
    
    st.subheader("Fiber Distance (miles)")
    st.markdown("""
    **Units:** miles  
    **Default:** 10.0 miles
    
    Distance to nearest Point of Presence (POP) for fiber connection.
    
    **Build Costs:**
    - Aerial: $50,000/mile
    - Underground (rural): $70,000-$96,000/mile
    - Rocky terrain: $150,000/mile
    
    **Amortization:** Typically 20 years for private deployments
    """)
    
    st.header("Cost Calculations")
    
    st.subheader("Starlink Cost")
    st.code("""
Starlink_Total_Cost_per_month = N_starlink × C_starlink
Starlink_Cost_per_TB = Starlink_Total_Cost_per_month / Total_TB_per_month
""", language="python")
    
    st.subheader("Sneakernet Cost")
    st.code("""
Sneakernet_Cost_per_trip = 2 × D_sneakernet × C_sneakernet  # Round trip
Sneakernet_Total_Cost_per_month = T_sneakernet × Sneakernet_Cost_per_trip
Sneakernet_Cost_per_TB = Sneakernet_Total_Cost_per_month / Total_TB_per_month
""", language="python")
    
    st.subheader("Fiber Cost")
    st.code("""
Fiber_Total_CapEx = D_fiber × C_fiber
Fiber_Monthly_CapEx = Fiber_Total_CapEx / (Y_fiber × 12)
Fiber_Total_Cost_per_month = Fiber_Monthly_CapEx + OpEx_fiber
Fiber_Cost_per_TB = Fiber_Total_Cost_per_month / Total_TB_per_month
""", language="python")
    
    st.header("Mode Recommendation")
    
    st.markdown("""
    The calculator compares cost per TB for all three modes and recommends the lowest-cost option
    that can meet capacity requirements.
    
    **Key Considerations:**
    - Starlink: Limited by data buckets (2025 pricing model)
    - Sneakernet: Limited by trip frequency and capacity
    - Fiber: Effectively unlimited capacity
    """)

