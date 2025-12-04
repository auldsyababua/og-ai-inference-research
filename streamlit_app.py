#!/usr/bin/env python3
"""
Unified Off-Grid AI Inference Calculator - Streamlit Web App
A user-friendly web interface for the unified calculator
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
from datetime import datetime

# Page config - MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="Unified Off-Grid AI Inference Calculator",
    page_icon="🔌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Try to connect to Snowflake (optional - falls back to local CSV files if not available)
SNOWFLAKE_AVAILABLE = False
try:
    snowflake_conn = st.connection("snowflake", type="snowflake")
    SNOWFLAKE_AVAILABLE = True
except Exception as e:
    # Snowflake connection not configured or unavailable
    # Will use local CSV files instead
    pass

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3498db;
        margin: 0.5rem 0;
    }
    .risk-green {
        color: #27ae60;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .risk-yellow {
        color: #f39c12;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .risk-red {
        color: #e74c3c;
        font-weight: bold;
        font-size: 1.2rem;
    }
    /* Hide anchor links on headers */
    h3 a, h2 a, h1 a {
        display: none !important;
    }
    /* Hide the anchor icon that appears on hover */
    .stHeadingWithActionElements a {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'results' not in st.session_state:
    st.session_state.results = None

# Documentation page mapping
PARAM_DOC_MAP = {
    # Generator Risk Parameters
    "Per-GPU Power Step": "1_Generator_Risk_Parameters",
    "Correlation Factor": "1_Generator_Risk_Parameters", 
    "Transition Time": "1_Generator_Risk_Parameters",
    
    # Operational Parameters
    "Islanded Operation": "2_Operational_Parameters",
    "Black Start Required": "2_Operational_Parameters",
    "Load Sequencing Available": "2_Operational_Parameters",
    "Risk Tolerance": "2_Operational_Parameters",
    
    # Data Logistics
    "Inbound Data": "4_Data_Logistics",
    "Outbound Data": "4_Data_Logistics",
    "Starlink Terminals": "4_Data_Logistics",
    "Sneakernet Distance": "4_Data_Logistics",
    "Fiber Distance": "4_Data_Logistics",
    
    # GPU Configuration
    "GPU Count": "5_GPU_Types",
    "GPU Type": "5_GPU_Types",
    
    # Generator Configuration
    "Manufacturer": "6_Generator_Models",
    "Model": "6_Generator_Models",
}

def get_doc_link(param_name):
    """Get documentation page link for a parameter"""
    page = PARAM_DOC_MAP.get(param_name)
    if page:
        # Streamlit pages use format: /page_name (without .py extension)
        return f"/{page}"
    return None

def format_help_text(base_text, param_name):
    """Format help text (plain text only - Streamlit help doesn't support links)"""
    # Note: Streamlit's help parameter does NOT support markdown links
    # Links are added separately using st.page_link()
    return base_text

def get_page_path(param_name):
    """Get page file path for st.page_link() - relative to main script"""
    page = PARAM_DOC_MAP.get(param_name)
    if page:
        # st.page_link() expects path relative to main script (unified-calculator-app.py)
        # Since app is in tools/ and pages are in tools/pages/, use relative path
        return f"pages/{page}.py"
    return None

def render_doc_link(param_name, label=None, icon="📖"):
    """Render documentation link using st.page_link() with error handling"""
    page_path = get_page_path(param_name)
    if page_path:
        try:
            # Try st.page_link() first
            st.page_link(page_path, label=label or "Learn more →", icon=icon)
        except (KeyError, Exception) as e:
            # Fallback: Use markdown link if st.page_link() fails
            # This can happen if pages aren't detected yet or path format is wrong
            page_name = PARAM_DOC_MAP.get(param_name, "")
            if page_name:
                # Use the page name as URL (Streamlit's internal format)
                st.markdown(f"[{label or 'Learn more →'}](/{page_name})")

# Title
st.markdown('<div class="main-header">🔌 Unified Off-Grid AI Inference Calculator</div>', unsafe_allow_html=True)
st.markdown("**Version 2.0** | Calculate generator risk, BESS sizing, and data logistics costs")

# Sidebar for navigation and info
with st.sidebar:
    st.header("📋 Navigation")
    st.markdown("""
    **Quick Guide:**
    1. Fill in your deployment configuration
    2. Click "Calculate" at the bottom
    3. View results in the dashboard
    
    **Sections:**
    - GPU Configuration
    - Generator Configuration
    - Operational Parameters
    - Data Logistics (optional)
    """)
    
    st.header("ℹ️ About")
    st.info("""
    This calculator helps you:
    - Assess GPU-generator compatibility
    - Size BESS requirements
    - Compare data transfer costs
    - Estimate total deployment costs
    """)

# Load data and functions (cached)
@st.cache_data
def load_data():
    """Load CSV data and generator specs - supports both local file system and Snowflake stages"""
    BASE_PATH = None
    data = {}
    
    # Try to use Snowflake stage first (when running in Snowflake Streamlit Apps)
    try:
        session = st.connection('snowflake').session()
        st.info("📊 Loading data from Snowflake stage...")
        
        # CSV files in stage (uploaded to @streamlit_apps/models/)
        stage_csv_files = {
            'compat_matrix': '@streamlit_apps/models/gpu-generator-compatibility/GPU-Generator-Compatibility-Matrix-v1.csv',
            'bess_sizing': '@streamlit_apps/models/bess-sizing/BESS-Sizing-v1.csv',
            'data_logistics': '@streamlit_apps/models/data-logistics/DataLogistics-v1.csv'
        }
        
        for name, stage_path in stage_csv_files.items():
            try:
                # Read CSV from stage using Snowpark
                df_snowpark = session.read.option("INFER_SCHEMA", "true").option("HEADER", "true").csv(stage_path)
                data[name] = df_snowpark.to_pandas()
                st.success(f"✓ Loaded {name} from Snowflake stage")
            except Exception as e:
                st.warning(f"⚠️ Could not load {name} from stage: {e}. Trying fallback...")
                # Fallback to local file system
                BASE_PATH = None
                break
        
        # If all CSVs loaded successfully from stage, skip file system fallback
        if len(data) == len(stage_csv_files):
            BASE_PATH = "@streamlit_apps"  # Stage path for reference
            return BASE_PATH, data, GENERATOR_DB, GPU_POWER_PROFILES
            
    except Exception as e:
        # Not running in Snowflake or connection failed - use file system fallback
        st.info("📁 Deployed on Render with embedded data files")
        BASE_PATH = None
    
    # Fallback: Load from local file system
    if BASE_PATH is None:
        # Detect base path
        paths_to_try = [
            os.getcwd(),
            '/home/jovyan/work/og-ai-inference-research',
            '/srv/projects/og-ai-inference-research'
        ]
        
        for path in paths_to_try:
            if os.path.exists(os.path.join(path, 'models')):
                BASE_PATH = path
                break
        
        if BASE_PATH is None:
            BASE_PATH = os.getcwd()
            st.warning(f"⚠️ Could not detect project root, using: {BASE_PATH}")
        
        # Load CSVs from file system
        csv_files = {
            'compat_matrix': 'models/gpu-generator-compatibility/GPU-Generator-Compatibility-Matrix-v1.csv',
            'bess_sizing': 'models/bess-sizing/BESS-Sizing-v1.csv',
            'data_logistics': 'models/data-logistics/DataLogistics-v1.csv'
        }
        
        for name, rel_path in csv_files.items():
            if name not in data:  # Only load if not already loaded from stage
                file_path = os.path.join(BASE_PATH, rel_path)
                try:
                    if os.path.exists(file_path):
                        data[name] = pd.read_csv(file_path)
                    else:
                        data[name] = pd.DataFrame()
                except Exception as e:
                    st.error(f"Error loading {name}: {e}")
                    data[name] = pd.DataFrame()
    
    # Generator database
    GENERATOR_DB = {
        'Caterpillar': {
            'G3520_Fast_Response': {
                'power_kw': 2500,
                'load_acceptance_pct': 100,
                'type': 'Natural_Gas_Fast_Response',
                'h_eff_s': 3.0,
                'r_eff_pu': 0.04,
                'max_step_pct': 100
            },
            'CG170-16': {
                'power_kw': 1560,
                'load_acceptance_pct': 20,
                'type': 'Natural_Gas',
                'h_eff_s': 5.0,
                'r_eff_pu': 0.04,
                'max_step_pct': 20
            },
            'CG260-16': {
                'power_kw': 4300,
                'load_acceptance_pct': 16,
                'type': 'Natural_Gas_CG260',
                'h_eff_s': 5.0,
                'r_eff_pu': 0.05,
                'max_step_pct': 16
            },
            'G3516C_Island_Mode': {
                'power_kw': 1660,
                'load_acceptance_pct': 75,
                'type': 'Natural_Gas_Fast_Response',
                'h_eff_s': 4.0,
                'r_eff_pu': 0.04,
                'max_step_pct': 75
            }
        },
        'Standard': {
            'Natural_Gas_Standard': {
                'power_kw': 1000,
                'load_acceptance_pct': 30,
                'type': 'Natural_Gas',
                'h_eff_s': 4.0,
                'r_eff_pu': 0.04,
                'max_step_pct': 30
            },
            'Diesel_Standard': {
                'power_kw': 1000,
                'load_acceptance_pct': 70,
                'type': 'Diesel',
                'h_eff_s': 3.0,
                'r_eff_pu': 0.04,
                'max_step_pct': 70
            }
        }
    }
    
    GPU_POWER_PROFILES = {
        'H100_PCIe': 3.5,
        'H100_SXM': 7.0,
        'A100_PCIe': 2.5
    }
    
    return BASE_PATH, data, GENERATOR_DB, GPU_POWER_PROFILES

BASE_PATH, data, GENERATOR_DB, GPU_POWER_PROFILES = load_data()

# Import calculation functions (simplified versions)
def calculate_generator_risk(n_gpus, delta_p_gpu, correlation_c, delta_t, p_rated_gen, h_eff, r_eff, f_nom, max_step_pct):
    """Calculate generator risk assessment"""
    delta_p_cluster = correlation_c * n_gpus * delta_p_gpu
    ramp_rate = delta_p_cluster / delta_t if delta_t > 0 else 0
    step_fraction = delta_p_cluster / p_rated_gen if p_rated_gen > 0 else 0
    delta_f_over_f = -r_eff * step_fraction
    s_base = p_rated_gen
    rocof_pu_per_s = -delta_p_cluster / (2 * h_eff * s_base) if (h_eff * s_base) > 0 else 0
    rocof_hz_per_s = rocof_pu_per_s * f_nom
    step_within_limit = (step_fraction * 100) < max_step_pct
    step_pct = step_fraction * 100
    
    if step_pct < max_step_pct * 0.5:
        risk_level = 'GREEN'
    elif step_pct < max_step_pct:
        risk_level = 'YELLOW'
    else:
        risk_level = 'RED'
    
    return {
        'delta_p_cluster_kw': delta_p_cluster,
        'ramp_rate_kw_per_s': ramp_rate,
        'step_fraction': step_fraction,
        'delta_f_over_f_pu': delta_f_over_f,
        'delta_f_hz': delta_f_over_f * f_nom,
        'rocof_hz_per_s': rocof_hz_per_s,
        'step_within_limit': step_within_limit,
        'risk_level': risk_level,
        'step_pct': step_pct
    }

def recommend_bess(n_gpu, p_gpu, p_gen, gen_load_acceptance_pct, gen_type,
                   black_start, load_sequencing, risk_tolerance='Medium'):
    """Recommend BESS type and sizing (assumes islanded/off-grid operation)"""
    gpu_cluster_power = n_gpu * p_gpu
    max_load_step = gpu_cluster_power
    gen_load_acceptance_kw = p_gen * (gen_load_acceptance_pct / 100)
    load_step_magnitude = max_load_step - gen_load_acceptance_kw

    # Rule 1: Small cluster with fast-response generator + high risk tolerance → No BESS
    if (n_gpu <= 4 and
        ('Fast_Response' in gen_type or 'Rich_Burn' in gen_type) and
        risk_tolerance == 'High'):
        bess_type = 'No_BESS'
        bess_power_kw = 0
        bess_energy_kwh = 0
        bess_cost_usd = 0
        rationale = f"Small cluster (≤4 GPUs) with fast-response generator. No-BESS viable with proper controls."

    # Rule 2: AGGRESSIVE load sequencing + High risk → 50-100kW Buffer BESS
    # (Load sequencing reduces effective step to 50-100kW regardless of generator capacity)
    elif load_sequencing and risk_tolerance == 'High':
        bess_type = 'Buffer'
        bess_power_kw = min(100, max(50, gpu_cluster_power * 0.05))
        bess_energy_kwh = bess_power_kw * 1.0
        bess_cost_usd = 30000 + (bess_power_kw - 50) * 500
        rationale = f"Phase-stepped GPU startup (GPUs starting in sequence rather than all at once) + aggressive load sequencing limits effective step to 50-100kW. Buffer BESS sufficient for transient bridge (islanded)."

    # Rule 3: MODERATE load sequencing (Medium/Low risk) → 150-200kW Grid-Forming BESS
    # (Load sequencing reduces effective step to 100-200kW)
    elif load_sequencing:
        bess_type = 'Grid_Forming'
        bess_power_kw = min(200, max(150, gpu_cluster_power * 0.1))
        bess_energy_kwh = max(100, bess_power_kw * 0.5)
        bess_cost_usd = 100000 + (bess_power_kw - 150) * 600
        rationale = f"Load sequencing reduces effective step to 100-200kW. Grid-Forming BESS (150-200kW) required for islanded frequency stability and transient response."

    # Rule 4: NO load sequencing + Generator CAN handle unmanaged step → 400-600kW Grid-Forming BESS
    # (Still need large BESS for islanded frequency stability despite generator capacity)
    elif load_step_magnitude <= 0:
        bess_type = 'Grid_Forming'
        bess_power_kw = max(400, min(600, gpu_cluster_power * 0.5))
        bess_energy_kwh = max(100, bess_power_kw * 0.25)
        bess_cost_usd = 350000 + (bess_power_kw - 400) * 750
        rationale = f"{gen_type} generator ({gen_load_acceptance_pct}% acceptance) can handle {max_load_step:.1f}kW step, but islanded operation requires 400-600kW Grid-Forming BESS for frequency regulation, voltage support, and fast transient response without grid connection."

    # Rule 5: NO load sequencing + Generator CANNOT handle unmanaged step → 400-600kW+ Grid-Forming BESS
    # (Need large BESS to handle both the step AND provide islanded frequency support)
    else:
        bess_power_kw = min(600, max(400, load_step_magnitude * 1.2))
        bess_energy_kwh = max(100, bess_power_kw * 0.25)
        bess_cost_usd = 350000 + (bess_power_kw - 400) * 750
        bess_type = 'Grid_Forming'
        if 'CG260' in gen_type:
            rationale = f"{gen_type} ({gen_load_acceptance_pct}% first step) cannot handle {max_load_step:.1f}kW step. Grid-forming BESS (400-600kW) required for islanded stability."
        else:
            rationale = f"{gen_type} generator ({gen_load_acceptance_pct}% acceptance) cannot handle {max_load_step:.1f}kW GPU step. Grid-forming BESS (400-600kW) required for islanded stability."

    return {
        'bess_type': bess_type,
        'bess_power_kw': bess_power_kw,
        'bess_energy_kwh': bess_energy_kwh,
        'bess_cost_usd': bess_cost_usd,
        'rationale': rationale,
        'load_step_magnitude_kw': load_step_magnitude,
        'gpu_cluster_power_kw': gpu_cluster_power,
        'gen_load_acceptance_kw': gen_load_acceptance_kw
    }

def compare_data_modes(w_inbound_tb, w_outbound_tb, n_starlink, c_starlink, b_starlink, 
                       eta_starlink, d_sneakernet, c_sneakernet, t_sneakernet, cap_sneakernet,
                       d_fiber, c_fiber, y_fiber, opex_fiber):
    """Compare data transfer modes"""
    total_tb = w_inbound_tb + w_outbound_tb
    seconds_per_month = 30.44 * 24 * 3600
    starlink_usable_tb_per_terminal = (b_starlink * eta_starlink * seconds_per_month) / (8 * 1e6)
    starlink_total_capacity = n_starlink * starlink_usable_tb_per_terminal
    starlink_total_cost = n_starlink * c_starlink
    starlink_cost_per_tb = starlink_total_cost / total_tb if total_tb > 0 else float('inf')
    starlink_can_meet = starlink_total_capacity >= total_tb
    
    sneakernet_total_capacity = t_sneakernet * cap_sneakernet
    sneakernet_cost_per_trip = 2 * d_sneakernet * c_sneakernet
    sneakernet_total_cost = t_sneakernet * sneakernet_cost_per_trip
    sneakernet_cost_per_tb = sneakernet_total_cost / total_tb if total_tb > 0 else float('inf')
    sneakernet_can_meet = sneakernet_total_capacity >= total_tb
    
    fiber_total_capex = d_fiber * c_fiber
    fiber_monthly_capex = fiber_total_capex / (y_fiber * 12)
    fiber_total_cost = fiber_monthly_capex + opex_fiber
    fiber_cost_per_tb = fiber_total_cost / total_tb if total_tb > 0 else float('inf')
    
    # Filter out infinite costs (when total_tb = 0)
    costs = []
    if starlink_can_meet and not np.isinf(starlink_cost_per_tb):
        costs.append(('Starlink', starlink_cost_per_tb))
    if sneakernet_can_meet and not np.isinf(sneakernet_cost_per_tb):
        costs.append(('Sneakernet', sneakernet_cost_per_tb))
    if not np.isinf(fiber_cost_per_tb):
        costs.append(('Fiber', fiber_cost_per_tb))
    
    if costs:
        costs.sort(key=lambda x: x[1])
        recommended_mode = costs[0][0]
        # Calculate savings only if we have at least 2 valid costs
        if len(costs) > 1:
            cost_savings = costs[1][1] - costs[0][1]
            # Handle case where both might be inf (shouldn't happen after filtering, but safety check)
            if np.isinf(cost_savings) or np.isnan(cost_savings):
                cost_savings = 0
        else:
            cost_savings = 0
    else:
        # No valid modes (either can't meet demand or all costs are infinite)
        recommended_mode = 'None'
        cost_savings = 0
    
    return {
        'total_tb_per_month': total_tb,
        'starlink': {
            'capacity_tb': starlink_total_capacity,
            'can_meet': starlink_can_meet,
            'cost_per_month': starlink_total_cost,
            'cost_per_tb': starlink_cost_per_tb
        },
        'sneakernet': {
            'capacity_tb': sneakernet_total_capacity,
            'can_meet': sneakernet_can_meet,
            'cost_per_month': sneakernet_total_cost,
            'cost_per_tb': sneakernet_cost_per_tb
        },
        'fiber': {
            'capex': fiber_total_capex,
            'monthly_capex': fiber_monthly_capex,
            'cost_per_month': fiber_total_cost,
            'cost_per_tb': fiber_cost_per_tb
        },
        'recommended_mode': recommended_mode,
        'cost_savings_vs_next_best': cost_savings
    }

# Input Form
st.markdown('<div class="section-header">📝 Deployment Configuration</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🔌 GPU Configuration")
    gpu_count = st.number_input("GPU Count", min_value=1, max_value=1000, value=142, step=1,
                                help=format_help_text("Total number of GPUs in the cluster. Used to calculate total cluster power and load step magnitude.", "GPU Count"))
    render_doc_link("GPU Count", label="Learn more about GPU Count →", icon="📖")
    gpu_type = st.selectbox("GPU Type", options=list(GPU_POWER_PROFILES.keys()), index=0,
                            help=format_help_text("GPU model type. Different models have different power ratings and characteristics. See documentation for detailed comparisons.", "GPU Type"))
    render_doc_link("GPU Type", label="Learn more about GPU Types →", icon="📖")
    gpu_power = GPU_POWER_PROFILES[gpu_type]
    st.info(f"**GPU Power:** {gpu_power} kW (auto-filled)")

with col2:
    st.subheader("⚡ Generator Configuration")
    gen_manufacturer = st.selectbox("Manufacturer", options=list(GENERATOR_DB.keys()), index=0,
                                    help=format_help_text("Generator manufacturer. Different manufacturers offer different models with varying power ratings, efficiency, and load acceptance capabilities.", "Manufacturer"))
    render_doc_link("Manufacturer", label="Learn more about Generator Models →", icon="📖")
    gen_models = list(GENERATOR_DB[gen_manufacturer].keys())
    gen_model = st.selectbox("Model", options=gen_models, index=0,
                            help=format_help_text("Specific generator model. Each model has different power ratings, load acceptance percentages, and dynamic response characteristics. See documentation for detailed model comparisons.", "Model"))
    render_doc_link("Model", label="Learn more about Generator Models →", icon="📖")
    
    # Auto-fill generator power
    gen_specs = GENERATOR_DB[gen_manufacturer][gen_model]
    gen_power = gen_specs['power_kw']
    st.info(f"**Generator Power:** {gen_power} kW (auto-filled)")
    st.caption(f"Load Acceptance: {gen_specs['load_acceptance_pct']}%")

with col3:
    st.subheader("⚙️ Operational Parameters")
    st.info("**Note:** All deployments are assumed to be islanded (off-grid) operation.")
    black_start = st.checkbox("Black Start Required", value=False,
                             help=format_help_text("Generator must be able to start without external power source. Affects BESS sizing requirements.", "Black Start Required"))
    load_sequencing = st.checkbox("Load Sequencing Available", value=False,
                                 help=format_help_text("GPU cluster can be powered on gradually in stages (phase-stepped startup), reducing initial load step magnitude. Enables smaller BESS if implemented aggressively.", "Load Sequencing Available"))
    render_doc_link("Load Sequencing Available", label="Learn more about Operational Parameters →", icon="📖")
    risk_tolerance = st.selectbox("Risk Tolerance", options=['Low', 'Medium', 'High'], index=1,
                                 help=format_help_text("Acceptable risk level for generator stability. Low = conservative (larger BESS), High = aggressive (smaller/no BESS with load sequencing).", "Risk Tolerance"))

# Advanced Parameters (collapsible)
with st.expander("🔧 Advanced Generator Risk Parameters"):
    col1, col2, col3 = st.columns(3)
    with col1:
        delta_p_gpu = st.number_input("Per-GPU Power Step (kW)", min_value=0.1, max_value=10.0, value=0.25, step=0.05,
                                      help=format_help_text("Power change per GPU during state transitions (e.g., idle to full load). Typical values: 0.25-0.5 kW for H100 GPUs. Higher values increase generator stress.", "Per-GPU Power Step"))
    with col2:
        correlation = st.slider("Correlation Factor", min_value=0.0, max_value=1.0, value=0.7, step=0.1,
                               help=format_help_text("Synchronization factor for GPU power steps (0.0 = fully uncorrelated, 1.0 = perfectly synchronized). Lower values reduce effective cluster power step. Typical: 0.6-0.8 for coordinated workloads.", "Correlation Factor"))
    with col3:
        delta_t = st.number_input("Transition Time (s)", min_value=0.1, max_value=10.0, value=1.0, step=0.1,
                                 help=format_help_text("Time duration over which the power step occurs. Shorter times = higher ramp rates = greater generator stress. Typical: 0.5-2.0 seconds depending on workload startup characteristics.", "Transition Time"))
    # Add documentation link for advanced parameters
    render_doc_link("Per-GPU Power Step", label="Learn more about Generator Risk Parameters →", icon="📖")

# Data Logistics (collapsible)
with st.expander("📡 Data Logistics (Optional)"):
    col1, col2 = st.columns(2)
    with col1:
        inbound_tb = st.number_input("Inbound Data (TB/month)", min_value=0.0, value=400.0, step=10.0,
                                     help=format_help_text("Monthly inbound data volume: model weights, training datasets, and other input data transferred to the site.", "Inbound Data"))
        outbound_tb = st.number_input("Outbound Data (TB/month)", min_value=0.0, value=50.0, step=10.0,
                                      help=format_help_text("Monthly outbound data volume: inference results, embeddings, and other output data transferred from the site.", "Outbound Data"))
        starlink_terminals = st.number_input("Starlink Terminals", min_value=1, value=15, step=1,
                                            help=format_help_text("Number of Starlink satellite terminals. Each terminal provides ~100-150 Mbps effective bandwidth. Note: 2025 pricing uses data buckets with throttling after cap.", "Starlink Terminals"))
    with col2:
        sneakernet_distance = st.number_input("Sneakernet Distance (miles)", min_value=0.0, value=200.0, step=10.0,
                                              help=format_help_text("One-way distance to site for physical data transport. Typical capacity: 120 TB per trip using 6× 20TB drives with RAID-Z2.", "Sneakernet Distance"))
        fiber_distance = st.number_input("Fiber Distance (miles)", min_value=0.0, value=10.0, step=1.0,
                                        help=format_help_text("Distance to nearest Point of Presence (POP) for fiber connection. Build costs: $50K/mile (aerial) to $150K/mile (rocky terrain).", "Fiber Distance"))
    # Add documentation link for data logistics
    render_doc_link("Inbound Data", label="Learn more about Data Logistics →", icon="📖")

# Calculate Button
st.markdown("---")
calculate_button = st.button("🚀 Calculate", type="primary", use_container_width=True)

# Calculations
if calculate_button:
    with st.spinner("Running calculations..."):
        # Get generator specs
        gen_load_acceptance_pct = gen_specs['load_acceptance_pct']
        gen_type = gen_specs['type']
        h_eff = gen_specs['h_eff_s']
        r_eff = gen_specs['r_eff_pu']
        max_step_pct = gen_specs['max_step_pct']
        
        # 1. Generator Risk
        risk_results = calculate_generator_risk(
            gpu_count, delta_p_gpu, correlation, delta_t,
            gen_power, h_eff, r_eff, 60, max_step_pct
        )
        
        # 2. BESS Recommendation
        bess_results = recommend_bess(
            gpu_count, gpu_power, gen_power, gen_load_acceptance_pct,
            gen_type, black_start, load_sequencing, risk_tolerance
        )
        
        # 3. Data Logistics
        data_results = compare_data_modes(
            inbound_tb, outbound_tb, starlink_terminals, 290, 100, 0.6,
            sneakernet_distance, 1.2, 4, 120,
            fiber_distance, 50000, 20, 208
        )
        
        # Store results
        st.session_state.results = {
            'generator_risk': risk_results,
            'bess': bess_results,
            'data_logistics': data_results,
            'inputs': {
                'gpu_count': gpu_count,
                'gpu_type': gpu_type,
                'gpu_power': gpu_power,
                'gen_manufacturer': gen_manufacturer,
                'gen_model': gen_model,
                'gen_power': gen_power
            }
        }

# Display Results
if st.session_state.results:
    results = st.session_state.results
    
    st.markdown("---")
    st.markdown('<div class="section-header">📊 Results Dashboard</div>', unsafe_allow_html=True)
    
    # Generator Risk
    st.subheader("🔌 Generator Risk Assessment")
    risk = results['generator_risk']
    
    risk_colors = {'GREEN': '🟢', 'YELLOW': '🟡', 'RED': '🔴'}
    risk_icon = risk_colors.get(risk['risk_level'], '⚪')
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Risk Level", f"{risk_icon} {risk['risk_level']}")
    with col2:
        st.metric("Power Step", f"{risk['delta_p_cluster_kw']:.1f} kW")
    with col3:
        st.metric("Step Fraction", f"{risk['step_pct']:.2f}%")
    with col4:
        st.metric("Within Limits", "✓ Yes" if risk['step_within_limit'] else "✗ No")
    
    st.caption(f"Ramp Rate: {risk['ramp_rate_kw_per_s']:.2f} kW/s | RoCoF: {risk['rocof_hz_per_s']:.4f} Hz/s")
    
    # BESS Recommendation
    st.subheader("🔋 BESS Sizing Recommendation")
    bess = results['bess']
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("BESS Type", bess['bess_type'])
    with col2:
        st.metric("Power Rating", f"{bess['bess_power_kw']:.1f} kW")
    with col3:
        st.metric("Energy Capacity", f"{bess['bess_energy_kwh']:.1f} kWh")
    with col4:
        st.metric("Estimated Cost", f"${bess['bess_cost_usd']:,.0f}")
    
    st.info(f"**Rationale:** {bess['rationale']}")
    
    # Data Logistics
    st.subheader("📡 Data Logistics Cost Comparison")
    data = results['data_logistics']
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Starlink Cost/TB", f"${data['starlink']['cost_per_tb']:.2f}", 
                 delta="Can meet" if data['starlink']['can_meet'] else "Cannot meet")
    with col2:
        st.metric("Sneakernet Cost/TB", f"${data['sneakernet']['cost_per_tb']:.2f}",
                 delta="Can meet" if data['sneakernet']['can_meet'] else "Cannot meet")
    with col3:
        st.metric("Fiber Cost/TB", f"${data['fiber']['cost_per_tb']:.2f}", delta="Unlimited")
    
    if data['recommended_mode'] != 'None':
        st.success(f"✅ **Recommended:** {data['recommended_mode']} (Savings: ${data['cost_savings_vs_next_best']:.2f}/TB vs next best)")
    else:
        st.error("⚠️ **Warning:** No data transfer mode can meet demand requirements")
    
    # Cost Summary
    st.subheader("💰 Cost Summary")
    mode_lower = data['recommended_mode'].lower()
    if mode_lower == 'starlink':
        data_monthly_cost = data['starlink']['cost_per_month']
    elif mode_lower == 'sneakernet':
        data_monthly_cost = data['sneakernet']['cost_per_month']
    elif mode_lower == 'fiber':
        data_monthly_cost = data['fiber']['cost_per_month']
    else:
        data_monthly_cost = 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("BESS CapEx", f"${bess['bess_cost_usd']:,.0f}")
    with col2:
        st.metric("Data OpEx (Monthly)", f"${data_monthly_cost:,.0f}")
    with col3:
        st.metric("Data OpEx (Annual)", f"${data_monthly_cost * 12:,.0f}")
    
    # Visualizations
    st.subheader("📈 Visualizations")
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Power profile
    ax1 = axes[0]
    categories = ['GPU Cluster', 'Generator', 'BESS']
    powers = [bess['gpu_cluster_power_kw'], results['inputs']['gen_power'], bess['bess_power_kw']]
    colors = ['#4CAF50', '#2196F3', '#FF9800']
    bars = ax1.bar(categories, powers, color=colors)
    ax1.set_ylabel('Power (kW)')
    ax1.set_title('Power Profile Comparison')
    ax1.grid(True, alpha=0.3)
    for bar, power in zip(bars, powers):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height, f'{power:.0f} kW', ha='center', va='bottom')
    
    # Data logistics cost
    ax2 = axes[1]
    modes = ['Starlink', 'Sneakernet', 'Fiber']
    costs_per_tb = [
        data['starlink']['cost_per_tb'] if data['starlink']['can_meet'] else np.nan,
        data['sneakernet']['cost_per_tb'] if data['sneakernet']['can_meet'] else np.nan,
        data['fiber']['cost_per_tb']
    ]
    # Filter out NaN and infinite values
    valid_modes = [m for m, c in zip(modes, costs_per_tb) if not np.isnan(c) and not np.isinf(c)]
    valid_costs = [c for c in costs_per_tb if not np.isnan(c) and not np.isinf(c)]
    
    bars2 = ax2.bar(valid_modes, valid_costs, color=['#9C27B0', '#00BCD4', '#8BC34A'])
    ax2.set_ylabel('Cost per TB ($)')
    ax2.set_title('Data Transfer Cost Comparison')
    ax2.grid(True, alpha=0.3)
    for bar, cost in zip(bars2, valid_costs):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height, f'${cost:.2f}', ha='center', va='bottom')
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # Export option
    st.markdown("---")
    if st.button("💾 Export Results to CSV"):
        export_data = {
            'Timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            'GPU_Count': [gpu_count],
            'GPU_Type': [gpu_type],
            'GPU_Power_kW': [gpu_power],
            'Generator_Model': [gen_model],
            'Generator_Power_kW': [gen_power],
            'Risk_Level': [risk['risk_level']],
            'BESS_Type': [bess['bess_type']],
            'BESS_Cost_USD': [bess['bess_cost_usd']],
            'Data_Recommended_Mode': [data['recommended_mode']]
        }
        df_export = pd.DataFrame(export_data)
        csv = df_export.to_csv(index=False)
        st.download_button("Download CSV", csv, "unified_calculator_results.csv", "text/csv")

