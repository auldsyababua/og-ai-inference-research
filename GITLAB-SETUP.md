# GitLab Repository Setup

This repository is ready to be pushed to GitLab. Follow these steps:

## Quick Setup

### Option 1: Automated Setup (Recommended)

If you have a GitLab personal access token:

```bash
export GITLAB_TOKEN=your-token-here
./setup-gitlab.sh
git push -u origin main
```

### Option 2: Manual Setup via Web UI

1. Go to your GitLab instance: `http://workhorse.local/gitlab` (or your GitLab URL)
2. Click "New project" → "Create blank project"
3. Project name: `og-ai-inference-research`
4. Description: `Off-grid AI inference infrastructure research - modeling natural gas generators, GPU power dynamics, and BESS integration`
5. Visibility: Public (or Private, as preferred)
6. **DO NOT** initialize with README (we already have one)
7. Click "Create project"

Then add the remote and push:

```bash
# Replace with your actual GitLab URL
git remote add origin http://workhorse.local/gitlab/your-username/og-ai-inference-research.git

# Or if using SSH:
git remote add origin git@workhorse.local:your-username/og-ai-inference-research.git

git push -u origin main
```

### Option 3: Manual Setup via API

```bash
# Set your GitLab token
export GITLAB_TOKEN=your-token-here

# Create repository
curl --request POST \
  --header "PRIVATE-TOKEN: ${GITLAB_TOKEN}" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "og-ai-inference-research",
    "description": "Off-grid AI inference infrastructure research",
    "visibility": "public"
  }' \
  "http://workhorse.local/gitlab/api/v4/projects"

# Then add remote and push (use the URL from the response)
git remote add origin <repository-url>
git push -u origin main
```

## Notes

- This is a **research repository** with minimal CI/CD (just basic validation)
- The `.gitlab-ci.yml` is intentionally minimal - no complex pipelines needed
- PDF files are included in the repository (consider Git LFS if they become too large)

## Repository Structure

- `data/` - Structured technical data (generators, GPU profiles)
- `research/` - Consolidated research reports and source materials
- `models/` - Calculators and simulation tools
- `docs/` - Project documentation
- `prompts/research/` - Research prompts for future work

## Current Status

- ✅ Phase 1 Foundation: 100% Complete
- 🔄 Phase 2 Research Consolidation: 90% Complete
- 🔄 Phase 3 Expansion: 10% Complete

See `STATUS.md` for detailed progress.

