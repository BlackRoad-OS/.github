#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════
# BlackRoad Tunnel Manager CLI
# Manage all Cloudflare tunnels across the mesh from any node
#
# Usage:
#   ./tunnel-manager.sh status            — Show all tunnel statuses
#   ./tunnel-manager.sh health            — Deep health check all endpoints
#   ./tunnel-manager.sh restart <node>    — Restart a specific tunnel
#   ./tunnel-manager.sh restart-all       — Restart all tunnels
#   ./tunnel-manager.sh logs <node>       — Stream tunnel logs
#   ./tunnel-manager.sh connections       — Show active tunnel connections
#   ./tunnel-manager.sh dns-check         — Verify all DNS records resolve
#   ./tunnel-manager.sh metrics           — Show tunnel metrics
#   ./tunnel-manager.sh rotate <node>     — Rotate tunnel credentials
#   ./tunnel-manager.sh provision-dns     — Provision all DNS records via API
# ═══════════════════════════════════════════════════════════════════
set -euo pipefail

# ─── Configuration ───────────────────────────────────────────────
declare -A NODES=(
  [lucidia]="blackroad-primary"
  [aria]="blackroad-storage"
  [alice]="blackroad-agents"
  [octavia]="blackroad-compute"
)

declare -A NODE_IPS=(
  [lucidia]="lucidia.blackroad.ts.net"
  [aria]="aria.blackroad.ts.net"
  [alice]="alice.blackroad.ts.net"
  [octavia]="octavia.blackroad.ts.net"
)

# All domains we expect to be routable
DOMAINS=(
  # Primary (lucidia)
  "api.blackroad.ai"
  "metrics.blackroad.ai"
  "auth.blackroad.ai"
  "vault.blackroad.ai"
  "inference.blackroad.ai"
  "gov.blackroad.ai"
  "ssh.blackroad.ai"
  "prometheus.blackroad.ai"
  # Storage (aria)
  "storage.blackroad.ai"
  "storage-console.blackroad.ai"
  "gdrive.blackroad.ai"
  "backup.blackroad.ai"
  "db.blackroad.ai"
  "redis.blackroad.ai"
  # Agents (alice)
  "agents.blackroad.ai"
  "ai.blackroad.ai"
  "mcp.blackroad.ai"
  "hailo-alice.blackroad.ai"
  # Compute (octavia)
  "jobs.blackroad.ai"
  "content.blackroad.ai"
  "social.blackroad.ai"
  "game.blackroad.ai"
  "meta.blackroad.ai"
  "figma.blackroad.ai"
  "assets.blackroad.ai"
  "lab.blackroad.ai"
  # Edge
  "edge.blackroad.ai"
  "cdn.blackroad.ai"
  "learn.blackroad.ai"
  "docs.blackroad.ai"
)

# Health check endpoints (HTTP endpoints we can probe)
declare -A HEALTH_ENDPOINTS=(
  # Primary (lucidia)
  [api]="https://api.blackroad.ai/health"
  [metrics]="https://metrics.blackroad.ai/health"
  [auth]="https://auth.blackroad.ai/health"
  [inference]="https://inference.blackroad.ai/health"
  [gov]="https://gov.blackroad.ai/health"
  # Storage (aria)
  [storage]="https://storage.blackroad.ai/minio/health/live"
  [gdrive]="https://gdrive.blackroad.ai/health"
  [backup]="https://backup.blackroad.ai/health"
  # Agents (alice)
  [agents]="https://agents.blackroad.ai/health"
  [ai]="https://ai.blackroad.ai/health"
  [mcp]="https://mcp.blackroad.ai/health"
  # Compute (octavia)
  [jobs]="https://jobs.blackroad.ai/health"
  [content]="https://content.blackroad.ai/health"
  [social]="https://social.blackroad.ai/health"
  [game]="https://game.blackroad.ai/health"
  [figma]="https://figma.blackroad.ai/health"
  [assets]="https://assets.blackroad.ai/health"
  [lab]="https://lab.blackroad.ai/health"
  # Edge
  [edge]="https://edge.blackroad.ai/health"
)

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# ─── Commands ────────────────────────────────────────────────────

cmd_status() {
  echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
  echo -e "${CYAN}  BlackRoad Tunnel Mesh Status${NC}"
  echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
  echo ""

  for node in "${!NODES[@]}"; do
    tunnel="${NODES[$node]}"
    ip="${NODE_IPS[$node]}"

    # Check if node is reachable via Tailscale
    if ping -c 1 -W 2 "$ip" &>/dev/null; then
      node_status="${GREEN}reachable${NC}"
    else
      node_status="${RED}unreachable${NC}"
    fi

    # Check tunnel service (only works if running on that node)
    svc_status="${YELLOW}unknown${NC}"
    if systemctl is-active "cloudflared-${node}" &>/dev/null 2>&1; then
      svc_status="${GREEN}active${NC}"
    elif ssh -o ConnectTimeout=3 -o StrictHostKeyChecking=no "$ip" \
         "systemctl is-active cloudflared-${node}" 2>/dev/null | grep -q "active"; then
      svc_status="${GREEN}active${NC}"
    fi

    echo -e "  ${BLUE}${node}${NC} (${tunnel})"
    echo -e "    Tailscale:  $node_status"
    echo -e "    Tunnel svc: $svc_status"
    echo -e "    Hostname:   $ip"
    echo ""
  done
}

cmd_health() {
  echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
  echo -e "${CYAN}  Deep Health Check — All Tunnel Endpoints${NC}"
  echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
  echo ""

  local total=0
  local healthy=0
  local unhealthy=0
  local unreachable=0

  for name in $(echo "${!HEALTH_ENDPOINTS[@]}" | tr ' ' '\n' | sort); do
    url="${HEALTH_ENDPOINTS[$name]}"
    total=$((total + 1))

    status_code=$(curl -sf -o /dev/null -w "%{http_code}" --connect-timeout 5 --max-time 10 "$url" 2>/dev/null || echo "000")

    if [[ "$status_code" == "200" ]]; then
      echo -e "  ${GREEN}[OK]${NC}  ${name} → $url"
      healthy=$((healthy + 1))
    elif [[ "$status_code" == "000" ]]; then
      echo -e "  ${RED}[--]${NC}  ${name} → $url (unreachable)"
      unreachable=$((unreachable + 1))
    else
      echo -e "  ${YELLOW}[${status_code}]${NC} ${name} → $url"
      unhealthy=$((unhealthy + 1))
    fi
  done

  echo ""
  echo -e "  ────────────────────────────────────────"
  echo -e "  Total: $total | ${GREEN}Healthy: $healthy${NC} | ${YELLOW}Unhealthy: $unhealthy${NC} | ${RED}Unreachable: $unreachable${NC}"
  echo ""

  if [[ $unhealthy -gt 0 ]] || [[ $unreachable -gt 0 ]]; then
    return 1
  fi
}

cmd_restart() {
  local node="${1:-}"
  if [[ -z "$node" ]]; then
    echo "Usage: $0 restart <node>"
    echo "  Nodes: ${!NODES[*]}"
    exit 1
  fi

  local ip="${NODE_IPS[$node]:-}"
  if [[ -z "$ip" ]]; then
    echo "Unknown node: $node"
    exit 1
  fi

  echo -e "${CYAN}Restarting tunnel on ${node}...${NC}"

  # Try local first
  if systemctl is-active "cloudflared-${node}" &>/dev/null 2>&1; then
    systemctl restart "cloudflared-${node}"
    echo -e "  ${GREEN}Restarted locally${NC}"
  else
    echo "  Connecting to $ip via SSH..."
    ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no "$ip" \
      "sudo systemctl restart cloudflared-${node}" 2>/dev/null
    echo -e "  ${GREEN}Restarted remotely${NC}"
  fi

  sleep 2
  echo "  Checking status..."

  local svc_status
  svc_status=$(ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no "$ip" \
    "systemctl is-active cloudflared-${node}" 2>/dev/null || echo "unknown")
  echo -e "  Service: ${GREEN}${svc_status}${NC}"
}

cmd_restart_all() {
  echo -e "${CYAN}Restarting all tunnels...${NC}"
  echo ""
  for node in "${!NODES[@]}"; do
    cmd_restart "$node"
    echo ""
  done
}

cmd_logs() {
  local node="${1:-}"
  if [[ -z "$node" ]]; then
    echo "Usage: $0 logs <node>"
    echo "  Nodes: ${!NODES[*]}"
    exit 1
  fi

  local ip="${NODE_IPS[$node]:-}"
  if [[ -z "$ip" ]]; then
    echo "Unknown node: $node"
    exit 1
  fi

  echo -e "${CYAN}Streaming logs for cloudflared-${node}...${NC}"
  echo "  (Ctrl+C to stop)"
  echo ""

  # Try local first
  if systemctl is-active "cloudflared-${node}" &>/dev/null 2>&1; then
    journalctl -u "cloudflared-${node}" -f --no-pager
  else
    ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no "$ip" \
      "journalctl -u cloudflared-${node} -f --no-pager"
  fi
}

cmd_connections() {
  echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
  echo -e "${CYAN}  Active Tunnel Connections${NC}"
  echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
  echo ""

  for node in "${!NODES[@]}"; do
    tunnel="${NODES[$node]}"
    echo -e "  ${BLUE}${tunnel}${NC} (${node}):"

    # Try to get tunnel info from Cloudflare API
    if [[ -n "${CLOUDFLARE_API_TOKEN:-}" ]]; then
      curl -s "https://api.cloudflare.com/client/v4/accounts/${CLOUDFLARE_ACCOUNT_ID}/cfd_tunnel" \
        -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
        -H "Content-Type: application/json" 2>/dev/null | \
        python3 -c "
import sys, json
data = json.load(sys.stdin)
for t in data.get('result', []):
    if t['name'] == '$tunnel':
        conns = t.get('connections', [])
        print(f'    Status: {t[\"status\"]}')
        print(f'    ID: {t[\"id\"][:12]}...')
        for c in conns:
            print(f'    Connection: {c.get(\"colo_name\", \"?\")} ({c.get(\"origin_ip\", \"?\")})')
        break
" 2>/dev/null || echo "    (Could not fetch from API)"
    else
      echo "    Set CLOUDFLARE_API_TOKEN to see connection details"
    fi
    echo ""
  done
}

cmd_dns_check() {
  echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
  echo -e "${CYAN}  DNS Resolution Check — All Domains${NC}"
  echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
  echo ""

  local resolved=0
  local failed=0

  for domain in "${DOMAINS[@]}"; do
    result=$(dig +short "$domain" 2>/dev/null | head -1)
    if [[ -n "$result" ]]; then
      echo -e "  ${GREEN}[OK]${NC}  ${domain} → ${result}"
      resolved=$((resolved + 1))
    else
      echo -e "  ${RED}[--]${NC}  ${domain} (NXDOMAIN)"
      failed=$((failed + 1))
    fi
  done

  echo ""
  echo -e "  ────────────────────────────────────────"
  echo -e "  Total: ${#DOMAINS[@]} | ${GREEN}Resolved: $resolved${NC} | ${RED}Failed: $failed${NC}"
}

cmd_metrics() {
  echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
  echo -e "${CYAN}  Tunnel Metrics${NC}"
  echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
  echo ""

  for node in "${!NODES[@]}"; do
    tunnel="${NODES[$node]}"
    ip="${NODE_IPS[$node]}"

    echo -e "  ${BLUE}${node}${NC} (${tunnel}):"

    # Try to get metrics from the node's cloudflared metrics endpoint
    metrics_url="http://${ip}:2000/metrics"
    result=$(curl -s --connect-timeout 3 "$metrics_url" 2>/dev/null || echo "")

    if [[ -n "$result" ]]; then
      # Extract key metrics
      connections=$(echo "$result" | grep "cloudflared_tunnel_active_sessions" | tail -1 | awk '{print $2}' || echo "?")
      requests=$(echo "$result" | grep "cloudflared_tunnel_total_requests" | tail -1 | awk '{print $2}' || echo "?")
      errors=$(echo "$result" | grep "cloudflared_tunnel_request_errors" | tail -1 | awk '{print $2}' || echo "?")

      echo "    Active sessions:  $connections"
      echo "    Total requests:   $requests"
      echo "    Request errors:   $errors"
    else
      echo "    (Metrics endpoint not reachable)"
    fi
    echo ""
  done
}

cmd_rotate() {
  local node="${1:-}"
  if [[ -z "$node" ]]; then
    echo "Usage: $0 rotate <node>"
    exit 1
  fi

  local tunnel="${NODES[$node]:-}"
  if [[ -z "$tunnel" ]]; then
    echo "Unknown node: $node"
    exit 1
  fi

  echo -e "${YELLOW}Rotating credentials for tunnel: $tunnel ($node)${NC}"
  echo ""
  echo "  This will:"
  echo "  1. Generate new tunnel token"
  echo "  2. Deploy to node"
  echo "  3. Restart tunnel service"
  echo ""
  read -p "  Continue? [y/N] " -n 1 -r
  echo ""

  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "  Aborted."
    exit 0
  fi

  echo "  Generating new token..."
  NEW_TOKEN=$(cloudflared tunnel token "$tunnel" 2>/dev/null || echo "")

  if [[ -z "$NEW_TOKEN" ]]; then
    echo -e "  ${RED}Failed to generate token. Run 'cloudflared tunnel login' first.${NC}"
    exit 1
  fi

  local ip="${NODE_IPS[$node]}"
  echo "  Deploying to $ip..."
  ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no "$ip" \
    "sudo cloudflared service install $NEW_TOKEN" 2>/dev/null

  echo "  Restarting tunnel..."
  cmd_restart "$node"

  echo -e "  ${GREEN}Credentials rotated successfully${NC}"
}

cmd_provision_dns() {
  echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
  echo -e "${CYAN}  Provision DNS Records via Cloudflare API${NC}"
  echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
  echo ""

  if [[ -z "${CLOUDFLARE_API_TOKEN:-}" ]] || [[ -z "${CLOUDFLARE_ZONE_ID:-}" ]]; then
    echo "  Required environment variables:"
    echo "    CLOUDFLARE_API_TOKEN"
    echo "    CLOUDFLARE_ZONE_ID"
    echo ""
    echo "  Get zone ID: curl -s 'https://api.cloudflare.com/client/v4/zones' \\"
    echo "    -H 'Authorization: Bearer \$CLOUDFLARE_API_TOKEN' | jq '.result[] | {name, id}'"
    exit 1
  fi

  CF_API="https://api.cloudflare.com/client/v4/zones/${CLOUDFLARE_ZONE_ID}/dns_records"

  # DNS records to provision (name → target)
  declare -A DNS_RECORDS=(
    # Primary tunnel
    [api]="blackroad-primary.cfargotunnel.com"
    [metrics]="blackroad-primary.cfargotunnel.com"
    [auth]="blackroad-primary.cfargotunnel.com"
    [vault]="blackroad-primary.cfargotunnel.com"
    [inference]="blackroad-primary.cfargotunnel.com"
    [gov]="blackroad-primary.cfargotunnel.com"
    [ssh]="blackroad-primary.cfargotunnel.com"
    [prometheus]="blackroad-primary.cfargotunnel.com"
    # Storage tunnel
    [storage]="blackroad-storage.cfargotunnel.com"
    [storage-console]="blackroad-storage.cfargotunnel.com"
    [gdrive]="blackroad-storage.cfargotunnel.com"
    [backup]="blackroad-storage.cfargotunnel.com"
    [db]="blackroad-storage.cfargotunnel.com"
    [redis]="blackroad-storage.cfargotunnel.com"
    # Agents tunnel
    [agents]="blackroad-agents.cfargotunnel.com"
    [ai]="blackroad-agents.cfargotunnel.com"
    [mcp]="blackroad-agents.cfargotunnel.com"
    [hailo-alice]="blackroad-agents.cfargotunnel.com"
    # Compute tunnel
    [jobs]="blackroad-compute.cfargotunnel.com"
    [content]="blackroad-compute.cfargotunnel.com"
    [social]="blackroad-compute.cfargotunnel.com"
    [game]="blackroad-compute.cfargotunnel.com"
    [meta]="blackroad-compute.cfargotunnel.com"
    [figma]="blackroad-compute.cfargotunnel.com"
    [assets]="blackroad-compute.cfargotunnel.com"
    [lab]="blackroad-compute.cfargotunnel.com"
    # Edge
    [edge]="blackroad-api-gateway.workers.dev"
    [cdn]="blackroad-assets.r2.dev"
    # Education
    [learn]="blackroad-storage.cfargotunnel.com"
    [docs]="blackroad-storage.cfargotunnel.com"
    # SSH nodes
    [ssh-aria]="blackroad-storage.cfargotunnel.com"
    [ssh-alice]="blackroad-agents.cfargotunnel.com"
    [ssh-octavia]="blackroad-compute.cfargotunnel.com"
    # Metrics nodes
    [aria-metrics]="blackroad-storage.cfargotunnel.com"
    [alice-metrics]="blackroad-agents.cfargotunnel.com"
    [octavia-metrics]="blackroad-compute.cfargotunnel.com"
  )

  local created=0
  local updated=0
  local failed=0

  for name in $(echo "${!DNS_RECORDS[@]}" | tr ' ' '\n' | sort); do
    target="${DNS_RECORDS[$name]}"
    fqdn="${name}.blackroad.ai"

    # Non-proxied records
    proxied="true"
    if [[ "$name" == "prometheus" ]] || [[ "$name" == *"-metrics"* ]]; then
      proxied="false"
    fi

    # Check if record exists
    existing=$(curl -s "${CF_API}?name=${fqdn}&type=CNAME" \
      -H "Authorization: Bearer ${CLOUDFLARE_API_TOKEN}" \
      -H "Content-Type: application/json" 2>/dev/null)

    record_id=$(echo "$existing" | python3 -c "
import sys, json
data = json.load(sys.stdin)
results = data.get('result', [])
print(results[0]['id'] if results else '')
" 2>/dev/null || echo "")

    if [[ -n "$record_id" ]]; then
      # Update existing
      result=$(curl -s -X PUT "${CF_API}/${record_id}" \
        -H "Authorization: Bearer ${CLOUDFLARE_API_TOKEN}" \
        -H "Content-Type: application/json" \
        --data "{\"type\":\"CNAME\",\"name\":\"${name}\",\"content\":\"${target}\",\"proxied\":${proxied}}" 2>/dev/null)

      if echo "$result" | python3 -c "import sys,json; sys.exit(0 if json.load(sys.stdin).get('success') else 1)" 2>/dev/null; then
        echo -e "  ${YELLOW}[UPD]${NC} ${fqdn} → ${target}"
        updated=$((updated + 1))
      else
        echo -e "  ${RED}[ERR]${NC} ${fqdn}: Failed to update"
        failed=$((failed + 1))
      fi
    else
      # Create new
      result=$(curl -s -X POST "${CF_API}" \
        -H "Authorization: Bearer ${CLOUDFLARE_API_TOKEN}" \
        -H "Content-Type: application/json" \
        --data "{\"type\":\"CNAME\",\"name\":\"${name}\",\"content\":\"${target}\",\"proxied\":${proxied}}" 2>/dev/null)

      if echo "$result" | python3 -c "import sys,json; sys.exit(0 if json.load(sys.stdin).get('success') else 1)" 2>/dev/null; then
        echo -e "  ${GREEN}[NEW]${NC} ${fqdn} → ${target}"
        created=$((created + 1))
      else
        echo -e "  ${RED}[ERR]${NC} ${fqdn}: Failed to create"
        failed=$((failed + 1))
      fi
    fi
  done

  echo ""
  echo -e "  ────────────────────────────────────────"
  echo -e "  ${GREEN}Created: $created${NC} | ${YELLOW}Updated: $updated${NC} | ${RED}Failed: $failed${NC}"
}

cmd_help() {
  echo "BlackRoad Tunnel Manager"
  echo ""
  echo "Usage: $0 <command> [args]"
  echo ""
  echo "Commands:"
  echo "  status              Show all tunnel statuses"
  echo "  health              Deep health check all endpoints"
  echo "  restart <node>      Restart a specific tunnel"
  echo "  restart-all         Restart all tunnels"
  echo "  logs <node>         Stream tunnel logs"
  echo "  connections         Show active tunnel connections"
  echo "  dns-check           Verify all DNS records resolve"
  echo "  metrics             Show tunnel metrics"
  echo "  rotate <node>       Rotate tunnel credentials"
  echo "  provision-dns       Provision all DNS records via API"
  echo ""
  echo "Nodes: lucidia, aria, alice, octavia"
}

# ─── Dispatch ────────────────────────────────────────────────────
COMMAND="${1:-help}"
shift || true

case "$COMMAND" in
  status)        cmd_status ;;
  health)        cmd_health ;;
  restart)       cmd_restart "$@" ;;
  restart-all)   cmd_restart_all ;;
  logs)          cmd_logs "$@" ;;
  connections)   cmd_connections ;;
  dns-check)     cmd_dns_check ;;
  metrics)       cmd_metrics ;;
  rotate)        cmd_rotate "$@" ;;
  provision-dns) cmd_provision_dns ;;
  help|--help|-h) cmd_help ;;
  *) echo "Unknown command: $COMMAND"; cmd_help; exit 1 ;;
esac
