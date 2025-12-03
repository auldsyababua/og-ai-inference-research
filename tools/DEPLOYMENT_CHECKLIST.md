# Deployment Checklist for Off-Grid Calculator

## Prerequisites

### 1. Streamlit Community Cloud Deployment
- [ ] GitHub repository created (public or private with Streamlit Cloud access)
- [ ] Code pushed to GitHub
- [ ] Streamlit Community Cloud account connected to GitHub
- [ ] App deployed via Streamlit Cloud UI

**No API keys needed** - Streamlit Community Cloud uses GitHub OAuth

### 2. Cloudflare DNS Configuration
**Required API Credentials:**
- [ ] Cloudflare API Token (with DNS:Edit permission for 10nz.tools zone)
- [ ] OR Cloudflare Account Email + Global API Key
- [ ] Zone ID for 10nz.tools domain

**To get these:**
1. Go to Cloudflare Dashboard → 10nz.tools domain
2. Zone ID is in the right sidebar
3. API Token: Profile → API Tokens → Create Token → DNS:Edit permission

### 3. Snowflake (Optional - only if using Snowflake Streamlit Apps)
**Required Credentials:**
- [ ] Snowflake Account Identifier (e.g., `xy12345.us-east-1`)
- [ ] Snowflake Username
- [ ] Snowflake Password (or key-pair authentication)
- [ ] Warehouse name
- [ ] Database name
- [ ] Schema name

**Note:** Snowflake Streamlit Apps are for apps that need Snowflake data integration. If you just want to host the calculator, use Streamlit Community Cloud instead.

## Files Ready for Deployment

✅ `requirements.txt` - Created
✅ `unified-calculator-app.py` - Main app file
✅ `models/` directory - CSV data files needed
✅ `pages/` directory - Multi-page structure

## Deployment Steps

### Step 1: Prepare GitHub Repository
```bash
cd /srv/projects/og-ai-inference-research
# Create a new repo or use existing one
# Push code including tools/ directory
```

### Step 2: Deploy to Streamlit Community Cloud
1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select repository, branch, and main file: `tools/unified-calculator-app.py`
5. Click "Deploy"

### Step 3: Configure Cloudflare DNS (if using custom domain)
Once Streamlit app is deployed, get the URL (e.g., `https://my-calc.streamlit.app`)

Then use Wrangler to create CNAME record:
```bash
wrangler dns create calculator.10nz.tools CNAME <streamlit-url>
```

Or if using a different hosting service with custom domain support, create A/CNAME record pointing to that service.

### Step 4: Update Frontend Tool Card
Update the route in `/srv/projects/bbui-fresh/src/features/tools/grid.tsx`:
- If using Streamlit Community Cloud: Use the `*.streamlit.app` URL
- If using custom domain: Use `https://calculator.10nz.tools`

## API Keys Needed

Please provide the following so I can automate the Cloudflare DNS setup:

1. **Cloudflare API Token** (preferred) OR **Email + Global API Key**
2. **Cloudflare Zone ID** for 10nz.tools
3. **Streamlit app URL** (after deployment) - if you want me to update DNS automatically

For Snowflake (only if using Snowflake Streamlit Apps):
- Snowflake account details (see above)

## Environment Variables

Once you provide the API keys, I'll add them to:
- `/srv/projects/bbui-fresh/.dev.vars` (for Wrangler/Cloudflare)
- Or create a `.env` file if needed

