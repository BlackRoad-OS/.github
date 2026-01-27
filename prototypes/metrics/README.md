# BlackRoad Metrics

> **Real-time KPIs. Know if something's dead.**

```
Status: PROTOTYPE
Purpose: Dynamic counting, health checks, dashboards
```

---

## Quick Start

```bash
# See everything at a glance
python -m metrics.dashboard

# Just the numbers
python -m metrics.count

# Health check
python -m metrics.health

# Watch mode (updates every 5s)
python -m metrics.dashboard --watch
```

---

## What It Tracks

### Code Metrics
- Total files
- Lines of code
- Commits today/all time
- Languages breakdown

### Org Metrics
- Blueprints complete
- Orgs active vs planned
- Repos defined vs created

### Health Metrics
- Node status (online/offline)
- Last signal time
- Error rate
- Response latency

### Session Metrics
- Files created this session
- Lines written
- Commits made
- Time elapsed

---

## Example Output

```
╔══════════════════════════════════════════════════════════════╗
║                    BLACKROAD DASHBOARD                        ║
║                    2026-01-27 14:30:00                        ║
╠══════════════════════════════════════════════════════════════╣
║  CODE          │  ORGS          │  HEALTH                    ║
║  ─────────────────────────────────────────────────────────   ║
║  Files:    67  │  Blueprints: 15/15 ✔️  │  Bridge: 🟢 ONLINE  ║
║  Lines: 8,432  │  Active:      1/15    │  Nodes:  1/7 online ║
║  Commits:  12  │  Repos:      1/80     │  Errors: 0          ║
╠══════════════════════════════════════════════════════════════╣
║  RECENT SIGNALS                                              ║
║  ─────────────────────────────────────────────────────────   ║
║  14:29:55  🎯 OS → AI : route query                         ║
║  14:29:50  ✔️ AI → OS : query complete                      ║
║  14:29:45  💓 OS → ALL : heartbeat                          ║
╠══════════════════════════════════════════════════════════════╣
║  SESSION                                                     ║
║  ─────────────────────────────────────────────────────────   ║
║  Duration: 2h 15m  │  Files: +50  │  Lines: +6,000          ║
╚══════════════════════════════════════════════════════════════╝
```

---

*If something's dead, we'll know.*
