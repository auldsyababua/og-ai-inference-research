#!/bin/bash
# Run the DCGM User Guide scraper with dependency checking

set -e

echo "========================================"
echo "NVIDIA DCGM User Guide Scraper"
echo "========================================"
echo ""

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 not found"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check for required packages
echo ""
echo "Checking Python dependencies..."

if python3 -c "import requests" 2>/dev/null; then
    echo "✓ requests module found"
else
    echo "⚠️  requests module not found, attempting to install..."
    pip3 install --user requests || {
        echo "❌ Failed to install requests"
        exit 1
    }
fi

if python3 -c "import bs4" 2>/dev/null; then
    echo "✓ beautifulsoup4 module found"
else
    echo "⚠️  beautifulsoup4 module not found, attempting to install..."
    pip3 install --user beautifulsoup4 || {
        echo "❌ Failed to install beautifulsoup4"
        exit 1
    }
fi

echo ""
echo "========================================"
echo "Running scraper..."
echo "========================================"
echo ""

# Run the scraper
cd /srv/projects/og-ai-inference-research
python3 scripts/scrape_dcgm_enhanced.py

exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "✅ Scraping completed successfully!"
    echo "========================================"
else
    echo ""
    echo "========================================"
    echo "❌ Scraping failed with exit code: $exit_code"
    echo "========================================"
fi

exit $exit_code
