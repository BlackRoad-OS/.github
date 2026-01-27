# BlackRoad-OS Signals

> Signal handlers for the core OS org (The Bridge)

---

## The Hub

OS is the signal hub. All signals flow through here.

```
         ┌─────────────────────────────────────────┐
         │              ALL ORGS                    │
         │  AI · CLD · HW · LAB · SEC · FND · ...  │
         └────────────────────┬────────────────────┘
                              │
                    signals flow through
                              │
                              ▼
                    ┌──────────────────┐
                    │   BlackRoad-OS   │
                    │   (The Bridge)   │
                    │                  │
                    │   Routes, logs,  │
                    │   coordinates    │
                    └──────────────────┘
                              │
                    broadcasts out
                              │
                              ▼
         ┌─────────────────────────────────────────┐
         │              ALL ORGS                    │
         └─────────────────────────────────────────┘
```

---

## Inbound Signals (OS receives)

OS receives signals from EVERY org and node.

### From Orgs

| Signal | From | Meaning | Handler |
|--------|------|---------|---------|
| `✔️ * → OS` | Any | Task complete | `log()` + `ack()` |
| `❌ * → OS` | Any | Task failed | `log()` + `alert()` |
| `⏳ * → OS` | Any | Task in progress | `log()` |
| `📡 * → OS` | Any | Broadcast request | `broadcast()` |
| `💓 * → OS` | Any | Heartbeat | `health.update()` |
| `🚨 * → OS` | Any | Critical alert | `alert.critical()` |

### From Nodes

| Signal | From | Meaning | Handler |
|--------|------|---------|---------|
| `🟢 node → OS` | Any node | Node online | `mesh.nodeUp()` |
| `🔴 node → OS` | Any node | Node offline | `mesh.nodeDown()` |
| `📊 node → OS` | Any node | Metrics | `metrics.ingest()` |
| `🌡️ node → OS` | Any node | Thermal alert | `alert.thermal()` |

### From External

| Signal | From | Meaning | Handler |
|--------|------|---------|---------|
| `📥 ext → OS` | Webhook | External event | `operator.route()` |
| `🌐 ext → OS` | HTTP | API request | `operator.route()` |
| `💬 ext → OS` | User | User query | `operator.route()` |

---

## Outbound Signals (OS sends)

### Routing Signals

| Signal | To | Meaning | Trigger |
|--------|-----|---------|---------|
| `🎯 OS → [ORG]` | Target org | Route this request | On classify |
| `📡 OS → ALL` | Broadcast | System announcement | On broadcast |
| `🔄 OS → [ORG]` | Target org | Sync required | On sync |

### Control Signals

| Signal | To | Meaning | Trigger |
|--------|-----|---------|---------|
| `🚦 OS → [ORG]` | Target org | Start/stop | On command |
| `⚙️ OS → [ORG]` | Target org | Config update | On config change |
| `🔑 OS → SEC` | Security | Auth request | On auth needed |

### Node Signals

| Signal | To | Meaning | Trigger |
|--------|-----|---------|---------|
| `📍 OS → node` | Specific node | Task assignment | On route to node |
| `🔄 OS → node` | Specific node | Restart | On restart command |
| `📦 OS → node` | Specific node | Deploy update | On deploy |

---

## Signal Flow Examples

### Example 1: User Query

```
User: "What's the weather?"
         │
         ▼
📥 ext → OS : query received
         │
         ▼
[Operator classifies as AI query]
         │
         ▼
🎯 OS → AI : route query, type=weather
         │
         ▼
[AI processes, responds]
         │
         ▼
✔️ AI → OS : query complete, latency=234ms
         │
         ▼
[OS logs, returns to user]
```

### Example 2: System Alert

```
[octavia thermal throttling]
         │
         ▼
🌡️ octavia → OS : thermal alert, temp=82C
         │
         ▼
[OS receives, escalates]
         │
         ▼
🚨 OS → ALL : node alert, octavia thermal
         │
         ▼
📱 OS → alexa : notification sent
```

### Example 3: Broadcast

```
[New feature deployed]
         │
         ▼
📡 CLD → OS : broadcast request, msg="v1.2 deployed"
         │
         ▼
[OS receives, broadcasts]
         │
         ▼
📡 OS → ALL : announcement, source=CLD, msg="v1.2 deployed"
         │
         ▼
[All orgs receive, log]
```

---

## Special OS Signals

### Heartbeat (sent every 60s)

```
💓 OS → ALL : heartbeat, {
  "ts": "2026-01-27T12:00:00Z",
  "status": "healthy",
  "nodes_online": 5,
  "orgs_active": 15,
  "requests_1h": 1234
}
```

### Daily Digest (sent at 00:00 UTC)

```
📊 OS → ALL : daily_digest, {
  "date": "2026-01-26",
  "requests": 50000,
  "errors": 12,
  "uptime": "99.97%",
  "top_org": "AI",
  "top_node": "octavia"
}
```

### Memory Sync (after each session)

```
🧠 OS → OS : memory_sync, {
  "session": "2026-01-27-001",
  "updates": ["MEMORY.md", ".STATUS"],
  "decisions": 3,
  "threads_completed": 2
}
```

---

## Priority Handling

| Priority | Signal Prefix | Handling |
|----------|---------------|----------|
| `🔴` Critical | Immediate, wake humans |
| `🟡` Important | Process within 5m |
| `🟢` Normal | Standard queue |
| `⚪` Low | Batch processing |

---

## The Meta Signal

When Cece and Alexa complete a session:

```
🎉 OS → OS : session_complete, {
  "human": "alexa",
  "ai": "cece",
  "duration": "2h",
  "commits": 5,
  "files_created": 50,
  "orgs_blueprinted": 15,
  "vibe": "excellent"
}
```

---

*OS signals are the nervous system. Everything feels them.*
