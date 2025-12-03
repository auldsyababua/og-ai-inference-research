#!/usr/bin/env python3
"""
Add public key to Snowflake user via Python API
Uses external browser authentication (opens browser window)
"""
import snowflake.connector
import os
import sys

# Configuration
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT", "ZWZLXDA-MEB82135")
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER", "10NETZERO")
SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN")

# Public key (base64, no BEGIN/END lines)
PUBLIC_KEY = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvMG95iR8+lUCpuxmwoox4yHMHCWpXJePI5m9RhN8mzCDnWtPymmzSA0lVTgUauC6nkh1lRNgVL8Cv7QMeZjjntz1DTImlUcTcyWF2xhskPwDQpvm+wdpO7wM2lD5F3RaRih1miyzpliPSSv5/uspmyyNI0VYTqs/0b74rAvec3HVZ733XFXxleb7+aIQvlsCIq/mdy87HHN9EG2jN4Nac0f32CVXxZoEF30y4OxDzmuQuZXCK8n2j/Q8rM9Jkp2s9tvsXIluFEt9WEpNgTQhHS9oggpGzpvoYNFJ6t8zMtxqFnKse4HgiYr0n5yaUvPxErJxt6Lw6Kb1d429+EC0qwIDAQAB"

def main():
    print("=" * 60)
    print("ADDING PUBLIC KEY TO SNOWFLAKE VIA API")
    print("=" * 60)
    print(f"Account: {SNOWFLAKE_ACCOUNT}")
    print(f"User: {SNOWFLAKE_USER}")
    print(f"Role: {SNOWFLAKE_ROLE}")
    print()
    print("This will open a browser window for authentication...")
    print()
    
    try:
        # Connect using external browser authentication
        # This will open a browser window for you to log in
        print("Connecting to Snowflake (browser window will open)...")
        conn = snowflake.connector.connect(
            user=SNOWFLAKE_USER,
            account=SNOWFLAKE_ACCOUNT,
            authenticator='externalbrowser',  # Opens browser for SSO/MFA
            role=SNOWFLAKE_ROLE
        )
        
        cursor = conn.cursor()
        
        # Execute the ALTER USER command
        print(f"\nAdding public key to user {SNOWFLAKE_USER}...")
        sql = f"ALTER USER {SNOWFLAKE_USER} SET RSA_PUBLIC_KEY='{PUBLIC_KEY}'"
        cursor.execute(sql)
        
        print("✓ Public key added successfully!")
        
        # Verify the key was added
        print("\nVerifying key was added...")
        cursor.execute(f"DESC USER {SNOWFLAKE_USER}")
        result = cursor.fetchall()
        
        # Look for RSA_PUBLIC_KEY in the result
        key_found = False
        for row in result:
            if len(row) >= 2 and 'RSA_PUBLIC_KEY' in str(row[0]).upper():
                key_found = True
                print(f"✓ Found RSA_PUBLIC_KEY: {row[1] if len(row) > 1 else 'Set'}")
                break
        
        if not key_found:
            print("⚠ Key may have been added but not visible in DESC output")
            print("  (This is normal - the key is stored securely)")
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("SUCCESS!")
        print("=" * 60)
        print("Public key has been added to Snowflake.")
        print("\nNext step: Test the connection with key-pair authentication:")
        print("  python3 test_snowflake_connection.py")
        
    except snowflake.connector.errors.ProgrammingError as e:
        if "Insufficient privileges" in str(e):
            print("\n" + "=" * 60)
            print("✗ INSUFFICIENT PRIVILEGES")
            print("=" * 60)
            print("You need ACCOUNTADMIN role to alter user settings.")
            print("\nMake sure you:")
            print("1. Logged in with ACCOUNTADMIN role in the browser")
            print("2. Or have USERADMIN role with privileges to alter users")
        else:
            print(f"\n✗ SQL Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you complete the browser authentication")
        print("2. Check that you have ACCOUNTADMIN role")
        print("3. Verify the account identifier is correct")
        sys.exit(1)

if __name__ == "__main__":
    main()

