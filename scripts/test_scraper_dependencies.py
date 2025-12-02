#!/usr/bin/env python3
"""
Test if scraper dependencies are available
"""

import sys

print("Testing Python environment for DCGM scraper...")
print(f"Python version: {sys.version}\n")

# Test requests
try:
    import requests
    print("✓ requests module: INSTALLED")
    print(f"  Version: {requests.__version__}")
except ImportError:
    print("✗ requests module: NOT FOUND")
    print("  Install with: pip3 install requests")

# Test BeautifulSoup
try:
    from bs4 import BeautifulSoup
    print("✓ beautifulsoup4 module: INSTALLED")
    try:
        print(f"  Version: {BeautifulSoup.__version__}")
    except:
        print("  Version: Unknown")
except ImportError:
    print("✗ beautifulsoup4 module: NOT FOUND")
    print("  Install with: pip3 install beautifulsoup4")

print("\n" + "="*60)

# Test simple HTTP request
try:
    import requests
    print("\nTesting network connectivity to docs.nvidia.com...")
    response = requests.head("https://docs.nvidia.com", timeout=5)
    print(f"✓ Connection successful (status: {response.status_code})")
except Exception as e:
    print(f"✗ Connection failed: {e}")

print("\n" + "="*60)
print("\nIf both modules are installed, you can run:")
print("  python3 scripts/scrape_dcgm_simple.py")
print("\nOtherwise, install dependencies:")
print("  pip3 install --user requests beautifulsoup4")
