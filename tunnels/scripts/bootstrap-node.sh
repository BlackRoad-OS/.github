#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════
# BlackRoad Node Bootstrap Script
# Installs cloudflared + tailscale, provisions tunnel, starts services
#
# Usage:
#   sudo ./bootstrap-node.sh <node-name>
#   sudo ./bootstrap-node.sh lucidia
#   sudo ./bootstrap-node.sh aria
#   sudo ./bootstrap-node.sh alice
#   sudo ./bootstrap-node.sh octavia
# ═══════════════════════════════════════════════════════════════════
set -euo pipefail

# ─── Validation ──────────────────────────────────────────────────
NODE_NAME="${1:-}"
if [[ -z "$NODE_NAME" ]]; then
  echo "Usage: $0 <node-name>"
  echo "  Nodes: lucidia, aria, alice, octavia, arcadia, cecilia"
  exit 1
fi

# Map node → tunnel name
declare -A TUNNEL_MAP=(
  [lucidia]=blackroad-primary
  [aria]=blackroad-storage
  [alice]=blackroad-agents
  [octavia]=blackroad-compute
)

TUNNEL_NAME="${TUNNEL_MAP[$NODE_NAME]:-}"
if [[ -z "$TUNNEL_NAME" ]]; then
  echo "Warning: No Cloudflare tunnel defined for node '$NODE_NAME'"
  echo "  Will install tailscale only."
fi

ARCH=$(dpkg --print-architecture 2>/dev/null || uname -m)
case "$ARCH" in
  aarch64|arm64) CF_ARCH="arm64" ;;
  x86_64|amd64)  CF_ARCH="amd64" ;;
  armhf|armv7l)  CF_ARCH="arm"   ;;
  *) echo "Unsupported architecture: $ARCH"; exit 1 ;;
esac

echo "═══════════════════════════════════════════════════════════════"
echo "  BlackRoad Node Bootstrap"
echo "  Node:    $NODE_NAME"
echo "  Tunnel:  ${TUNNEL_NAME:-none}"
echo "  Arch:    $ARCH ($CF_ARCH)"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# ─── 1. System update ────────────────────────────────────────────
echo "[1/7] Updating system packages..."
apt-get update -qq
apt-get upgrade -y -qq

# ─── 2. Install cloudflared ──────────────────────────────────────
echo "[2/7] Installing cloudflared..."
if ! command -v cloudflared &>/dev/null; then
  curl -sL "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-${CF_ARCH}" \
    -o /usr/local/bin/cloudflared
  chmod +x /usr/local/bin/cloudflared
  echo "  Installed: $(cloudflared --version)"
else
  echo "  Already installed: $(cloudflared --version)"
fi

# ─── 3. Install Tailscale ───────────────────────────────────────
echo "[3/7] Installing Tailscale..."
if ! command -v tailscale &>/dev/null; then
  curl -fsSL https://tailscale.com/install.sh | sh
  echo "  Installed: $(tailscale --version)"
else
  echo "  Already installed: $(tailscale --version)"
fi

# ─── 4. Configure Tailscale ─────────────────────────────────────
echo "[4/7] Configuring Tailscale..."
TAILSCALE_ARGS="--hostname=${NODE_NAME}"

# Node-specific Tailscale options
case "$NODE_NAME" in
  lucidia)
    TAILSCALE_ARGS+=" --advertise-routes=192.168.1.0/24 --accept-dns=false"
    ;;
esac

if tailscale status &>/dev/null; then
  echo "  Tailscale already connected"
  tailscale status | head -5
else
  echo "  Starting Tailscale..."
  echo "  Run manually: tailscale up $TAILSCALE_ARGS"
  echo "  (Requires interactive auth key or pre-auth key)"

  if [[ -n "${TAILSCALE_AUTHKEY:-}" ]]; then
    tailscale up --authkey="$TAILSCALE_AUTHKEY" $TAILSCALE_ARGS
    echo "  Connected via auth key"
  else
    echo "  Set TAILSCALE_AUTHKEY env var or run: tailscale up $TAILSCALE_ARGS"
  fi
fi

# ─── 5. Configure Cloudflare Tunnel ─────────────────────────────
if [[ -n "$TUNNEL_NAME" ]]; then
  echo "[5/7] Configuring Cloudflare Tunnel: $TUNNEL_NAME..."

  CRED_DIR="/etc/cloudflared"
  mkdir -p "$CRED_DIR"

  CONFIG_SRC="$(dirname "$0")/../cloudflared-${NODE_NAME}.yaml"
  CONFIG_DST="${CRED_DIR}/${NODE_NAME}.yaml"

  if [[ -f "$CONFIG_SRC" ]]; then
    cp "$CONFIG_SRC" "$CONFIG_DST"
    echo "  Config installed: $CONFIG_DST"
  else
    echo "  Warning: Config not found at $CONFIG_SRC"
    echo "  You'll need to copy the config manually."
  fi

  # Check for credentials
  CRED_FILE="${CRED_DIR}/${TUNNEL_NAME}.json"
  if [[ -f "$CRED_FILE" ]]; then
    echo "  Credentials found: $CRED_FILE"
  else
    echo "  No credentials found at $CRED_FILE"
    echo "  Run: cloudflared tunnel login"
    echo "  Then: cloudflared tunnel create $TUNNEL_NAME"
    echo "  This creates the credentials file automatically."

    if cloudflared tunnel list 2>/dev/null | grep -q "$TUNNEL_NAME"; then
      echo "  Tunnel '$TUNNEL_NAME' exists in Cloudflare. Fetching credentials..."
      # The credentials file should already exist if tunnel was created here
    fi
  fi

  # Install systemd service
  echo "  Installing systemd service..."
  cat > "/etc/systemd/system/cloudflared-${NODE_NAME}.service" << SYSTEMD
[Unit]
Description=Cloudflare Tunnel - ${NODE_NAME} (${TUNNEL_NAME})
After=network-online.target tailscaled.service
Wants=network-online.target

[Service]
Type=notify
ExecStart=/usr/local/bin/cloudflared tunnel --config ${CONFIG_DST} --no-autoupdate run
Restart=always
RestartSec=5
StartLimitInterval=0

# Security hardening
User=root
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=/etc/cloudflared /var/log
PrivateTmp=true

# Logging
StandardOutput=journal
StandardError=journal
SyslogIdentifier=cloudflared-${NODE_NAME}

# Resource limits
LimitNOFILE=65535
TimeoutStartSec=30
WatchdogSec=60

[Install]
WantedBy=multi-user.target
SYSTEMD

  systemctl daemon-reload
  echo "  Service installed: cloudflared-${NODE_NAME}.service"
else
  echo "[5/7] Skipping Cloudflare Tunnel (no tunnel for this node)"
fi

# ─── 6. Configure logrotate ─────────────────────────────────────
echo "[6/7] Configuring log rotation..."
cat > "/etc/logrotate.d/cloudflared" << LOGROTATE
/var/log/cloudflared/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0640 root root
}
LOGROTATE

mkdir -p /var/log/cloudflared

# ─── 7. Create management symlinks ──────────────────────────────
echo "[7/7] Creating management utilities..."

# Quick-status script
cat > "/usr/local/bin/tunnel-status" << 'SCRIPT'
#!/usr/bin/env bash
echo "═══════════════════════════════════════════"
echo "  BlackRoad Tunnel Status"
echo "═══════════════════════════════════════════"
echo ""
echo "── Cloudflare Tunnel ──"
systemctl is-active cloudflared-* 2>/dev/null || echo "  No tunnel service found"
for svc in /etc/systemd/system/cloudflared-*.service; do
  [ -f "$svc" ] || continue
  name=$(basename "$svc" .service)
  status=$(systemctl is-active "$name" 2>/dev/null || echo "inactive")
  echo "  $name: $status"
done
echo ""
echo "── Tailscale ──"
tailscale status 2>/dev/null || echo "  Not connected"
echo ""
echo "── Connections ──"
cloudflared tunnel info 2>/dev/null | head -10 || echo "  No active tunnel info"
SCRIPT
chmod +x /usr/local/bin/tunnel-status

# Quick-restart script
cat > "/usr/local/bin/tunnel-restart" << 'SCRIPT'
#!/usr/bin/env bash
echo "Restarting tunnel services..."
for svc in /etc/systemd/system/cloudflared-*.service; do
  [ -f "$svc" ] || continue
  name=$(basename "$svc" .service)
  echo "  Restarting $name..."
  systemctl restart "$name"
done
echo "Done. Status:"
tunnel-status
SCRIPT
chmod +x /usr/local/bin/tunnel-restart

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  Bootstrap Complete!"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "  Next steps:"
echo ""

if [[ -n "$TUNNEL_NAME" ]]; then
  if [[ ! -f "${CRED_DIR}/${TUNNEL_NAME}.json" ]]; then
    echo "  1. Authenticate:  cloudflared tunnel login"
    echo "  2. Create tunnel: cloudflared tunnel create $TUNNEL_NAME"
    echo "  3. Start tunnel:  systemctl enable --now cloudflared-${NODE_NAME}"
  else
    echo "  1. Start tunnel:  systemctl enable --now cloudflared-${NODE_NAME}"
  fi
fi

echo "  Check status:     tunnel-status"
echo "  View logs:        journalctl -u cloudflared-${NODE_NAME} -f"
echo ""
