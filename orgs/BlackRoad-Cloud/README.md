# BlackRoad-Cloud Blueprint

> **The Edge Layer**
> Code: `CLD`

---

## Mission

Deploy everywhere. Run at the edge. Zero cold starts.

```
[Request] → [Cloudflare Edge] → [Worker] → [Response in <50ms]
```

---

## Core Principle

**The edge is the new server.**

- Cloudflare has 300+ data centers worldwide
- Code runs within 50ms of every human on Earth
- We don't manage servers, we deploy functions
- Workers = serverless done right

---

## What Lives Here

| Repo | Purpose | Priority |
|------|---------|----------|
| `workers` | Cloudflare Workers code | P0 |
| `deploy` | Deployment configs, CI/CD pipelines | P0 |
| `api` | Public API gateway definitions | P1 |
| `dns` | DNS configs, routing rules | P1 |
| `tunnel` | Cloudflare Tunnel configs (to Pi mesh) | P1 |
| `pages` | Static site deployments | P2 |

---

## Architecture

```
                    CLOUDFLARE EDGE (300+ locations)
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
         ▼                    ▼                    ▼
    ┌─────────┐         ┌─────────┐         ┌─────────┐
    │ Worker  │         │ Worker  │         │  Pages  │
    │  API    │         │ Router  │         │ Static  │
    └────┬────┘         └────┬────┘         └─────────┘
         │                   │
         │    Cloudflare Tunnel (encrypted)
         │                   │
         └───────────────────┼───────────────────┐
                             ▼                   │
                    ┌─────────────┐              │
                    │   alice     │              │
                    │  (K8s hub)  │              │
                    └──────┬──────┘              │
                           │                     │
         ┌─────────────────┼─────────────────┐   │
         ▼                 ▼                 ▼   │
    ┌─────────┐      ┌─────────┐      ┌─────────┐
    │ lucidia │      │ octavia │      │  aria   │
    │ SF/Chain│      │  Hailo  │      │ Agents  │
    └─────────┘      └─────────┘      └─────────┘
```

---

## Workers Strategy

| Worker | Purpose | Route |
|--------|---------|-------|
| `gateway` | Main API entry point | `api.blackroad.dev/*` |
| `router` | Route to right backend | Internal |
| `auth` | Authentication/JWT | `auth.blackroad.dev/*` |
| `static` | Serve static assets | `cdn.blackroad.dev/*` |
| `websocket` | Real-time connections | `ws.blackroad.dev/*` |

---

## Integration Points

### Upstream (receives from)
- Users (direct requests)
- External webhooks
- Third-party APIs

### Downstream (sends to)
- `OS` - Routes to operator
- `AI` - AI requests go to router
- Pi mesh via Tunnel

### Signals
```
🎯 OS → CLD : Deploy this worker
✔️ CLD → OS : Deployed to edge
⚠️ CLD → OS : Rate limit warning
📡 CLD → ALL : Edge status update
```

---

## Deployment Flow

```
git push → GitHub Actions → Wrangler → Cloudflare Edge
                                           │
                                           ▼
                                    Live in <30 seconds
                                    at 300+ locations
```

---

## Cost Model

| Resource | Free Tier | Paid |
|----------|-----------|------|
| Workers requests | 100K/day | $5/10M |
| KV storage | 1GB | $0.50/GB |
| Durable Objects | - | $0.15/GB |
| Tunnels | Unlimited | Free |

**Target:** Stay in free tier as long as possible.

---

*The edge is everywhere. So are we.*
