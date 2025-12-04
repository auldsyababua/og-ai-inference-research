#!/usr/bin/env python3
"""
GPU Types Documentation
Detailed documentation for GPU types and their power characteristics
"""

import streamlit as st
import os
import sys

st.set_page_config(
    page_title="GPU Types - Documentation",
    page_icon="🔌",
    layout="wide"
)

st.title("🔌 GPU Types Documentation")

st.markdown("""
This page provides detailed documentation for **GPU types** available in the calculator,
including power ratings, characteristics, and use cases.
""")

# Navigation
st.markdown("---")
st.markdown("[← Back to Calculator](/unified-calculator-app)")
st.markdown("---")

# Load GPU power profiles
GPU_POWER_PROFILES = {
    'H100_PCIe': 3.5,
    'H100_SXM': 7.0,
    'A100_PCIe': 2.5
}

st.header("Available GPU Types")

st.subheader("H100 PCIe")
st.markdown("""
**Power Rating:** 3.5 kW per GPU  
**TDP:** 350W (default), 310W (down-rated mode)  
**Memory:** 80GB HBM2e  
**Memory Bandwidth:** 2.0 TB/s  
**Form Factor:** Full-height, full-length (FHFL) dual-slot PCIe card

**Characteristics:**
- **Steady-state inference power:** 220-260W (63-74% of TDP)
- **Idle power (warm):** 60-80W (17-23% of TDP)
- **Idle power (cold):** 35-45W (10-13% of TDP)
- **Peak power:** 310-350W (89-100% of TDP)
- **Power step (idle→inference):** 0.2-0.25 kW

**Use Cases:**
- Standard server deployments
- Power-efficient off-grid deployments
- Workloads requiring PCIe form factor
- Deployments without liquid cooling infrastructure

**Advantages:**
- Lower power consumption than SXM variant
- Standard PCIe form factor (easier integration)
- Suitable for air-cooled servers
- Lower cost per GPU

**Considerations:**
- Lower peak performance than SXM variant
- Requires adequate server airflow for cooling
""")

st.subheader("H100 SXM")
st.markdown("""
**Power Rating:** 7.0 kW per GPU  
**TDP:** 700W  
**Memory:** 80GB HBM2e  
**Memory Bandwidth:** 3.0 TB/s  
**Form Factor:** SXM5 module (requires specialized server)

**Characteristics:**
- **Steady-state inference power:** 500-600W (71-86% of TDP)
- **Idle power:** ~100-150W
- **Peak power:** 650-700W (93-100% of TDP)
- **Power step:** ~0.5-0.6 kW

**Use Cases:**
- High-throughput inference workloads
- Training workloads
- Maximum performance requirements
- Deployments with liquid cooling infrastructure

**Advantages:**
- Higher peak performance than PCIe variant
- Better memory bandwidth (3.0 TB/s vs 2.0 TB/s)
- Optimized for high-performance computing

**Considerations:**
- Requires liquid cooling infrastructure
- Higher power consumption (2× PCIe variant)
- Requires specialized server platforms (DGX, HGX)
- Higher cost per GPU
""")

st.subheader("A100 PCIe")
st.markdown("""
**Power Rating:** 2.5 kW per GPU  
**TDP:** 250W (default), 300W (max)  
**Memory:** 40GB or 80GB HBM2  
**Memory Bandwidth:** 1.9 TB/s  
**Form Factor:** Full-height, full-length (FHFL) dual-slot PCIe card

**Characteristics:**
- **Steady-state inference power:** 150-200W (60-80% of TDP)
- **Idle power:** 30-50W
- **Peak power:** 250-300W
- **Power step:** ~0.15-0.2 kW

**Use Cases:**
- Legacy deployments
- Cost-sensitive deployments
- Lower power density requirements
- Workloads that don't require H100 performance

**Advantages:**
- Lower power consumption
- Lower cost (if available on secondary market)
- Proven reliability
- Good performance for many inference workloads

**Considerations:**
- Lower performance than H100
- Older architecture
- May have limited availability
""")

st.header("Power Profile Comparison")

import pandas as pd

comparison_data = {
    'GPU Type': ['H100 PCIe', 'H100 SXM', 'A100 PCIe'],
    'Power Rating (kW)': [3.5, 7.0, 2.5],
    'TDP (W)': [350, 700, 250],
    'Typical Inference Power (W)': ['220-260', '500-600', '150-200'],
    'Idle Power (W)': ['60-80', '100-150', '30-50'],
    'Memory (GB)': [80, 80, '40/80'],
    'Memory Bandwidth (TB/s)': [2.0, 3.0, 1.9],
}

df = pd.DataFrame(comparison_data)
st.dataframe(df, use_container_width=True, hide_index=True)

st.header("Selection Guidelines")

st.markdown("""
**Choose H100 PCIe if:**
- You need H100 performance but want standard server integration
- Power efficiency is a priority
- You don't have liquid cooling infrastructure
- Cost per GPU is a consideration

**Choose H100 SXM if:**
- You need maximum performance
- You have liquid cooling infrastructure
- High-throughput workloads are primary use case
- Cost per GPU is less of a concern

**Choose A100 PCIe if:**
- H100 performance is not required
- Cost optimization is critical
- Lower power density is needed
- Legacy compatibility is required
""")

st.header("References")

st.markdown("""
- GPU Power Profiles: `data/gpu-profiles/GPU-Power-Profiles.md`
- GPU Phase Research: `research/gpu-phase-research/CONSOLIDATED-SUMMARY.md`
- NVIDIA Documentation: `docs/nvidia-manuals/`
""")

