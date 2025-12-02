#!/bin/bash
# Fallback DCGM scraper using curl and basic text processing
# Use this if Python packages are not available

set -e

BASE_URL="https://docs.nvidia.com/datacenter/dcgm/latest/user-guide"
OUTPUT_DIR="/srv/projects/og-ai-inference-research/docs/nvidia-manuals/dcgm-pages"
FINAL_OUTPUT="/srv/projects/og-ai-inference-research/docs/nvidia-manuals/NVIDIA-DCGM-User-Guide.md"

echo "=============================================="
echo "NVIDIA DCGM User Guide Scraper (curl version)"
echo "=============================================="
echo ""

# Check for curl
if ! command -v curl &> /dev/null; then
    echo "ERROR: curl not found"
    echo "Install with: sudo apt-get install curl"
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

# List of known DCGM documentation pages
# These are common pages in DCGM documentation
PAGES=(
    "index.html"
    "dcgm-user-guide.html"
    "getting-started.html"
    "installation.html"
    "configuration.html"
    "dcgmi-user-guide.html"
    "dcgm-api-reference.html"
    "field-identifiers.html"
    "health-monitoring.html"
    "diagnostics.html"
    "profiling.html"
    "policy-management.html"
    "integration.html"
    "troubleshooting.html"
)

echo "Downloading pages..."
echo ""

# Download each page
for page in "${PAGES[@]}"; do
    url="$BASE_URL/$page"
    output="$OUTPUT_DIR/$page"

    echo "  Fetching: $page"

    if curl -sf -o "$output" "$url" 2>/dev/null; then
        echo "    ✓ Downloaded"
    else
        echo "    ✗ Not found (may not exist)"
    fi

    sleep 0.5  # Be polite
done

echo ""
echo "=============================================="
echo "Downloaded pages saved to: $OUTPUT_DIR"
echo ""
echo "To convert to markdown, you can:"
echo "1. Use Python script: python3 scripts/scrape_dcgm_simple.py"
echo "2. Use pandoc: pandoc page.html -o page.md"
echo "3. Manually copy content from HTML files"
echo ""
echo "Downloaded HTML files can be viewed in a browser:"
echo "  firefox $OUTPUT_DIR/index.html"
echo "=============================================="

# Count downloaded files
count=$(find "$OUTPUT_DIR" -name "*.html" | wc -l)
echo ""
echo "Total pages downloaded: $count"

if [ "$count" -gt 0 ]; then
    echo ""
    echo "Next steps:"
    echo "1. View the HTML files in a browser"
    echo "2. Run the Python scraper to convert to markdown"
    echo "3. Or manually extract content"
fi
