# Deploying Agents to Cloudflare Workers

This directory contains Cloudflare Worker implementations of the BlackRoad agents.

## Overview

Each agent can be deployed as an edge worker for global, low-latency access:

- **agent-router.js** - Routes requests to appropriate agents
- **coder-agent.js** - Code generation/review agent
- More agents can be added following the same pattern

## Prerequisites

1. **Cloudflare Account**: Sign up at https://cloudflare.com
2. **Wrangler CLI**: Already installed in the codespace
3. **Login**: Run `wrangler login` to authenticate

## Setup

### 1. Login to Cloudflare

```bash
wrangler login
```

This opens a browser to authorize wrangler with your Cloudflare account.

### 2. Create KV Namespace

```bash
# Create KV for agent state
wrangler kv:namespace create "AGENT_KV"

# Copy the ID and update wrangler.toml
```

### 3. Create D1 Database (optional)

```bash
# Create D1 database for collaboration tracking
wrangler d1 create blackroad-agents

# Copy the database_id and update wrangler.toml
```

### 4. Set Secrets (optional)

For cloud model fallback:

```bash
# OpenAI API key (optional)
wrangler secret put OPENAI_API_KEY

# Anthropic API key (optional)
wrangler secret put ANTHROPIC_API_KEY

# Ollama API URL (if running on separate server)
wrangler secret put OLLAMA_API_URL
```

## Deploy

### Deploy Router

```bash
wrangler deploy agent-router.js --name agent-router
```

### Deploy Coder Agent

```bash
wrangler deploy coder-agent.js --name coder-agent
```

### Deploy All

```bash
# Deploy everything
for worker in *.js; do
    name=$(basename "$worker" .js)
    wrangler deploy "$worker" --name "$name"
done
```

## Configuration

Edit `wrangler.toml` to customize:

```toml
name = "agent-router"
main = "agent-router.js"
compatibility_date = "2024-01-27"

# KV namespace for state
[[kv_namespaces]]
binding = "AGENT_KV"
id = "YOUR_KV_ID"  # Replace with your KV ID

# D1 database (optional)
[[d1_databases]]
binding = "AGENT_DB"
database_name = "blackroad-agents"
database_id = "YOUR_D1_ID"  # Replace with your D1 ID
```

## Usage

### Health Check

```bash
curl https://agent-router.YOUR-SUBDOMAIN.workers.dev/health
```

### Ask a Question

```bash
curl -X POST https://agent-router.YOUR-SUBDOMAIN.workers.dev/ask \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Write a Python function to reverse a string"
  }'
```

The router will automatically select the appropriate agent.

### Specify Agent

```bash
curl -X POST https://agent-router.YOUR-SUBDOMAIN.workers.dev/ask \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Design a color palette",
    "agent": "designer"
  }'
```

### List Agents

```bash
curl https://agent-router.YOUR-SUBDOMAIN.workers.dev/agents
```

## Architecture

```
┌─────────────────────────────────────────┐
│         Cloudflare Edge Network         │
├─────────────────────────────────────────┤
│                                         │
│  ┌────────────────────────────────┐   │
│  │      agent-router.js           │   │
│  │  (Main entry point)            │   │
│  └───────────┬────────────────────┘   │
│              │                         │
│      ┌───────┼──────┐                 │
│      ▼       ▼      ▼                 │
│  ┌──────┐ ┌──────┐ ┌──────┐          │
│  │Coder │ │Design│ │ Ops  │          │
│  │Agent │ │Agent │ │Agent │          │
│  └──────┘ └──────┘ └──────┘          │
│      │       │      │                 │
│      └───────┼──────┘                 │
│              ▼                         │
│         ┌─────────┐                   │
│         │   KV    │  (State)          │
│         │   D1    │  (History)        │
│         └─────────┘                   │
│                                         │
└─────────────────────────────────────────┘
```

## Adding New Agents

1. **Create worker file**:
   ```javascript
   // designer-agent.js
   export default {
     async fetch(request, env, ctx) {
       // Agent logic here
     }
   }
   ```

2. **Add to router**:
   ```javascript
   // agent-router.js
   const AGENT_URLS = {
     designer: 'https://designer-agent.YOUR.workers.dev',
     // ...
   }
   ```

3. **Deploy**:
   ```bash
   wrangler deploy designer-agent.js --name designer-agent
   ```

## Local Development

Test workers locally before deploying:

```bash
# Run locally
wrangler dev agent-router.js

# Test
curl http://localhost:8787/health
```

## Monitoring

View logs in Cloudflare dashboard:
1. Go to https://dash.cloudflare.com
2. Select "Workers & Pages"
3. Click on your worker
4. View "Logs" tab

Or stream logs with wrangler:

```bash
wrangler tail agent-router
```

## Cost

Cloudflare Workers free tier:
- **100,000 requests/day** - Free
- **10ms CPU time per request** - Free
- Additional usage: $0.50 per million requests

For most use cases, this stays free!

## Troubleshooting

### "No such namespace"

Create KV namespace:
```bash
wrangler kv:namespace create "AGENT_KV"
```

### "Authorization failed"

Re-login:
```bash
wrangler logout
wrangler login
```

### "Module not found"

Check that worker file exists and is specified in command:
```bash
wrangler deploy agent-router.js --name agent-router
```

## Custom Domains

Connect a custom domain:

```bash
# Add route in wrangler.toml
routes = [
  { pattern = "agents.yourdomain.com/*", zone_name = "yourdomain.com" }
]
```

## Security

1. **Use secrets** for API keys (never commit keys!)
2. **Enable rate limiting** in production
3. **Add CORS headers** as needed
4. **Validate inputs** in all endpoints
5. **Use environment variables** for configuration

## Resources

- [Cloudflare Workers Docs](https://developers.cloudflare.com/workers/)
- [Wrangler CLI Docs](https://developers.cloudflare.com/workers/wrangler/)
- [Workers Examples](https://developers.cloudflare.com/workers/examples/)
- [KV Storage](https://developers.cloudflare.com/workers/runtime-apis/kv/)
- [D1 Database](https://developers.cloudflare.com/d1/)

---

*Deploy globally in seconds. Scale to millions. $0 to start.*
