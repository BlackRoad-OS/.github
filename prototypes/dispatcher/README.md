# Dispatcher

> **Routes requests to the right service in the right org.**

```
Prototype: dispatcher
Status: ACTIVE
Version: 0.1.0
```

---

## What It Does

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Query     │ ──→ │  Operator   │ ──→ │ Dispatcher  │ ──→ │   Service   │
│  (input)    │     │ (classify)  │     │  (route)    │     │  (execute)  │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                          │                   │
                          ▼                   ▼
                    ┌───────────┐       ┌───────────┐
                    │ Classify  │       │  routes/  │
                    │  by type  │       │ registry  │
                    └───────────┘       └───────────┘
```

The Dispatcher:
1. **Receives** a request (text, API call, webhook)
2. **Classifies** it using the Operator
3. **Looks up** the target org and service in the registry
4. **Calls** the service endpoint
5. **Returns** the response

---

## Quick Start

```bash
# Dispatch a query (auto-routes to right org)
python -m dispatcher dispatch "sync salesforce contacts"
# → Routes to FND.salesforce

# Dispatch to specific org/service
python -m dispatcher dispatch-to FND salesforce

# List all routes
python -m dispatcher routes

# Check service health
python -m dispatcher health

# Interactive mode
python -m dispatcher interactive
```

---

## The Registry

All routing is defined in `routes/registry.yaml`:

```yaml
orgs:
  FND:
    name: BlackRoad-Foundation
    services:
      salesforce:
        endpoint: http://lucidia:8091/v1/salesforce
        health: http://lucidia:8091/health
      stripe:
        endpoint: http://lucidia:8092/v1/stripe

  AI:
    name: BlackRoad-AI
    services:
      router:
        endpoint: http://alice:8080/v1/complete
      agents:
        endpoint: http://alice:8082/v1/agents

rules:
  - pattern: "salesforce"
    org: FND
    service: salesforce
    priority: 100
```

---

## Python API

```python
from dispatcher import Dispatcher

# Create dispatcher
dispatcher = Dispatcher()

# Dispatch a query (auto-classifies and routes)
result = await dispatcher.dispatch("sync salesforce contacts")
print(f"Routed to: {result.org}.{result.service}")
print(f"Response: {result.response.data}")

# Dispatch to specific target
result = await dispatcher.dispatch_to("FND", "salesforce", data={
    "action": "sync",
    "objects": ["Contact", "Lead"]
})

# List all routes
for route in dispatcher.list_routes():
    print(f"{route['org']}.{route['service']} -> {route['endpoint']}")

# Health check
health = await dispatcher.health_check("FND", "salesforce")
print(f"Status: {health.value}")

# Check all services
all_health = await dispatcher.health_check_all()
for org, services in all_health.items():
    for service, status in services.items():
        print(f"{org}.{service}: {status.value}")

# Close when done
await dispatcher.close()
```

---

## CLI Commands

```bash
# Dispatch query (auto-route)
dispatcher dispatch "deploy my cloudflare worker"
dispatcher dispatch "what is 2+2" --mock

# Dispatch to specific target
dispatcher dispatch-to FND salesforce
dispatcher dispatch-to AI router --data '{"prompt": "hello"}'

# List routes
dispatcher routes

# Health checks
dispatcher health
dispatcher health --org FND

# Ping specific service
dispatcher ping FND.salesforce
dispatcher ping AI.router

# Interactive mode
dispatcher interactive
dispatcher interactive --mock
```

---

## Directory Structure

```
dispatcher/
├── dispatcher/
│   ├── __init__.py
│   ├── __main__.py
│   ├── core.py        ← Main Dispatcher class
│   ├── registry.py    ← Load/manage routes
│   ├── client.py      ← HTTP service client
│   └── cli.py         ← CLI interface
└── README.md
```

---

## How Routing Works

### 1. Classification
The Operator classifies the query:
```
"sync salesforce contacts"
  → category: crm
  → org: FND
  → confidence: 95%
```

### 2. Registry Lookup
The Dispatcher looks up the service:
```
FND:
  default_service: crm
  services:
    salesforce: http://lucidia:8091/v1/salesforce
    stripe: http://lucidia:8092/v1/stripe
```

### 3. Service Call
The client calls the endpoint:
```
POST http://lucidia:8091/v1/salesforce
{
  "query": "sync salesforce contacts",
  "context": {}
}
```

### 4. Response
```
{
  "success": true,
  "synced": 150,
  "objects": ["Contact"]
}
```

---

## Signals

```
🎯 OS → FND : dispatched, service=salesforce, latency=234ms
🎯 OS → AI : dispatched, service=router, latency=450ms
❌ OS → HW : dispatch_failed, error=connection_refused
🟢 OS → OS : health_check, FND.salesforce=healthy
```

---

## Mock Mode

For testing without real services:

```python
from dispatcher import Dispatcher
from dispatcher.client import MockServiceClient

# Use mock client
dispatcher = Dispatcher(mock=True)

# Or with custom responses
mock = MockServiceClient(responses={
    "http://lucidia:8091/v1/salesforce": {"synced": 100}
})
dispatcher = Dispatcher(client=mock)
```

---

*Every request finds its home.*
