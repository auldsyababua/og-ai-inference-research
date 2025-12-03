# Create Network Policy via SQL

Since the "Bypass requirement for network policy" option isn't available in your UI, create a network policy via SQL instead.

## Option 1: Allow All IPs (Easier, Less Secure)

Run this SQL in Snowflake:

```sql
-- Create network policy that allows all IPs
CREATE NETWORK POLICY IF NOT EXISTS ALLOW_ALL_IPS
  ALLOWED_IP_LIST = ('0.0.0.0/0')
  COMMENT = 'Allow all IPs for PAT authentication';

-- Assign it to your user
ALTER USER 10NETZERO SET NETWORK_POLICY = 'ALLOW_ALL_IPS';
```

## Option 2: Allow Specific IP Range (More Secure)

If you know your IP address or IP range:

```sql
-- Replace with your actual IP or IP range
CREATE NETWORK POLICY IF NOT EXISTS ALLOW_HOMELAB_IPS
  ALLOWED_IP_LIST = ('<your-ip>/32', '<another-ip>/32')
  COMMENT = 'Allow specific IPs for PAT authentication';

-- Assign it to your user
ALTER USER 10NETZERO SET NETWORK_POLICY = 'ALLOW_HOMELAB_IPS';
```

## How to Run

1. **Log into Snowflake**: https://ZWZLXDA-MEB82135.snowflakecomputing.com
2. **Open a Worksheet**
3. **Make sure you're using ACCOUNTADMIN role**
4. **Paste and run** the SQL commands above
5. **Then use your PAT** - it should work now!

## After Creating the Policy

Once the network policy is created and assigned, your PAT will work:

```bash
cd /srv/projects/og-ai-inference-research/tools
python3 add_public_key_with_pat.py "<your-pat-token>"
```

## Note

The "Bypass requirement for network policy" option may only be available:
- For certain account types
- When creating tokens via SQL (not UI)
- For service accounts vs. human users

Creating a network policy is the standard approach and will work for all cases.

