#!/bin/bash
#
# Complete solution: Create network policy SQL + Test PAT
# This script provides SQL commands and then tests PAT authentication
#

set -euo pipefail

echo "============================================================"
echo "SNOWFLAKE PAT NETWORK POLICY SOLUTION"
echo "============================================================"
echo ""
echo "STEP 1: Run these SQL commands in Snowflake Web UI"
echo "============================================================"
echo ""
echo "Copy and paste this SQL into Snowflake Worksheet:"
echo ""
cat << 'EOF'
-- Create network policy that allows all IPs
CREATE NETWORK POLICY IF NOT EXISTS ALLOW_ALL_IPS
  ALLOWED_IP_LIST = ('0.0.0.0/0')
  COMMENT = 'Allow all IPs for PAT authentication';

-- Assign it to your user
ALTER USER 10NETZERO SET NETWORK_POLICY = 'ALLOW_ALL_IPS';

-- Verify (optional)
SHOW NETWORK POLICIES LIKE 'ALLOW_ALL_IPS';
DESC USER 10NETZERO;
EOF

echo ""
echo "============================================================"
echo "STEP 2: After running SQL, test PAT authentication"
echo "============================================================"
echo ""
echo "Once you've run the SQL commands above, provide your PAT token:"
echo ""
read -p "Enter your PAT token: " PAT_TOKEN

if [ -z "$PAT_TOKEN" ]; then
    echo "Error: PAT token required"
    exit 1
fi

echo ""
echo "Testing PAT authentication..."
cd "$(dirname "$0")"
python3 add_public_key_with_pat.py "$PAT_TOKEN"

