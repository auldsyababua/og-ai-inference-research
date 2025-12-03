#!/usr/bin/env python3
"""
Add public key to Snowflake user via REST API
Alternative approach if Python connector doesn't work
"""
import requests
import json
import os
import sys
import time

# Configuration
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT", "ZWZLXDA-MEB82135")
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER", "10NETZERO")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD", "eNCt-L.WDm4ZKVADTbw8")
SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN")

# Public key (base64)
PUBLIC_KEY = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvMG95iR8+lUCpuxmwoox4yHMHCWpXJePI5m9RhN8mzCDnWtPymmzSA0lVTgUauC6nkh1lRNgVL8Cv7QMeZjjntz1DTImlUcTcyWF2xhskPwDQpvm+wdpO7wM2lD5F3RaRih1miyzpliPSSv5/uspmyyNI0VYTqs/0b74rAvec3HVZ733XFXxleb7+aIQvlsCIq/mdy87HHN9EG2jN4Nac0f32CVXxZoEF30y4OxDzmuQuZXCK8n2j/Q8rM9Jkp2s9tvsXIluFEt9WEpNgTQhHS9oggpGzpvoYNFJ6t8zMtxqFnKse4HgiYr0n5yaUvPxErJxt6Lw6Kb1d429+EC0qwIDAQAB"

def get_oauth_token():
    """
    Get OAuth token from Snowflake
    Note: This is a simplified approach - Snowflake REST API typically requires
    OAuth setup or session tokens from the web UI
    """
    # Snowflake REST API endpoint
    account_locator = SNOWFLAKE_ACCOUNT.split('-')[0] if '-' in SNOWFLAKE_ACCOUNT else SNOWFLAKE_ACCOUNT
    url = f"https://{SNOWFLAKE_ACCOUNT}.snowflakecomputing.com/oauth/token-request"
    
    # This is a placeholder - actual OAuth flow is more complex
    print("Note: Snowflake REST API requires OAuth setup or session tokens")
    print("This approach may not work without proper OAuth configuration")
    return None

def main():
    print("=" * 60)
    print("ADDING PUBLIC KEY VIA REST API")
    print("=" * 60)
    print("\n⚠️  Note: Snowflake REST API requires:")
    print("   1. OAuth token setup, OR")
    print("   2. Session token from web UI, OR")
    print("   3. SQL API with proper authentication")
    print("\nAlternative: Use the Python connector with password auth")
    print("(if MFA can be temporarily disabled or bypassed)")
    print()
    
    # Try password authentication as fallback
    print("Attempting password authentication...")
    try:
        import snowflake.connector
        conn = snowflake.connector.connect(
            user=SNOWFLAKE_USER,
            password=SNOWFLAKE_PASSWORD,
            account=SNOWFLAKE_ACCOUNT,
            role=SNOWFLAKE_ROLE
        )
        
        cursor = conn.cursor()
        print(f"✓ Connected! Adding public key to user {SNOWFLAKE_USER}...")
        
        sql = f"ALTER USER {SNOWFLAKE_USER} SET RSA_PUBLIC_KEY='{PUBLIC_KEY}'"
        cursor.execute(sql)
        print("✓ Public key added successfully!")
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("SUCCESS!")
        print("=" * 60)
        print("Public key has been added to Snowflake.")
        print("\nNext step: Test the connection:")
        print("  python3 test_snowflake_connection.py")
        
    except snowflake.connector.errors.ProgrammingError as e:
        if "Multi-factor authentication" in str(e):
            print("\n✗ MFA is required - password authentication won't work")
            print("\nOptions:")
            print("1. Temporarily disable MFA in Snowflake user settings")
            print("2. Use the web UI to run the SQL command manually")
            print("3. Use Snowflake's SQL API with OAuth (requires setup)")
        else:
            print(f"\n✗ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

