#!/bin/bash
# Master DCGM Scraper - Tries multiple methods in order of preference

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="/srv/projects/og-ai-inference-research"
OUTPUT_FILE="$PROJECT_DIR/docs/nvidia-manuals/NVIDIA-DCGM-User-Guide.md"

echo "================================================================================"
echo "NVIDIA DCGM User Guide Scraper - Master Script"
echo "================================================================================"
echo ""
echo "This script will try multiple methods to scrape the DCGM documentation:"
echo "  1. Python scraper (simple version) - Best quality"
echo "  2. Python scraper (enhanced version) - More features"
echo "  3. curl + HTML download - Fallback"
echo "  4. Manual instructions - Last resort"
echo ""
echo "================================================================================"
echo ""

# Method 1: Try simple Python scraper
echo "[Method 1] Trying Python scraper (simple)..."
echo ""

if command -v python3 &> /dev/null; then
    echo "  ✓ Python 3 found: $(python3 --version 2>&1)"

    # Check if dependencies are installed
    if python3 -c "import requests; import bs4" 2>/dev/null; then
        echo "  ✓ Required packages (requests, beautifulsoup4) found"
        echo ""
        echo "  Running scraper..."
        echo ""

        cd "$PROJECT_DIR"
        if python3 "$SCRIPT_DIR/scrape_dcgm_simple.py"; then
            echo ""
            echo "================================================================================"
            echo "✅ SUCCESS! DCGM User Guide scraped successfully"
            echo "================================================================================"
            echo ""
            echo "Output file: $OUTPUT_FILE"
            echo ""

            if [ -f "$OUTPUT_FILE" ]; then
                size=$(wc -c < "$OUTPUT_FILE")
                lines=$(wc -l < "$OUTPUT_FILE")
                echo "File size: $((size / 1024)) KB"
                echo "Line count: $lines"
                echo ""
                echo "First few lines:"
                head -n 20 "$OUTPUT_FILE"
            fi

            exit 0
        else
            echo "  ✗ Python scraper failed"
        fi
    else
        echo "  ✗ Required packages not found"
        echo ""
        echo "  Attempting to install packages..."

        if pip3 install --user requests beautifulsoup4 2>/dev/null; then
            echo "  ✓ Packages installed successfully"
            echo ""
            echo "  Retrying scraper..."

            cd "$PROJECT_DIR"
            if python3 "$SCRIPT_DIR/scrape_dcgm_simple.py"; then
                echo ""
                echo "================================================================================"
                echo "✅ SUCCESS! DCGM User Guide scraped successfully"
                echo "================================================================================"
                exit 0
            fi
        else
            echo "  ✗ Package installation failed"
        fi
    fi
else
    echo "  ✗ Python 3 not found"
fi

echo ""
echo "-------------------------------------------------------------------------------"
echo ""

# Method 2: Try enhanced Python scraper
echo "[Method 2] Trying Python scraper (enhanced)..."
echo ""

if command -v python3 &> /dev/null && python3 -c "import requests; import bs4" 2>/dev/null; then
    echo "  Running enhanced scraper..."

    cd "$PROJECT_DIR"
    if python3 "$SCRIPT_DIR/scrape_dcgm_enhanced.py"; then
        echo ""
        echo "================================================================================"
        echo "✅ SUCCESS! DCGM User Guide scraped successfully (enhanced version)"
        echo "================================================================================"
        exit 0
    else
        echo "  ✗ Enhanced scraper failed"
    fi
else
    echo "  ✗ Skipping (dependencies not available)"
fi

echo ""
echo "-------------------------------------------------------------------------------"
echo ""

# Method 3: Try curl download
echo "[Method 3] Trying curl download..."
echo ""

if command -v curl &> /dev/null; then
    echo "  ✓ curl found"
    echo ""

    if bash "$SCRIPT_DIR/scrape_dcgm_curl.sh"; then
        echo ""
        echo "================================================================================"
        echo "✅ HTML pages downloaded successfully"
        echo "================================================================================"
        echo ""
        echo "HTML files saved to: $PROJECT_DIR/docs/nvidia-manuals/dcgm-pages/"
        echo ""
        echo "NEXT STEPS:"
        echo "1. View HTML files in browser: firefox docs/nvidia-manuals/dcgm-pages/index.html"
        echo "2. Install Python packages and run scraper to convert to markdown"
        echo "3. Or manually extract content from HTML files"
        echo ""
        exit 0
    else
        echo "  ✗ curl download failed"
    fi
else
    echo "  ✗ curl not found"
fi

echo ""
echo "-------------------------------------------------------------------------------"
echo ""

# Method 4: Manual instructions
echo "[Method 4] Manual scraping required"
echo ""
echo "================================================================================"
echo "❌ Automatic scraping failed - Manual intervention required"
echo "================================================================================"
echo ""
echo "Please follow the manual scraping guide:"
echo "  File: $SCRIPT_DIR/MANUAL-SCRAPING-GUIDE.md"
echo ""
echo "Quick manual method:"
echo "  1. Open: https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/index.html"
echo "  2. Navigate through all sections"
echo "  3. Use browser 'Save As' or 'Print to PDF' for each page"
echo "  4. Combine pages manually"
echo ""
echo "Or install required packages:"
echo "  pip3 install --user requests beautifulsoup4"
echo "  python3 scripts/scrape_dcgm_simple.py"
echo ""
echo "================================================================================"

exit 1
