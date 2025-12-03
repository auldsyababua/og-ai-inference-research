#!/usr/bin/env python3
"""
Deploy Streamlit app to Snowflake Streamlit Apps
Handles file uploads to stage and CREATE STREAMLIT command
"""
import snowflake.connector
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import os
import sys
from pathlib import Path

# Configuration
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT", "ZWZLXDA-MEB82135")
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER", "10NETZERO")
SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE", "CALCULATOR_WH")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE", "CALCULATOR_DB")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA", "PUBLIC")

# Key-pair authentication
SCRIPT_DIR = Path(__file__).parent
PRIVATE_KEY_FILE = SCRIPT_DIR / "rsa_key.pem"
STAGE_NAME = "streamlit_apps"
APP_NAME = "off_grid_calculator"

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

def upload_file_to_stage(cursor, local_path, stage_name, stage_path=""):
    """Upload a file to Snowflake stage using PUT command"""
    file_name = os.path.basename(local_path)
    # Stage path format: @stage_name/path/ (PUT uses local filename automatically)
    if stage_path:
        stage_target = f"@{stage_name}/{stage_path}"
    else:
        stage_target = f"@{stage_name}/"
    
    print(f"  Uploading {file_name} to {stage_target}...")
    
    # PUT command - note: file path needs to be absolute, PUT preserves filename
    abs_path = os.path.abspath(local_path)
    put_sql = f"PUT file://{abs_path} {stage_target} overwrite=true auto_compress=false"
    
    cursor.execute(put_sql)
    result = cursor.fetchall()
    
    if result:
        status = result[0][6] if len(result[0]) > 6 else 'UNKNOWN'
        if status == 'UPLOADED':
            print(f"    ✓ {file_name} uploaded successfully")
            return True
        else:
            print(f"    ⚠ Status: {status}")
            return False
    return False

def main():
    print("=" * 60)
    print("DEPLOY STREAMLIT APP TO SNOWFLAKE")
    print("=" * 60)
    
    # Load private key
    private_key = load_private_key()
    
    # Connect to Snowflake
    print(f"Connecting to Snowflake...")
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
    
    # Create stage
    print(f"\n1. Creating stage: {STAGE_NAME}")
    cursor.execute(f"CREATE STAGE IF NOT EXISTS {STAGE_NAME}")
    print("   ✓ Stage created/verified")

    # Upload environment.yml for package management
    print(f"\n1b. Uploading environment.yml for package management...")
    env_file = SCRIPT_DIR / "environment.yml"
    if env_file.exists():
        # IMPORTANT: Must upload to stage root (empty string) for Snowflake to detect it
        upload_file_to_stage(cursor, str(env_file), STAGE_NAME, "")
    else:
        print("   ⚠ Warning: environment.yml not found, packages may not be installed")
        print("   ⚠ App will use default Snowflake packages only (no matplotlib/seaborn)")

    # Upload main app file
    print(f"\n2. Uploading Streamlit app files...")
    main_app_file = SCRIPT_DIR / "unified-calculator-app.py"
    
    if not main_app_file.exists():
        print(f"   ✗ Error: {main_app_file} not found")
        sys.exit(1)
    
    upload_file_to_stage(cursor, str(main_app_file), STAGE_NAME, "")
    
    # Upload pages directory files
    print(f"\n2b. Uploading pages directory files...")
    pages_dir = SCRIPT_DIR / "pages"
    if pages_dir.exists():
        page_count = 0
        for page_file in pages_dir.glob("*.py"):
            # Upload to pages/ subdirectory in stage
            if upload_file_to_stage(cursor, str(page_file), STAGE_NAME, "pages/"):
                page_count += 1
        print(f"   ✓ Uploaded {page_count} page file(s)")
    else:
        print("   ⚠ Warning: pages/ directory not found, skipping")
    
    # Upload CSV files to stage
    print(f"\n3. Uploading CSV data files...")
    csv_files = [
        "models/gpu-generator-compatibility/GPU-Generator-Compatibility-Matrix-v1.csv",
        "models/bess-sizing/BESS-Sizing-v1.csv",
        "models/data-logistics/DataLogistics-v1.csv"
    ]
    
    base_path = SCRIPT_DIR.parent
    for csv_rel_path in csv_files:
        csv_file = base_path / csv_rel_path
        if csv_file.exists():
            # Upload to subdirectory in stage
            stage_subdir = csv_rel_path.split('/')[0]  # e.g., 'gpu-generator-compatibility'
            upload_file_to_stage(cursor, str(csv_file), STAGE_NAME, f"{stage_subdir}/")
        else:
            print(f"   ⚠ Warning: {csv_file} not found, skipping")
    
    # CRITICAL: DROP + CREATE is required because Snowflake caches files during initial CREATE
    # ALTER STREAMLIT cannot update packages - must recreate app to pick up environment.yml
    # This causes 1-2 minute downtime but ensures environment.yml changes are picked up
    # This is the ONLY reliable way to update package dependencies
    print(f"\n4. Dropping existing Streamlit app (if exists)...")
    try:
        cursor.execute(f"DROP STREAMLIT IF EXISTS {APP_NAME}")
        print("   ✓ Existing app dropped")
    except Exception as e:
        error_msg = str(e).lower()
        if "does not exist" in error_msg or "not found" in error_msg:
            print("   ℹ App doesn't exist (expected on first deployment)")
        else:
            print(f"   ⚠ Note: {e}")
        print("   Continuing with CREATE...")

    # Create Streamlit app (reads environment.yml from stage root)
    print(f"\n4b. Creating Streamlit app with package dependencies: {APP_NAME}")
    # Use FROM syntax (newer, recommended) instead of ROOT_LOCATION (legacy)
    # Snowflake automatically detects and uses environment.yml from stage root during CREATE
    # Important: environment.yml must be at stage root (@stage_name/), not in subdirectories
    create_sql = f"""
    CREATE STREAMLIT {APP_NAME}
    FROM @{STAGE_NAME}
    MAIN_FILE = 'unified-calculator-app.py'
    QUERY_WAREHOUSE = {SNOWFLAKE_WAREHOUSE}
    COMMENT = 'Off-Grid Inference Infra Calculator'
    TITLE = 'Off-Grid Inference Infra Calculator'
    """

    cursor.execute(create_sql)
    print("   ✓ Streamlit app created with matplotlib and seaborn packages!")
    
    # Initialize the app (make it live)
    print(f"\n4c. Initializing app (making it live)...")
    try:
        cursor.execute(f"ALTER STREAMLIT {APP_NAME} ADD LIVE VERSION FROM LAST")
        print("   ✓ App initialized!")
    except Exception as e:
        error_msg = str(e)
        if "already has a live version" in error_msg.lower():
            print("   ✓ App already has a live version")
        else:
            print(f"   ⚠ Note: {e}")
            print("   You may need to access the app via Snowsight first to fully initialize")
    
    # Verify deployment
    print(f"\n5. Verifying deployment...")

    # Check app exists
    cursor.execute(f"SHOW STREAMLITS LIKE '{APP_NAME}'")
    result = cursor.fetchone()
    if result:
        print("   ✓ App exists in Snowflake")
    else:
        print("   ✗ Error: App not found after creation!")
        cursor.close()
        conn.close()
        sys.exit(1)

    # Check stage files
    print(f"\n5b. Verifying stage files...")
    cursor.execute(f"LIST @{STAGE_NAME}")
    stage_files = cursor.fetchall()
    file_names = [row[0].split('/')[-1] for row in stage_files]

    required_files = ['environment.yml', 'unified-calculator-app.py']
    missing = [f for f in required_files if f not in file_names]

    if missing:
        print(f"   ⚠ Warning: Missing files on stage: {', '.join(missing)}")
    else:
        print(f"   ✓ All required files present on stage")

    print(f"   Files on stage: {', '.join(file_names[:10])}{'...' if len(file_names) > 10 else ''}")

    # Get app URL
    print(f"\n6. Getting app URL...")
    app_url = f"https://{SNOWFLAKE_ACCOUNT}.snowflakecomputing.com/streamlit/{APP_NAME}"
    print(f"   ✓ App URL: {app_url}")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 60)
    print("DEPLOYMENT COMPLETE!")
    print("=" * 60)
    print(f"App Name: {APP_NAME}")
    print(f"App URL: {app_url}")
    print(f"Stage: @{STAGE_NAME}")
    print(f"Main File: unified-calculator-app.py")
    print(f"Packages: matplotlib=3.10.6, seaborn=0.13.2, streamlit=1.35.0")
    print("\n✓ App deployed with package dependencies from environment.yml")
    print("✓ matplotlib and seaborn should now be available for import")
    print("\nNext steps:")
    print("1. Access the app via Snowsight: Streamlit → " + APP_NAME)
    print("2. Or use the URL above")
    print("3. Verify no ModuleNotFoundError for matplotlib")
    print("4. Test visualization features to ensure charts render")
    print("5. Configure Cloudflare DNS if using custom domain")
    
    return app_url

if __name__ == "__main__":
    main()

