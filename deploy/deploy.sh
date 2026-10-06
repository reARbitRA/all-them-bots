#!/usr/bin/env bash
# ==============================================================================
# FABLE-OMEGA Ultra-Low-Cost 1-Click VPS Deployment Script
# Deploys the multi-tenant bot fleet on any Ubuntu/Debian VPS in < 3 minutes.
# Safe to re-run (idempotent). Run as the user that will own the app (not root).
# ==============================================================================
set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/reARbitRA/all-them-bots.git}"
BRANCH="${BRANCH:-main}"
INSTALL_DIR="${INSTALL_DIR:-$HOME/fable-omega}"
PORT="${PORT:-8000}"
SERVICE_NAME="${SERVICE_NAME:-fable-omega}"

echo "============================================================"
echo "⚡ FABLE-OMEGA 1-CLICK BOT FLEET DEPLOYMENT"
echo "============================================================"
echo "  target dir : $INSTALL_DIR"
echo "  port       : $PORT"
echo "  branch     : $BRANCH"
echo "============================================================"

# --- 1. System dependencies -------------------------------------------------
echo "[1/5] Installing OS runtime..."
sudo apt-get update -y
sudo apt-get install -y --no-install-recommends \
    python3 python3-pip python3-venv python3-dev \
    git curl ca-certificates \
    build-essential

# --- 2. Clone / update repository ------------------------------------------
echo "[2/5] Cloning / updating source..."
if [ -d "$INSTALL_DIR/.git" ]; then
    cd "$INSTALL_DIR"
    git fetch --all --prune
    git checkout "$BRANCH"
    git reset --hard "origin/$BRANCH"
else
    git clone --branch "$BRANCH" "$REPO_URL" "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

# --- 3. Virtualenv + dependencies ------------------------------------------
echo "[3/5] Building Python virtualenv..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
# shellcheck disable=SC1091
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# --- 4. Data dir + environment ---------------------------------------------
echo "[4/5] Preparing data directory & environment..."
mkdir -p data var
if [ ! -f .env ]; then
    cp .env.example .env
    echo ""
    echo "  ⚠  A default .env was created at $INSTALL_DIR/.env"
    echo "     Edit it now (set SERVICE_API_KEY, TELEGRAM tokens, etc.) and re-run:"
    echo "       $0"
    exit 0
fi

# --- 5. Systemd service ----------------------------------------------------
echo "[5/5] Registering systemd service..."
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
sudo tee "$SERVICE_FILE" >/dev/null <<EOF
[Unit]
Description=Fable-Omega Multi-Tenant Bot Fleet Service
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$INSTALL_DIR
ExecStart=$INSTALL_DIR/.venv/bin/python $INSTALL_DIR/run.py --host 0.0.0.0 --port $PORT
Restart=always
RestartSec=5
EnvironmentFile=-$INSTALL_DIR/.env
Environment=PYTHONUNBUFFERED=1
Environment=MALLOC_TRIM_THRESHOLD_=100000

# Hardening
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=$INSTALL_DIR/data $INSTALL_DIR/var $INSTALL_DIR/artifacts
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_NAME"
sudo systemctl restart "$SERVICE_NAME"
sleep 3

# --- verify ----------------------------------------------------------------
echo ""
echo "============================================================"
echo "Verifying health probe..."
if curl -fsS "http://127.0.0.1:${PORT}/healthz" >/dev/null; then
    echo "✅ healthz OK"
else
    echo "⚠  healthz did not return 200 yet. Check logs:  journalctl -u $SERVICE_NAME -f"
fi
echo ""
echo "============================================================"
echo "✅ DEPLOYMENT COMPLETE"
echo "📊 Dashboard:       http://<VPS_IP>:${PORT}/"
echo "🔗 Health probe:    http://<VPS_IP>:${PORT}/healthz"
echo "📂 Working dir:     $INSTALL_DIR"
echo "🛠 Service name:    $SERVICE_NAME"
echo "📜 Logs:            sudo journalctl -u $SERVICE_NAME -f"
echo "============================================================"
