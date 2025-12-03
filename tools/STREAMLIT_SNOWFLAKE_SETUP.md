# Streamlit + Snowflake Connection Setup

## Overview

This guide explains how to deploy the Streamlit app and connect it to Snowflake for data storage/retrieval.

## Authentication Issue

**Current Status**: MFA (Multi-Factor Authentication) is required for the Snowflake account.

**Options to resolve**:

### Option 1: Disable MFA (Not Recommended for Production)
- Go to Snowflake web UI
- User settings → Security → Disable MFA
- **Note**: This reduces security

### Option 2: Use Key-Pair Authentication (Recommended)
1. Generate a key pair:
   ```bash
   openssl genrsa -out rsa_key.pem 2048
   openssl rsa -in rsa_key.pem -pubout -out rsa_key.pub
   ```
2. Add public key to Snowflake user
3. Update `secrets.toml` to use `private_key_file` instead of `password`

### Option 3: Use External Browser Auth (For Local Development)
- Use `authenticator = "externalbrowser"` in connection config
- This opens a browser for authentication

## Configuration Files

### 1. Local Development: `.streamlit/secrets.toml`

```toml
[connections.snowflake]
account = "ZWZLXDA-MEB82135"
user = "10NETZERO"
password = "eNCt-L.WDm4ZKVADTbw8"
role = "ACCOUNTADMIN"
warehouse = "CALCULATOR_WH"  # Set after creating warehouse
database = "CALCULATOR_DB"   # Set after creating database
schema = "PUBLIC"
```

### 2. Streamlit Community Cloud: App Secrets

When deploying to Streamlit Community Cloud:
1. Go to your app settings
2. Click "Secrets"
3. Add the same configuration as above

**Important**: Never commit `secrets.toml` to git!

## Deployment Steps

### Step 1: Set Up Snowflake Resources

1. **Log into Snowflake**: https://ZWZLXDA-MEB82135.snowflakecomputing.com
2. **Create Warehouse** (if not exists):
   ```sql
   CREATE WAREHOUSE IF NOT EXISTS CALCULATOR_WH
   WITH WAREHOUSE_SIZE = 'X-SMALL'
   AUTO_SUSPEND = 60
   AUTO_RESUME = TRUE;
   ```
3. **Create Database** (if not exists):
   ```sql
   CREATE DATABASE IF NOT EXISTS CALCULATOR_DB;
   USE DATABASE CALCULATOR_DB;
   CREATE SCHEMA IF NOT EXISTS PUBLIC;
   ```
4. **Resume Warehouse**:
   ```sql
   ALTER WAREHOUSE CALCULATOR_WH RESUME;
   ```

### Step 2: Import CSV Data to Snowflake (Optional)

If you want to store CSV data in Snowflake tables:

```sql
USE DATABASE CALCULATOR_DB;
USE SCHEMA PUBLIC;

-- Create tables
CREATE TABLE IF NOT EXISTS gpu_generator_compatibility (
    -- Define columns based on CSV structure
);

CREATE TABLE IF NOT EXISTS bess_sizing (
    -- Define columns based on CSV structure
);

CREATE TABLE IF NOT EXISTS data_logistics (
    -- Define columns based on CSV structure
);

-- Import data (using Snowflake UI or COPY INTO commands)
```

### Step 3: Deploy to Streamlit Community Cloud

1. **Push code to GitHub** (create a repo if needed)
2. **Go to**: https://share.streamlit.io
3. **Sign in** with GitHub
4. **Click "New app"**
5. **Select**:
   - Repository: Your GitHub repo
   - Branch: `main` (or your branch)
   - Main file: `tools/unified-calculator-app.py`
6. **Add Secrets**:
   - Click "Advanced settings" → "Secrets"
   - Add the Snowflake connection config (same as `secrets.toml`)
7. **Deploy!**

### Step 4: Set Up Cloudflare DNS

Once Streamlit app is deployed and you have the URL:

```bash
cd /srv/projects/bbui-fresh
./scripts/setup-cloudflare-dns.sh https://your-app-name.streamlit.app
```

Or manually in Cloudflare Dashboard:
- Type: CNAME
- Name: `calculator`
- Target: `your-app-name.streamlit.app`
- Proxy: Enabled

### Step 5: Update Frontend Tool Card

The tool card in `src/features/tools/grid.tsx` already points to `https://calculator.10nz.tools` - no changes needed once DNS is set up.

## Current App Behavior

The Streamlit app is designed to:
1. **Try to connect to Snowflake** first (if configured)
2. **Fall back to local CSV files** if Snowflake is unavailable
3. This allows the app to work both locally and in production

## Troubleshooting

### MFA Required Error
- **Solution**: Use key-pair authentication or disable MFA (not recommended)

### Warehouse Suspended
- **Solution**: Resume warehouse: `ALTER WAREHOUSE CALCULATOR_WH RESUME;`

### Connection Timeout
- **Solution**: Check firewall/network settings
- Verify warehouse is running

### CSV Files Not Found
- **Solution**: Ensure CSV files are in the repo or import them to Snowflake tables

## Next Steps

1. ✅ Resolve MFA/authentication issue
2. ✅ Create warehouse and database in Snowflake
3. ✅ Deploy to Streamlit Community Cloud
4. ✅ Set up Cloudflare DNS
5. ✅ Test the deployed app

