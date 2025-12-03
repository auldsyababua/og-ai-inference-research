#!/usr/bin/env python3
"""
Diagnostic script to test JupyterLab notebook access.
Run this in a Jupyter terminal or Python cell to diagnose 404 issues.
"""

import os
import json
import sys
from pathlib import Path

def test_notebook_access():
    """Test if notebook can be accessed and parsed"""
    print("=" * 60)
    print("JupyterLab Notebook Access Diagnostic")
    print("=" * 60)
    
    # Test paths
    paths_to_test = [
        '/home/jovyan/work/og-ai-inference-research/tools/unified-calculator.ipynb',
        '/srv/projects/og-ai-inference-research/tools/unified-calculator.ipynb',
        'tools/unified-calculator.ipynb',
        './tools/unified-calculator.ipynb',
        '../tools/unified-calculator.ipynb',
    ]
    
    print("\n1. Testing file existence...")
    found_path = None
    for path in paths_to_test:
        if os.path.exists(path):
            print(f"   ✓ Found: {path}")
            found_path = path
            break
        else:
            print(f"   ✗ Not found: {path}")
    
    if not found_path:
        print("\n   ERROR: Notebook file not found in any expected location!")
        return False
    
    print(f"\n2. Testing file permissions...")
    stat_info = os.stat(found_path)
    print(f"   Size: {stat_info.st_size:,} bytes")
    print(f"   Permissions: {oct(stat_info.st_mode)[-3:]}")
    print(f"   Readable: {os.access(found_path, os.R_OK)}")
    print(f"   Writable: {os.access(found_path, os.W_OK)}")
    
    print(f"\n3. Testing JSON validity...")
    try:
        with open(found_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)
        print(f"   ✓ Valid JSON")
        print(f"   ✓ Notebook format: {nb.get('nbformat')}.{nb.get('nbformat_minor')}")
        print(f"   ✓ Cells: {len(nb.get('cells', []))}")
    except json.JSONDecodeError as e:
        print(f"   ✗ Invalid JSON: {e}")
        return False
    except Exception as e:
        print(f"   ✗ Error reading file: {e}")
        return False
    
    print(f"\n4. Testing notebook structure...")
    required_keys = ['cells', 'metadata', 'nbformat', 'nbformat_minor']
    missing_keys = [k for k in required_keys if k not in nb]
    if missing_keys:
        print(f"   ✗ Missing keys: {missing_keys}")
        return False
    else:
        print(f"   ✓ All required keys present")
    
    print(f"\n5. Testing cell structure...")
    cells = nb.get('cells', [])
    cell_issues = []
    for i, cell in enumerate(cells):
        if 'cell_type' not in cell:
            cell_issues.append(f"Cell {i}: missing cell_type")
        if 'source' not in cell:
            cell_issues.append(f"Cell {i}: missing source")
    
    if cell_issues:
        print(f"   ✗ Cell issues found:")
        for issue in cell_issues:
            print(f"      - {issue}")
        return False
    else:
        print(f"   ✓ All {len(cells)} cells have required fields")
    
    print(f"\n6. Testing metadata...")
    metadata = nb.get('metadata', {})
    kernelspec = metadata.get('kernelspec', {})
    language_info = metadata.get('language_info', {})
    
    if kernelspec:
        print(f"   ✓ Kernelspec: {kernelspec.get('name', 'N/A')}")
    else:
        print(f"   ⚠ Warning: No kernelspec found")
    
    if language_info:
        print(f"   ✓ Language info: {language_info.get('name', 'N/A')}")
    else:
        print(f"   ⚠ Warning: No language_info found")
    
    print(f"\n7. Testing file encoding...")
    try:
        with open(found_path, 'rb') as f:
            raw_content = f.read()
        # Check for null bytes in raw content
        has_null_bytes = b'\x00' in raw_content
        if has_null_bytes:
            null_count = raw_content.count(b'\x00')
            print(f"   ✗ Found {null_count} null byte(s) in file")
            return False
        # Try to decode as UTF-8
        content = raw_content.decode('utf-8')
        print(f"   ✓ Valid UTF-8 encoding")
        print(f"   ✓ No null bytes found")
    except UnicodeDecodeError as e:
        print(f"   ✗ Encoding issue: {e}")
        return False
    
    print(f"\n8. Testing JupyterLab API access (if available)...")
    try:
        import requests
        # This would require JupyterLab to be running and accessible
        # We can't test this from inside the container easily
        print(f"   ⚠ Skipped: Requires JupyterLab API access")
    except ImportError:
        print(f"   ⚠ Skipped: requests not available")
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print("✓ File exists and is readable")
    print("✓ Valid JSON structure")
    print("✓ Proper notebook format")
    print("✓ All cells valid")
    print("✓ Proper metadata")
    print("\nIf you're still getting 404 errors:")
    print("1. Clear browser cache (Ctrl+Shift+R)")
    print("2. Try accessing via file browser (not direct URL)")
    print("3. Check browser console (F12) for specific errors")
    print("4. Try uploading the file via JupyterLab interface")
    print("=" * 60)
    
    return True

if __name__ == '__main__':
    success = test_notebook_access()
    sys.exit(0 if success else 1)

