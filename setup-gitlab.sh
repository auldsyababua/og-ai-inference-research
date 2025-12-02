#!/bin/bash
# GitLab Repository Setup Script
# For path-prefixed GitLab instances (workhorse.local/gitlab)

set -e

GITLAB_HOST="workhorse.local"
GITLAB_PATH_PREFIX="/gitlab"
GITLAB_BASE_URL="http://${GITLAB_HOST}${GITLAB_PATH_PREFIX}"
REPO_NAME="og-ai-inference-research"
REPO_DESCRIPTION="Off-grid AI inference infrastructure research - modeling natural gas generators, GPU power dynamics, and BESS integration"

echo "=== GitLab Repository Setup ==="
echo ""
echo "Repository: ${REPO_NAME}"
echo "GitLab URL: ${GITLAB_BASE_URL}"
echo ""

# Check if GitLab token is available
if [ -z "$GITLAB_TOKEN" ]; then
    echo "⚠️  GITLAB_TOKEN environment variable not set"
    echo ""
    echo "To create the repository, you have two options:"
    echo ""
    echo "Option 1: Create via GitLab Web UI"
    echo "  1. Go to: ${GITLAB_BASE_URL}"
    echo "  2. Create a new project named: ${REPO_NAME}"
    echo "  3. Copy the repository URL"
    echo "  4. Run: git remote add origin <repository-url>"
    echo "  5. Run: git push -u origin main"
    echo ""
    echo "Option 2: Create via API (requires token)"
    echo "  1. Get your GitLab personal access token"
    echo "  2. Export it: export GITLAB_TOKEN=your-token-here"
    echo "  3. Run this script again"
    echo ""
    exit 1
fi

echo "Creating repository via GitLab API..."
echo ""

# Create repository via API
RESPONSE=$(curl -s -w "\n%{http_code}" \
    --request POST \
    --header "PRIVATE-TOKEN: ${GITLAB_TOKEN}" \
    --header "Content-Type: application/json" \
    --data "{
        \"name\": \"${REPO_NAME}\",
        \"description\": \"${REPO_DESCRIPTION}\",
        \"visibility\": \"public\",
        \"initialize_with_readme\": false
    }" \
    "${GITLAB_BASE_URL}/api/v4/projects")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -eq 201 ]; then
    echo "✅ Repository created successfully!"
    echo ""
    
    # Extract SSH URL (preferred) or HTTP URL
    SSH_URL=$(echo "$BODY" | grep -o '"ssh_url_to_repo":"[^"]*' | cut -d'"' -f4 || echo "")
    HTTP_URL=$(echo "$BODY" | grep -o '"http_url_to_repo":"[^"]*' | cut -d'"' -f4 || echo "")
    
    if [ -n "$SSH_URL" ]; then
        REPO_URL="$SSH_URL"
    elif [ -n "$HTTP_URL" ]; then
        REPO_URL="$HTTP_URL"
    else
        # Fallback: construct URL
        REPO_URL="${GITLAB_BASE_URL}/$(whoami)/${REPO_NAME}.git"
    fi
    
    echo "Repository URL: ${REPO_URL}"
    echo ""
    echo "Setting up git remote..."
    git remote add origin "${REPO_URL}" 2>/dev/null || git remote set-url origin "${REPO_URL}"
    echo "✅ Remote 'origin' configured"
    echo ""
    echo "To push your code:"
    echo "  git push -u origin main"
    echo ""
else
    echo "❌ Failed to create repository"
    echo "HTTP Code: ${HTTP_CODE}"
    echo "Response: ${BODY}"
    echo ""
    echo "Common issues:"
    echo "  - Invalid GitLab token"
    echo "  - Repository name already exists"
    echo "  - Network connectivity issues"
    echo ""
    echo "You can create the repository manually via GitLab web UI:"
    echo "  ${GITLAB_BASE_URL}/-/projects/new"
    exit 1
fi

