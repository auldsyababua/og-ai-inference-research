#!/bin/bash
# Start Streamlit app in Jupyter container

echo "🚀 Starting Streamlit Unified Calculator App..."
echo ""

# Check if Streamlit is already running
if docker exec jupyter ps aux | grep -q "[s]treamlit"; then
    echo "⚠️  Streamlit is already running!"
    echo ""
    echo "To access it, you need to set up port forwarding:"
    echo "  Option 1: docker port-forward jupyter 8501:8501"
    echo "  Option 2: ssh -L 8501:localhost:8501 user@workhorse.local"
    echo ""
    echo "Then access at: http://localhost:8501"
    exit 0
fi

# Start Streamlit in background
echo "Starting Streamlit server..."
docker exec -d jupyter streamlit run \
    /home/jovyan/work/og-ai-inference-research/tools/unified-calculator-app.py \
    --server.port 8501 \
    --server.address 0.0.0.0 \
    --server.headless true

sleep 2

# Check if it started
if docker exec jupyter ps aux | grep -q "[s]treamlit"; then
    echo "✅ Streamlit is now running!"
    echo ""
    echo "📋 To access the app:"
    echo ""
    echo "Method 1 - Port Forwarding (Recommended):"
    echo "  Run this in another terminal:"
    echo "    docker port-forward jupyter 8501:8501"
    echo "  Then open: http://localhost:8501"
    echo ""
    echo "Method 2 - SSH Tunnel (if remote):"
    echo "  ssh -L 8501:localhost:8501 user@workhorse.local"
    echo "  Then open: http://localhost:8501"
    echo ""
    echo "Method 3 - Direct (if on same network):"
    CONTAINER_IP=$(docker inspect jupyter --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' 2>/dev/null)
    if [ ! -z "$CONTAINER_IP" ]; then
        echo "  Container IP: $CONTAINER_IP"
        echo "  Access at: http://$CONTAINER_IP:8501"
    fi
    echo ""
    echo "To stop: docker exec jupyter pkill -f streamlit"
else
    echo "❌ Failed to start Streamlit. Check logs:"
    echo "   docker logs jupyter --tail 50"
fi

