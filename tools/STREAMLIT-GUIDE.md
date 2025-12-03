# Streamlit Web App - User-Friendly Interface

## Overview

The Streamlit web app provides a **much more user-friendly interface** than the Jupyter notebook. It's a clean, modern web interface that doesn't require any Jupyter knowledge.

## Features

✅ **Clean, modern web interface**  
✅ **No Jupyter knowledge required**  
✅ **Step-by-step forms**  
✅ **Real-time calculations**  
✅ **Beautiful visualizations**  
✅ **Easy to use for non-technical users**

## Installation

### Option 1: Install in Jupyter Container

```bash
docker exec jupyter pip install streamlit
```

### Option 2: Install on Host

```bash
pip install streamlit
```

## Running the App

### From Jupyter Container

```bash
docker exec -it jupyter streamlit run /home/jovyan/work/og-ai-inference-research/tools/unified-calculator-app.py --server.port 8501 --server.address 0.0.0.0
```

Then access at: `http://workhorse.local/jupyter/streamlit/` (if Traefik is configured)

### From Host Machine

```bash
cd /srv/projects/og-ai-inference-research/tools
streamlit run unified-calculator-app.py
```

Then access at: `http://localhost:8501`

## Setting Up Traefik Route (Optional)

To access via `http://workhorse.local/calculator/`, add to Traefik:

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.calculator.rule=Host(`workhorse.local`) && PathPrefix(`/calculator`)"
  - "traefik.http.services.calculator.loadbalancer.server.port=8501"
```

## Comparison: Notebook vs Streamlit

| Feature | Jupyter Notebook | Streamlit App |
|---------|------------------|---------------|
| **Ease of Use** | Requires Jupyter knowledge | No special knowledge needed |
| **Interface** | Cluttered widgets | Clean web forms |
| **Navigation** | Scroll through cells | Organized sections |
| **Results** | Mixed with code | Clean dashboard |
| **Visualizations** | Embedded in notebook | Large, clear charts |
| **Mobile Friendly** | No | Yes (responsive) |
| **Sharing** | Share notebook file | Share URL |

## Usage

1. **Open the app** in your browser
2. **Fill in the form:**
   - GPU Configuration (count, type)
   - Generator Configuration (manufacturer, model)
   - Operational Parameters (checkboxes)
   - Data Logistics (optional, expandable)
3. **Click "Calculate"** button
4. **View results** in the dashboard:
   - Generator Risk Assessment
   - BESS Sizing Recommendation
   - Data Logistics Comparison
   - Cost Summary
   - Visualizations
5. **Export results** to CSV (optional)

## Advantages

- **No code visible** - Just clean forms and results
- **Better organization** - Sections are clearly separated
- **Responsive design** - Works on tablets/phones
- **Professional appearance** - Looks like a real web app
- **Easier to share** - Just send a URL
- **Better for presentations** - Clean, professional look

## When to Use Which

- **Use Streamlit** if:
  - You want a user-friendly interface
  - You're sharing with non-technical users
  - You want a professional web app
  - You don't need to modify the code

- **Use Jupyter Notebook** if:
  - You need to modify calculations
  - You want to see/edit the code
  - You're doing development/debugging
  - You need advanced Jupyter features

