# Next Steps - Key Format Fixed! ✅

## Status

✅ **Key format issue resolved** - The private key is now being loaded correctly using the cryptography library
⚠️ **Public key needs to be added to Snowflake** - The "JWT token is invalid" error means Snowflake doesn't have your public key yet

## What Was Fixed

1. ✅ Updated `test_snowflake_connection.py` to use `cryptography` library
2. ✅ Updated `setup_snowflake_resources.py` to use `cryptography` library  
3. ✅ Added `cryptography>=41.0.0` to `requirements.txt`
4. ✅ Private key is now properly converted from PEM to DER format (what Snowflake expects)

## Add Public Key to Snowflake

The error "JWT token is invalid" means the public key hasn't been added to Snowflake yet. Here's your public key:

### Full Public Key (for UI):
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

### Base64 Only (for SQL):
```
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvMG95iR8+lUCpuxmwoox4yHMHCWpXJePI5m9RhN8mzCDnWtPymmzSA0lVTgUauC6nkh1lRNgVL8Cv7QMeZjjntz1DTImlUcTcyWF2xhskPwDQpvm+wdpO7wM2lD5F3RaRih1miyzpliPSSv5/uspmyyNI0VYTqs/0b74rAvec3HVZ733XFXxleb7+aIQvlsCIq/mdy87HHN9EG2jN4Nac0f32CVXxZoEF30y4OxDzmuQuZXCK8n2j/Q8rM9Jkp2s9tvsXIluFEt9WEpNgTQhHS9oggpGzpvoYNFJ6t8zMtxqFnKse4HgiYr0n5yaUvPxErJxt6Lw6Kb1d429+EC0qwIDAQAB
```

## How to Add Public Key

### Option 1: Via Snowflake Web UI (Easiest)

1. Log into: https://ZWZLXDA-MEB82135.snowflakecomputing.com
2. Click your username (top right) → **"User Profile"**
3. Go to **"Security"** tab
4. Scroll to **"Public Keys"** section
5. Click **"Add Public Key"**
6. Copy the **full public key** (with BEGIN/END lines) from above
7. Paste and click **"Add"**

### Option 2: Via SQL

Run this in Snowflake (replace with the base64 key above):

```sql
ALTER USER 10NETZERO SET RSA_PUBLIC_KEY='MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvMG95iR8+lUCpuxmwoox4yHMHCWpXJePI5m9RhN8mzCDnWtPymmzSA0lVTgUauC6nkh1lRNgVL8Cv7QMeZjjntz1DTImlUcTcyWF2xhskPwDQpvm+wdpO7wM2lD5F3RaRih1miyzpliPSSv5/uspmyyNI0VYTqs/0b74rAvec3HVZ733XFXxleb7+aIQvlsCIq/mdy87HHN9EG2jN4Nac0f32CVXxZoEF30y4OxDzmuQuZXCK8n2j/Q8rM9Jkp2s9tvsXIluFEt9WEpNgTQhHS9oggpGzpvoYNFJ6t8zMtxqFnKse4HgiYr0n5yaUvPxErJxt6Lw6Kb1d429+EC0qwIDAQAB';
```

## After Adding Public Key

### Test Connection:
```bash
cd /srv/projects/og-ai-inference-research/tools
python3 test_snowflake_connection.py
```

Expected output when successful:
```
✓ CONNECTION SUCCESSFUL!
User: 10NETZERO
Role: ACCOUNTADMIN
Account: ZWZLXDA
```

### Set Up Resources:
```bash
python3 setup_snowflake_resources.py
```

This will create:
- Warehouse: `CALCULATOR_WH`
- Database: `CALCULATOR_DB`
- Schema: `PUBLIC`

## Troubleshooting

### Still getting "JWT token is invalid"
- Verify the public key was added correctly in Snowflake
- Check User → Security → Public Keys to see if it's listed
- Make sure you're logged in as the correct user (10NETZERO)

### "Invalid key pair" error
- Make sure you added the **public key** (not private key) to Snowflake
- Verify the key format is correct (should have BEGIN/END lines for UI)

### Connection works but setup fails
- Make sure you have ACCOUNTADMIN role
- Check that billing is configured (warehouses need to be active)

