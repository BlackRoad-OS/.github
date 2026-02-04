# AI Provider Failover Chain

> **Route to intelligence. If one path fails, take another.**

The failover chain ensures requests always reach an AI provider by cascading through a priority-ordered list of providers with health tracking, circuit breaking, and automatic recovery.

## Architecture

```
[Request] --> [Failover Router]
                    |
                    ├── 1. Claude (primary)
                    |     ├── healthy? --> route here
                    |     └── failing? --> circuit open, skip
                    |
                    ├── 2. GPT (secondary)
                    |     ├── healthy? --> route here
                    |     └── failing? --> circuit open, skip
                    |
                    ├── 3. Llama (local/tertiary)
                    |     ├── healthy? --> route here
                    |     └── failing? --> circuit open, skip
                    |
                    └── 4. All down --> queue + retry
```

## Features

- **Priority-based routing** - Tries providers in order of preference
- **Circuit breaker** - Opens after N failures, half-opens after cooldown
- **Health checks** - Periodic pings to track provider status
- **Latency tracking** - Records response times per provider
- **Retry with backoff** - Exponential backoff on transient failures
- **Request queuing** - Queues requests when all providers are down
- **Provider scoring** - Weighted scoring based on latency, reliability, cost

## Files

| File | Purpose |
|------|---------|
| `provider.py` | Provider abstraction and health tracking |
| `circuit_breaker.py` | Circuit breaker pattern implementation |
| `failover_router.py` | Core routing logic with failover |
| `config.py` | Provider configuration and defaults |

## Usage

```python
from failover_router import FailoverRouter
from config import DEFAULT_PROVIDERS

router = FailoverRouter(DEFAULT_PROVIDERS)
response = await router.route(prompt="What is BlackRoad?", max_tokens=500)
```

---

*Intelligence is already out there. We just need reliable paths to reach it.*
