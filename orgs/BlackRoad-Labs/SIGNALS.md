# BlackRoad-Labs Signals

> Signal handlers for the Labs org

---

## Inbound Signals (LAB receives)

| Signal | From | Meaning | Handler |
|--------|------|---------|---------|
| `🧪 OS → LAB` | Bridge | Start experiment | `experiments.create()` |
| `🎯 * → LAB` | Any org | "Can we try X?" | `sandbox.test()` |
| `🔴 OS → LAB` | Bridge | Kill experiment | `experiments.stop()` |

---

## Outbound Signals (LAB sends)

| Signal | To | Meaning | Trigger |
|--------|-----|---------|---------|
| `🧪 LAB → OS` | Bridge | Experiment started | On create |
| `📊 LAB → OS` | Bridge | Results available | On completion |
| `🎓 LAB → [ORG]` | Target org | Graduating feature | On graduation |
| `🗑️ LAB → ARC` | Archive | Archiving experiment | On archive |
| `❌ LAB → OS` | Bridge | Experiment failed | On failure |

---

## Experiment Lifecycle Signals

```
# Start
🧪 LAB → OS : experiment=routing-benchmark, status=started, est=7d

# Progress
📈 LAB → OS : experiment=routing-benchmark, progress=45%, findings="10K/s achieved"

# Success
✔️📊 LAB → OS : experiment=routing-benchmark, status=success, results=attached

# Graduation
🎓 LAB → AI : graduating mini-router, ready for integration

# Failure
❌ LAB → OS : experiment=lora-range, status=failed, reason="range insufficient"
🗑️ LAB → ARC : archiving lora-range, post_mortem=attached
```

---

## Discovery Signals

When Labs finds something interesting:

```
# Breakthrough
💡 LAB → OS : discovery="Hailo can do 50fps object detection"

# Warning
⚠️ LAB → OS : finding="Pi thermal throttles at 26 TOPS sustained"

# Question
❓ LAB → AI : "Can Claude handle this edge case?"
```

---

## Sandbox Signals

```
# Sandbox is informal, minimal signals
🏖️ LAB → OS : sandbox activity, files=12, last_active=2h_ago

# Cleanup
🧹 LAB → OS : sandbox cleanup, deleted=45_files, freed=2.3GB
```

---

## Research Signals

```
# New research published
📚 LAB → EDU : research published, topic="routing-latency", file=research/routing/latency-analysis.md

# Research request
🔍 LAB → OS : research needed, topic="WebXR performance"
```

---

*Labs signals are experiments in themselves.*
