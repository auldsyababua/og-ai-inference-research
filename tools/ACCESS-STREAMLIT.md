# Accessing the Streamlit Web App

## ✅ Streamlit is Running!

The Streamlit app is now running in the Jupyter container on port 8501.

## Access Methods

### Method 1: Port Forwarding (Quick Access)

Forward the port from the container to your host:

```bash
docker port-forward jupyter 8501:8501
```

Or use SSH tunnel if accessing remotely:
```bash
ssh -L 8501:localhost:8501 user@workhorse.local
```

Then access at: **http://localhost:8501**

### Method 2: Direct Container Access (If on Same Network)

If you're on the same network as the container:

```bash
# Find container IP
docker inspect jupyter --format='{{.NetworkSettings.IPAddress}}'
```

Then access at: **http://<container-ip>:8501**

### Method 3: Traefik Route (Recommended for Production)

Add a Traefik route to access via `http://workhorse.local/calculator/`:

**Option A: Add to Jupyter container labels** (if you control docker-compose):
```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.calculator.rule=Host(`workhorse.local`) && PathPrefix(`/calculator`)"
  - "traefik.http.services.calculator.loadbalancer.server.port=8501"
  - "traefik.http.routers.calculator.middlewares=lan-only"
```

**Option B: Create separate Streamlit container** with Traefik labels pointing to Jupyter:8501

### Method 4: SSH Tunnel (Remote Access)

If accessing from a remote machine:

```bash
ssh -L 8501:localhost:8501 user@workhorse.local
```

Then access at: **http://localhost:8501**

## Current Status

- ✅ Streamlit installed (version 1.51.0)
- ✅ App file exists and is valid
- ✅ Streamlit process running (PID: check with `docker exec jupyter ps aux | grep streamlit`)
- ⚠️ Port 8501 needs to be exposed/accessible

## Quick Test

Test if Streamlit is responding:

```bash
docker exec jupyter curl -s http://localhost:8501 | head -20
```

You should see HTML output if it's working.

## Stopping the App

To stop Streamlit:

```bash
docker exec jupyter pkill -f streamlit
```

## Restarting the App

To restart:

```bash
docker exec -d jupyter streamlit run /home/jovyan/work/og-ai-inference-research/tools/unified-calculator-app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true
```

## Troubleshooting

### Port Not Accessible

If you can't access the app:

1. **Check if Streamlit is running:**
   ```bash
   docker exec jupyter ps aux | grep streamlit
   ```

2. **Check if port is listening:**
   ```bash
   docker exec jupyter netstat -tlnp | grep 8501
   ```

3. **Check Streamlit logs:**
   ```bash
   docker logs jupyter --tail 50 | grep -i streamlit
   ```

4. **Try accessing from inside container:**
   ```bash
   docker exec jupyter curl http://localhost:8501
   ```

### App Not Loading

- Check for Python errors in Streamlit output
- Verify all dependencies are installed
- Check file paths are correct

### Need to Expose Port

If you need to expose port 8501 from the container:

```bash
# Stop container
docker stop jupyter

# Restart with port mapping (if you control docker run/compose)
docker run ... -p 8501:8501 ...

# Or add to docker-compose.yml:
ports:
  - "8501:8501"
```

## Next Steps

1. **Set up port forwarding or Traefik route** (choose method above)
2. **Access the app** in your browser
3. **Fill in the form** with your deployment configuration
4. **Click Calculate** to see results
5. **Export results** to CSV if needed

The Streamlit interface is much more user-friendly than the Jupyter notebook!

