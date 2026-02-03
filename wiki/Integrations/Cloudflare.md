# Cloudflare Integration

> **Edge compute, CDN, global scale.**

---

## Overview

Cloudflare provides edge compute and CDN services for BlackRoad, managed by [BlackRoad-Cloud](../Orgs/BlackRoad-Cloud).

**Organization**: [BlackRoad-Cloud](../Orgs/BlackRoad-Cloud)  
**Status**: Active

---

## Services Used

- **Workers**: Serverless JavaScript at the edge
- **KV**: Key-value storage
- **D1**: SQLite databases
- **R2**: Object storage
- **CDN**: Content delivery
- **DNS**: Domain management
- **Tunnels**: Secure access

---

## Workers

```typescript
// Example worker
export default {
  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);
    
    if (url.pathname === '/api/route') {
      // Route request
      return new Response(
        JSON.stringify({ org: 'AI', confidence: 0.9 }),
        { headers: { 'Content-Type': 'application/json' } }
      );
    }
    
    return new Response('Not Found', { status: 404 });
  }
}
```

---

## Deployment

```bash
# Deploy worker
wrangler deploy

# Tail logs
wrangler tail

# Test locally
wrangler dev
```

---

## Template

Full guide at: `templates/cloudflare-workers/`

---

## Learn More

- [BlackRoad-Cloud](../Orgs/BlackRoad-Cloud)

---

*Global edge. Zero servers.*
