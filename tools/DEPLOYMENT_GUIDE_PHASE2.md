# Phase 2 Deployment Guide: Automated Package Management

## Overview

This guide covers Phase 2 of the matplotlib/seaborn fix: automating package management via `environment.yml` in the deployment script.

**Status**: Code changes complete, ready for deployment
**Prerequisites**: Phase 1 must be complete (packages added via Snowsight UI)
**Expected Downtime**: 1-2 minutes during deployment
**Risk Level**: Low-Medium (well-tested, clear rollback path)

## What Changed

### Files Modified

1. **`tools/environment.yml`** (NEW)
   - Conda environment specification
   - Pinned versions: matplotlib=3.10.6, seaborn=0.13.2, streamlit=1.35.0
   - Ensures reproducible deployments

2. **`tools/deploy_to_snowflake_streamlit.py`** (MODIFIED)
   - Uploads environment.yml to stage
   - Implements DROP + CREATE workflow (replaces CREATE OR REPLACE)
   - Adds deployment verification checks
   - Enhanced output messaging

### Key Changes in Deployment Script

**Change 1: Upload environment.yml** (after line 94)
```python
# Upload environment.yml for package management
print(f"\n1b. Uploading environment.yml for package management...")
env_file = SCRIPT_DIR / "environment.yml"
if env_file.exists():
    upload_file_to_stage(cursor, str(env_file), STAGE_NAME, "")
else:
    print("   ⚠ Warning: environment.yml not found")
```

**Change 2: DROP before CREATE** (replaces CREATE OR REPLACE)
```python
# Drop existing app to pick up new environment.yml
print(f"\n4. Dropping existing Streamlit app (if exists)...")
cursor.execute(f"DROP STREAMLIT IF EXISTS {APP_NAME}")

# Create Streamlit app (reads environment.yml from stage)
print(f"\n4b. Creating Streamlit app with package dependencies...")
create_sql = f"""
CREATE STREAMLIT {APP_NAME}
FROM @{STAGE_NAME}
MAIN_FILE = 'unified-calculator-app.py'
...
"""
```

**Change 3: Deployment Verification**
```python
# Verify deployment
print(f"\n5. Verifying deployment...")
cursor.execute(f"SHOW STREAMLITS LIKE '{APP_NAME}'")
# ... check app exists

# Check stage files
cursor.execute(f"LIST @{STAGE_NAME}")
# ... verify environment.yml present
```

## Pre-Deployment Checklist

- [ ] Phase 1 complete (matplotlib/seaborn working via UI)
- [ ] Git changes committed (for rollback capability)
- [ ] `tools/environment.yml` exists locally
- [ ] `tools/deploy_to_snowflake_streamlit.py` updated
- [ ] Snowflake credentials configured
- [ ] Private key (`rsa_key.pem`) in tools/ directory
- [ ] Maintenance window scheduled and communicated to users

## Deployment Steps

### 1. Verify Prerequisites

```bash
cd /srv/projects/og-ai-inference-research/tools

# Check files exist
ls -la environment.yml
ls -la deploy_to_snowflake_streamlit.py
ls -la rsa_key.pem

# Verify git status
git status
```

### 2. Test in Non-Production (Optional but Recommended)

If you have a dev/staging environment:

```bash
# Modify script temporarily to use test app name
# Deploy to test environment
python3 deploy_to_snowflake_streamlit.py

# Verify test app works
# Restore production app name
```

### 3. Announce Maintenance Window

**Example notification:**
```
🔧 Maintenance Notice: Streamlit Calculator App
Time: [DATE] at [TIME]
Duration: ~2 minutes
Impact: Brief app downtime for package management upgrade
Benefit: Resolves matplotlib import errors permanently
```

### 4. Execute Deployment

```bash
cd /srv/projects/og-ai-inference-research/tools

# Run deployment script
python3 deploy_to_snowflake_streamlit.py
```

### 5. Monitor Output

Expected output:
```
============================================================
DEPLOY STREAMLIT APP TO SNOWFLAKE
============================================================
Connecting to Snowflake...
✓ Connected!

1. Creating stage: streamlit_apps
   ✓ Stage created/verified

1b. Uploading environment.yml for package management...
  Uploading environment.yml to @streamlit_apps/...
    ✓ environment.yml uploaded successfully

2. Uploading Streamlit app files...
  ...

4. Dropping existing Streamlit app (if exists)...
   ✓ Existing app dropped

4b. Creating Streamlit app with package dependencies: off_grid_calculator
   ✓ Streamlit app created with matplotlib and seaborn packages!

5. Verifying deployment...
   ✓ App exists in Snowflake

5b. Verifying stage files...
   ✓ All required files present on stage

6. Getting app URL...
   ✓ App URL: https://ZWZLXDA-MEB82135.snowflakecomputing.com/streamlit/off_grid_calculator

============================================================
DEPLOYMENT COMPLETE!
============================================================
```

### 6. Post-Deployment Verification

**Immediate Checks:**
- [ ] Deployment script completed without errors
- [ ] App URL accessible
- [ ] App loads without ModuleNotFoundError
- [ ] No errors in Snowflake logs

**Functional Testing:**
- [ ] Navigate to app URL
- [ ] Test all pages (especially visualization pages):
  - Generator Risk Parameters
  - BESS Sizing
  - Data Logistics
- [ ] Verify charts/plots render correctly
- [ ] Check for any new errors or warnings

**Verification via Snowsight:**
- [ ] Open app in Snowsight editor
- [ ] Click "Packages" button
- [ ] Verify matplotlib=3.10.6, seaborn=0.13.2 listed
- [ ] Check stage files: `LIST @streamlit_apps` (should show environment.yml)

**SQL Verification:**
```sql
-- Check app exists
SHOW STREAMLIT off_grid_calculator;

-- Check stage files
LIST @streamlit_apps;

-- Should see: environment.yml, unified-calculator-app.py, pages/, models/
```

### 7. Announce Completion

**Example notification:**
```
✅ Maintenance Complete: Streamlit Calculator App
Status: Deployed successfully
Changes: Package management now automated via environment.yml
Result: matplotlib and seaborn permanently configured
Next deployment: Will automatically include package dependencies
```

## Rollback Plan

If deployment fails or issues occur:

### Option A: Revert Git Changes

```bash
cd /srv/projects/og-ai-inference-research

# Revert deployment script changes
git checkout HEAD -- tools/deploy_to_snowflake_streamlit.py

# Remove environment.yml
rm tools/environment.yml

# Redeploy with old script (CREATE OR REPLACE, no packages)
cd tools
python3 deploy_to_snowflake_streamlit.py
```

### Option B: Manual SQL Recovery

**⚠️ Important**: Manual SQL recovery will NOT include package dependencies. After using this option, you must re-add matplotlib and seaborn via Phase 1 (UI method).

```sql
-- Drop problematic app
DROP STREAMLIT IF EXISTS off_grid_calculator;

-- Recreate manually (will use existing stage files but NOT environment.yml)
CREATE STREAMLIT off_grid_calculator
FROM @streamlit_apps
MAIN_FILE = 'unified-calculator-app.py'
QUERY_WAREHOUSE = CALCULATOR_WH;
```

**After manual recovery:**
1. Open app in Snowsight editor
2. Click "Packages" → Add matplotlib and seaborn manually
3. Or use Option A (git revert) to restore full functionality

### Option C: Fall Back to Phase 1

If Phase 2 deployment fails, Phase 1 (UI-added packages) remains active:
1. Packages added via UI persist independently
2. App continues working with matplotlib/seaborn
3. Fix deployment script issues offline
4. Retry Phase 2 when ready

**Recovery Time**: 5-10 minutes
**Data Loss**: None (Streamlit is stateless)

## Troubleshooting

### Issue: environment.yml not found

**Symptom:**
```
⚠ Warning: environment.yml not found, packages may not be installed
```

**Fix:**
```bash
cd /srv/projects/og-ai-inference-research
cp .scratch/raep-debug/02-snowflake-matplotlib-import/tests/environment.yml tools/
```

### Issue: DROP STREAMLIT fails

**Symptom:**
```
Error dropping streamlit: [SQL error message]
```

**Fix:**
- Usually safe to ignore if CREATE succeeds
- CREATE OR REPLACE should work as fallback
- Check app exists: `SHOW STREAMLIT off_grid_calculator`

### Issue: CREATE fails after DROP

**Symptom:**
```
Error creating streamlit: [SQL error message]
```

**Fix:**
1. Check error message for specifics
2. Verify stage has required files: `LIST @streamlit_apps`
3. Manually recreate via SQL (Option B rollback)
4. Fall back to Phase 1 UI method

### Issue: Packages not installed after deployment

**Symptom:**
- ModuleNotFoundError still occurs
- Packages not visible in Snowsight → Packages

**Fix:**
1. Verify environment.yml on stage: `LIST @streamlit_apps`
2. Check environment.yml syntax (should match tools/environment.yml)
3. Drop and recreate app manually via SQL
4. If persistent, use Phase 1 UI method as fallback

### Issue: App downtime longer than expected

**Expected**: 30-60 seconds
**If longer**:
1. Check Snowflake service status
2. Monitor Snowsight → Streamlit section
3. Check warehouse is running: `SHOW WAREHOUSES`
4. Contact Snowflake support if >5 minutes

## Validation Checklist

Post-deployment validation:

**Infrastructure:**
- [ ] environment.yml exists on stage (`LIST @streamlit_apps`)
- [ ] App exists (`SHOW STREAMLIT off_grid_calculator`)
- [ ] All stage files present (environment.yml, .py files, CSV files)

**Packages:**
- [ ] Packages visible in Snowsight → Packages
- [ ] matplotlib=3.10.6 listed
- [ ] seaborn=0.13.2 listed
- [ ] streamlit=1.35.0 listed

**Functionality:**
- [ ] App loads without errors
- [ ] No ModuleNotFoundError
- [ ] All pages accessible
- [ ] Visualizations render correctly
- [ ] No new errors introduced

**Documentation:**
- [ ] Deployment logged in issue tracker
- [ ] Git commit with descriptive message
- [ ] Team notified of changes

## Future Deployments

**Adding New Packages:**
1. Edit `tools/environment.yml`
2. Add package to dependencies list
3. Run deployment script (DROP + CREATE picks up changes)
4. No manual UI steps required

**Example - Adding pandas:**
```yaml
name: sf_env
channels:
  - snowflake
dependencies:
  - streamlit=1.35.0
  - matplotlib=3.10.6
  - seaborn=0.13.2
  - pandas=2.1.0  # New package
```

**Updating Package Versions:**
1. Edit version in `tools/environment.yml`
2. Test in non-prod if available
3. Deploy during maintenance window
4. Verify updated versions in Snowsight → Packages

## Benefits Achieved

✅ **Automated**: No manual UI steps for package management
✅ **Version Controlled**: environment.yml tracked in git
✅ **Reproducible**: Same packages deployed every time
✅ **Documented**: Clear deployment and rollback procedures
✅ **Sustainable**: Future package changes are straightforward

## Support

**Issues during deployment:**
- Check troubleshooting section above
- Review error messages in deployment script output
- Fall back to Phase 1 (UI method) if needed
- Consult `.scratch/raep-debug/02-snowflake-matplotlib-import/10-handoff.md` for investigation details

**Questions:**
- Refer to Snowflake Streamlit documentation
- Check `tools/README.md` for additional context
- Review RAEP investigation artifacts in `.scratch/raep-debug/02-snowflake-matplotlib-import/`

---

**Document Version**: 1.0
**Last Updated**: 2025-12-03
**Related**: Phase 1 completed via UI, RAEP investigation in .scratch/raep-debug/02-snowflake-matplotlib-import/
