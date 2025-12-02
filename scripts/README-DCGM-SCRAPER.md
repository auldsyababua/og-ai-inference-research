# NVIDIA DCGM User Guide Scraper

This directory contains Python scripts to scrape the NVIDIA DCGM User Guide from the official NVIDIA documentation website.

## Purpose

Scrape the complete NVIDIA DCGM (Data Center GPU Manager) User Guide documentation from:
https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/index.html

Output: `docs/nvidia-manuals/NVIDIA-DCGM-User-Guide.md`

## Scripts

### 1. `scrape_dcgm_simple.py` (RECOMMENDED)

**Simple, reliable scraper with minimal dependencies.**

**Features:**
- Clean markdown output
- Automatic link discovery and crawling
- Table of contents generation
- Progress indicators
- Error handling

**Dependencies:**
- Python 3.6+
- `requests` library
- `beautifulsoup4` library

**Usage:**
```bash
cd /srv/projects/og-ai-inference-research
python3 scripts/scrape_dcgm_simple.py
```

### 2. `scrape_dcgm_enhanced.py`

**Enhanced version with better HTML-to-Markdown conversion.**

More sophisticated HTML parsing with better handling of:
- Code blocks with syntax highlighting
- Tables
- Definition lists
- Nested lists
- Images and links

**Dependencies:** Same as simple version

**Usage:**
```bash
cd /srv/projects/og-ai-inference-research
python3 scripts/scrape_dcgm_enhanced.py
```

### 3. `scrape_dcgm_guide.py`

**Original full-featured version.**

Most comprehensive with detailed element processing.

**Usage:**
```bash
cd /srv/projects/og-ai-inference-research
python3 scripts/scrape_dcgm_guide.py
```

## Installation

### Install Dependencies

```bash
# Using pip
pip3 install requests beautifulsoup4

# Or using pip with user flag
pip3 install --user requests beautifulsoup4

# Or using apt (Debian/Ubuntu)
sudo apt-get install python3-requests python3-bs4
```

## Quick Start

### Method 1: Direct Python Execution

```bash
cd /srv/projects/og-ai-inference-research

# Install dependencies if needed
pip3 install --user requests beautifulsoup4

# Run the scraper (use simple version first)
python3 scripts/scrape_dcgm_simple.py
```

### Method 2: Using the Shell Wrapper

```bash
cd /srv/projects/og-ai-inference-research

# Make executable
chmod +x RUN_DCGM_SCRAPER.sh

# Run
./RUN_DCGM_SCRAPER.sh
```

### Method 3: Using the Enhanced Wrapper

```bash
cd /srv/projects/og-ai-inference-research

# Make executable
chmod +x scripts/run_dcgm_scraper.sh

# Run (includes dependency check and installation)
./scripts/run_dcgm_scraper.sh
```

## Output

The scraper will create:

**File:** `/srv/projects/og-ai-inference-research/docs/nvidia-manuals/NVIDIA-DCGM-User-Guide.md`

**Contents:**
- Complete DCGM User Guide documentation
- Table of contents with links
- All sections from the online documentation
- Code examples preserved in code blocks
- Tables converted to markdown format
- Source URLs for each section
- Metadata (scrape date, page count, etc.)

## Expected Output

```
================================================================================
NVIDIA DCGM User Guide Scraper
================================================================================
Starting URL: https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/index.html
Output: /srv/projects/og-ai-inference-research/docs/nvidia-manuals/NVIDIA-DCGM-User-Guide.md
================================================================================

Starting crawl...

[1] https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/index.html
  Fetching: https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/index.html
  ✓ DCGM User Guide
  Found 15 new pages

[2] https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/overview.html
  Fetching: https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/overview.html
  ✓ Overview
  Found 3 new pages

... (continues for all pages)

✓ Crawled 25 pages

Generating markdown document...

✓ Saved successfully!
  File: /srv/projects/og-ai-inference-research/docs/nvidia-manuals/NVIDIA-DCGM-User-Guide.md
  Size: 245.3 KB
  Pages: 25
  Characters: 251,234
```

## What Gets Scraped

The scraper will automatically discover and download all pages including:

- **Introduction & Overview**
  - What is DCGM
  - Architecture
  - Capabilities

- **Installation**
  - Package installation
  - Docker containers
  - Kubernetes integration

- **Configuration**
  - Daemon configuration
  - Security settings
  - Remote management

- **Usage & Commands**
  - dcgmi command-line tool
  - Field IDs and metrics
  - Health checks
  - Diagnostics

- **API Reference**
  - C API documentation
  - Python bindings
  - Go bindings

- **Integration**
  - Prometheus exporter
  - Kubernetes operator
  - SLURM integration

- **Monitoring & Diagnostics**
  - GPU monitoring
  - Profiling
  - Alerts and notifications

- **Troubleshooting**
  - Common issues
  - Error codes
  - Debug procedures

## Features

### Automatic Navigation
- Discovers all documentation pages automatically
- Follows internal links within the DCGM user guide
- Handles Sphinx documentation structure

### Content Preservation
- Converts HTML to clean markdown
- Preserves code blocks
- Converts tables to markdown tables
- Maintains heading hierarchy
- Preserves lists (ordered and unordered)

### Output Quality
- Generates table of contents with links
- Includes source URLs for each section
- Adds metadata (scrape date, page count)
- Clean, readable markdown format

### Error Handling
- Retries on transient network errors
- Continues on individual page failures
- Reports progress and errors clearly

## Troubleshooting

### Missing Dependencies

**Error:**
```
ModuleNotFoundError: No module named 'requests'
```

**Solution:**
```bash
pip3 install --user requests beautifulsoup4
```

### Connection Errors

**Error:**
```
ERROR: Connection timeout
```

**Solution:**
- Check internet connection
- Try again after a few seconds
- Check if docs.nvidia.com is accessible

### Permission Errors

**Error:**
```
PermissionError: [Errno 13] Permission denied
```

**Solution:**
```bash
# Ensure output directory exists and is writable
mkdir -p /srv/projects/og-ai-inference-research/docs/nvidia-manuals
chmod u+w /srv/projects/og-ai-inference-research/docs/nvidia-manuals
```

## Estimated Time

- **Small sites (10-20 pages):** 30-60 seconds
- **Medium sites (20-40 pages):** 1-3 minutes
- **Large sites (40+ pages):** 3-5 minutes

The scraper includes polite rate limiting (0.5 second delay between requests) to avoid overwhelming the server.

## Post-Scraping

After successful scraping:

1. **Verify the output:**
   ```bash
   ls -lh docs/nvidia-manuals/NVIDIA-DCGM-User-Guide.md
   head -n 50 docs/nvidia-manuals/NVIDIA-DCGM-User-Guide.md
   ```

2. **Update collection status:**
   Edit `docs/nvidia-manuals/COLLECTION-STATUS.md` to mark DCGM guide as collected

3. **Commit to git:**
   ```bash
   git add docs/nvidia-manuals/NVIDIA-DCGM-User-Guide.md
   git commit -m "Add NVIDIA DCGM User Guide documentation"
   ```

## Notes

- **Legal:** This documentation is property of NVIDIA Corporation. Scraped for research and reference purposes.
- **Freshness:** The scraper fetches the latest version from docs.nvidia.com
- **Updates:** Re-run the scraper periodically to get updated documentation
- **Rate Limiting:** Built-in delays respect NVIDIA's servers

## Related Documentation

After scraping DCGM User Guide, also scrape:
- MIG User Guide: https://docs.nvidia.com/datacenter/tesla/mig-user-guide/
- NVML API Reference: Already collected as PDF

## Support

For issues with the scraper scripts:
1. Check this README for troubleshooting steps
2. Verify dependencies are installed
3. Check network connectivity
4. Review error messages carefully

---

**Last Updated:** 2025-12-02
**Author:** AI Research Team
**Purpose:** Infrastructure documentation for power management research
