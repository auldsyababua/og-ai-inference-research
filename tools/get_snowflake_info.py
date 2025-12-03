#!/usr/bin/env python3
"""
Query Snowflake to get current warehouse, database, and schema
"""
import snowflake.connector
import sys

# Snowflake connection details
SNOWFLAKE_ACCOUNT = "ZWZLXDA-MEB82135"
SNOWFLAKE_USER = "10NETZERO"
SNOWFLAKE_PASSWORD = "eNCt-L.WDm4ZKVADTbw8"
SNOWFLAKE_ROLE = "ACCOUNTADMIN"

try:
    # Connect to Snowflake
    conn = snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        role=SNOWFLAKE_ROLE
    )
    
    cursor = conn.cursor()
    
    # Get current warehouse
    cursor.execute("SELECT CURRENT_WAREHOUSE()")
    warehouse = cursor.fetchone()[0]
    
    # Get current database
    cursor.execute("SELECT CURRENT_DATABASE()")
    database = cursor.fetchone()[0]
    
    # Get current schema
    cursor.execute("SELECT CURRENT_SCHEMA()")
    schema = cursor.fetchone()[0]
    
    # Get available warehouses
    cursor.execute("SHOW WAREHOUSES")
    warehouses = cursor.fetchall()
    
    # Get available databases
    cursor.execute("SHOW DATABASES")
    databases = cursor.fetchall()
    
    print("=" * 60)
    print("SNOWFLAKE CONNECTION INFO")
    print("=" * 60)
    print(f"Account: {SNOWFLAKE_ACCOUNT}")
    print(f"User: {SNOWFLAKE_USER}")
    print(f"Role: {SNOWFLAKE_ROLE}")
    print()
    print("CURRENT VALUES:")
    print(f"  Warehouse: {warehouse or '(none)'}")
    print(f"  Database: {database or '(none)'}")
    print(f"  Schema: {schema or '(none)'}")
    print()
    print("AVAILABLE WAREHOUSES:")
    for wh in warehouses:
        print(f"  - {wh[0]}")
    print()
    print("AVAILABLE DATABASES:")
    for db in databases:
        print(f"  - {db[1]}")  # Database name is typically in column 1
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"Error connecting to Snowflake: {e}", file=sys.stderr)
    sys.exit(1)

