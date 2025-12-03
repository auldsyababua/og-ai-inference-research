# Snowflake PAT (Programmatic Access Token) Setup Guide

## Current Issue

The token you provided appears to be invalid or expired, or it might be a session token rather than a PAT.

## How to Create a Proper PAT

### Step 1: Create PAT in Snowflake

1. **Log into Snowflake**: https://ZWZLXDA-MEB82135.snowflakecomputing.com
2. **Go to**: User Profile → Security → Programmatic Access Tokens
3. **Click**: "Create Token" or "Generate Token"
4. **Configure**:
   - Name: `homelab-automation` (or your choice)
   - Expiration: Set appropriate expiration (or no expiration)
   - Permissions: Ensure it has ACCOUNTADMIN role or USERADMIN privileges
5. **Copy the token** immediately (you won't see it again!)

### Step 2: Use the PAT

Once you have a valid PAT, you can use it in several ways:

#### Option A: Pass as argument
```bash
python3 add_public_key_with_pat.py "your-pat-token-here"
```

#### Option B: Set as environment variable
```bash
export SNOWFLAKE_PAT_TOKEN="your-pat-token-here"
python3 add_public_key_with_pat.py
```

#### Option C: Save to file
```bash
echo "your-pat-token-here" > homelab-token-secret.txt
python3 add_public_key_with_pat.py
```

## Alternative: Use Session Token from Browser

If you're already logged into Snowflake in your browser, you can extract the session token:

1. Open browser DevTools (F12)
2. Go to Application/Storage → Cookies
3. Find cookie: `snowflake-session-token` or similar
4. Copy the value
5. Use it with the script

## Token Format

PAT tokens typically:
- Are long alphanumeric strings
- May include dashes or underscores
- Are different from session tokens (which are usually JWTs)

The token you provided looks like a JWT (has dots separating three parts), which suggests it might be a session token rather than a PAT.

## Quick Test

After getting a valid PAT, test it:

```bash
python3 add_public_key_with_pat.py "<your-pat-token>"
```

If successful, you'll see:
```
✓ Connected successfully!
✓ Public key added successfully!
```

## Troubleshooting

### "Invalid OAuth access token"
- Token may be expired
- Token may be a session token (not a PAT)
- Token may not have correct permissions

### "Insufficient privileges"
- PAT needs ACCOUNTADMIN role or USERADMIN privileges
- Create a new PAT with proper permissions

### Token not working
- Verify token was copied correctly (no extra spaces)
- Check token hasn't expired
- Ensure token has necessary role assignments

