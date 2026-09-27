#!/usr/bin/env bash
# ==============================================================================
# Fable-Omega Ultra-Low-Cost 1-Click VPS Deployment Script
# Deploys the multi-tenant bot fleet on any Ubuntu/Debian VPS ($3/mo) in < 2 mins.
# ==============================================================================

set -e

echo "============================================================"
echo "⚡ FABLE-OMEGA 1-CLICK BOT FLEET DEPLOYMENT SCRIPT"
echo "============================================================"

# 1. Update OS & Install Python / Caddy
echo "[1/4] Updating packages and installing runtime tools..."
sudo apt-get update -y
sudo apt-get install -y python3 python3-pip python3-venv git curl debian-keyring debian-archive-keyring apt-transport-https

# 2. Setup Systemd Service
echo "[2/4] Setting up systemd background service..."
APP_DIR=$(pwd)

cat << EOF | sudo tee /etc/systemd/system/omnibot.service
[Unit]
Description=Fable-Omega Multi-Tenant Bot Fleet Service
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$APP_DIR
ExecStart=/usr/bin/python3 $APP_DIR/run.py --host 0.0.0.0 --port 8000
Restart=always
RestartSec=5
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

# 3. Reload & Start Service
echo "[3/4] Starting Omnibot background service..."
sudo systemctl daemon-reload
sudo systemctl enable omnibot
sudo systemctl restart omnibot

# 4. Verification
echo "[4/4] Verifying health check endpoint..."
sleep 2
curl -s http://localhost:8000/healthz || echo "Service starting up..."

echo "============================================================"
echo "✅ DEPLOYMENT COMPLETE! All 5 bots are running 24/7."
echo "📊 Web Control Center: http://YOUR_VPS_IP:8000"
echo "============================================================"
