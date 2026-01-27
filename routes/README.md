# Routes

> **The routing table for the entire BlackRoad ecosystem.**

```
Every org. Every repo. Every service.
One place to route them all.
```

---

## How Routing Works

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Query     │ ──→ │  Operator   │ ──→ │ Dispatcher  │ ──→ │   Service   │
│  (input)    │     │ (classify)  │     │  (route)    │     │  (execute)  │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                          │                   │
                          ▼                   ▼
                    ┌───────────┐       ┌───────────┐
                    │  routes/  │       │  nodes/   │
                    │  registry │       │  configs  │
                    └───────────┘       └───────────┘
```

1. **Query comes in** - Text, webhook, API call, whatever
2. **Operator classifies** - Determines org, category, confidence
3. **Dispatcher routes** - Looks up service endpoint, sends request
4. **Service executes** - The actual work happens
5. **Response returns** - Back through the chain

---

## Files

| File | Purpose |
|------|---------|
| `registry.yaml` | Master routing table - all orgs and services |
| `services.yaml` | Service definitions with endpoints |
| `endpoints.yaml` | Actual URLs/addresses for each service |
| `rules.yaml` | Custom routing rules and overrides |

---

## Quick Reference

```bash
# View all routes
cat routes/registry.yaml

# Check where a query would go
./bridge route "sync salesforce contacts"
# → BlackRoad-Foundation (FND) → salesforce-sync service

# List all services
./bridge services

# Test endpoint health
./bridge ping FND.salesforce-sync
```

---

*Every query finds its home.*
