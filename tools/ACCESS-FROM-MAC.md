# Accessing Streamlit from Your Mac

## Your Setup
- **Mac IP:** 10.0.0.2
- **Workhorse:** workhorse.local
- **Streamlit running:** Port 8501 in Jupyter container

## Quick Access Methods

### Method 1: SSH Tunnel (Easiest - Recommended)

Run this command on your Mac:

```bash
ssh -L 8501:localhost:8501 user@workhorse.local
```

**Replace `user` with your actual username on workhorse.**

Then open in your Mac's browser:
**http://localhost:8501**

This creates a secure tunnel from your Mac to the Streamlit app.

### Method 2: Expose Port from Container (If you have Docker access)

If you can modify the Jupyter container to expose port 8501:

```bash
# Stop container
docker stop jupyter

# Restart with port mapping (adjust based on your docker setup)
docker start jupyter -p 8501:8501
```

Then access at: **http://workhorse.local:8501**

### Method 3: Add Traefik Route (Permanent Solution)

Add Streamlit to Traefik so you can access via `http://workhorse.local/calculator/`

This requires adding labels to the Jupyter container or creating a Traefik service.

## Testing Connection

From your Mac, test if you can reach workhorse:

```bash
# Test basic connectivity
ping workhorse.local

# Test SSH access
ssh user@workhorse.local "echo 'Connected!'"
```

## Troubleshooting

### SSH Tunnel Not Working

1. **Check SSH access:**
   ```bash
   ssh user@workhorse.local
   ```

2. **Check if port 8501 is already in use on Mac:**
   ```bash
   lsof -i :8501
   ```
   If something is using it, use a different local port:
   ```bash
   ssh -L 8502:localhost:8501 user@workhorse.local
   ```
   Then access at: http://localhost:8502

### Can't Access workhorse.local

Try using the IP address instead:
```bash
# Find workhorse IP
ping workhorse.local
# Use that IP in SSH command
ssh -L 8501:localhost:8501 user@<workhorse-ip>
```

## Quick Start Command

**Copy and run this on your Mac:**

```bash
ssh -L 8501:localhost:8501 $(whoami)@workhorse.local
```

Then open: **http://localhost:8501** in your browser.

Keep the SSH session open while using the app!

