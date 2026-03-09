# API Gateway Worker

> **The edge is the front door. Cloudflare is the bouncer.**

A Cloudflare Workers-based API gateway that handles routing, rate limiting,
authentication, CORS, and request transformation at the edge - before
requests ever hit the BlackRoad infrastructure.

## Architecture

```
[Internet]
     │
     ▼
[Cloudflare Edge]  (280+ cities worldwide)
     │
     ▼
[API Gateway Worker]
     │
     ├── 1. CORS handling
     ├── 2. Rate limiting (via KV)
     ├── 3. API key authentication
     ├── 4. Request validation
     ├── 5. Route matching
     ├── 6. Request transformation
     ├── 7. Upstream forwarding
     └── 8. Response caching
            │
            ▼
     [BlackRoad Backend]
     (Pi cluster / Cloud)
```

## Files

| File | Purpose |
|------|---------|
| `worker.js` | Main Cloudflare Worker script |
| `wrangler.toml` | Cloudflare deployment configuration |

## Routes

| Method | Path | Description |
|--------|------|-------------|
| POST | `/v1/route` | Route an AI request |
| POST | `/v1/complete` | Direct completion |
| GET | `/v1/health` | Health check |
| GET | `/v1/status` | System status |
| POST | `/v1/webhook/:provider` | Webhook receiver |
| GET | `/v1/templates` | List prompt templates |

## Deployment

```bash
npm install -g wrangler
wrangler login
wrangler deploy
```
