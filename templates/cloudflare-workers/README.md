# Cloudflare Workers

> **Edge compute. 300+ locations. Milliseconds from users.**
> **Now with full API gateway, tunnels to every node, and the complete Cloudflare platform.**

```
Org: BlackRoad-Cloud (CLD)
Node: shellfish (gateway)
Runtime: V8 Isolates
Latency: <50ms worldwide
Workers: 4 (api-gateway, webhook-receiver, asset-proxy, cron-worker)
Tunnels: 4 (lucidia, aria, alice, octavia)
```

---

## Architecture

```
                              ┌──────────────────────────────────────────┐
                              │        Cloudflare Edge (300+ PoPs)       │
┌───────────┐                 │                                          │
│   User    │ ──── HTTPS ───→ │  ┌────────────────────────────────────┐  │
│ (anywhere)│                 │  │     blackroad-api-gateway Worker   │  │
└───────────┘                 │  │                                    │  │
                              │  │  ┌──────┐ ┌──────┐ ┌───────────┐  │  │
┌───────────┐                 │  │  │ Auth │ │ Rate │ │  Routing  │  │  │
│ WebSocket │ ──── WSS ────→  │  │  │ JWT  │ │Limit │ │ Classify  │  │  │
│  Client   │                 │  │  └──────┘ └──────┘ └───────────┘  │  │
└───────────┘                 │  └──────────────┬─────────────────────┘  │
                              │                 │                        │
                              │  ┌──────────────┴─────────────────────┐  │
                              │  │         Edge Services              │  │
                              │  │  KV   D1   R2   AI   Queues       │  │
                              │  │  Vectorize   Durable Objects       │  │
                              │  │  Analytics Engine                  │  │
                              │  └──────────────┬─────────────────────┘  │
                              └─────────────────┼────────────────────────┘
                                                │
                          ┌─────────────────────┼─────────────────────┐
                          │        Cloudflare Tunnels (4)             │
                          │                                           │
                ┌─────────┴──────┐  ┌──────────┴──┐  ┌──────┴──────┐
                │  blackroad-    │  │  blackroad-  │  │  blackroad- │
                │  primary       │  │  storage     │  │  agents     │  ...
                └───────┬────────┘  └──────┬───────┘  └──────┬──────┘
                        │                  │                  │
          ┌─────────────┴────┐    ┌────────┴──────┐   ┌──────┴───────┐
          │    lucidia       │    │     aria      │   │    alice     │
          │  (primary)       │    │  (storage)    │   │  (agents)   │
          │                  │    │               │   │             │
          │  Operator  8080  │    │  MinIO  9000  │   │ Agents 8082 │
          │  Metrics   9090  │    │  PG     5432  │   │ AI     8080 │
          │  Auth      8087  │    │  Redis  6379  │   │ MCP    8083 │
          │  Vault     8200  │    │  GDrive 8097  │   │ Hailo  5000 │
          │  Hailo     5000  │    │  Backup 8098  │   └─────────────┘
          │  Sensors   8085  │    └───────────────┘
          │  Mesh      8086  │
          │  SF        8091  │    ┌───────────────┐
          │  Stripe    8092  │    │   octavia     │
          │  Gov       8096  │    │  (compute)    │
          │  Portfolio 8101  │    │               │
          │  Enterprise8102  │    │  Jobs    8081 │
          └──────────────────┘    │  Content 8093 │
                                  │  Social  8094 │
            ← Tailscale Mesh →    │  Game    8095 │
                                  │  Figma   8099 │
                                  │  Assets  8100 │
                                  │  Lab     8090 │
                                  └───────────────┘
```

---

## What's Included

| Component | Description | Count |
|-----------|-------------|-------|
| **Workers** | Edge compute functions | 4 |
| **KV** | Key-value namespaces | 5 |
| **D1** | SQLite database tables | 9 |
| **R2** | Object storage buckets | 2 |
| **Queues** | Async message queues | 4 |
| **Durable Objects** | Stateful edge actors | 3 |
| **Vectorize** | Vector search index | 1 |
| **Analytics Engine** | Request-level analytics | 1 |
| **Workers AI** | LLM, embeddings, classification | 3 models |
| **Tunnels** | Secure origin connections | 4 |
| **Domains** | Routed subdomains | 30+ |

---

## Quick Start

```bash
# Install Wrangler CLI
npm install -g wrangler

# Login
wrangler login

# Clone the worker
cd workers/api-gateway

# Develop locally
wrangler dev

# Deploy to staging
wrangler deploy --env staging

# Deploy to production
wrangler deploy
```

---

## Worker Directory

```
workers/
└── api-gateway/
    ├── src/
    │   └── index.ts         ← Full API gateway (auth, rate limit, routing, proxy)
    ├── wrangler.toml        ← All bindings (KV, D1, R2, AI, Queues, DO, Vectorize)
    ├── schema.sql           ← D1 database schema (9 tables)
    └── openapi.yaml         ← OpenAPI 3.1 spec (all endpoints)

tunnels/
├── cloudflared-lucidia.yaml  ← Primary node tunnel (15 services)
├── cloudflared-aria.yaml     ← Storage node tunnel (7 services)
├── cloudflared-alice.yaml    ← Agent node tunnel (7 services)
├── cloudflared-octavia.yaml  ← Compute node tunnel (11 services)
└── mesh-topology.yaml        ← Full mesh topology + DNS mapping
```

---

## API Endpoints

### Public (No Auth)
| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Edge health check (KV, D1, R2) |
| GET | `/v1/status` | Full system + node status |
| POST | `/v1/auth/login` | Login → JWT token |
| POST | `/v1/auth/register` | Register new user |
| POST | `/v1/auth/refresh` | Refresh JWT token |

### Webhooks (Signature-Verified)
| Method | Path | Source |
|--------|------|--------|
| POST | `/v1/webhooks/github` | X-Hub-Signature-256 |
| POST | `/v1/webhooks/stripe` | Stripe-Signature |
| POST | `/v1/webhooks/salesforce` | - |
| POST | `/v1/webhooks/slack` | - |
| POST | `/v1/webhooks/cloudflare` | - |
| POST | `/v1/webhooks/figma` | - |
| POST | `/v1/webhooks/google` | - |

### AI (Authenticated)
| Method | Path | Description |
|--------|------|-------------|
| POST | `/v1/ai/complete` | Text completion (Llama 3.1) |
| POST | `/v1/ai/embed` | Text → vector embeddings |
| POST | `/v1/ai/classify` | Text classification |
| GET/POST | `/v1/ai/agents` | Autonomous agent management |

### Edge Data (Authenticated)
| Method | Path | Service |
|--------|------|---------|
| GET/PUT/DELETE | `/v1/kv/{key}` | KV Store |
| GET/POST | `/v1/db/{table}` | D1 Database |
| GET/PUT/DELETE/HEAD | `/v1/storage/{key}` | R2 Storage |
| POST | `/v1/vectorize` | Vector search |

### Org Proxies (Authenticated → Tunnel → Origin)
| Path | Tunnel | Origin |
|------|--------|--------|
| `/v1/hw/*` | blackroad-primary | lucidia |
| `/v1/sec/*` | blackroad-primary | lucidia |
| `/v1/fnd/*` | blackroad-primary | lucidia |
| `/v1/gov/*` | blackroad-primary | lucidia |
| `/v1/ven/*` | blackroad-primary | lucidia |
| `/v1/bbx/*` | blackroad-primary | lucidia |
| `/v1/med/*` | blackroad-compute | octavia |
| `/v1/int/*` | blackroad-compute | octavia |
| `/v1/stu/*` | blackroad-compute | octavia |
| `/v1/lab/*` | blackroad-compute | octavia |
| `/v1/edu/*` | blackroad-storage | aria |
| `/v1/arc/*` | blackroad-storage | aria |

### WebSocket
| Path | Description |
|------|-------------|
| `wss://api.blackroad.ai/ws?room=signals` | Real-time signal stream |

---

## Authentication

Three methods supported:

```bash
# 1. JWT Bearer Token
curl -H "Authorization: Bearer <token>" https://api.blackroad.ai/v1/ai/complete

# 2. API Key
curl -H "X-API-Key: <key>" https://api.blackroad.ai/v1/ai/complete

# 3. Session Cookie (browser)
curl -b "session_id=<id>" https://api.blackroad.ai/v1/ai/complete
```

---

## Tunnels

4 Cloudflare Tunnels connecting edge to Pi cluster:

```
blackroad-primary  → lucidia  (15 services, 8 domains)
blackroad-storage  → aria     (7 services, 6 domains)
blackroad-agents   → alice    (7 services, 4 domains)
blackroad-compute  → octavia  (11 services, 8 domains)
```

### Setup a tunnel:

```bash
# On the Pi node
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64 \
  -o /usr/local/bin/cloudflared && chmod +x /usr/local/bin/cloudflared

# Authenticate
cloudflared tunnel login

# Create
cloudflared tunnel create blackroad-primary

# Run with config
cloudflared tunnel --config /etc/cloudflared/lucidia.yaml run

# Enable as systemd service
cloudflared service install
systemctl enable --now cloudflared
```

---

## Durable Objects

| Object | Purpose |
|--------|---------|
| `RateLimiter` | Per-key sliding window rate limiting (1000 req/min) |
| `SessionManager` | Server-side session store with strong consistency |
| `WebSocketRoom` | Real-time signal broadcasting via rooms |

---

## Queues

| Queue | Purpose | Batch |
|-------|---------|-------|
| `blackroad-webhooks` | Inbound webhook processing | 10 / 30s |
| `blackroad-analytics` | Request analytics events | 50 / 60s |
| `blackroad-signals` | Inter-org signal fanout | 10 / 10s |
| `blackroad-dlq` | Dead letter (failed messages) | 10 / 300s |

---

## Scheduled Tasks (CRON)

| Schedule | Task |
|----------|------|
| `*/5 * * * *` | Health check all 4 nodes |
| `0 * * * *` | Hourly metrics aggregation |
| `0 0 * * *` | Daily API key rotation |

---

## Edge Services

### KV (5 Namespaces)
```typescript
// CACHE — API response cache (TTL: 1h)
await env.CACHE.put("user:123", JSON.stringify(data), { expirationTtl: 3600 });
const user = await env.CACHE.get("user:123", "json");

// SESSIONS — User sessions (TTL: 24h)
// RATE_LIMITS — Rate limiting counters (TTL: 60s)
// CONFIG — Dynamic configuration (persistent)
// API_KEYS — API key store (persistent)
```

### D1 (9 Tables)
```sql
-- users, sessions, api_keys, signals, audit_log,
-- routing_rules, webhooks, node_health, metrics_hourly
SELECT * FROM signals ORDER BY created_at DESC LIMIT 50;
```

### R2 (2 Buckets)
```typescript
// blackroad-assets — Public CDN (cdn.blackroad.ai)
await env.ASSETS.put("files/doc.pdf", fileData);

// blackroad-uploads — Private user uploads
await env.UPLOADS.put("user/123/photo.jpg", imageData);
```

### Workers AI
```typescript
// Text completion
const result = await env.AI.run("@cf/meta/llama-3.1-8b-instruct", {
  messages: [{ role: "user", content: prompt }],
});

// Embeddings
const vectors = await env.AI.run("@cf/baai/bge-base-en-v1.5", {
  text: ["Document to embed"],
});

// Classification
const label = await env.AI.run("@cf/huggingface/distilbert-sst-2-int8", {
  text: "Classify this text",
});
```

### Vectorize
```typescript
// Upsert vectors
await env.VECTORIZE.upsert([{ id: "doc-1", values: [...], metadata: { title: "Doc" } }]);

// Query similar
const matches = await env.VECTORIZE.query(queryVector, { topK: 10 });
```

---

## Deployment

```bash
# Deploy all workers (staging)
gh workflow run deploy-worker.yml -f worker=all -f environment=staging

# Deploy single worker (production)
gh workflow run deploy-worker.yml -f worker=api-gateway -f environment=production

# Deploy with canary rollout (10% → monitor → 100%)
gh workflow run deploy-worker.yml -f worker=all -f environment=production -f canary=true
```

---

## CLI Commands

```bash
# Worker operations
wrangler dev                    # Local development
wrangler deploy                 # Deploy to production
wrangler tail                   # Stream live logs
wrangler deploy --env staging   # Deploy to staging

# KV operations
wrangler kv:key put --binding=CACHE "key" "value"
wrangler kv:key get --binding=CACHE "key"
wrangler kv:key list --binding=CACHE --prefix="user:"

# D1 operations
wrangler d1 execute blackroad --file=./schema.sql
wrangler d1 execute blackroad --command "SELECT * FROM users"

# R2 operations
wrangler r2 object put blackroad-assets/file.txt --file=./file.txt
wrangler r2 object get blackroad-assets/file.txt

# Queue operations
wrangler queues list

# Secrets
wrangler secret put JWT_SECRET
wrangler secret put STRIPE_WEBHOOK_SECRET
wrangler secret put GITHUB_WEBHOOK_SECRET

# Tunnel status
cloudflared tunnel info blackroad-primary
cloudflared tunnel list
```

---

## Signals

```
🚀 CLD → OS : worker_deployed, worker=api-gateway, version=v2.0.0
🌐 CLD → OS : request_routed, path=/v1/ai/complete, edge=SFO
📡 CLD → OS : webhook_received, source=github
⚠️ CLD → OS : rate_limited, ip=x.x.x.x, blocked=true
📊 CLD → OS : traffic_report, requests=1M, p50=12ms, p99=45ms
🔄 CLD → OS : tunnel_status, tunnel=blackroad-primary, status=healthy
🧠 CLD → AI : ai_request, model=llama-3.1, tokens=150
💾 CLD → ARC : object_stored, key=assets/logo.png, size=45KB
🔐 CLD → SEC : auth_event, type=login, user=admin@blackroad.ai
```

---

*The edge is closer than you think. Now it's the gateway to everything.*
