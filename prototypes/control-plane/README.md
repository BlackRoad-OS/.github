# Control Plane

> **One CLI to rule them all. The Bridge's unified interface.**

```
Prototype: control-plane
Status: ACTIVE
Version: 0.1.0
```

---

## What It Does

```
                    ┌─────────────────────────────────────┐
                    │         CONTROL PLANE               │
                    │   The unified Bridge interface      │
                    └──────────────┬──────────────────────┘
                                   │
         ┌─────────────┬───────────┼───────────┬─────────────┐
         ▼             ▼           ▼           ▼             ▼
    ┌─────────┐   ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
    │Operator │   │ Metrics │ │Explorer │ │ Status  │ │ Signals │
    │ (route) │   │ (KPIs)  │ │(browse) │ │(beacon) │ │ (emit)  │
    └─────────┘   └─────────┘ └─────────┘ └─────────┘ └─────────┘
```

The Control Plane unifies all Bridge prototypes into a single interface:

- **Operator** - Route queries to the right org
- **Metrics** - Monitor ecosystem health and KPIs
- **Explorer** - Browse and search the ecosystem
- **Status** - Quick state beacon
- **Signals** - Emit and coordinate signals

---

## Quick Start

```bash
# Quick status
python -m control_plane status

# Full dashboard
python -m control_plane dashboard

# Route a query
python -m control_plane route "What is the weather?"

# Browse ecosystem
python -m control_plane browse

# List orgs
python -m control_plane orgs

# List templates
python -m control_plane templates

# Emit signal
python -m control_plane signal "ping" --target AI

# Search
python -m control_plane search "salesforce"

# Interactive mode (no arguments)
python -m control_plane
```

---

## Interactive Mode

```
$ python -m control_plane

  BLACKROAD CONTROL PLANE
  ========================================

  Commands: status, dashboard, route, browse, orgs, templates, signal, search, quit

  bridge> status

  BLACKROAD BRIDGE
  ========================================

  Status:     ONLINE
  Session:    SESSION_2
  Orgs:       1/16 active
  Nodes:      1/7 online
  Prototypes: 4 ready
  Templates:  6 ready

  ========================================

  bridge> route deploy my app to production
  -> BlackRoad-Cloud (85%)

  bridge> orgs
  [ACTIVE ] BlackRoad-OS
            Core infrastructure. The Bridge.
  [PLANNED] BlackRoad-AI
            Route to intelligence, don't build it.
  ...

  bridge> quit
  Goodbye!
```

---

## Commands

| Command | Description |
|---------|-------------|
| `status` | Quick status readout |
| `dashboard` | Full metrics dashboard |
| `route <query>` | Route a query through the Operator |
| `browse [path]` | Browse the ecosystem |
| `orgs` | List all organizations |
| `templates` | List all templates |
| `signal <msg>` | Emit a signal |
| `search <query>` | Search the ecosystem |

---

## Python API

```python
from control_plane.bridge import get_bridge

# Get the singleton Bridge
bridge = get_bridge()

# Get status
state = bridge.get_state()
print(f"Orgs: {state.orgs_total}")
print(f"Nodes: {state.nodes_online}/{state.nodes_total}")

# Route a query
result = bridge.route("deploy my worker")
print(f"Destination: {result['org']}")

# Get dashboard
print(bridge.dashboard())

# Browse
print(bridge.browse("orgs/"))

# List orgs
for org in bridge.list_orgs():
    print(f"{org['name']}: {org['mission']}")

# Emit signal
bridge.signal("ping", "AI")
```

---

## Architecture

```
control-plane/
├── control_plane/
│   ├── __init__.py      ← Package init
│   ├── __main__.py      ← Module entry
│   ├── bridge.py        ← Core Bridge class
│   └── cli.py           ← CLI interface
└── README.md
```

The Bridge class provides:
- Lazy loading of Operator, Metrics, Explorer
- State aggregation from all prototypes
- Unified routing interface
- Signal emission
- Ecosystem search

---

## Signals

```
🎯 OS → OS : control_plane_started
📊 OS → OS : status_requested
🔀 OS → AI : query_routed, confidence=95%
📡 OS → OS : signal_emitted, target=AI
```

---

*The Bridge is always watching.*
