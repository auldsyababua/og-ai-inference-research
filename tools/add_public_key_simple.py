#!/usr/bin/env python3
"""
Simplified script to add public key - uses password auth
If MFA is enabled, you'll need to temporarily disable it or use the web UI
"""
import snowflake.connector
import os
import sys

# Configuration
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT", "ZWZLXDA-MEB82135")
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER", "10NETZERO")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD", "eNCt-L.WDm4ZKVADTbw8")
SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN")

PUBLIC_KEY = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvMG95iR8+lUCpuxmwoox4yHMHCWpXJePI5m9RhN8mzCDnWtPymmzSA0lVTgUauC6nkh1lRNgVL8Cv7QMeZjjntz1DTImlUcTcyWF2xhskPwDQpvm+wdpO7wM2lD5F3RaRih1miyzpliPSSv5/uspmyyNI0VYTqs/0b74rAvec3HVZ733XFXxleb7+aIQvlsCIq/mdy87HHN9EG2jN4Nac0f32CVXxZoEF30y4OxDzmuQuZXCK8n2j/Q8rM9Jkp2s9tvsXIluFEt9WEpNgTQhHS9oggpGzpvoYNFJ6t8zMtxqFnKse4HgiYr0n5yaUvPxErJxt6Lw6Kb1d429+EC0qwIDAQAB"

def main():
    print("=" * 60)
    print("ADDING PUBLIC KEY TO SNOWFLAKE")
    print("=" * 60)
    
    try:
        print(f"Connecting to {SNOWFLAKE_ACCOUNT} as {SNOWFLAKE_USER}...")
        conn = snowflake.connector.connect(
            user=SNOWFLAKE_USER,
            password=SNOWFLAKE_PASSWORD,
            account=SNOWFLAKE_ACCOUNT,
            role=SNOWFLAKE_ROLE
        )
        
        cursor = conn.cursor()
        print(f"✓ Connected! Adding public key...")
        
        sql = f"ALTER USER {SNOWFLAKE_USER} SET RSA_PUBLIC_KEY='{PUBLIC_KEY}'"
        cursor.execute(sql)
        print("✓ Public key added successfully!")
        
        # Verify
        cursor.execute(f"DESC USER {SNOWFLAKE_USER}")
        print("\n✓ Verification: User description retrieved")
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("SUCCESS!")
        print("=" * 60)
        print("Public key has been added.")
        print("\nTest connection:")
        print("  python3 test_snowflake_connection.py")
        
    except snowflake.connector.errors.ProgrammingError as e:
        if "Multi-factor authentication" in str(e):
            print("\n" + "=" * 60)
            print("⚠️  MFA IS REQUIRED")
            print("=" * 60)
            print("\nSince MFA is enabled, you have two options:")
            print("\nOption 1: Temporarily disable MFA (quickest)")
            print("  1. Log into Snowflake web UI")
            print("  2. Go to User Profile → Security")
            print("  3. Temporarily disable MFA")
            print("  4. Run this script again")
            print("  5. Re-enable MFA after adding the key")
            print("\nOption 2: Use Web UI (no MFA change needed)")
            print("  1. Log into Snowflake web UI")
            print("  2. Open a Worksheet")
            print("  3. Run this SQL command:")
            print(f"\n     ALTER USER {SNOWFLAKE_USER} SET RSA_PUBLIC_KEY='{PUBLIC_KEY}';")
            print("\nThe SQL command is also saved in: add_public_key.sql")
        else:
            print(f"\n✗ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

