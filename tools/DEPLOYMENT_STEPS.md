# Deployment Steps - Streamlit + Snowflake

## Current Status

✅ **Billing resolved** - Snowflake account is active
⚠️ **MFA required** - Need to resolve authentication method

## Step-by-Step Deployment

### Step 1: Resolve MFA Authentication

Your Snowflake account requires MFA. Choose one:

#### Option A: Key-Pair Authentication (Recommended)

```bash
# Generate key pair
cd /srv/projects/og-ai-inference-research/tools
openssl genrsa -out rsa_key.pem 2048
openssl rsa -in rsa_key.pem -pubout -out rsa_key.pub

# Add public key to Snowflake user (via SQL or UI)
# Then update secrets.toml to use:
# private_key_file = "rsa_key.pem"
```

#### Option B: Disable MFA (Not Recommended)
- Go to Snowflake web UI → User settings → Security → Disable MFA

### Step 2: Set Up Snowflake Resources

```bash
cd /srv/projects/og-ai-inference-research/tools
python3 setup_snowflake_resources.py
```

This creates:
- Warehouse: `CALCULATOR_WH`
- Database: `CALCULATOR_DB`
- Schema: `PUBLIC`

### Step 3: Deploy to Streamlit Community Cloud

1. **Push code to GitHub** (create repo if needed):
   ```bash
   cd /srv/projects/og-ai-inference-research
   git init
   git add .
   git commit -m "Initial commit: Off-grid calculator"
   # Create repo on GitHub, then:
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Deploy on Streamlit Community Cloud**:
   - Go to https://share.streamlit.io
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Main file: `tools/unified-calculator-app.py`
   - Click "Advanced settings" → "Secrets"
   - Add Snowflake connection config (same as `.streamlit/secrets.toml`)

3. **Deploy!**

### Step 4: Set Up Cloudflare DNS

Once you have the Streamlit app URL:

```bash
cd /srv/projects/bbui-fresh
./scripts/setup-cloudflare-dns.sh https://your-app-name.streamlit.app
```

### Step 5: Verify

1. Check Streamlit app is accessible
2. Check `calculator.10nz.tools` resolves correctly
3. Test the calculator functionality

## Files Created

- ✅ `requirements.txt` - Includes `snowflake-connector-python[pandas]`
- ✅ `.streamlit/secrets.toml` - Snowflake connection config
- ✅ `setup_snowflake_resources.py` - Creates warehouse/database/schema
- ✅ `unified-calculator-app.py` - Updated to use Snowflake connection (with fallback)

## Important Notes

1. **Never commit `secrets.toml`** - Add to `.gitignore`
2. **For Streamlit Cloud**: Add secrets via app settings UI
3. **CSV files**: Currently loaded from local filesystem. Can be imported to Snowflake tables later if needed
4. **MFA**: Must be resolved before deployment

## Troubleshooting

### MFA Error
- Use key-pair authentication or disable MFA

### Warehouse Suspended
- Run: `ALTER WAREHOUSE CALCULATOR_WH RESUME;` in Snowflake

### Connection Failed
- Verify credentials in `secrets.toml`
- Check warehouse is running
- Verify network/firewall settings

