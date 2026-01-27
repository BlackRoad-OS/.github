# BlackRoad Nodes

> **The physical layer. Pi cluster + cloud endpoints.**

```
7 Nodes, 1 Mesh
Connected via Tailscale
```

---

## The Node Mesh

```
                         ┌─────────────────┐
                         │    INTERNET     │
                         └────────┬────────┘
                                  │
                         ┌────────┴────────┐
                         │   CLOUDFLARE    │
                         │    (edge)       │
                         └────────┬────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
     ┌────────┴────────┐ ┌───────┴───────┐ ┌────────┴────────┐
     │   SHELLFISH     │ │   TAILSCALE   │ │    CECILIA      │
     │   (gateway)     │ │    (mesh)     │ │    (dev)        │
     │   Cloud Worker  │ │               │ │   Local dev     │
     └────────┬────────┘ └───────┬───────┘ └─────────────────┘
              │                   │
              └─────────┬─────────┘
                        │
            ┌───────────┼───────────┐
            │           │           │
     ┌──────┴──────┐ ┌──┴──┐ ┌──────┴──────┐
     │  LUCIDIA    │ │     │ │   ARCADIA   │
     │  (primary)  │ │     │ │  (mobile)   │
     │  Pi 5 8GB   │ │     │ │   iPhone    │
     │  Hailo-8    │ │     │ └─────────────┘
     └──────┬──────┘ │     │
            │        │     │
     ┌──────┴──────┐ │     │
     │  OCTAVIA    │ │     │
     │  (compute)  │ │     │
     │  Pi 5 4GB   │ │     │
     │  Hailo-8    │ │     │
     └──────┬──────┘ │     │
            │        │     │
     ┌──────┴──────┐ │     │
     │   ARIA      │ │     │
     │  (storage)  │─┘     │
     │  Pi 5 4GB   │       │
     │  NVMe SSD   │       │
     └──────┬──────┘       │
            │              │
     ┌──────┴──────┐       │
     │   ALICE     │───────┘
     │  (agents)   │
     │  Pi 5 4GB   │
     │  Hailo-8    │
     └─────────────┘
```

---

## Node Registry

| Node | Type | Role | Hardware | Status |
|------|------|------|----------|--------|
| **lucidia** | Pi 5 | Primary | 8GB RAM, Hailo-8, NVMe | OFFLINE |
| **octavia** | Pi 5 | Compute | 4GB RAM, Hailo-8 | OFFLINE |
| **aria** | Pi 5 | Storage | 4GB RAM, 2TB NVMe | OFFLINE |
| **alice** | Pi 5 | Agents | 4GB RAM, Hailo-8 | OFFLINE |
| **shellfish** | Cloud | Gateway | CF Worker | OFFLINE |
| **cecilia** | Dev | Local | Laptop/Desktop | ACTIVE |
| **arcadia** | Mobile | Field | iPhone/iPad | OFFLINE |

---

## Services by Node

### lucidia (Primary)
```yaml
services:
  - blackroad-operator      # Main routing
  - blackroad-metrics       # KPI dashboard
  - tailscale-relay         # Mesh coordinator
  - hailo-inference         # Local AI (26 TOPS)
  - cloudflare-tunnel       # External access
```

### octavia (Compute)
```yaml
services:
  - hailo-inference         # AI processing
  - job-worker              # Background jobs
  - data-pipeline           # ETL processing
```

### aria (Storage)
```yaml
services:
  - minio                   # S3-compatible storage
  - postgres                # Database
  - redis                   # Cache
  - backup-agent            # Automated backups
```

### alice (Agents)
```yaml
services:
  - agent-runtime           # AI agent execution
  - hailo-inference         # Local AI
  - mcp-server              # Model Context Protocol
```

### shellfish (Gateway)
```yaml
services:
  - cloudflare-worker       # Edge routing
  - kv-cache                # Edge cache
  - d1-database             # Edge database
  - r2-storage              # Object storage
```

### cecilia (Dev)
```yaml
services:
  - local-dev               # Development environment
  - claude-code             # AI pair programming
  - bridge-cli              # Control plane
```

### arcadia (Mobile)
```yaml
services:
  - mobile-client           # iOS/Android app
  - push-notifications      # Alerts
  - offline-sync            # Local storage
```

---

## Network Configuration

### Tailscale Mesh
```
Network: blackroad-mesh
DNS: *.blackroad.ts.net

Hostnames:
  lucidia.blackroad.ts.net    100.x.x.1
  octavia.blackroad.ts.net    100.x.x.2
  aria.blackroad.ts.net       100.x.x.3
  alice.blackroad.ts.net      100.x.x.4
  shellfish.blackroad.ts.net  100.x.x.5
  cecilia.blackroad.ts.net    100.x.x.6
  arcadia.blackroad.ts.net    100.x.x.7
```

### Cloudflare Tunnels
```
Tunnel: blackroad-primary
  → lucidia:8080  (API)
  → lucidia:22    (SSH)

Tunnel: blackroad-storage
  → aria:9000     (Minio)
  → aria:5432     (Postgres)
```

---

## Quick Commands

```bash
# Check node status
./bridge status

# SSH to node
ssh pi@lucidia.blackroad.ts.net

# Deploy to node
./scripts/deploy.sh lucidia

# View node logs
ssh lucidia "journalctl -u blackroad-operator -f"

# Restart service
ssh lucidia "sudo systemctl restart blackroad-operator"
```

---

## Signals

```
🟢 HW → OS : node_online, node=lucidia
🔴 HW → OS : node_offline, node=octavia
📊 HW → OS : metrics_report, cpu=45%, mem=60%
🔄 HW → OS : service_restarted, node=aria, service=minio
```

---

*Hardware is the foundation. Software is the soul.*
