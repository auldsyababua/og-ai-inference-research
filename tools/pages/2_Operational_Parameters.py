#!/usr/bin/env python3
"""
Operational Parameters Documentation
Detailed documentation for operational parameters affecting BESS sizing
"""

import streamlit as st
import os
import sys

st.set_page_config(
    page_title="Operational Parameters - Documentation",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ Operational Parameters Documentation")

st.markdown("""
This page provides detailed documentation for the **Operational Parameters** that affect BESS sizing decisions.
These parameters describe how your deployment operates and what capabilities are required.
""")

# Navigation
st.markdown("---")
st.markdown("[← Back to Calculator](/unified-calculator-app)")
st.markdown("---")

st.header("Parameter Descriptions")

st.subheader("Islanded Operation")
st.markdown("""
**Type:** Boolean (checkbox)  
**Default:** True

**Description:**  
Indicates whether the generator operates independently without a grid connection.

**Impact on BESS Sizing:**
- **Islanded = True:** Requires **Grid-Forming BESS** for frequency stability
  - Generator cannot rely on grid for frequency support
  - BESS must provide synthetic inertia and frequency regulation
  - Minimum BESS power: 400 kW (even if generator can handle load step)
  
- **Islanded = False:** May use **Buffer BESS** if generator can handle load step
  - Grid-connected operation provides frequency support
  - BESS only needed for transient ride-through
  - Smaller BESS sufficient (50-100 kW)

**When to Use:**
- ✅ Remote sites without grid access
- ✅ Microgrid deployments
- ✅ Backup power systems
- ❌ Grid-tied installations
""")

st.subheader("Black Start Required")
st.markdown("""
**Type:** Boolean (checkbox)  
**Default:** False

**Description:**  
Indicates whether the generator must be able to start without an external power source.

**Impact on BESS Sizing:**
- **Black Start = True:** Requires **Grid-Forming BESS**
  - BESS must provide initial power to start generator
  - Generator cannot start without external power source
  - BESS must have sufficient energy capacity for startup sequence
  
- **Black Start = False:** Standard BESS sizing applies
  - Generator can start from grid or other power source
  - No additional BESS capacity required for startup

**When to Use:**
- ✅ Primary power systems (no backup generator)
- ✅ Remote sites without grid access
- ✅ Critical infrastructure requiring autonomous operation
- ❌ Sites with grid connection or backup generators
""")

st.subheader("Load Sequencing Available")
st.markdown("""
**Type:** Boolean (checkbox)  
**Default:** False

**Description:**  
Indicates whether the GPU cluster can be powered on gradually in stages, reducing the initial load step magnitude.

**Impact on BESS Sizing:**
- **Load Sequencing = True:** May allow **Buffer BESS** instead of Grid-Forming
  - Effective load step reduced by 50-70%
  - If reduced step < 200 kW, Buffer BESS sufficient
  - Reduces BESS cost from $350K+ to $30K-$60K
  
- **Load Sequencing = False:** Uses full cluster power step
  - Conservative worst-case assumption
  - Entire cluster transitions simultaneously
  - Requires larger BESS if generator cannot handle step

**How It Works:**
Load sequencing powers on GPUs in stages:
1. Stage 1: Start 25% of GPUs
2. Wait for generator to stabilize
3. Stage 2: Start next 25% of GPUs
4. Repeat until all GPUs are online

**When to Use:**
- ✅ Workloads that can tolerate gradual startup
- ✅ GPU clusters with sequencing controllers
- ✅ Deployments with flexible startup requirements
- ❌ Workloads requiring immediate full power
""")

st.subheader("Risk Tolerance")
st.markdown("""
**Type:** Dropdown (Low, Medium, High)  
**Default:** Medium

**Description:**  
Acceptable risk level for generator stability. Affects BESS sizing conservatism.

**Impact on BESS Sizing:**

**Low Risk Tolerance:**
- Most conservative approach
- Larger BESS with higher safety margins
- May recommend Grid-Forming BESS even when Buffer might work
- Best for critical deployments

**Medium Risk Tolerance:**
- Balanced approach (default)
- Standard BESS sizing formulas
- Appropriate for most deployments

**High Risk Tolerance:**
- Aggressive approach
- Smaller BESS or No-BESS possible
- Only for small clusters (≤4 GPUs) with fast-response generators
- May accept higher generator stress

**When to Use:**
- **Low:** Critical infrastructure, high-value deployments
- **Medium:** Standard deployments (recommended default)
- **High:** Experimental deployments, cost-sensitive projects
""")

st.header("BESS Type Decision Logic")

st.markdown("""
The operational parameters interact with generator capabilities to determine BESS type:

1. **No-BESS:** Only if all conditions met:
   - ≤4 GPUs
   - Fast-response generator
   - Not islanded
   - High risk tolerance

2. **Buffer BESS:** If:
   - Generator can handle load step, OR
   - Load sequencing reduces step < 200 kW

3. **Grid-Forming BESS:** If:
   - Generator cannot handle load step, AND
   - Islanded operation OR black-start required
""")

st.header("References")

st.markdown("""
- BESS Sizing Calculator: `models/bess-sizing/formulas.md`
- BESS Decision Analysis: `research/bess-decision-analysis/BESS-DECISION-CONSOLIDATED-ANALYSIS.md`
- ISO 8528-5: Performance classes for generator sets
""")

