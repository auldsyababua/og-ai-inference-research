#!/usr/bin/env python3
"""
Deploy Streamlit app to Snowflake Streamlit Apps

This script:
1. Connects to Snowflake
2. Creates/updates database, schema, and warehouse if needed
3. Uploads CSV data files to Snowflake stage
4. Creates the Streamlit app
5. Gets the app URL
"""
import snowflake.connector
import os
import sys
from pathlib import Path

# Configuration - load from environment or use defaults
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT", "ZWZLXDA-MEB82135")
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER", "10NETZERO")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD", "eNCt-L.WDm4ZKVADTbw8")
SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE", "")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE", "CALCULATOR_DB")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA", "PUBLIC")

# App configuration
APP_NAME = "off_grid_calculator"
STREAMLIT_FILE = "unified-calculator-app.py"

def connect_to_snowflake():
    """Connect to Snowflake"""
    print(f"Connecting to Snowflake account: {SNOWFLAKE_ACCOUNT}")
    conn = snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        role=SNOWFLAKE_ROLE
    )
    return conn

def setup_warehouse(cursor, warehouse_name):
    """Create warehouse if it doesn't exist"""
    if not warehouse_name:
        warehouse_name = "CALCULATOR_WH"
    
    print(f"Setting up warehouse: {warehouse_name}")
    cursor.execute(f"""
        CREATE WAREHOUSE IF NOT EXISTS {warehouse_name}
        WITH WAREHOUSE_SIZE = 'X-SMALL'
        AUTO_SUSPEND = 60
        AUTO_RESUME = TRUE
        INITIALLY_SUSPENDED = FALSE
    """)
    cursor.execute(f"USE WAREHOUSE {warehouse_name}")
    return warehouse_name

def setup_database_schema(cursor, database_name, schema_name):
    """Create database and schema if they don't exist"""
    print(f"Setting up database: {database_name}, schema: {schema_name}")
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
    cursor.execute(f"USE DATABASE {database_name}")
    cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")
    cursor.execute(f"USE SCHEMA {schema_name}")

def upload_csv_files(cursor, base_path):
    """Upload CSV files to Snowflake stage"""
    print("Uploading CSV files to Snowflake stage...")
    
    # Create stage for CSV files
    cursor.execute("CREATE STAGE IF NOT EXISTS calculator_data")
    
    csv_files = {
        'compat_matrix': 'models/gpu-generator-compatibility/GPU-Generator-Compatibility-Matrix-v1.csv',
        'bess_sizing': 'models/bess-sizing/BESS-Sizing-v1.csv',
        'data_logistics': 'models/data-logistics/DataLogistics-v1.csv'
    }
    
    for name, rel_path in csv_files.items():
        file_path = os.path.join(base_path, rel_path)
        if os.path.exists(file_path):
            print(f"  Uploading {name}...")
            cursor.execute(f"""
                PUT file://{file_path} @calculator_data/{name}/
                AUTO_COMPRESS=FALSE
            """)
        else:
            print(f"  Warning: {file_path} not found, skipping {name}")

def create_streamlit_app(cursor, app_name, streamlit_file_path):
    """Create Streamlit app in Snowflake"""
    print(f"Creating Streamlit app: {app_name}")
    
    # Read the Streamlit app file
    with open(streamlit_file_path, 'r') as f:
        app_code = f.read()
    
    # Create stage for the app code
    cursor.execute("CREATE STAGE IF NOT EXISTS streamlit_apps")
    
    # Upload the app file
    cursor.execute(f"""
        PUT file://{streamlit_file_path} @streamlit_apps/
        AUTO_COMPRESS=FALSE
    """)
    
    # Create the Streamlit app
    # Note: Snowflake Streamlit Apps use CREATE STREAMLIT command
    # The file needs to be referenced from the stage
    cursor.execute(f"""
        CREATE OR REPLACE STREAMLIT {app_name}
        ROOT_LOCATION = '@streamlit_apps'
        MAIN_FILE = '/{streamlit_file_path}'
        QUERY_WAREHOUSE = {SNOWFLAKE_WAREHOUSE or 'CALCULATOR_WH'}
    """)
    
    print(f"✓ Streamlit app '{app_name}' created successfully")

def get_app_url(cursor, app_name, account):
    """Get the Streamlit app URL"""
    # Snowflake Streamlit Apps URL format:
    # https://<account>.snowflakecomputing.com/<path-to-app>
    # The exact path depends on Snowflake's internal routing
    
    cursor.execute(f"SHOW STREAMLITS LIKE '{app_name}'")
    result = cursor.fetchone()
    
    if result:
        # The URL structure varies, but typically:
        account_locator = account.split('-')[0] if '-' in account else account
        app_url = f"https://{account}.snowflakecomputing.com/streamlit/{app_name}"
        return app_url
    else:
        return None

def main():
    """Main deployment function"""
    print("=" * 60)
    print("SNOWFLAKE STREAMLIT APP DEPLOYMENT")
    print("=" * 60)
    
    # Get base path (project root)
    script_dir = Path(__file__).parent
    base_path = script_dir.parent
    
    streamlit_file_path = script_dir / STREAMLIT_FILE
    
    if not streamlit_file_path.exists():
        print(f"Error: Streamlit file not found: {streamlit_file_path}")
        sys.exit(1)
    
    try:
        # Connect to Snowflake
        conn = connect_to_snowflake()
        cursor = conn.cursor()
        
        # Setup warehouse
        warehouse = setup_warehouse(cursor, SNOWFLAKE_WAREHOUSE)
        
        # Setup database and schema
        setup_database_schema(cursor, SNOWFLAKE_DATABASE, SNOWFLAKE_SCHEMA)
        
        # Upload CSV files
        upload_csv_files(cursor, base_path)
        
        # Create Streamlit app
        create_streamlit_app(cursor, APP_NAME, str(streamlit_file_path))
        
        # Get app URL
        app_url = get_app_url(cursor, APP_NAME, SNOWFLAKE_ACCOUNT)
        
        print("\n" + "=" * 60)
        print("DEPLOYMENT COMPLETE")
        print("=" * 60)
        print(f"App Name: {APP_NAME}")
        print(f"App URL: {app_url or '(Check Snowflake UI for URL)'}")
        print(f"Database: {SNOWFLAKE_DATABASE}")
        print(f"Schema: {SNOWFLAKE_SCHEMA}")
        print(f"Warehouse: {warehouse}")
        
        cursor.close()
        conn.close()
        
        return app_url
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

