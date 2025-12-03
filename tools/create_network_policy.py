#!/usr/bin/env python3
"""
Create a network policy for PAT authentication
This allows PATs to work without the bypass option
"""
import snowflake.connector
import os
import sys
import socket

# Configuration
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT", "ZWZLXDA-MEB82135")
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER", "10NETZERO")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD", "eNCt-L.WDm4ZKVADTbw8")
SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN")

# Network policy name
POLICY_NAME = "ALLOW_ALL_IPS"  # Or make it more restrictive

def get_public_ip():
    """Get public IP address (simplified - may need adjustment)"""
    try:
        import urllib.request
        ip = urllib.request.urlopen('https://api.ipify.org').read().decode('utf8')
        return ip
    except:
        return None

def main():
    print("=" * 60)
    print("CREATING NETWORK POLICY FOR PAT AUTHENTICATION")
    print("=" * 60)
    
    # Get public IP
    public_ip = get_public_ip()
    if public_ip:
        print(f"Detected public IP: {public_ip}")
        print("Note: You may want to use 0.0.0.0/0 to allow all IPs (less secure)")
    
    print("\nThis script will create a network policy that allows all IPs.")
    print("For production, you should restrict this to specific IP ranges.")
    print()
    
    try:
        # Connect using password (since PAT needs network policy)
        print("Connecting to Snowflake...")
        conn = snowflake.connector.connect(
            user=SNOWFLAKE_USER,
            password=SNOWFLAKE_PASSWORD,
            account=SNOWFLAKE_ACCOUNT,
            role=SNOWFLAKE_ROLE
        )
        
        cursor = conn.cursor()
        print("✓ Connected!")
        
        # Check if policy already exists
        print(f"\nChecking if network policy '{POLICY_NAME}' exists...")
        cursor.execute(f"SHOW NETWORK POLICIES LIKE '{POLICY_NAME}'")
        existing = cursor.fetchall()
        
        if existing:
            print(f"✓ Network policy '{POLICY_NAME}' already exists")
            print("  Updating to allow all IPs...")
            cursor.execute(f"""
                ALTER NETWORK POLICY {POLICY_NAME}
                SET ALLOWED_IP_LIST = ('0.0.0.0/0')
            """)
            print("✓ Policy updated")
        else:
            print(f"Creating network policy '{POLICY_NAME}'...")
            cursor.execute(f"""
                CREATE NETWORK POLICY IF NOT EXISTS {POLICY_NAME}
                ALLOWED_IP_LIST = ('0.0.0.0/0')
                COMMENT = 'Allow all IPs for PAT authentication'
            """)
            print("✓ Policy created")
        
        # Assign policy to user
        print(f"\nAssigning network policy to user {SNOWFLAKE_USER}...")
        cursor.execute(f"ALTER USER {SNOWFLAKE_USER} SET NETWORK_POLICY = '{POLICY_NAME}'")
        print("✓ Network policy assigned to user")
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("SUCCESS!")
        print("=" * 60)
        print("Network policy created and assigned.")
        print("\nNow you can use your PAT token:")
        print("  python3 add_public_key_with_pat.py '<your-pat-token>'")
        
    except snowflake.connector.errors.ProgrammingError as e:
        if "Multi-factor authentication" in str(e):
            print("\n✗ MFA is required - can't use password authentication")
            print("\nYou'll need to:")
            print("1. Create the network policy via SQL in Snowflake web UI:")
            print(f"   CREATE NETWORK POLICY {POLICY_NAME} ALLOWED_IP_LIST = ('0.0.0.0/0');")
            print(f"   ALTER USER {SNOWFLAKE_USER} SET NETWORK_POLICY = '{POLICY_NAME}';")
            print("\n2. Then use your PAT token")
        else:
            print(f"\n✗ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

