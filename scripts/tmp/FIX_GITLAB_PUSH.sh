#!/bin/bash
#
# GitLab Push Fix: Add WiFi Subnet to Traefik IP Whitelist
# Issue: HTTP 403 Forbidden when pushing via WiFi (192.168.1.x)
# Root Cause: Traefik lan-only middleware blocks WiFi subnet
# Solution: Add 192.168.1.0/24 to IP whitelist
#
# Date: 2025-12-02
# Reference: /srv/projects/mac-workhorse-integration/GITLAB-HTTP-403-INVESTIGATION.md

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}GitLab Push Fix - Adding WiFi Subnet to Traefik Whitelist${NC}\n"

# Configuration
TRAEFIK_COMPOSE="/srv/projects/mac-workhorse-integration/services/compose/traefik/docker-compose.yml"
TRAEFIK_BACKUP="${TRAEFIK_COMPOSE}.backup-$(date +%Y%m%d-%H%M%S)"

# Verify file exists
if [ ! -f "$TRAEFIK_COMPOSE" ]; then
    echo -e "${RED}ERROR: Traefik compose file not found: $TRAEFIK_COMPOSE${NC}"
    exit 1
fi

# Show current whitelist
echo -e "${YELLOW}Current IP whitelist:${NC}"
grep "lan-only.ipallowlist.sourcerange" "$TRAEFIK_COMPOSE"
echo

# Check if WiFi subnet already added
if grep -q "192.168.1.0/24" "$TRAEFIK_COMPOSE"; then
    echo -e "${GREEN}✓ WiFi subnet (192.168.1.0/24) already in whitelist${NC}"
    echo -e "${YELLOW}Checking if GitLab push works now...${NC}\n"

    # Test GitLab API access
    if curl -s -u admin:tonto989 "http://workhorse.local/gitlab/api/v4/user" | grep -q "username"; then
        echo -e "${GREEN}✓ GitLab API accessible!${NC}\n"
        echo "You can now push to GitLab:"
        echo "  cd /srv/projects/og-ai-inference-research"
        echo "  git push -u origin main"
    else
        echo -e "${RED}✗ GitLab API still returns 403${NC}"
        echo "Other issue may be present. Check logs:"
        echo "  docker logs traefik 2>&1 | tail -50"
    fi
    exit 0
fi

# Create backup
echo -e "${YELLOW}Creating backup: $TRAEFIK_BACKUP${NC}"
cp "$TRAEFIK_COMPOSE" "$TRAEFIK_BACKUP"

# Update whitelist (add 192.168.1.0/24 for WiFi)
echo -e "${YELLOW}Adding 192.168.1.0/24 to IP whitelist...${NC}"
sed -i 's|lan-only.ipallowlist.sourcerange=\(.*\)|lan-only.ipallowlist.sourcerange=\1,192.168.1.0/24|' "$TRAEFIK_COMPOSE"

# Show updated whitelist
echo -e "${GREEN}Updated IP whitelist:${NC}"
grep "lan-only.ipallowlist.sourcerange" "$TRAEFIK_COMPOSE"
echo

# Restart Traefik
echo -e "${YELLOW}Restarting Traefik to apply changes...${NC}"
cd "$(dirname "$TRAEFIK_COMPOSE")"
docker-compose restart traefik

# Wait for Traefik to be ready
echo -e "${YELLOW}Waiting 10 seconds for Traefik to fully restart...${NC}"
sleep 10

# Test GitLab access
echo -e "${YELLOW}Testing GitLab API access...${NC}"
if curl -s -u admin:tonto989 "http://workhorse.local/gitlab/api/v4/user" | grep -q "username"; then
    echo -e "${GREEN}✓ SUCCESS! GitLab API now accessible${NC}\n"

    echo -e "${GREEN}Fix applied successfully!${NC}"
    echo
    echo "You can now push to GitLab:"
    echo "  cd /srv/projects/og-ai-inference-research"
    echo "  git push -u origin main"
    echo
    echo "Backup saved to: $TRAEFIK_BACKUP"
else
    echo -e "${RED}✗ GitLab API still returns 403${NC}"
    echo
    echo "Rolling back changes..."
    mv "$TRAEFIK_BACKUP" "$TRAEFIK_COMPOSE"
    docker-compose restart traefik
    echo
    echo -e "${RED}Fix failed. Check Traefik logs:${NC}"
    echo "  docker logs traefik 2>&1 | tail -50"
    exit 1
fi
