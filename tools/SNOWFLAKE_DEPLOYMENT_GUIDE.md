# Snowflake Streamlit App Deployment Guide

## Overview

Since you want to deploy privately (not public GitHub), we'll use **Snowflake Streamlit Apps** which allows private deployment without exposing code publicly.

## Environment Variables Status

### ✅ Found (from /srv/projects/bigsirflrts/.env)
- `CLOUDFLARE_API_TOKEN` - Available
- `CLOUDFLARE_ZONE_ID` - Available (26b8bc8be5ffa06c4850054639bdfbb0)
- `CLOUDFLARE_DOMAIN` - Available (10nz.tools)

### ❌ Need from You (Snowflake Credentials)
- `SNOWFLAKE_ACCOUNT` - Account identifier (e.g., `xy12345.us-east-1`)
- `SNOWFLAKE_USER` - Username
- `SNOWFLAKE_PASSWORD` - Password
- `SNOWFLAKE_WAREHOUSE` - Warehouse name
- `SNOWFLAKE_DATABASE` - Database name  
- `SNOWFLAKE_SCHEMA` - Schema name
- `SNOWFLAKE_ROLE` - Role name (optional)

## Snowflake Streamlit Apps Deployment

Snowflake Streamlit Apps are created and managed via SQL commands in Snowflake. The deployment process:

1. **Connect to Snowflake** using credentials
2. **Create a Streamlit app** using `CREATE STREAMLIT` SQL command
3. **Upload the Python code** (the Streamlit app file)
4. **Get the Streamlit app URL** from Snowflake
5. **Configure Cloudflare DNS** to point to the Snowflake Streamlit URL

## Files Needed for Deployment

✅ `tools/unified-calculator-app.py` - Main Streamlit app
✅ `tools/requirements.txt` - Dependencies (Snowflake may handle this differently)
✅ `tools/pages/` - Multi-page structure (if Snowflake supports it)
✅ `models/` - CSV data files (need to be uploaded to Snowflake stage or table)

## Important Notes

1. **Data Files**: The CSV files in `models/` need to be accessible to the Streamlit app. Options:
   - Upload to Snowflake stage (internal stage)
   - Import into Snowflake tables
   - Store in Snowflake file format

2. **Dependencies**: Snowflake Streamlit Apps have built-in support for common packages, but may need specific packages installed

3. **URL Format**: Snowflake Streamlit Apps have URLs like:
   - `https://<account>.snowflakecomputing.com/<path-to-app>`
   - Or custom domain if configured

## Next Steps

Once you provide Snowflake credentials, I'll:

1. Create a deployment script that:
   - Connects to Snowflake
   - Creates the Streamlit app
   - Uploads the code and data files
   - Gets the app URL

2. Configure Cloudflare DNS:
   - Create CNAME record: `calculator.10nz.tools` → Snowflake Streamlit URL
   - Or configure custom domain in Snowflake if supported

3. Update frontend tool card:
   - Update route in `src/features/tools/grid.tsx` to final URL

## Questions for You

1. Do you already have a Snowflake account set up?
2. Do you have a preferred database/schema/warehouse for this app?
3. How do you want to handle the CSV data files?
   - Upload to Snowflake stage?
   - Import into tables?
   - Other method?
4. Do you want a custom domain (`calculator.10nz.tools`) or use Snowflake's default URL?

