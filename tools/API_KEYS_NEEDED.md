# API Keys and Credentials Needed for Deployment

## Summary

I've prepared everything needed for deployment. Here's what I need from you to complete the setup:

## 1. Cloudflare DNS Configuration (Required)

To create the `calculator.10nz.tools` DNS record, I need:

### Option A: API Token (Recommended)
- **Cloudflare API Token** with:
  - Permissions: `Zone:Read`, `DNS:Edit`
  - Zone Resources: Include `10nz.tools` zone

**How to get it:**
1. Go to https://dash.cloudflare.com/profile/api-tokens
2. Click "Create Token"
3. Use "Edit zone DNS" template
4. Select your `10nz.tools` zone
5. Copy the token

### Option B: Account Email + Global API Key
- **Cloudflare Account Email**
- **Global API Key** (from https://dash.cloudflare.com/profile/api-tokens)

### Also Needed:
- **Zone ID** for `10nz.tools` (found in Cloudflare dashboard → 10nz.tools → right sidebar)

**Once you provide these, I'll:**
- Add them to `/srv/projects/bbui-fresh/.dev.vars` (or `.env`)
- Use Wrangler to create the DNS CNAME record pointing to the Streamlit app

## 2. Streamlit Community Cloud (No API Keys Needed)

Streamlit Community Cloud uses GitHub OAuth, so **no API keys are required**. However, you'll need to:

1. **Push the code to GitHub** (public repo or private with Streamlit Cloud access)
2. **Deploy manually** via https://share.streamlit.io OR I can guide you through it

**Files ready for deployment:**
- ✅ `tools/unified-calculator-app.py` - Main app
- ✅ `tools/requirements.txt` - Dependencies
- ✅ `tools/pages/` - Multi-page structure
- ✅ `models/` - CSV data files

**After deployment, you'll get a URL like:** `https://your-app-name.streamlit.app`

## 3. Snowflake (Optional - Only if Using Snowflake Streamlit Apps)

**Note:** Snowflake Streamlit Apps are for apps that need Snowflake data integration. If you just want to host the calculator externally, skip this.

If you want to use Snowflake Streamlit Apps, I'll need:
- **Snowflake Account Identifier** (e.g., `xy12345.us-east-1`)
- **Snowflake Username**
- **Snowflake Password** (or key-pair authentication)
- **Warehouse name**
- **Database name**
- **Schema name**

## What I'll Do Once You Provide Credentials

1. **Add credentials to `.dev.vars` or `.env`** (securely, not committed to git)
2. **Create Cloudflare DNS record** using Wrangler:
   ```bash
   wrangler dns create calculator.10nz.tools CNAME <streamlit-url>
   ```
3. **Update the tool card** in `/srv/projects/bbui-fresh/src/features/tools/grid.tsx` with the final URL

## Alternative: Manual DNS Setup

If you prefer to set up DNS manually:
1. Deploy Streamlit app to Streamlit Community Cloud
2. Get the Streamlit URL (e.g., `https://my-calc.streamlit.app`)
3. In Cloudflare Dashboard → DNS → Add record:
   - Type: CNAME
   - Name: `calculator`
   - Target: `my-calc.streamlit.app` (or the actual Streamlit URL)
   - Proxy: Enabled (orange cloud)
4. Update the tool card route in `grid.tsx` to `https://calculator.10nz.tools`

## Files Created

I've created these files to help with deployment:
- ✅ `tools/requirements.txt` - Python dependencies
- ✅ `tools/DEPLOYMENT_CHECKLIST.md` - Step-by-step checklist
- ✅ `DEPLOYMENT_PLAN.md` - Overview of deployment options

## Next Steps

**Please provide:**
1. Cloudflare API Token (or Email + Global API Key) + Zone ID
2. Let me know if you want to use Streamlit Community Cloud or Snowflake
3. After Streamlit deployment, share the URL so I can update DNS and the tool card

Once I have these, I can complete the Cloudflare DNS setup and update the frontend tool card automatically.

