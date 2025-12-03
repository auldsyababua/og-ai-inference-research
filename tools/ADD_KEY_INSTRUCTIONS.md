# Add Public Key to Snowflake via SQL

## SQL Command

Copy and paste this SQL command into Snowflake:

```sql
ALTER USER 10NETZERO SET RSA_PUBLIC_KEY='MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvMG95iR8+lUCpuxmwoox4yHMHCWpXJePI5m9RhN8mzCDnWtPymmzSA0lVTgUauC6nkh1lRNgVL8Cv7QMeZjjntz1DTImlUcTcyWF2xhskPwDQpvm+wdpO7wM2lD5F3RaRih1miyzpliPSSv5/uspmyyNI0VYTqs/0b74rAvec3HVZ733XFXxleb7+aIQvlsCIq/mdy87HHN9EG2jN4Nac0f32CVXxZoEF30y4OxDzmuQuZXCK8n2j/Q8rM9Jkp2s9tvsXIluFEt9WEpNgTQhHS9oggpGzpvoYNFJ6t8zMtxqFnKse4HgiYr0n5yaUvPxErJxt6Lw6Kb1d429+EC0qwIDAQAB';
```

## How to Run

### Option A: Via Snowflake Web UI (Snowsight)

1. **Log into Snowflake**: https://ZWZLXDA-MEB82135.snowflakecomputing.com
2. **Open a Worksheet** (click "Worksheets" in left sidebar)
3. **Make sure you're using ACCOUNTADMIN role** (check top right)
4. **Paste the SQL command** above
5. **Click "Run"** (or press Ctrl+Enter)
6. **Verify success**: You should see "Statement executed successfully"

### Option B: Via snowsql CLI (if installed)

```bash
snowsql -a ZWZLXDA-MEB82135 -u 10NETZERO -r ACCOUNTADMIN
```

Then paste the SQL command.

## Verify the Key Was Added

After running the ALTER command, verify with:

```sql
DESC USER 10NETZERO;
```

Look for `RSA_PUBLIC_KEY` in the output - it should show your public key.

## Test Connection

After adding the key, test the connection:

```bash
cd /srv/projects/og-ai-inference-research/tools
python3 test_snowflake_connection.py
```

Expected output:
```
✓ CONNECTION SUCCESSFUL!
```

## Troubleshooting

### "Insufficient privileges" error
- Make sure you're logged in as ACCOUNTADMIN role
- Or ensure your role has USER ADMIN privileges

### "Invalid key format" error
- Make sure you copied the entire base64 string (no spaces, no line breaks)
- The key should be one continuous string

### Still getting "JWT token is invalid"
- Wait a few seconds after adding the key (propagation delay)
- Verify the key was added: `DESC USER 10NETZERO;`
- Make sure you're testing with the same user (10NETZERO)

