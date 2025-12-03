#!/usr/bin/env python3
"""
Check Streamlit app status and initialize if needed
"""
import snowflake.connector
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import os

# Configuration
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT", "ZWZLXDA-MEB82135")
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER", "10NETZERO")
SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE", "CALCULATOR_WH")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE", "CALCULATOR_DB")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA", "PUBLIC")
APP_NAME = "off_grid_calculator"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PRIVATE_KEY_FILE = os.path.join(SCRIPT_DIR, "rsa_key.pem")

def load_private_key():
    """Load private key from PEM file"""
    with open(PRIVATE_KEY_FILE, 'rb') as f:
        private_key_pem = f.read()
    private_key = serialization.load_pem_private_key(
        private_key_pem, password=None, backend=default_backend()
    )
    return private_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

def main():
    print("=" * 60)
    print("CHECKING STREAMLIT APP STATUS")
    print("=" * 60)
    
    private_key = load_private_key()
    
    conn = snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        private_key=private_key,
        account=SNOWFLAKE_ACCOUNT,
        role=SNOWFLAKE_ROLE,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA
    )
    
    cursor = conn.cursor()
    print("✓ Connected!")
    
    # Check if app exists
    print(f"\n1. Checking if app '{APP_NAME}' exists...")
    cursor.execute(f"SHOW STREAMLITS LIKE '{APP_NAME}'")
    result = cursor.fetchall()
    
    if not result:
        print(f"   ✗ App '{APP_NAME}' not found!")
        print("   Run deploy_to_snowflake_streamlit.py first")
        return
    
    print(f"   ✓ App found!")
    print(f"   Columns: {[desc[0] for desc in cursor.description]}")
    
    # Show app details
    for row in result:
        print(f"\n   App Details:")
        for i, col in enumerate(cursor.description):
            print(f"     {col[0]}: {row[i]}")
    
    # Try to initialize the app
    print(f"\n2. Initializing app (making it live)...")
    try:
        # ALTER STREAMLIT ... ADD LIVE VERSION FROM LAST
        cursor.execute(f"ALTER STREAMLIT {APP_NAME} ADD LIVE VERSION FROM LAST")
        print("   ✓ App initialized successfully!")
    except Exception as e:
        error_msg = str(e)
        if "already has a live version" in error_msg.lower():
            print("   ✓ App already has a live version")
        elif "no versions" in error_msg.lower():
            print("   ⚠ No versions found - app may need to be created first")
        else:
            print(f"   ⚠ Error: {e}")
    
    # Describe the app
    print(f"\n3. Describing app...")
    try:
        cursor.execute(f"DESC STREAMLIT {APP_NAME}")
        desc_result = cursor.fetchall()
        print("   App description:")
        for row in desc_result:
            print(f"     {row[0]}: {row[1]}")
    except Exception as e:
        print(f"   ⚠ Error describing app: {e}")
    
    # Get app URL
    print(f"\n4. App Access:")
    print(f"   URL: https://{SNOWFLAKE_ACCOUNT}.snowflakecomputing.com/streamlit/{APP_NAME}")
    print(f"   Or access via Snowsight: Streamlit → {APP_NAME}")
    print(f"\n   Note: If 404, try accessing via Snowsight first to initialize the app")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()

