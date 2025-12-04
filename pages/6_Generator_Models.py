#!/usr/bin/env python3
"""
Generator Models Documentation
Detailed documentation for generator models and their specifications
"""

import streamlit as st
import os
import sys

st.set_page_config(
    page_title="Generator Models - Documentation",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Generator Models Documentation")

st.markdown("""
This page provides detailed documentation for **generator models** available in the calculator,
including power ratings, load acceptance capabilities, and use cases.
""")

# Navigation
st.markdown("---")
st.markdown("[← Back to Calculator](/unified-calculator-app)")
st.markdown("---")

st.header("Caterpillar Generators")

st.subheader("G3520 Fast Response")
st.markdown("""
**Power Rating:** 2,500 kW  
**Load Acceptance:** 100%  
**Type:** Natural Gas Fast Response  
**Inertia Constant (H):** 3.0 seconds  
**Governor Droop (R):** 0.04 (4%)  
**Max Step:** 100%

**Characteristics:**
- **Fast response capability:** ISO 8528-5 Class G2 + NFPA 110 compliant
- **Block load capability:** Can accept 100% load step
- **Start time:** ~10 seconds to ready-for-load
- **Applications:** Data centers, standby power, mission-critical applications

**Advantages:**
- Excellent dynamic response
- Can handle large load steps without BESS
- Proven reliability for data center applications
- Fast startup time

**Considerations:**
- Higher cost than standard generators
- Optimized for fast response (may have lower efficiency than continuous-duty models)
""")

st.subheader("CG170-16")
st.markdown("""
**Power Rating:** 1,560 kW  
**Load Acceptance:** 20%  
**Type:** Natural Gas  
**Inertia Constant (H):** 5.0 seconds  
**Governor Droop (R):** 0.04 (4%)  
**Max Step:** 20%

**Characteristics:**
- **Efficiency:** 43.3% electrical efficiency
- **Applications:** Industrial prime power, CHP, microgrids, continuous operation
- **Overhaul interval:** 64,000 hours
- **Fuel flexibility:** Natural gas, biogas, coal gas, synthesis gas

**Advantages:**
- High efficiency for continuous operation
- Long overhaul intervals (reduced maintenance)
- Proven reliability in industrial applications
- Good for microgrid baseload

**Considerations:**
- Limited load acceptance (20%) - requires BESS for large load steps
- Slower response than fast-response models
- Designed for continuous operation, not fast transients
""")

st.subheader("CG260-16")
st.markdown("""
**Power Rating:** 4,300 kW  
**Load Acceptance:** 16% (first step)  
**Type:** Natural Gas CG260  
**Inertia Constant (H):** 5.0 seconds  
**Governor Droop (R):** 0.05 (5%)  
**Max Step:** 16% (first step, multi-step capable)

**Characteristics:**
- **Efficiency:** 44.6% electrical efficiency (highest in CG series)
- **Applications:** Utility-scale microgrids, base load, large deployments
- **Overhaul interval:** 80,000 hours (longest in fleet)
- **Fuel flexibility:** Natural gas, biogas, coal gas, synthesis gas, hydrogen (up to 25%)

**Advantages:**
- Highest efficiency in CG series
- Longest overhaul interval (minimizes fleet maintenance)
- Hydrogen-ready capability (up to 25% H₂)
- Multi-step load acceptance (can ramp in stages)
- Large power rating for utility-scale deployments

**Considerations:**
- Very limited first-step acceptance (16%) - requires BESS or multi-step sequencing
- Large physical footprint
- Higher initial cost
- Requires careful load sequencing for large steps
""")

st.subheader("G3516C Island Mode")
st.markdown("""
**Power Rating:** 1,660 kW  
**Load Acceptance:** 75%  
**Type:** Natural Gas Fast Response  
**Inertia Constant (H):** 4.0 seconds  
**Governor Droop (R):** 0.04 (4%)  
**Max Step:** 75%

**Characteristics:**
- **Island mode optimized:** Designed for standalone operation
- **Applications:** Microgrids, islanded operation, remote sites
- **Response capability:** Good dynamic response for islanded operation

**Advantages:**
- Good load acceptance (75%)
- Optimized for islanded operation
- Better than standard models for standalone operation

**Considerations:**
- Lower power rating than G3520
- May still require BESS for very large clusters
""")

st.header("Standard Generators")

st.subheader("Natural Gas Standard")
st.markdown("""
**Power Rating:** 1,000 kW  
**Load Acceptance:** 30%  
**Type:** Natural Gas  
**Inertia Constant (H):** 4.0 seconds  
**Governor Droop (R):** 0.04 (4%)  
**Max Step:** 30%

**Characteristics:**
- Generic standard natural gas generator
- Typical industrial generator specifications
- Moderate load acceptance capability

**Use Cases:**
- General-purpose deployments
- Standard industrial applications
- Baseline reference for comparisons
""")

st.subheader("Diesel Standard")
st.markdown("""
**Power Rating:** 1,000 kW  
**Load Acceptance:** 70%  
**Type:** Diesel  
**Inertia Constant (H):** 3.0 seconds  
**Governor Droop (R):** 0.04 (4%)  
**Max Step:** 70%

**Characteristics:**
- Standard diesel generator
- Higher load acceptance than natural gas standard
- Faster response than natural gas

**Use Cases:**
- Backup power applications
- Deployments requiring higher load acceptance
- Applications where diesel fuel is available
""")

st.header("Model Comparison Table")

import pandas as pd

comparison_data = {
    'Model': ['G3520 Fast Response', 'CG170-16', 'CG260-16', 'G3516C Island Mode', 'Natural Gas Standard', 'Diesel Standard'],
    'Power (kW)': [2500, 1560, 4300, 1660, 1000, 1000],
    'Load Acceptance (%)': [100, 20, 16, 75, 30, 70],
    'Type': ['Fast Response', 'Continuous', 'Continuous', 'Island Mode', 'Standard', 'Standard'],
    'H (seconds)': [3.0, 5.0, 5.0, 4.0, 4.0, 3.0],
    'Best For': [
        'Data centers, fast response',
        'Microgrid baseload, CHP',
        'Utility-scale, base load',
        'Islanded operation',
        'General purpose',
        'Backup power'
    ]
}

df = pd.DataFrame(comparison_data)
st.dataframe(df, use_container_width=True, hide_index=True)

st.header("Selection Guidelines")

st.markdown("""
**Choose G3520 Fast Response if:**
- You need fast response and 100% block load capability
- Data center or mission-critical application
- Want to minimize BESS requirements
- Fast startup is required

**Choose CG170-16 if:**
- You need continuous operation (microgrid baseload)
- High efficiency is priority
- Long maintenance intervals are important
- Moderate load steps are acceptable (with BESS)

**Choose CG260-16 if:**
- You need large power rating (utility-scale)
- Maximum efficiency is critical
- Hydrogen fuel capability is desired
- Multi-step load sequencing is available

**Choose G3516C Island Mode if:**
- Islanded operation is primary use case
- Good load acceptance needed without full fast-response cost
- Moderate power rating is sufficient

**Choose Standard models if:**
- General-purpose deployment
- Cost optimization is priority
- Specific model features not required
""")

st.header("Load Acceptance Explained")

st.markdown("""
**Load Acceptance** is the maximum percentage of rated power that a generator can accept as an instantaneous step load without causing instability or requiring BESS support.

- **100% acceptance:** Can accept full rated load instantly (G3520 Fast Response)
- **75% acceptance:** Can accept 75% of rated load instantly (G3516C Island Mode)
- **20-30% acceptance:** Can accept 20-30% instantly, requires BESS or sequencing for larger steps (CG170, Standard)
- **16% acceptance:** Very limited first step, designed for multi-step ramping (CG260-16)

**Impact on BESS Sizing:**
- Higher load acceptance = smaller BESS requirement
- Lower load acceptance = larger BESS requirement (or load sequencing needed)
""")

st.header("References")

st.markdown("""
- Caterpillar Generator Library: `data/generators/caterpillar/Caterpillar-Phase1-Library.md`
- Generator Technical Analysis: `data/generators/caterpillar/Caterpillar-Technical-Analysis.md`
- BESS Sizing Calculator: `models/bess-sizing/formulas.md`
""")

