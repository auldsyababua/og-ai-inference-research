# Accessing the Unified Calculator Notebook

If you're getting a 404 error when trying to access the notebook, try these steps:

## Method 1: Direct File Browser Access (Recommended)

1. **Open JupyterLab:** Navigate to `http://workhorse.local/jupyter/lab/`
2. **Authenticate:** Enter Jupyter token (get with: `docker exec jupyter jupyter server list`)
3. **Navigate in file browser:**
   - Navigate to `work` folder
   - Open `og-ai-inference-research` folder
   - Open `tools` folder
   - Double-click `unified-calculator.ipynb`

**Direct URL:** `http://workhorse.local/jupyter/lab/tree/work/og-ai-inference-research/tools/unified-calculator.ipynb`

## Method 2: Check File Location

The notebook should be at:
- **Inside Jupyter container:** `/home/jovyan/work/og-ai-inference-research/tools/unified-calculator.ipynb`
- **On host:** `/srv/projects/og-ai-inference-research/tools/unified-calculator.ipynb`

## Method 3: Verify File Exists

Run this in a Jupyter terminal or code cell:
```python
import os
notebook_path = '/home/jovyan/work/og-ai-inference-research/tools/unified-calculator.ipynb'
print(f"File exists: {os.path.exists(notebook_path)}")
print(f"File size: {os.path.getsize(notebook_path) if os.path.exists(notebook_path) else 0} bytes")
```

## Method 4: Upload via JupyterLab Interface

1. Open JupyterLab file browser
2. Navigate to `/home/jovyan/work/og-ai-inference-research/tools/`
3. Click upload button (↑ icon)
4. Select `unified-calculator.ipynb` from your local machine

## Troubleshooting 404 Errors

### If notebook file gives 404:
- Check file permissions: `chmod 644 unified-calculator.ipynb`
- Verify file is in correct location
- Try refreshing JupyterLab (F5)
- Clear browser cache

### If CSV files give 404 (within notebook):
- Run Cell 4 and check the BASE_PATH output
- Verify CSV files exist in `models/` directories
- Check the error messages for exact file paths

## Current File Status

- **Location:** `/srv/projects/og-ai-inference-research/tools/unified-calculator.ipynb`
- **Size:** ~54 KB
- **Format:** Jupyter Notebook 4.2
- **Kernel:** Python 3
- **Cells:** 9 (1 markdown + 8 code)

