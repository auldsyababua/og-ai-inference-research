#!/usr/bin/env python3
"""
BESS Sizing Documentation
Detailed documentation for BESS sizing calculations and decision logic
"""

import streamlit as st
import os
import sys

st.set_page_config(
    page_title="BESS Sizing - Documentation",
    page_icon="🔋",
    layout="wide"
)

st.title("🔋 BESS Sizing Documentation")

st.markdown("""
This page provides detailed documentation for **BESS (Battery Energy Storage System) sizing** calculations,
including decision logic, formulas, and cost estimation.
""")

# Navigation
st.markdown("---")
st.markdown("[← Back to Calculator](/unified-calculator-app)")
st.markdown("---")

# Load and display formulas
@st.cache_data
def load_formulas():
    """Load BESS sizing formulas markdown"""
    base_paths = [
        os.getcwd(),
        '/home/jovyan/work/og-ai-inference-research',
        '/srv/projects/og-ai-inference-research'
    ]
    
    for base_path in base_paths:
        formulas_path = os.path.join(base_path, 'models/bess-sizing/formulas.md')
        if os.path.exists(formulas_path):
            with open(formulas_path, 'r') as f:
                return f.read()
    return None

formulas_content = load_formulas()

if formulas_content:
    st.markdown(formulas_content)
else:
    st.warning("Could not load formulas documentation. Using inline content.")
    
    st.header("BESS Type Decision Logic")
    
    st.subheader("1. No-BESS Option")
    st.markdown("""
    **Conditions (all must be true):**
    - GPU count ≤ 4 units
    - Generator type = Fast-Response or Rich-Burn
    - Not islanded operation
    - Risk tolerance = High
    
    **Rationale:** Small clusters with fast-response generators may operate without BESS
    if proper controls are in place.
    """)
    
    st.subheader("2. Buffer BESS")
    st.markdown("""
    **Conditions:**
    - Generator can handle load step (gap ≤ 0), OR
    - Load step < 200 kW AND load sequencing available
    
    **Configuration:**
    - Power: 50-100 kW (20-40% of GPU cluster)
    - Energy: 50-100 kWh (1 hour at power rating)
    - Cost: $30,000-$60,000
    
    **Purpose:** Provides transient ride-through support only.
    """)
    
    st.subheader("3. Grid-Forming BESS")
    st.markdown("""
    **Conditions:**
    - Generator cannot handle load step (gap > 0), AND
    - Islanded operation OR black-start required
    
    **Configuration:**
    - Power: 400-600 kW (80-120% of gap, with safety margin)
    - Energy: 100-200 kWh (sufficient for transient support)
    - Cost: $350,000-$500,000
    
    **Purpose:** Provides frequency stability and synthetic inertia for islanded operation.
    """)
    
    st.header("Sizing Formulas")
    
    st.subheader("Buffer BESS Power")
    st.code("""
BESS_Power_kW = MAX(50, MIN(100, GPU_Cluster_Power_kW × 0.3))
""", language="python")
    
    st.subheader("Grid-Forming BESS Power")
    st.code("""
BESS_Power_kW = MAX(400, Load_Step_Magnitude_kW × 1.2)
""", language="python")
    
    st.subheader("BESS Energy")
    st.code("""
# Buffer BESS
BESS_Energy_kWh = BESS_Power_kW × 1.0

# Grid-Forming BESS  
BESS_Energy_kWh = MAX(100, BESS_Power_kW × 0.25)
""", language="python")
    
    st.header("Cost Estimation")
    
    st.subheader("Buffer BESS Cost")
    st.code("""
BESS_Cost_USD = 30000 + (BESS_Power_kW - 50) × 500
""", language="python")
    st.markdown("Range: $30,000-$60,000 (for 50-100 kW)")
    
    st.subheader("Grid-Forming BESS Cost")
    st.code("""
BESS_Cost_USD = 350000 + (BESS_Power_kW - 400) × 750
""", language="python")
    st.markdown("Range: $350,000-$500,000 (for 400-600 kW)")

