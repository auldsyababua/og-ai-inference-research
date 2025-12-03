# Key-Pair Authentication Setup - Complete ✅

## What Was Done

1. ✅ **RSA key pair generated**:
   - Private key: `rsa_key.pem` (secure, never share)
   - Public key: `rsa_key.pub` (safe to add to Snowflake)

2. ✅ **Configuration updated**:
   - `.streamlit/secrets.toml` now uses `private_key_file` instead of `password`
   - Private keys added to `.gitignore`

3. ✅ **Scripts updated**:
   - `setup_snowflake_resources.py` uses key-pair authentication
   - `test_snowflake_connection.py` created to test connection

## Next Step: Add Public Key to Snowflake

### Your Public Key

```
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvMG95iR8+lUCpuxmwoox
4yHMHCWpXJePI5m9RhN8mzCDnWtPymmzSA0lVTgUauC6nkh1lRNgVL8Cv7QMeZjj
ntz1DTImlUcTcyWF2xhskPwDQpvm+wdpO7wM2lD5F3RaRih1miyzpliPSSv5/usp
myyNI0VYTqs/0b74rAvec3HVZ733XFXxleb7+aIQvlsCIq/mdy87HHN9EG2jN4Na
c0f32CVXxZoEF30y4OxDzmuQuZXCK8n2j/Q8rM9Jkp2s9tvsXIluFEt9WEpNgTQh
HS9oggpGzpvoYNFJ6t8zMtxqFnKse4HgiYr0n5yaUvPxErJxt6Lw6Kb1d429+EC0
qwIDAQAB
-----END PUBLIC KEY-----
```

### How to Add It

#### Option 1: Via Snowflake Web UI (Recommended)

1. **Log into Snowflake**: https://ZWZLXDA-MEB82135.snowflakecomputing.com
2. **Click your username** (top right) → **"User Profile"**
3. **Go to**: **"Security"** tab
4. **Scroll to**: **"Public Keys"** section
5. **Click**: **"Add Public Key"** button
6. **Copy the entire public key** (including BEGIN/END lines) from above
7. **Paste** into the text area
8. **Click**: **"Add"** or **"Save"**

#### Option 2: Via SQL (If you have ACCOUNTADMIN access)

1. **Log into Snowflake** and open a worksheet
2. **Run this SQL** (replace `<PUBLIC_KEY>` with the key content):

```sql
ALTER USER 10NETZERO SET RSA_PUBLIC_KEY='MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvMG95iR8+lUCpuxmwoox4yHMHCWpXJePI5m9RhN8mzCDnWtPymmzSA0lVTgUauC6nkh1lRNgVL8Cv7QMeZjjntz1DTImlUcTcyWF2xhskPwDQpvm+wdpO7wM2lD5F3RaRih1miyzpliPSSv5/uspmyyNI0VYTqs/0b74rAvec3HVZ733XFXxleb7+aIQvlsCIq/mdy87HHN9EG2jN4Nac0f32CVXxZoEF30y4OxDzmuQuZXCK8n2j/Q8rM9Jkp2s9tvsXIluFEt9WEpNgTQhHS9oggpGzpvoYNFJ6t8zMtxqFnKse4HgiYr0n5yaUvPxErJxt6Lw6Kb1d429+EC0qwIDAQAB';
```

**Note**: For SQL, remove the `-----BEGIN PUBLIC KEY-----` and `-----END PUBLIC KEY-----` lines, keep only the base64 content.

## After Adding the Public Key

### Test the Connection

```bash
cd /srv/projects/og-ai-inference-research/tools
python3 test_snowflake_connection.py
```

If successful, you'll see:
```
✓ CONNECTION SUCCESSFUL!
```

### Set Up Snowflake Resources

```bash
python3 setup_snowflake_resources.py
```

This will create:
- Warehouse: `CALCULATOR_WH`
- Database: `CALCULATOR_DB`
- Schema: `PUBLIC`

## Security Notes

- ✅ Private key (`rsa_key.pem`) is in `.gitignore` - will not be committed
- ✅ Keep the private key secure - never share it
- ✅ The public key is safe to add to Snowflake
- ✅ For Streamlit Cloud deployment, you'll need to upload the private key as a secret

## Files Created

- `rsa_key.pem` - Private key (secure, in .gitignore)
- `rsa_key.pub` - Public key (safe to share)
- `test_snowflake_connection.py` - Test script
- `ADD_PUBLIC_KEY_TO_SNOWFLAKE.md` - Detailed instructions

## Troubleshooting

### "Invalid key pair" error
- Make sure you added the **public key** (not private key) to Snowflake
- Verify the key was added correctly (check User → Security → Public Keys)

### "Public key not found" error
- Make sure you're logged in as the correct user (10NETZERO)
- Check that the key was saved in Snowflake

### Connection still fails
- Verify the account identifier is correct: `ZWZLXDA-MEB82135`
- Check that the user has proper permissions
- Ensure the warehouse is running (if it exists)

