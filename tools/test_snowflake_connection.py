#!/usr/bin/env python3
"""
Test Snowflake connection using key-pair authentication
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
PRIVATE_KEY_FILE = os.path.join(os.path.dirname(__file__), "rsa_key.pem")

def load_private_key():
    """Load private key from PEM file and convert to format Snowflake expects"""
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

def test_connection():
    """Test Snowflake connection"""
    print("=" * 60)
    print("TESTING SNOWFLAKE CONNECTION")
    print("=" * 60)
    print(f"Account: {SNOWFLAKE_ACCOUNT}")
    print(f"User: {SNOWFLAKE_USER}")
    print(f"Private Key: {PRIVATE_KEY_FILE}")
    print()
    
    if not os.path.exists(PRIVATE_KEY_FILE):
        print(f"Error: Private key file not found: {PRIVATE_KEY_FILE}")
        print("\nMake sure rsa_key.pem exists in the tools/ directory")
        sys.exit(1)
    
    try:
        # Load private key
        private_key = load_private_key()
        
        # Connect using key-pair authentication
        print("Connecting to Snowflake...")
        conn = snowflake.connector.connect(
            user=SNOWFLAKE_USER,
            private_key=private_key,
            account=SNOWFLAKE_ACCOUNT,
            role=SNOWFLAKE_ROLE
        )
        
        cursor = conn.cursor()
        
        # Test query
        print("Running test query...")
        cursor.execute("SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_ACCOUNT()")
        result = cursor.fetchone()
        
        print("\n" + "=" * 60)
        print("✓ CONNECTION SUCCESSFUL!")
        print("=" * 60)
        print(f"User: {result[0]}")
        print(f"Role: {result[1]}")
        print(f"Account: {result[2]}")
        
        # Check for warehouse
        cursor.execute("SHOW WAREHOUSES")
        warehouses = cursor.fetchall()
        if warehouses:
            print(f"\nAvailable warehouses: {len(warehouses)}")
            for wh in warehouses[:5]:  # Show first 5
                print(f"  - {wh[0]}")
        else:
            print("\nNo warehouses found (will be created by setup script)")
        
        cursor.close()
        conn.close()
        
        print("\n✓ Key-pair authentication is working!")
        print("\nNext step: Run setup_snowflake_resources.py to create resources")
        
    except snowflake.connector.errors.DatabaseError as e:
        if "Invalid key pair" in str(e) or "RSA_PUBLIC_KEY" in str(e):
            print("\n" + "=" * 60)
            print("✗ AUTHENTICATION FAILED")
            print("=" * 60)
            print("The public key has not been added to Snowflake yet.")
            print("\nTo fix this:")
            print("1. Get your public key:")
            print(f"   cat {PRIVATE_KEY_FILE.replace('.pem', '.pub')}")
            print("\n2. Add it to Snowflake:")
            print("   - Via UI: User settings → Security → Public Keys → Add")
            print("   - Via SQL: ALTER USER 10NETZERO SET RSA_PUBLIC_KEY='<key>';")
            print("\nSee ADD_PUBLIC_KEY_TO_SNOWFLAKE.md for details")
        else:
            print(f"\n✗ Connection error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_connection()

