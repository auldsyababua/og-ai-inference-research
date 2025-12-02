# Manual NVIDIA DCGM User Guide Scraping Guide

If automated scraping scripts don't work, use this manual guide to capture the documentation.

## Target URL

https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/index.html

## Method 1: Browser "Print to PDF" (Easiest)

### Steps:

1. **Open the documentation in your browser:**
   ```
   https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/index.html
   ```

2. **Navigate to each section** and print each page:
   - File → Print (or Ctrl+P / Cmd+P)
   - Choose "Save as PDF"
   - Save to: `/srv/projects/og-ai-inference-research/docs/nvidia-manuals/dcgm-pages/`
   - Name format: `01-index.pdf`, `02-overview.pdf`, etc.

3. **Key pages to capture:**
   - index.html - Introduction
   - getting-started.html - Installation
   - dcgmi-user-guide.html - Command-line tool
   - dcgm-api-reference.html - API documentation
   - field-identifiers.html - Field IDs
   - config-options.html - Configuration
   - integration.html - Integration guides
   - troubleshooting.html - Troubleshooting

4. **Combine PDFs** (if desired):
   ```bash
   # Using pdfunite (part of poppler-utils)
   cd /srv/projects/og-ai-inference-research/docs/nvidia-manuals/dcgm-pages/
   pdfunite *.pdf ../NVIDIA-DCGM-User-Guide.pdf
   ```

## Method 2: wget Mirror (Automated)

### Prerequisites:
```bash
# Install wget if not available
sudo apt-get install wget
```

### Command:
```bash
cd /srv/projects/og-ai-inference-research/docs/nvidia-manuals/

# Mirror the entire user guide
wget \
  --recursive \
  --level=3 \
  --no-parent \
  --convert-links \
  --adjust-extension \
  --page-requisites \
  --no-host-directories \
  --directory-prefix=dcgm-mirror \
  https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/index.html

# This creates: dcgm-mirror/datacenter/dcgm/latest/user-guide/
```

### Convert to Single HTML:
```bash
# Combine all HTML pages
cat dcgm-mirror/datacenter/dcgm/latest/user-guide/*.html > DCGM-Combined.html
```

### Convert to PDF:
```bash
# Using wkhtmltopdf
wkhtmltopdf DCGM-Combined.html NVIDIA-DCGM-User-Guide.pdf

# Or using pandoc
pandoc DCGM-Combined.html -o NVIDIA-DCGM-User-Guide.pdf
```

## Method 3: Browser Developer Tools Copy

### Steps:

1. **Open page in browser with DevTools:**
   - Chrome/Edge: F12 or Ctrl+Shift+I
   - Firefox: F12 or Ctrl+Shift+I
   - Safari: Cmd+Option+I

2. **Copy main content:**
   - Right-click the main content area
   - "Inspect Element"
   - Find the `<main>` or `<article>` element
   - Right-click → Copy → Copy Element
   - Paste into a text editor

3. **Save as HTML:**
   - Save to: `/srv/projects/og-ai-inference-research/docs/nvidia-manuals/dcgm-scraped/`
   - Name: `page-title.html`

4. **Repeat for all sections**

5. **Convert HTML to Markdown:**
   ```bash
   # Using pandoc
   for file in dcgm-scraped/*.html; do
     pandoc "$file" -f html -t markdown -o "${file%.html}.md"
   done

   # Combine all markdown files
   cat dcgm-scraped/*.md > NVIDIA-DCGM-User-Guide.md
   ```

## Method 4: Copy-Paste Text (Last Resort)

### Steps:

1. **Open each page in browser**

2. **Select all text content:**
   - Ctrl+A or Cmd+A
   - Copy (Ctrl+C or Cmd+C)

3. **Paste into markdown file:**
   - Create file: `docs/nvidia-manuals/NVIDIA-DCGM-User-Guide.md`
   - Add heading for each section
   - Paste content
   - Format as markdown manually

4. **Manual formatting:**
   ```markdown
   # NVIDIA DCGM User Guide

   ## Overview
   [paste content here]

   ## Installation
   [paste content here]

   ## Configuration
   [paste content here]

   ... etc
   ```

## Required Sections to Capture

Check off each section as you capture it:

- [ ] **Introduction**
  - Overview
  - What is DCGM
  - Architecture

- [ ] **Installation**
  - Package installation (deb/rpm)
  - Docker containers
  - Kubernetes

- [ ] **Configuration**
  - Configuration file options
  - Daemon settings
  - Security

- [ ] **DCGMI Command-Line Tool**
  - Command reference
  - Examples
  - Common workflows

- [ ] **Field Identifiers**
  - Available metrics
  - Field ID reference
  - Supported fields by GPU

- [ ] **Health Checks**
  - Health monitoring
  - Diagnostic tests
  - Error detection

- [ ] **Policy Management**
  - Policy configuration
  - Violation handling

- [ ] **Profiling**
  - GPU profiling
  - Metrics collection

- [ ] **API Reference**
  - C API
  - Python bindings
  - Go bindings

- [ ] **Integration**
  - Prometheus exporter
  - Grafana dashboards
  - Kubernetes operator
  - SLURM plugin

- [ ] **Troubleshooting**
  - Common issues
  - Error codes
  - Debug logs

## Verification Checklist

After scraping, verify:

- [ ] All major sections captured
- [ ] Code examples preserved
- [ ] Tables readable
- [ ] Command syntax preserved
- [ ] File saved to: `docs/nvidia-manuals/NVIDIA-DCGM-User-Guide.md` or `.pdf`
- [ ] File size reasonable (200KB+ for markdown, 2MB+ for PDF)
- [ ] Table of contents added (manual or automated)

## Post-Processing

### Add Table of Contents:

```bash
# Using markdown-toc (npm package)
npm install -g markdown-toc
markdown-toc -i docs/nvidia-manuals/NVIDIA-DCGM-User-Guide.md
```

### Format Code Blocks:

Ensure code blocks are fenced:
```markdown
```bash
dcgmi discovery -l
```
```

### Add Metadata Header:

```markdown
# NVIDIA DCGM User Guide

**Source:** https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/
**Captured:** 2025-12-02
**Version:** Latest (as of capture date)
**Format:** Markdown

---

[Table of Contents]

---

## Introduction
...
```

## Tools to Install (Optional but Helpful)

```bash
# PDF tools
sudo apt-get install poppler-utils    # pdfunite, pdftotext
sudo apt-get install wkhtmltopdf       # HTML to PDF converter

# Markdown tools
npm install -g markdown-toc            # Generate TOC
npm install -g markdownlint-cli        # Lint markdown

# HTML/Document conversion
sudo apt-get install pandoc            # Universal converter
```

## Expected Result

**File:** `/srv/projects/og-ai-inference-research/docs/nvidia-manuals/NVIDIA-DCGM-User-Guide.md`

**Size:** 200-500 KB (markdown) or 2-10 MB (PDF)

**Sections:** 15-30 pages covering all aspects of DCGM

**Quality:**
- All text content preserved
- Code examples in code blocks
- Tables formatted
- Headings hierarchical
- Links preserved (if possible)

## If All Else Fails

Contact NVIDIA support or check if they provide:
- Official PDF download
- Documentation API
- Documentation repository

NVIDIA docs are sometimes available in their GitHub repositories or as downloadable PDFs.

---

**Note:** This manual guide is a fallback if the automated Python scrapers don't work due to missing dependencies or environment issues.
