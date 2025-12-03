#!/usr/bin/env python3
"""
Set up Snowflake resources (warehouse, database, schema) for the calculator app
This needs to be run once to create the necessary resources
"""
import snowflake.connector
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import os
import sys

# Configuration
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT", "ZWZLXDA-MEB82135")
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER", "10NETZERO")
SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN")

# Key-pair authentication
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PRIVATE_KEY_FILE = os.path.join(SCRIPT_DIR, "rsa_key.pem")

WAREHOUSE_NAME = "CALCULATOR_WH"
DATABASE_NAME = "CALCULATOR_DB"
SCHEMA_NAME = "PUBLIC"

def load_private_key():
    """Load private key from PEM file and convert to format Snowflake expects"""
    if not os.path.exists(PRIVATE_KEY_FILE):
        raise FileNotFoundError(f"Private key file not found: {PRIVATE_KEY_FILE}")
    
    with open(PRIVATE_KEY_FILE, 'rb') as f:
        private_key_pem = f.read()
    
    # Parse the PEM key
    private_key = serialization.load_pem_private_key(
        private_key_pem,
        password=None,  # No password for unencrypted key
        backend=default_backend()
    )
    
    # Convert to DER format (what Snowflake expects)
    private_key_der = private_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    return private_key_der

def main():
    print("=" * 60)
    print("SNOWFLAKE RESOURCE SETUP")
    print("=" * 60)
    
    try:
        # Load private key
        print(f"Loading private key from: {PRIVATE_KEY_FILE}")
        private_key = load_private_key()
        
        # Connect to Snowflake using key-pair authentication
        print(f"Connecting to Snowflake account: {SNOWFLAKE_ACCOUNT}")
        conn = snowflake.connector.connect(
            user=SNOWFLAKE_USER,
            private_key=private_key,
            account=SNOWFLAKE_ACCOUNT,
            role=SNOWFLAKE_ROLE
        )
        cursor = conn.cursor()
        
        # Create warehouse
        print(f"\n1. Creating warehouse: {WAREHOUSE_NAME}")
        cursor.execute(f"""
            CREATE WAREHOUSE IF NOT EXISTS {WAREHOUSE_NAME}
            WITH WAREHOUSE_SIZE = 'X-SMALL'
            AUTO_SUSPEND = 60
            AUTO_RESUME = TRUE
            INITIALLY_SUSPENDED = FALSE
        """)
        print(f"   ✓ Warehouse '{WAREHOUSE_NAME}' created/verified")
        
        # Resume warehouse (only if suspended)
        print(f"\n2. Checking warehouse status...")
        cursor.execute(f"SHOW WAREHOUSES LIKE '{WAREHOUSE_NAME}'")
        wh_info = cursor.fetchone()
        if wh_info and len(wh_info) > 6:
            state = wh_info[6] if len(wh_info) > 6 else 'UNKNOWN'
            if state == 'SUSPENDED':
                cursor.execute(f"ALTER WAREHOUSE {WAREHOUSE_NAME} RESUME")
                print(f"   ✓ Warehouse resumed")
            else:
                print(f"   ✓ Warehouse is already {state}")
        else:
            # Try to resume anyway (will fail gracefully if not suspended)
            try:
                cursor.execute(f"ALTER WAREHOUSE {WAREHOUSE_NAME} RESUME")
                print(f"   ✓ Warehouse resumed")
            except:
                print(f"   ✓ Warehouse is already running")
        
        # Create database
        print(f"\n3. Creating database: {DATABASE_NAME}")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")
        print(f"   ✓ Database '{DATABASE_NAME}' created/verified")
        
        # Use database
        cursor.execute(f"USE DATABASE {DATABASE_NAME}")
        
        # Create schema
        print(f"\n4. Creating schema: {SCHEMA_NAME}")
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA_NAME}")
        print(f"   ✓ Schema '{SCHEMA_NAME}' created/verified")
        
        # Verify setup
        print(f"\n5. Verifying setup...")
        cursor.execute(f"USE WAREHOUSE {WAREHOUSE_NAME}")
        cursor.execute(f"USE DATABASE {DATABASE_NAME}")
        cursor.execute(f"USE SCHEMA {SCHEMA_NAME}")
        
        cursor.execute("SELECT CURRENT_WAREHOUSE(), CURRENT_DATABASE(), CURRENT_SCHEMA()")
        result = cursor.fetchone()
        
        print("\n" + "=" * 60)
        print("SETUP COMPLETE")
        print("=" * 60)
        print(f"Warehouse: {result[0]}")
        print(f"Database: {result[1]}")
        print(f"Schema: {result[2]}")
        print("\nNext steps:")
        print("1. Update .streamlit/secrets.toml with:")
        print(f"   warehouse = \"{WAREHOUSE_NAME}\"")
        print(f"   database = \"{DATABASE_NAME}\"")
        print(f"   schema = \"{SCHEMA_NAME}\"")
        print("\n2. Deploy Streamlit app to Streamlit Community Cloud")
        print("3. Add secrets to Streamlit Cloud app settings")
        
        cursor.close()
        conn.close()
        
    except FileNotFoundError as e:
        print(f"\n✗ Error: {e}")
        print("\nMake sure rsa_key.pem exists in the tools/ directory")
        sys.exit(1)
    except snowflake.connector.errors.DatabaseError as e:
        if "Invalid key pair" in str(e) or "RSA_PUBLIC_KEY" in str(e):
            print("\n" + "=" * 60)
            print("✗ PUBLIC KEY NOT ADDED TO SNOWFLAKE")
            print("=" * 60)
            print("The public key has not been added to your Snowflake user yet.")
            print("\nTo fix this:")
            print("1. Get your public key:")
            print(f"   cat {PRIVATE_KEY_FILE.replace('.pem', '.pub')}")
            print("\n2. Add it to Snowflake:")
            print("   - Via UI: Log into Snowflake → User settings → Security → Public Keys → Add")
            print("   - Via SQL: ALTER USER 10NETZERO SET RSA_PUBLIC_KEY='<key-content>';")
            print("\nSee ADD_PUBLIC_KEY_TO_SNOWFLAKE.md for detailed instructions")
        else:
            print(f"\n✗ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

