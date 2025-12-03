#!/usr/bin/env python3
"""
Add public key to Snowflake user via Programmatic Access Token (PAT)
Uses the PAT token for authentication (bypasses MFA)
"""
import snowflake.connector
import os
import sys

# Configuration
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT", "ZWZLXDA-MEB82135")
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER", "10NETZERO")
SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN")

# Read PAT from command line argument, environment variable, or file
PAT_TOKEN = None

# Check command line argument
if len(sys.argv) > 1:
    PAT_TOKEN = sys.argv[1].strip()
# Check environment variable
elif os.getenv("SNOWFLAKE_PAT_TOKEN"):
    PAT_TOKEN = os.getenv("SNOWFLAKE_PAT_TOKEN").strip()
# Check file (if on Mac)
elif os.path.exists("/Users/colinaulds/Downloads/homelab-token-secret.txt"):
    with open("/Users/colinaulds/Downloads/homelab-token-secret.txt", 'r') as f:
        PAT_TOKEN = f.read().strip()
# Check file in current directory
elif os.path.exists("homelab-token-secret.txt"):
    with open("homelab-token-secret.txt", 'r') as f:
        PAT_TOKEN = f.read().strip()

if not PAT_TOKEN:
    print("Error: PAT token not found")
    print("\nUsage:")
    print("  python3 add_public_key_with_pat.py <token>")
    print("  OR")
    print("  export SNOWFLAKE_PAT_TOKEN='<token>'")
    print("  python3 add_public_key_with_pat.py")
    print("\nOr copy the token file to the current directory as 'homelab-token-secret.txt'")
    sys.exit(1)

# Public key (base64)
PUBLIC_KEY = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvMG95iR8+lUCpuxmwoox4yHMHCWpXJePI5m9RhN8mzCDnWtPymmzSA0lVTgUauC6nkh1lRNgVL8Cv7QMeZjjntz1DTImlUcTcyWF2xhskPwDQpvm+wdpO7wM2lD5F3RaRih1miyzpliPSSv5/uspmyyNI0VYTqs/0b74rAvec3HVZ733XFXxleb7+aIQvlsCIq/mdy87HHN9EG2jN4Nac0f32CVXxZoEF30y4OxDzmuQuZXCK8n2j/Q8rM9Jkp2s9tvsXIluFEt9WEpNgTQhHS9oggpGzpvoYNFJ6t8zMtxqFnKse4HgiYr0n5yaUvPxErJxt6Lw6Kb1d429+EC0qwIDAQAB"

def main():
    print("=" * 60)
    print("ADDING PUBLIC KEY TO SNOWFLAKE VIA PAT")
    print("=" * 60)
    print(f"Account: {SNOWFLAKE_ACCOUNT}")
    print(f"User: {SNOWFLAKE_USER}")
    print(f"Role: {SNOWFLAKE_ROLE}")
    print(f"Using PAT token: {PAT_TOKEN[:20]}...")
    print()
    
    try:
        # Connect using PAT
        # According to Snowflake docs, PATs can be used as the password parameter
        # https://docs.snowflake.com/en/user-guide/programmatic-access-tokens
        print("Connecting to Snowflake using PAT as password...")
        print(f"Connector version: {snowflake.connector.__version__}")
        
        # PAT authentication: use PAT as password (per Snowflake documentation)
        conn = snowflake.connector.connect(
            user=SNOWFLAKE_USER,
            password=PAT_TOKEN,  # PAT is used as password
            account=SNOWFLAKE_ACCOUNT,
            role=SNOWFLAKE_ROLE
        )
        
        cursor = conn.cursor()
        print("✓ Connected successfully!")
        
        # Execute the ALTER USER command
        # Username needs to be quoted if it starts with a number or contains special chars
        print(f"\nAdding public key to user {SNOWFLAKE_USER}...")
        sql = f'ALTER USER "{SNOWFLAKE_USER}" SET RSA_PUBLIC_KEY=\'{PUBLIC_KEY}\''
        cursor.execute(sql)
        print("✓ Public key added successfully!")
        
        # Verify the key was added
        print("\nVerifying key was added...")
        cursor.execute(f'DESC USER "{SNOWFLAKE_USER}"')
        result = cursor.fetchall()
        
        # Look for RSA_PUBLIC_KEY in the result
        key_found = False
        for row in result:
            if len(row) >= 2:
                field_name = str(row[0]).upper()
                if 'RSA_PUBLIC_KEY' in field_name:
                    key_found = True
                    print(f"✓ Found RSA_PUBLIC_KEY in user description")
                    # Show a masked version if available
                    if len(row) > 1:
                        value = str(row[1])
                        if value and value != 'None':
                            print(f"  Value: {value[:20]}... (masked)")
                    break
        
        if not key_found:
            print("✓ Key added (may not be visible in DESC output for security)")
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("SUCCESS!")
        print("=" * 60)
        print("Public key has been added to Snowflake user.")
        print("\nNext step: Test the connection with key-pair authentication:")
        print("  python3 test_snowflake_connection.py")
        
    except snowflake.connector.errors.ProgrammingError as e:
        error_msg = str(e)
        if "Network policy is required" in error_msg:
            print("\n" + "=" * 60)
            print("⚠️  NETWORK POLICY REQUIRED")
            print("=" * 60)
            print("PAT authentication requires a network policy for the user.")
            print("\nTo fix this, you have two options:")
            print("\nOption 1: Bypass network policy requirement (when generating PAT)")
            print("  1. Go to Snowflake web UI")
            print("  2. User Profile → Security → Programmatic Access Tokens")
            print("  3. When generating the token, check 'Bypass requirement for network policy'")
            print("  4. Generate a new token and use that")
            print("\nOption 2: Create a network policy")
            print("  1. Create a network policy that allows your IP address")
            print("  2. Assign it to the user: ALTER USER 10NETZERO SET NETWORK_POLICY='policy_name'")
        elif "Insufficient privileges" in error_msg:
            print("\n" + "=" * 60)
            print("✗ INSUFFICIENT PRIVILEGES")
            print("=" * 60)
            print("The PAT token doesn't have ACCOUNTADMIN privileges.")
            print("\nOptions:")
            print("1. Use a PAT token with ACCOUNTADMIN role")
            print("2. Grant USERADMIN role to the PAT token")
            print("3. Use the web UI to run the SQL command manually")
        elif "Invalid token" in error_msg or "authentication" in error_msg.lower():
            print("\n" + "=" * 60)
            print("✗ AUTHENTICATION FAILED")
            print("=" * 60)
            print("The PAT token may be invalid or expired.")
            print("\nCheck:")
            print("1. Token file exists and is readable")
            print("2. Token hasn't expired")
            print("3. Token has correct permissions")
        else:
            print(f"\n✗ SQL Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Verify PAT token is valid and not expired")
        print("2. Check account identifier is correct")
        print("3. Ensure PAT has necessary privileges")
        sys.exit(1)

if __name__ == "__main__":
    main()

