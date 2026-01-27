# BlackRoad-AI Signals

> Signal handlers for the AI org

---

## Inbound Signals (AI receives)

| Signal | From | Meaning | Handler |
|--------|------|---------|---------|
| `🎯 OS → AI` | Bridge | Route this request | `router.route()` |
| `🔄 OS → AI` | Bridge | Sync prompts/config | `prompts.sync()` |
| `⬇️ FND → AI` | Foundation | Customer context for personalization | `router.enrich()` |
| `🔴 SEC → AI` | Security | Block this pattern | `router.block()` |

---

## Outbound Signals (AI sends)

| Signal | To | Meaning | Trigger |
|--------|-----|---------|---------|
| `✔️ AI → OS` | Bridge | Request completed | After successful route |
| `❌ AI → OS` | Bridge | Request failed | On error |
| `⏳ AI → OS` | Bridge | Long task in progress | For async tasks |
| `⬆️ AI → ARC` | Archive | Log this interaction | After every request |
| `📡 AI → ALL` | Broadcast | Model status change | On provider issues |

---

## Signal Flow

```
                    ┌─────────────────┐
   OS ─────────────►│  SIGNAL PARSER  │
   FND ────────────►│                 │
   SEC ────────────►└────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
        ┌──────────┐  ┌──────────┐  ┌──────────┐
        │  ROUTE   │  │   SYNC   │  │  BLOCK   │
        │ requests │  │ configs  │  │ patterns │
        └────┬─────┘  └────┬─────┘  └────┬─────┘
             │             │             │
             └─────────────┼─────────────┘
                           ▼
                    ┌──────────────┐
                    │   ROUTER     │
                    │              │
                    │ Claude ──┐   │
                    │ GPT ─────┼───┼──► Response
                    │ Hailo ───┘   │
                    │ NumPy        │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
           ✔️ → OS     ⬆️ → ARC     📡 → ALL
           (done)      (log)       (status)
```

---

## Priority Handling

| Priority | Handling |
|----------|----------|
| `🔴` Critical | Immediate, bypass queue |
| `🟡` Important | Next in queue |
| `🟢` Normal | Standard queue |
| `⚪` Low | Batch processing |

---

## Error Signals

When things go wrong:

```
# Model provider down
📡🔴 AI → ALL : Claude API unavailable, routing to fallback

# Rate limited
⚠️ AI → OS : Rate limit hit for user X, queuing

# Complete failure
❌ AI → OS : Unable to route request, all providers failed
```

---

## Heartbeat

AI org sends periodic status:

```
# Every 60 seconds
💓 AI → OS : status=healthy, queue=12, latency_p50=234ms
```

---

*Signals keep the mesh alive.*
