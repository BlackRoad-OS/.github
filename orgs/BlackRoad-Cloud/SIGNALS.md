# BlackRoad-Cloud Signals

> Signal handlers for the Cloud org

---

## Inbound Signals (CLD receives)

| Signal | From | Meaning | Handler |
|--------|------|---------|---------|
| `🎯 OS → CLD` | Bridge | Deploy this | `deploy.run()` |
| `🔄 AI → CLD` | AI | Sync model configs | `workers.update()` |
| `🔴 SEC → CLD` | Security | Block this IP/pattern | `firewall.block()` |

---

## Outbound Signals (CLD sends)

| Signal | To | Meaning | Trigger |
|--------|-----|---------|---------|
| `✔️ CLD → OS` | Bridge | Deployment complete | After deploy |
| `❌ CLD → OS` | Bridge | Deploy failed | On error |
| `⚠️ CLD → OS` | Bridge | Rate limit/quota warning | At 80% usage |
| `📡 CLD → ALL` | Broadcast | Edge status change | On incidents |

---

## Edge Metrics Signals

```
# Every 5 minutes
📊 CLD → OS : requests=1.2M, p50=12ms, p99=45ms, errors=0.01%
```

---

## Deployment Signals

```
# Deployment lifecycle
⏳ CLD → OS : Deploying gateway@v1.2.3
✔️ CLD → OS : gateway@v1.2.3 live at 300 locations
📡 CLD → ALL : New API version available
```

---

## Tunnel Signals

```
# Tunnel status
💓 CLD → OS : tunnel=alice, status=healthy, latency=23ms
⚠️ CLD → OS : tunnel=alice, status=degraded, failover=shellfish
❌ CLD → OS : tunnel=alice, status=down, failover=active
```

---

*Edge signals travel at the speed of light.*
