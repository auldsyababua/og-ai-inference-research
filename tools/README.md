# Unified Calculator Tools

**Location:** `tools/unified-calculator.ipynb`  
**Version:** 1.0  
**Last Updated:** 2025-12-02

---

## Overview

The Unified Calculator is a single Jupyter notebook that consolidates all 6 calculators into one interactive interface:

1. **Generator Risk Calculator** - Assess GPU cluster compatibility with generators
2. **BESS Sizing Calculator** - Determine Battery Energy Storage System requirements
3. **GPU-Generator Compatibility Matrix** - Quick reference for compatible configurations
4. **Data Logistics Calculator** - Compare Starlink, Sneakernet, and Fiber costs
5. **Bitcoin Miner Integration** - (Optional) Miner load balancing
6. **Multi-step Ramp Simulator** - (Optional) CG260 multi-step ramp modeling

---

## Quick Start

### ⚠️ New to Jupyter Notebooks?
**Start here:** Read [`HOW-TO-USE-NOTEBOOK.md`](HOW-TO-USE-NOTEBOOK.md) for a complete beginner's guide with step-by-step instructions, screenshots, and troubleshooting.

### Access the Notebook

1. **Open JupyterLab:** Navigate to `http://workhorse.local/jupyter/lab/`
2. **Authenticate:** Enter Jupyter token (get with: `docker exec jupyter jupyter server list`)
3. **Navigate to:** `work/og-ai-inference-research/tools/` in the file browser
4. **Open:** `unified-calculator.ipynb`

**Direct URL:** `http://workhorse.local/jupyter/lab/tree/work/og-ai-inference-research/tools/unified-calculator.ipynb`

### Run the Calculator

#### First Time Setup:
1. **Run all cells** sequentially (Cell 1 → Cell 8)
   - Click `Run` → `Run All Cells` from the menu, OR
   - Click each cell and press `Shift + Enter` one by one
   - Wait for each cell to finish before running the next
   - **Note:** Cell 9 is empty and can be skipped

#### Every Time You Use It:
1. **Fill in inputs** using the interactive widgets that appear below Cell 5:
   - **GPU Configuration:** Count (slider), Type (dropdown), Power (number input)
   - **Generator Configuration:** Manufacturer (dropdown), Model (dropdown), Power (number input)
   - **Operational Parameters:** Islanded (checkbox), Black Start (checkbox), Load Sequencing (checkbox)
   - **Data Logistics:** Inbound/Outbound TB (number inputs), Distances (number inputs)

2. **Click "Calculate"** button (appears below the input widgets)

3. **View results** in the results dashboard (appears below the Calculate button):
   - Generator Risk Assessment
   - BESS Sizing Recommendation
   - GPU-Generator Compatibility
   - Data Logistics Cost Comparison
   - Cost Summary
   - Visualizations

4. **Export results** to CSV (optional):
   - Run Cell 8
   - Follow the prompts

### Quick Reference
- **Select a cell:** Click on it
- **Run a cell:** Press `Shift + Enter` (or click Run button)
- **Edit a cell:** Click in it, type, then run it
- **Move between cells:** Use arrow keys or click
- **Stop running cell:** Click Stop button (square icon) or press `Ctrl + C`

---

## Features

### Interactive Widgets

- **Dropdowns** for GPU type, generator model
- **Sliders** for GPU count, correlation factor
- **Number inputs** for power ratings, distances
- **Checkboxes** for boolean options
- **Calculate button** to trigger analysis

### Smart Defaults

- GPU power auto-filled based on GPU type
- Generator power auto-filled based on model
- Pre-populated with common configurations

### Unified Results Dashboard

- **Color-coded risk levels** (GREEN/YELLOW/RED)
- **BESS recommendations** with cost estimates
- **Data logistics comparison** with recommended mode
- **Cost summary** (CapEx/OpEx breakdown)
- **Visualizations** (power profiles, cost comparisons)

### Export Functionality

- Export results to CSV
- Timestamped filenames
- Saved to `outputs/unified-calculator-results/`

---

## Dependencies

### Pre-installed (datascience-notebook)

- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn

### Auto-installed (Cell 2)

- ipywidgets (for interactive widgets)
- plotly (optional, for interactive charts)

---

## File Structure

```
tools/
└── unified-calculator.ipynb          # Single self-contained notebook
```

All code, data loading, and calculations are in one notebook file.

---

## Troubleshooting

### Issue: Cannot find CSV files

**Solution:** Verify the notebook is in the correct location:
- Expected path: `/home/jovyan/work/og-ai-inference-research/tools/unified-calculator.ipynb`
- CSV files should be in: `../models/*/`

### Issue: Widgets not displaying

**Solution:** 
1. Ensure Cell 2 (package installation) ran successfully
2. Restart kernel: Kernel → Restart Kernel
3. Re-run cells sequentially

### Issue: Calculation button does nothing

**Solution:**
1. Ensure Cell 7 (calculation execution) ran successfully
2. Check that all input widgets have valid values
3. Look for error messages in the output area

### Issue: Results not displaying

**Solution:**
1. Ensure calculations completed successfully (check Cell 7 output)
2. Scroll down to Cell 8 (results display)
3. Re-run Cell 8 if needed

---

## Data Sources

The calculator uses data from:

- **Generator specifications:** `data/generators/caterpillar/`
- **GPU power profiles:** `data/gpu-profiles/GPU-Power-Profiles.md`
- **Compatibility matrix:** `models/gpu-generator-compatibility/GPU-Generator-Compatibility-Matrix-v1.csv`
- **BESS sizing examples:** `models/bess-sizing/BESS-Sizing-v1.csv`
- **Data logistics examples:** `models/data-logistics/DataLogistics-v1.csv`

---

## References

- Generator Risk Calculator: `models/generator-risk-calculator/`
- BESS Sizing Calculator: `models/bess-sizing/`
- GPU-Generator Compatibility: `models/gpu-generator-compatibility/`
- Data Logistics Calculator: `models/data-logistics/`
- Deployment Guide: `/srv/projects/mac-workhorse-integration/docs/guides/JUPYTER_DEPLOYMENT_PROMPT.md`

---

## Future Enhancements

- Save/load configuration presets
- Comparison mode (run multiple scenarios side-by-side)
- Sensitivity analysis (vary parameters and see impact)
- Integration with economic model (when complete)
- Multi-generator parallel configurations
- Bitcoin miner integration (when needed)

