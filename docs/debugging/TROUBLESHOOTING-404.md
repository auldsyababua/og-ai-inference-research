# Troubleshooting 404 Error for Unified Calculator Notebook

## Quick Checks

### 1. Verify File Exists in Container
Run this in a Jupyter terminal:
```bash
ls -lh /home/jovyan/work/og-ai-inference-research/tools/unified-calculator.ipynb
```

Expected output: Should show file with ~50KB size

### 2. Check File Permissions
```bash
stat /home/jovyan/work/og-ai-inference-research/tools/unified-calculator.ipynb
```

Expected: `-rw-r--r--` (644 permissions)

### 3. Validate Notebook Structure
Run this in a Jupyter Python cell:
```python
import json
with open('/home/jovyan/work/og-ai-inference-research/tools/unified-calculator.ipynb', 'r') as f:
    nb = json.load(f)
print(f"✓ Valid notebook with {len(nb['cells'])} cells")
```

## Common Causes and Solutions

### Issue: Browser Cache
**Solution:**
1. Hard refresh: `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (Mac)
2. Clear browser cache for `workhorse.local`
3. Try incognito/private browsing mode

### Issue: JupyterLab Cache
**Solution:**
1. Restart JupyterLab kernel
2. Clear JupyterLab cache: Settings → Advanced Settings → Reset

### Issue: File Path in URL
**Check the URL you're using:**
- ✅ Correct: `http://workhorse.local/jupyter/lab/tree/work/og-ai-inference-research/tools/unified-calculator.ipynb`
- ❌ Wrong: `http://workhorse.local/jupyter/lab/tree/og-ai-inference-research/tools/unified-calculator.ipynb` (missing `work/`)
- ❌ Wrong: `http://workhorse.local/lab/tree/...` (wrong base path - should be `/jupyter/`)

### Issue: File Not Visible in File Browser
**Solution:**
1. Navigate to `/home/jovyan/work/og-ai-inference-research/tools/` in file browser
2. Refresh file browser (F5)
3. If still not visible, try uploading via drag-and-drop

### Issue: Notebook Corrupted
**Solution:**
1. Verify file is valid JSON (see validation above)
2. If corrupted, re-download or recreate from backup
3. Check file size matches (~50KB)

## Alternative Access Methods

### Method 1: Direct File Browser
1. Open JupyterLab: `http://workhorse.local/jupyter/lab/`
2. Authenticate with Jupyter token (get with: `docker exec jupyter jupyter server list`)
3. Use file browser (left sidebar)
4. Navigate: `work` → `og-ai-inference-research` → `tools` → `unified-calculator.ipynb`
5. Double-click to open

### Method 2: Upload via JupyterLab
1. Open JupyterLab file browser
2. Navigate to `og-ai-inference-research/tools/`
3. Click upload button (↑ icon)
4. Select `unified-calculator.ipynb` from local machine

### Method 3: Copy via SMB
1. Mount SMB share: `smb://workhorse.local/Projects`
2. Copy notebook file to share
3. Refresh JupyterLab file browser

### Method 4: Create New Notebook and Copy Code
1. Create new notebook in JupyterLab
2. Copy code from each cell of `unified-calculator.ipynb`
3. Paste into new notebook cells

## Check Jupyter Logs

If 404 persists, check logs:
```bash
# On host machine
docker logs jupyter --tail 100 | grep -i "404\|error\|unified"

# Or check Traefik logs
docker logs traefik --tail 100 | grep -i "404\|jupyter"
```

## File Status (as of 2025-12-02)

- **Location:** `/srv/projects/og-ai-inference-research/tools/unified-calculator.ipynb`
- **Container Path:** `/home/jovyan/work/og-ai-inference-research/tools/unified-calculator.ipynb`
- **Size:** ~50KB
- **Format:** Jupyter Notebook 4.2
- **Status:** Valid JSON, 9 cells, proper metadata
- **Permissions:** 644 (readable by all)

## Still Having Issues?

1. **Check browser console** (F12) for specific error messages
2. **Try different browser** to rule out browser-specific issues
3. **Check network tab** to see exact URL returning 404
4. **Verify Traefik routing** is working for `/lab/` path

