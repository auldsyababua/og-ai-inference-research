# Add Public Key to Snowflake User

## Public Key Generated

The RSA key pair has been generated:
- **Private key**: `rsa_key.pem` (keep secure, never share)
- **Public key**: `rsa_key.pub` (add to Snowflake)

## Steps to Add Public Key to Snowflake

### Option 1: Via Snowflake Web UI (Easiest)

1. **Log into Snowflake**: https://ZWZLXDA-MEB82135.snowflakecomputing.com
2. **Go to**: User settings → Security → Public Keys
3. **Click**: "Add Public Key"
4. **Copy the public key** from `rsa_key.pub` (shown below)
5. **Paste** into the form
6. **Save**

### Option 2: Via SQL (ACCOUNTADMIN role required)

Run this SQL command in Snowflake:

```sql
ALTER USER 10NETZERO SET RSA_PUBLIC_KEY='<PUBLIC_KEY_CONTENT>';
```

Replace `<PUBLIC_KEY_CONTENT>` with the content from `rsa_key.pub` (remove BEGIN/END lines, keep only the key content).

## Your Public Key

```
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyK8vJ8Z5Q3x7V2mN9pL
... (full key will be shown when you run the script)
-----END PUBLIC KEY-----
```

**To get the full public key**, run:
```bash
cat /srv/projects/og-ai-inference-research/tools/rsa_key.pub
```

## After Adding the Public Key

1. **Test the connection**:
   ```bash
   cd /srv/projects/og-ai-inference-research/tools
   python3 setup_snowflake_resources.py
   ```

2. **If successful**, proceed with deployment steps

## Security Notes

- ✅ Private key (`rsa_key.pem`) is already in `.gitignore`
- ✅ Never commit the private key to git
- ✅ Keep the private key secure
- ✅ The public key can be shared (it's safe to add to Snowflake)

