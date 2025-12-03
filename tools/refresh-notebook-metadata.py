#!/usr/bin/env python3
"""
Refresh notebook metadata to ensure JupyterLab compatibility.
This script reads the notebook, ensures proper metadata, and saves it back.
"""

import json
import sys
from pathlib import Path

def refresh_notebook_metadata(notebook_path):
    """Refresh notebook metadata for JupyterLab compatibility"""
    
    print(f"Reading notebook: {notebook_path}")
    
    # Read notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    print(f"✓ Loaded notebook with {len(nb.get('cells', []))} cells")
    
    # Create backup BEFORE any modifications
    backup_path = str(notebook_path) + '.backup'
    print(f"\nCreating backup: {backup_path}")
    # Create a deep copy for backup to preserve original state
    import copy
    nb_backup = copy.deepcopy(nb)
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(nb_backup, f, indent=1, ensure_ascii=False)
    print(f"✓ Backup created before modifications")
    
    # Ensure proper format version
    if 'nbformat' not in nb:
        nb['nbformat'] = 4
    if 'nbformat_minor' not in nb:
        nb['nbformat_minor'] = 2
    
    print(f"✓ Format: {nb['nbformat']}.{nb['nbformat_minor']}")
    
    # Ensure metadata exists
    if 'metadata' not in nb:
        nb['metadata'] = {}
    
    metadata = nb['metadata']
    
    # Ensure kernelspec
    if 'kernelspec' not in metadata:
        metadata['kernelspec'] = {}
    
    kernelspec = metadata['kernelspec']
    if 'name' not in kernelspec:
        kernelspec['name'] = 'python3'
    if 'display_name' not in kernelspec:
        kernelspec['display_name'] = 'Python 3'
    if 'language' not in kernelspec:
        kernelspec['language'] = 'python'
    
    print(f"✓ Kernelspec: {kernelspec['name']}")
    
    # Ensure language_info
    if 'language_info' not in metadata:
        metadata['language_info'] = {}
    
    language_info = metadata['language_info']
    if 'name' not in language_info:
        language_info['name'] = 'python'
    if 'version' not in language_info:
        # Try to get Python version
        import sys
        language_info['version'] = sys.version.split()[0]
    
    print(f"✓ Language info: {language_info['name']}")
    
    # Ensure all cells have proper structure
    cells = nb.get('cells', [])
    for i, cell in enumerate(cells):
        if 'cell_type' not in cell:
            print(f"⚠ Warning: Cell {i} missing cell_type, skipping")
            continue
        if 'source' not in cell:
            cell['source'] = []
        if 'metadata' not in cell:
            cell['metadata'] = {}
    
    print(f"✓ All {len(cells)} cells validated")
    
    # Write refreshed notebook
    print(f"\nWriting refreshed notebook: {notebook_path}")
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    
    print("✓ Notebook refreshed successfully!")
    print(f"✓ Backup saved to: {backup_path}")
    
    return True

if __name__ == '__main__':
    notebook_path = '/srv/projects/og-ai-inference-research/tools/unified-calculator.ipynb'
    
    if len(sys.argv) > 1:
        notebook_path = sys.argv[1]
    
    try:
        success = refresh_notebook_metadata(notebook_path)
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

