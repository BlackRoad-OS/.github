# Cloudflare Workers

> **Integration Guide** — architectural reference for future implementation. Code snippets below are illustrative, not runnable.

> **Edge compute. 300+ locations. Milliseconds from users.**

```
Org: BlackRoad-Cloud (CLD)
Node: shellfish (gateway)
Runtime: V8 Isolates
Latency: <50ms worldwide
```

---

## What It Does

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│    User     │  ────→  │ Cloudflare  │  ────→  │   Origin    │
│  (anywhere) │  edge   │   Worker    │  tunnel │  (Pi mesh)  │
└─────────────┘         └─────────────┘         └─────────────┘
                              │
                    ┌─────────┴─────────┐
                    │   Edge Services   │
                    │  KV  D1  R2  AI   │
                    └───────────────────┘
```

1. **Workers** - Code at the edge
2. **KV** - Key-value storage
3. **D1** - SQLite at the edge
4. **R2** - Object storage (S3-compatible)
5. **Tunnels** - Secure connection to Pi cluster

---

## Quick Start

```bash
# Install Wrangler CLI
npm install -g wrangler

# Login
wrangler login

# Create worker
wrangler init blackroad-api

# Develop locally
wrangler dev

# Deploy
wrangler deploy
```

---

## Worker Structure

```
blackroad-api/
├── src/
│   ├── index.ts          ← Entry point
│   ├── router.ts         ← Request routing
│   ├── handlers/
│   │   ├── api.ts        ← API endpoints
│   │   ├── auth.ts       ← Authentication
│   │   └── proxy.ts      ← Proxy to origin
│   └── utils/
│       ├── response.ts
│       └── cors.ts
├── wrangler.toml         ← Config
└── package.json
```

---

## Example Worker

```typescript
// src/index.ts
export interface Env {
  KV: KVNamespace;
  DB: D1Database;
  BUCKET: R2Bucket;
  AI: any;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    // Route requests
    switch (url.pathname) {
      case "/api/route":
        return handleRoute(request, env);

      case "/api/status":
        return handleStatus(env);

      default:
        // Proxy to origin via tunnel
        return proxyToOrigin(request, env);
    }
  },
};

async function handleRoute(request: Request, env: Env) {
  const { query } = await request.json();

  // Use Workers AI for classification
  const result = await env.AI.run("@cf/meta/llama-2-7b-chat-int8", {
    messages: [{ role: "user", content: query }],
  });

  return Response.json({
    destination: classifyResponse(result),
    signal: "🎯 CLD → AI : routed",
  });
}

async function handleStatus(env: Env) {
  // Get from KV cache
  const status = await env.KV.get("system_status", "json");

  return Response.json({
    status: "healthy",
    cached: status,
    edge: request.cf?.colo, // Which edge location
  });
}
```

---

## Wrangler Config

```toml
# wrangler.toml
name = "blackroad-api"
main = "src/index.ts"
compatibility_date = "2024-01-01"

# KV Namespaces
[[kv_namespaces]]
binding = "KV"
id = "xxx"

# D1 Database
[[d1_databases]]
binding = "DB"
database_name = "blackroad"
database_id = "xxx"

# R2 Bucket
[[r2_buckets]]
binding = "BUCKET"
bucket_name = "blackroad-storage"

# Workers AI
[ai]
binding = "AI"

# Environment variables
[vars]
ENVIRONMENT = "production"

# Secrets (set via wrangler secret put)
# STRIPE_KEY
# SF_TOKEN

# Routes
routes = [
  { pattern = "api.blackroad.ai/*", zone_name = "blackroad.ai" }
]

# Tunnel to origin
[[services]]
binding = "ORIGIN"
service = "blackroad-tunnel"
```

---

## Edge Services

### KV (Key-Value)
```typescript
// Write
await env.KV.put("user:123", JSON.stringify(userData), {
  expirationTtl: 3600, // 1 hour
});

// Read
const user = await env.KV.get("user:123", "json");

// List
const keys = await env.KV.list({ prefix: "user:" });
```

### D1 (SQLite)
```typescript
// Query
const results = await env.DB.prepare(
  "SELECT * FROM users WHERE email = ?"
).bind(email).all();

// Insert
await env.DB.prepare(
  "INSERT INTO users (email, name) VALUES (?, ?)"
).bind(email, name).run();
```

### R2 (Object Storage)
```typescript
// Upload
await env.BUCKET.put("files/doc.pdf", fileData, {
  customMetadata: { userId: "123" },
});

// Download
const object = await env.BUCKET.get("files/doc.pdf");
const data = await object.arrayBuffer();

// List
const list = await env.BUCKET.list({ prefix: "files/" });
```

### Workers AI
```typescript
// Text generation
const response = await env.AI.run("@cf/meta/llama-2-7b-chat-int8", {
  messages: [{ role: "user", content: "Hello" }],
});

// Embeddings
const embeddings = await env.AI.run("@cf/baai/bge-base-en-v1.5", {
  text: "Document to embed",
});

// Image generation
const image = await env.AI.run("@cf/stabilityai/stable-diffusion-xl-base-1.0", {
  prompt: "A bridge connecting clouds",
});
```

---

## Tunnels (Connect to Pi Cluster)

```bash
# Install cloudflared on Pi
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64 -o cloudflared
chmod +x cloudflared

# Authenticate
./cloudflared tunnel login

# Create tunnel
./cloudflared tunnel create blackroad-mesh

# Configure
cat > ~/.cloudflared/config.yml << EOF
tunnel: blackroad-mesh
credentials-file: /home/pi/.cloudflared/xxx.json

ingress:
  - hostname: api.blackroad.ai
    service: http://localhost:8080
  - hostname: ssh.blackroad.ai
    service: ssh://localhost:22
  - service: http_status:404
EOF

# Run
./cloudflared tunnel run blackroad-mesh
```

---

## CLI Commands

```bash
# Deploy worker
wrangler deploy

# Tail logs
wrangler tail

# Dev mode (local)
wrangler dev

# KV operations
wrangler kv:key put --binding=KV "key" "value"
wrangler kv:key get --binding=KV "key"

# D1 operations
wrangler d1 execute blackroad --command "SELECT * FROM users"

# R2 operations
wrangler r2 object put blackroad-storage/file.txt --file=./file.txt

# Secrets
wrangler secret put STRIPE_KEY
```

---

## Signals

```
🚀 CLD → OS : worker_deployed, name=blackroad-api, version=v1.2.3
🌐 CLD → OS : tunnel_connected, node=lucidia, status=healthy
📊 CLD → OS : traffic_report, requests=1M, p50=12ms, p99=45ms
⚠️ CLD → OS : rate_limit, ip=x.x.x.x, blocked=true
```

---

*The edge is closer than you think.*
