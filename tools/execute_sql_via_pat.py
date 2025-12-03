#!/usr/bin/env python3
"""
Execute SQL commands via PAT after network policy is created
This script can be used once network policy is set up
"""
import snowflake.connector
import os
import sys

# Configuration
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT", "ZWZLXDA-MEB82135")
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER", "10NETZERO")
SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN")

# SQL commands to execute
SQL_COMMANDS = [
    """CREATE NETWORK POLICY IF NOT EXISTS ALLOW_ALL_IPS
  ALLOWED_IP_LIST = ('0.0.0.0/0')
  COMMENT = 'Allow all IPs for PAT authentication'""",
    "ALTER USER 10NETZERO SET NETWORK_POLICY = 'ALLOW_ALL_IPS'",
    "SHOW NETWORK POLICIES LIKE 'ALLOW_ALL_IPS'",
]

def main():
    # Get PAT token
    PAT_TOKEN = None
    if len(sys.argv) > 1:
        PAT_TOKEN = sys.argv[1].strip()
    elif os.getenv("SNOWFLAKE_PAT_TOKEN"):
        PAT_TOKEN = os.getenv("SNOWFLAKE_PAT_TOKEN").strip()
    else:
        print("Error: PAT token required")
        print("Usage: python3 execute_sql_via_pat.py <pat-token>")
        sys.exit(1)
    
    print("=" * 60)
    print("EXECUTING SQL VIA PAT")
    print("=" * 60)
    
    try:
        # Connect using PAT
        print("Connecting to Snowflake using PAT...")
        conn = snowflake.connector.connect(
            user=SNOWFLAKE_USER,
            password=PAT_TOKEN,
            account=SNOWFLAKE_ACCOUNT,
            role=SNOWFLAKE_ROLE
        )
        
        cursor = conn.cursor()
        print("✓ Connected successfully!")
        
        # Execute SQL commands
        for i, sql in enumerate(SQL_COMMANDS, 1):
            print(f"\n[{i}/{len(SQL_COMMANDS)}] Executing SQL...")
            print(f"SQL: {sql[:50]}...")
            cursor.execute(sql)
            
            # Fetch results if it's a SELECT/SHOW command
            if sql.strip().upper().startswith(('SELECT', 'SHOW', 'DESC')):
                result = cursor.fetchall()
                print(f"✓ Result: {len(result)} row(s)")
                if result:
                    for row in result[:3]:  # Show first 3 rows
                        print(f"  {row}")
            else:
                print("✓ Executed successfully")
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("SUCCESS!")
        print("=" * 60)
        print("Network policy created and assigned.")
        print("\nNow test adding the public key:")
        print("  python3 add_public_key_with_pat.py '<pat-token>'")
        
    except snowflake.connector.errors.ProgrammingError as e:
        error_msg = str(e)
        if "Network policy is required" in error_msg:
            print("\n" + "=" * 60)
            print("⚠️  NETWORK POLICY STILL REQUIRED")
            print("=" * 60)
            print("The network policy hasn't been created yet.")
            print("\nYou need to run the SQL commands manually in Snowflake web UI first.")
            print("See SOLUTION_NETWORK_POLICY.md for instructions.")
        else:
            print(f"\n✗ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

