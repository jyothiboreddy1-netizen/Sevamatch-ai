#!/bin/bash
# Stop SevaMatch AI live server and tunnel
pkill -f "uvicorn app.main:app"
pkill -f "cloudflared tunnel"
echo "SevaMatch live server and tunnel stopped."

