# Fix: Network Policy Required for PAT

## Issue

When using a PAT (Programmatic Access Token), you're getting:
```
Network policy is required.
```

## Solution

PATs require a network policy by default. You have two options:

### Option 1: Bypass Network Policy (Easiest - Recommended)

When generating the PAT in Snowflake:

1. **Go to**: Snowflake Web UI → User Profile → Security → Programmatic Access Tokens
2. **Click**: "Generate new token"
3. **In the dialog**, check the box: **"Bypass requirement for network policy"**
4. **Generate** the token
5. **Copy** the new token
6. **Use the new token** with the script

This bypasses the network policy requirement for this specific token.

### Option 2: Create a Network Policy

If you want to use network policies (more secure):

1. **Create a network policy** that allows your IP address:
```sql
CREATE NETWORK POLICY allow_homelab
  ALLOWED_IP_LIST = ('<your-ip-address>/32')
  COMMENT = 'Allow homelab access';
```

2. **Assign it to the user**:
```sql
ALTER USER 10NETZERO SET NETWORK_POLICY = 'allow_homelab';
```

3. **Then use the PAT** - it should work now

## Quick Fix

The fastest solution is to regenerate the PAT with "Bypass requirement for network policy" checked, then run:

```bash
python3 add_public_key_with_pat.py "<new-pat-token>"
```

## Note

The PAT you have is valid and working - it's just hitting the network policy requirement. Once you bypass it or set up a policy, it will work perfectly!

