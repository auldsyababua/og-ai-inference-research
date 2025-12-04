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

