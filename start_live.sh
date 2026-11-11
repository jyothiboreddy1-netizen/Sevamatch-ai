#!/bin/bash
# Start SevaMatch AI detached live server and Cloudflare tunnel

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Stop any existing instances
pkill -f "uvicorn app.main:app" 2>/dev/null
pkill -f "cloudflared tunnel" 2>/dev/null
sleep 1

# Start Backend (serves frontend + API)
echo "Starting backend..."
nohup backend/.venv/bin/python -m uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port 8000 > backend.log 2>&1 & disown

# Start Cloudflare Tunnel
echo "Starting Cloudflare live tunnel..."
nohup cloudflared tunnel --url http://localhost:8000 > tunnel.log 2>&1 & disown

sleep 4

TUNNEL_URL=$(grep -oE "https://[a-zA-Z0-9-]+\.trycloudflare\.com" tunnel.log | tail -n 1)
echo "=========================================="
echo "SevaMatch AI is LIVE at:"
echo "$TUNNEL_URL"
echo "=========================================="

