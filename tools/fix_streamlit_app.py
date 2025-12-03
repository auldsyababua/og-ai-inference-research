#!/usr/bin/env python3
"""
Fix Streamlit app by recreating with correct syntax
"""
import snowflake.connector
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import os

SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT", "ZWZLXDA-MEB82135")
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER", "10NETZERO")
SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE", "CALCULATOR_WH")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE", "CALCULATOR_DB")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA", "PUBLIC")
APP_NAME = "off_grid_calculator"
STAGE_NAME = "streamlit_apps"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PRIVATE_KEY_FILE = os.path.join(SCRIPT_DIR, "rsa_key.pem")

def load_private_key():
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
    print("FIXING STREAMLIT APP")
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
    
    # Check stage exists
    print(f"\n1. Checking stage '{STAGE_NAME}'...")
    cursor.execute(f"LIST @{STAGE_NAME}")
    files = cursor.fetchall()
    print(f"   ✓ Stage exists with {len(files)} file(s)")
    if files:
        print("   Sample files:")
        for f in files[:5]:
            print(f"     {f[0]}")
    
    # Drop existing app
    print(f"\n2. Dropping existing app '{APP_NAME}'...")
    try:
        cursor.execute(f"DROP STREAMLIT IF EXISTS {APP_NAME}")
        print("   ✓ App dropped")
    except Exception as e:
        print(f"   ⚠ Error dropping app: {e}")
    
    # Recreate with FROM syntax (newer, recommended)
    print(f"\n3. Creating app with FROM syntax...")
    create_sql = f"""
    CREATE STREAMLIT {APP_NAME}
    FROM @{STAGE_NAME}
    MAIN_FILE = 'unified-calculator-app.py'
    QUERY_WAREHOUSE = {SNOWFLAKE_WAREHOUSE}
    COMMENT = 'Off-Grid Inference Infra Calculator'
    TITLE = 'Off-Grid Inference Infra Calculator'
    """
    
    try:
        cursor.execute(create_sql)
        print("   ✓ App created with FROM syntax!")
    except Exception as e:
        print(f"   ✗ Error creating app: {e}")
        print(f"\n   Trying with ROOT_LOCATION syntax...")
        create_sql_legacy = f"""
        CREATE STREAMLIT {APP_NAME}
        ROOT_LOCATION = '@{STAGE_NAME}'
        MAIN_FILE = '/unified-calculator-app.py'
        QUERY_WAREHOUSE = {SNOWFLAKE_WAREHOUSE}
        COMMENT = 'Off-Grid Inference Infra Calculator'
        """
        try:
            cursor.execute(create_sql_legacy)
            print("   ✓ App created with ROOT_LOCATION syntax!")
        except Exception as e2:
            print(f"   ✗ Error: {e2}")
            return
    
    # Try to initialize
    print(f"\n4. Initializing app...")
    try:
        cursor.execute(f"ALTER STREAMLIT {APP_NAME} ADD LIVE VERSION FROM LAST")
        print("   ✓ App initialized!")
    except Exception as e:
        error_msg = str(e)
        if "already has a live version" in error_msg.lower():
            print("   ✓ App already has a live version")
        else:
            print(f"   ⚠ Initialization note: {e}")
            print("   You may need to access the app via Snowsight first")
    
    # Verify
    print(f"\n5. Verifying app...")
    cursor.execute(f"SHOW STREAMLITS LIKE '{APP_NAME}'")
    result = cursor.fetchone()
    if result:
        print(f"   ✓ App verified!")
        print(f"   URL ID: {result[8] if len(result) > 8 else 'N/A'}")
    
    print(f"\n" + "=" * 60)
    print("APP FIXED!")
    print("=" * 60)
    print(f"Access via Snowsight: Streamlit → {APP_NAME}")
    print(f"Or URL: https://{SNOWFLAKE_ACCOUNT}.snowflakecomputing.com/streamlit/{APP_NAME}")
    print("\nNote: If still 404, access via Snowsight first to fully initialize the app")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()

