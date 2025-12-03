# Solution: Network Policy for PAT Authentication

## Problem
PAT authentication fails with error: "Network policy is required"

## Root Cause
Snowflake requires a network policy for users using PATs by default. The "Bypass requirement for network policy" option is not available in the UI for your account/user type.

## Solution: Create Network Policy via SQL

### Step 1: Run SQL in Snowflake Web UI

1. **Log into Snowflake**: https://ZWZLXDA-MEB82135.snowflakecomputing.com
2. **Open a Worksheet** (left sidebar)
3. **Ensure you're using ACCOUNTADMIN role** (check top right)
4. **Copy and paste this SQL**:

```sql
-- Create network policy that allows all IPs
CREATE NETWORK POLICY IF NOT EXISTS ALLOW_ALL_IPS
  ALLOWED_IP_LIST = ('0.0.0.0/0')
  COMMENT = 'Allow all IPs for PAT authentication';

-- Assign it to your user
ALTER USER 10NETZERO SET NETWORK_POLICY = 'ALLOW_ALL_IPS';

-- Verify (optional)
SHOW NETWORK POLICIES LIKE 'ALLOW_ALL_IPS';
DESC USER 10NETZERO;
```

5. **Click "Run"** (or press Ctrl+Enter)
6. **Verify success**: You should see "Statement executed successfully"

### Step 2: Test PAT Authentication

After running the SQL, test your PAT:

```bash
cd /srv/projects/og-ai-inference-research/tools
python3 add_public_key_with_pat.py "<your-pat-token>"
```

Or use the automated script:

```bash
./create_network_policy_and_test.sh
```

## Alternative: Generate PAT with Bypass (If Needed)

If you prefer to generate a new PAT with bypass instead:

```sql
ALTER USER 10NETZERO ADD PROGRAMMATIC ACCESS TOKEN homelab_pat_bypass
  ROLE_RESTRICTION = 'ACCOUNTADMIN'
  MINS_TO_BYPASS_NETWORK_POLICY_REQUIREMENT = 1440
  COMMENT = 'PAT with 24-hour network policy bypass';
```

**Note**: This will output a new token_secret - copy it immediately!

## Security Note

Allowing all IPs (`0.0.0.0/0`) is less secure. For production, restrict to specific IPs:

```sql
CREATE NETWORK POLICY ALLOW_HOMELAB_IPS
  ALLOWED_IP_LIST = ('<your-ip>/32', '<another-ip>/32')
  COMMENT = 'Allow specific IPs for PAT authentication';
```

## Expected Result

After creating the network policy, your existing PAT token should work:

```
✓ Connected successfully!
✓ Public key added successfully!
```

