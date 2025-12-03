#!/usr/bin/env python3
"""
Generator Risk Parameters Documentation
Detailed documentation for generator risk calculator parameters
"""

import streamlit as st
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(
    page_title="Generator Risk Parameters - Documentation",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Generator Risk Parameters Documentation")

st.markdown("""
This page provides detailed documentation for the **Advanced Generator Risk Parameters** used in the calculator.
These parameters help assess how GPU power transitions affect generator stability.
""")

# Navigation
st.markdown("---")
st.markdown("[← Back to Calculator](/unified-calculator-app)")
st.markdown("---")

# Load and display formulas
@st.cache_data
def load_formulas():
    """Load generator risk formulas markdown"""
    base_paths = [
        os.getcwd(),
        '/home/jovyan/work/og-ai-inference-research',
        '/srv/projects/og-ai-inference-research'
    ]
    
    for base_path in base_paths:
        formulas_path = os.path.join(base_path, 'models/generator-risk-calculator/formulas.md')
        if os.path.exists(formulas_path):
            with open(formulas_path, 'r') as f:
                return f.read()
    return None

formulas_content = load_formulas()

if formulas_content:
    st.markdown(formulas_content)
else:
    st.warning("Could not load formulas documentation. Using inline content.")
    
    # Fallback content
    st.header("Input Parameters")
    
    st.subheader("Per-GPU Power Step (ΔP_gpu)")
    st.markdown("""
    **Units:** kW  
    **Range:** 0.1 - 10.0 kW  
    **Default:** 0.25 kW
    
    The power change per GPU during state transitions (e.g., idle to full load).
    
    **Typical Values:**
    - H100 PCIe: 0.25-0.5 kW
    - H100 SXM: 0.5-0.7 kW
    - A100 PCIe: 0.2-0.4 kW
    
    **Impact:** Higher values increase the total cluster power step, which increases generator stress.
    """)
    
    st.subheader("Correlation Factor (C)")
    st.markdown("""
    **Units:** Dimensionless (0-1)  
    **Range:** 0.0 - 1.0  
    **Default:** 0.7
    
    Synchronization factor for GPU power steps:
    - **0.0** = Fully uncorrelated (GPUs transition independently)
    - **1.0** = Perfectly synchronized (all GPUs transition simultaneously)
    
    **Typical Values:**
    - Coordinated workloads: 0.6-0.8
    - Independent workloads: 0.3-0.5
    - Worst-case (conservative): 1.0
    
    **Impact:** Lower correlation reduces effective cluster power step, reducing generator stress.
    """)
    
    st.subheader("Transition Time (Δt)")
    st.markdown("""
    **Units:** seconds  
    **Range:** 0.1 - 10.0 s  
    **Default:** 1.0 s
    
    Time duration over which the power step occurs.
    
    **Typical Values:**
    - Fast workload startup: 0.5-1.0 s
    - Gradual startup: 2.0-5.0 s
    - Controlled sequencing: 5.0-10.0 s
    
    **Impact:** Shorter transition times create higher ramp rates, increasing generator stress.
    """)
    
    st.header("Calculated Outputs")
    
    st.subheader("1. Cluster Power Step")
    st.code("""
ΔP_cluster = C × N × ΔP_gpu
""", language="python")
    st.markdown("Total power change when the specified fraction of GPUs transition.")
    
    st.subheader("2. Ramp Rate")
    st.code("""
RampRate = ΔP_cluster / Δt
""", language="python")
    st.markdown("Rate at which the cluster load changes (kW/s).")
    
    st.subheader("3. Step Fraction")
    st.code("""
StepFraction = ΔP_cluster / P_rated
""", language="python")
    st.markdown("Load step as a fraction of generator capacity.")
    
    st.subheader("4. Risk Level Classification")
    st.markdown("""
- **GREEN:** Less than 50% of generator's max step
- **YELLOW:** Between 50% and 100% of max step  
- **RED:** Exceeds generator's max step capability
    """)

