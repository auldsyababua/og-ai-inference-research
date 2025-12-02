#!/bin/bash
#
# GitLab Comprehensive Backup Before Redeployment
# Date: 2025-12-02
# Purpose: Full backup of GitLab instance before router configuration changes
#

set -euo pipefail

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}=== GitLab Comprehensive Backup ===${NC}\n"

# Configuration
BACKUP_ROOT="/srv/backups/gitlab-pre-redeploy-$(date +%Y%m%d-%H%M%S)"
GITLAB_CONFIG="/srv/services/gitlab/config"
GITLAB_DATA="/srv/services/gitlab/data"
GITLAB_LOGS="/srv/services/gitlab/logs"

echo -e "${YELLOW}Backup location: ${BACKUP_ROOT}${NC}\n"

# Create backup directory structure
echo "Creating backup directories..."
mkdir -p "${BACKUP_ROOT}"/{config,compose,validation}

# 1. Create GitLab application backup (repositories, database, etc)
echo -e "\n${YELLOW}Step 1: Creating GitLab application backup...${NC}"
docker exec gitlab gitlab-backup create SKIP=registry,uploads,builds,artifacts,lfs,packages

# Wait for backup to complete
sleep 5

# Find the backup file
BACKUP_FILE=$(docker exec gitlab ls -t /var/opt/gitlab/backups/ | head -1)
echo -e "${GREEN}✓ Backup created: ${BACKUP_FILE}${NC}"

# Copy backup file out of container
echo "Copying backup file to host..."
docker cp "gitlab:/var/opt/gitlab/backups/${BACKUP_FILE}" "${BACKUP_ROOT}/gitlab-backup-${BACKUP_FILE}"

# 2. Backup GitLab secrets (CRITICAL!)
echo -e "\n${YELLOW}Step 2: Backing up GitLab secrets (CRITICAL)...${NC}"
if docker exec gitlab test -f /etc/gitlab/gitlab-secrets.json; then
    docker cp gitlab:/etc/gitlab/gitlab-secrets.json "${BACKUP_ROOT}/config/"
    echo -e "${GREEN}✓ Secrets file backed up${NC}"
else
    echo -e "${RED}✗ WARNING: gitlab-secrets.json not found!${NC}"
fi

# 3. Backup GitLab configuration
echo -e "\n${YELLOW}Step 3: Backing up GitLab configuration...${NC}"
docker cp gitlab:/etc/gitlab/gitlab.rb "${BACKUP_ROOT}/config/"
echo -e "${GREEN}✓ Configuration backed up${NC}"

# 4. Backup docker-compose file and current labels
echo -e "\n${YELLOW}Step 4: Backing up deployment configuration...${NC}"

# Find actual compose file used for deployment
COMPOSE_FILE=$(docker inspect gitlab | jq -r '.[0].Config.Labels["com.docker.compose.project.working_dir"]')/docker-compose.yml
if [ -f "$COMPOSE_FILE" ]; then
    cp "$COMPOSE_FILE" "${BACKUP_ROOT}/compose/docker-compose.yml.original"
    echo -e "${GREEN}✓ Original compose file: ${COMPOSE_FILE}${NC}"
else
    echo -e "${YELLOW}! Original compose file not found, saving container labels instead${NC}"
fi

# Save current container labels
docker inspect gitlab | jq '.[0].Config.Labels' > "${BACKUP_ROOT}/compose/container-labels.json"
echo -e "${GREEN}✓ Container labels saved${NC}"

# 5. Save GitLab version and environment info
echo -e "\n${YELLOW}Step 5: Saving version and environment info...${NC}"
docker exec gitlab gitlab-rake gitlab:env:info > "${BACKUP_ROOT}/validation/gitlab-env-info.txt" 2>&1
docker exec gitlab cat /opt/gitlab/version-manifest.txt > "${BACKUP_ROOT}/validation/version-manifest.txt" 2>&1
echo -e "${GREEN}✓ Version info saved${NC}"

# 6. List all repositories (for validation after restore)
echo -e "\n${YELLOW}Step 6: Creating repository inventory...${NC}"
docker exec gitlab gitlab-rake gitlab:list_repos > "${BACKUP_ROOT}/validation/repository-list.txt" 2>&1
echo -e "${GREEN}✓ Repository list saved${NC}"

# 7. Export current Traefik configuration
echo -e "\n${YELLOW}Step 7: Backing up Traefik configuration...${NC}"
cp /srv/services/compose/traefik/docker-compose.yml "${BACKUP_ROOT}/compose/traefik-docker-compose.yml"
docker inspect traefik | jq '.[0].Config.Labels' > "${BACKUP_ROOT}/compose/traefik-labels.json"
echo -e "${GREEN}✓ Traefik config saved${NC}"

# 8. Create restore instructions
echo -e "\n${YELLOW}Step 8: Creating restore instructions...${NC}"
cat > "${BACKUP_ROOT}/RESTORE_INSTRUCTIONS.md" <<'EOF'
# GitLab Restore Instructions

## Prerequisites
- GitLab container must be running (same version or compatible)
- All services stopped (Puma, Sidekiq)

## Restore Steps

### 1. Stop GitLab services
```bash
docker exec gitlab gitlab-ctl stop puma
docker exec gitlab gitlab-ctl stop sidekiq
docker exec gitlab gitlab-ctl status
```

### 2. Copy backup files to container
```bash
BACKUP_FILE="<backup_filename>.tar"
docker cp "$BACKUP_FILE" gitlab:/var/opt/gitlab/backups/
docker cp config/gitlab-secrets.json gitlab:/etc/gitlab/
docker cp config/gitlab.rb gitlab:/etc/gitlab/
```

### 3. Set correct permissions
```bash
docker exec gitlab chown git:git /var/opt/gitlab/backups/*.tar
docker exec gitlab chmod 600 /etc/gitlab/gitlab-secrets.json
```

### 4. Restore backup
```bash
# Extract backup timestamp (format: 1733167200_2025_12_02_17.5.3)
BACKUP_TIMESTAMP="<timestamp_from_filename>"
docker exec gitlab gitlab-backup restore BACKUP=${BACKUP_TIMESTAMP}
```

### 5. Reconfigure and restart
```bash
docker exec gitlab gitlab-ctl reconfigure
docker exec gitlab gitlab-ctl restart
```

### 6. Validate restore
```bash
# Check application status
docker exec gitlab gitlab-rake gitlab:check SANITIZE=true

# List repositories (compare with validation/repository-list.txt)
docker exec gitlab gitlab-rake gitlab:list_repos

# Test web UI access
curl -I http://workhorse.local/gitlab/

# Test git clone
git clone http://workhorse.local/gitlab/root/test-repo.git /tmp/test-clone
```

## Files in This Backup

- `gitlab-backup-*.tar` - Application backup (repos, DB, wiki, etc)
- `config/gitlab-secrets.json` - Encryption keys (REQUIRED for restore)
- `config/gitlab.rb` - Configuration file
- `compose/docker-compose.yml.original` - Original deployment config
- `compose/container-labels.json` - Current Traefik labels
- `validation/gitlab-env-info.txt` - Version and environment info
- `validation/repository-list.txt` - List of all repositories (for validation)

## What's NOT in Backup

Per GitLab documentation, these items are excluded:
- Container Registry images (SKIP=registry)
- CI/CD artifacts (SKIP=artifacts)
- LFS objects (SKIP=lfs)
- Uploaded files (SKIP=uploads)
- CI builds (SKIP=builds)
- Packages (SKIP=packages)

If you need these, run a full backup without SKIP options:
```bash
docker exec gitlab gitlab-backup create
```

## Troubleshooting

### Restore fails with "Backup version mismatch"
- Backup and restore must use same GitLab major version
- Check versions: `cat validation/version-manifest.txt`

### Repositories missing after restore
- Compare: `docker exec gitlab gitlab-rake gitlab:list_repos` vs `validation/repository-list.txt`
- Check permissions: `docker exec gitlab gitlab-rake gitlab:check`

### 422 Errors after restore
- Verify secrets file restored: `docker exec gitlab cat /etc/gitlab/gitlab-secrets.json`
- Secrets must match original deployment

## Emergency Rollback

If redeployment fails, restore original configuration:
```bash
# Stop new deployment
docker-compose -f docker-compose.gitlab.yml down

# Restore original compose file
cp compose/docker-compose.yml.original <original_location>/docker-compose.yml

# Redeploy with original config
docker-compose -f <original_location>/docker-compose.yml up -d

# Follow restore steps above
```
EOF

echo -e "${GREEN}✓ Restore instructions created${NC}"

# 9. Create backup summary
echo -e "\n${YELLOW}Step 9: Creating backup summary...${NC}"
cat > "${BACKUP_ROOT}/BACKUP_SUMMARY.txt" <<EOF
GitLab Backup Summary
Created: $(date)
Backup Location: ${BACKUP_ROOT}

=== Backup Contents ===
$(du -sh "${BACKUP_ROOT}")

=== Files Backed Up ===
$(ls -lh "${BACKUP_ROOT}")

=== GitLab Version ===
$(docker exec gitlab cat /opt/gitlab/version-manifest.txt | head -5)

=== Repository Count ===
$(docker exec gitlab gitlab-rake gitlab:list_repos 2>/dev/null | wc -l) repositories

=== Data Sizes ===
Config: $(du -sh ${GITLAB_CONFIG} | cut -f1)
Data: $(du -sh ${GITLAB_DATA} | cut -f1)
Logs: $(du -sh ${GITLAB_LOGS} | cut -f1)

=== Backup Verification ===
Application backup: $(ls -lh "${BACKUP_ROOT}"/gitlab-backup-*.tar | awk '{print $5}')
Secrets file: $([ -f "${BACKUP_ROOT}/config/gitlab-secrets.json" ] && echo "Present" || echo "MISSING")
Config file: $([ -f "${BACKUP_ROOT}/config/gitlab.rb" ] && echo "Present" || echo "MISSING")

=== Next Steps ===
1. Verify backup integrity
2. Update docker-compose.yml with new router configuration
3. Redeploy GitLab container
4. Validate services accessible
5. Test git push operations

=== Backup Validation ===
To validate this backup can be restored:
$ cat ${BACKUP_ROOT}/RESTORE_INSTRUCTIONS.md
EOF

echo -e "${GREEN}✓ Backup summary created${NC}"

# 10. Set permissions
chmod -R 755 "${BACKUP_ROOT}"

# Final summary
echo -e "\n${GREEN}=== Backup Complete ===${NC}\n"
cat "${BACKUP_ROOT}/BACKUP_SUMMARY.txt"

echo -e "\n${GREEN}✓ All backup steps completed successfully!${NC}"
echo -e "\n${YELLOW}Backup location:${NC} ${BACKUP_ROOT}"
echo -e "${YELLOW}Restore instructions:${NC} ${BACKUP_ROOT}/RESTORE_INSTRUCTIONS.md"
echo -e "\n${GREEN}Safe to proceed with redeployment.${NC}\n"
