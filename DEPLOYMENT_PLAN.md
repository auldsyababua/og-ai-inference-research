# Streamlit Calculator Deployment Plan

## Overview
Deploy the Off-Grid Inference Infra Calculator to Streamlit Community Cloud and configure Cloudflare DNS.

## Deployment Options

### Option 1: Streamlit Community Cloud (Recommended)
- **Pros**: Free, easy deployment, automatic HTTPS
- **Cons**: Requires public GitHub repo, no custom domain support (only *.streamlit.app)
- **URL Format**: `https://<app-name>.streamlit.app`

### Option 2: Snowflake Streamlit Apps
- **Pros**: Integrated with Snowflake data, can use Snowflake authentication
- **Cons**: Requires Snowflake account, apps run inside Snowflake
- **Note**: This is for apps that need Snowflake data integration, not just hosting

### Option 3: Self-Hosted (Railway, Render, etc.)
- **Pros**: Custom domain support (calculator.10nz.tools)
- **Cons**: Costs money, more setup required
- **URL Format**: `https://calculator.10nz.tools` (via Cloudflare DNS)

## Required API Keys/Credentials

### For Cloudflare DNS (via Wrangler)
- **Cloudflare API Token** with DNS edit permissions
- Or **Cloudflare Account Email + Global API Key**
- **Zone ID** for 10nz.tools domain

### For Streamlit Community Cloud
- **GitHub Personal Access Token** (if automating via API)
- Or manual deployment via web UI (no API keys needed)

### For Snowflake (if using Snowflake Streamlit Apps)
- **Snowflake Account** identifier
- **Snowflake Username** and **Password** (or key-pair auth)
- **Snowflake Warehouse, Database, Schema** names

## Files Needed for Deployment

1. **requirements.txt** - Python dependencies
2. **streamlit_app.py** or **unified-calculator-app.py** - Main app file
3. **models/** directory - CSV data files
4. **pages/** directory - Multi-page structure (if used)
5. **README.md** - Documentation

## Next Steps

1. Create requirements.txt
2. Prepare GitHub repository (if using Streamlit Community Cloud)
3. Configure Cloudflare DNS (if using custom domain)
4. Deploy to chosen platform
5. Update tool card route in frontend

