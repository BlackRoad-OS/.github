# SIGNALS

> **Morse code for agents.**
> Lightweight coordination across the ecosystem.

---

## The Idea

When something happens in The Bridge, we signal downstream.
When something happens downstream, agents signal back.

```
✔️ = done, pass it on
⏳ = working on it
❌ = blocked/failed
📡 = broadcasting to all
🎯 = targeted to specific org
```

---

## Signal Format

```
[TIMESTAMP] [SIGNAL] [SOURCE] → [TARGET] : [MESSAGE]
```

Example:
```
2026-01-27T14:30:00Z ✔️ .github → BlackRoad-AI : MEMORY.md updated, sync context
2026-01-27T14:31:00Z 📡 .github → ALL : New architecture decision logged
2026-01-27T14:32:00Z 🎯 .github → BlackRoad-Hardware : Node configs needed for octavia
```

---

## Signal Types

### State Signals

| Signal | Meaning | Use |
|--------|---------|-----|
| `✔️` | Complete | Task done, ready for next step |
| `⏳` | In Progress | Working on it |
| `❌` | Blocked | Can't proceed, needs help |
| `⚠️` | Warning | Something needs attention |
| `💤` | Idle | Waiting for input |

### Routing Signals

| Signal | Meaning | Use |
|--------|---------|-----|
| `📡` | Broadcast | Send to all orgs/agents |
| `🎯` | Targeted | Send to specific org/agent |
| `🔄` | Sync | Request bidirectional sync |
| `⬆️` | Upstream | Pull data from source |
| `⬇️` | Downstream | Push data to target |

### Priority Signals

| Signal | Meaning | Use |
|--------|---------|-----|
| `🔴` | Critical | Drop everything |
| `🟡` | Important | Handle soon |
| `🟢` | Normal | Regular priority |
| `⚪` | Low | When you get to it |

---

## Org Addresses

Each org has a shortcode for routing:

| Org | Code | Focus |
|-----|------|-------|
| BlackRoad-OS | `OS` | Core infra (The Bridge) |
| BlackRoad-AI | `AI` | Models, routing |
| BlackRoad-Cloud | `CLD` | Cloud services |
| BlackRoad-Labs | `LAB` | Research |
| BlackRoad-Security | `SEC` | Security |
| BlackRoad-Foundation | `FND` | CRM, business |
| BlackRoad-Media | `MED` | Content |
| BlackRoad-Hardware | `HW` | IoT, devices |
| BlackRoad-Education | `EDU` | Learning |
| BlackRoad-Gov | `GOV` | Governance |
| BlackRoad-Interactive | `INT` | Games, metaverse |
| BlackRoad-Archive | `ARC` | Storage |
| BlackRoad-Studio | `STU` | Design |
| BlackRoad-Ventures | `VEN` | Commerce |
| Blackbox-Enterprises | `BBX` | Enterprise |

---

## Node Addresses

Physical nodes in the mesh:

| Node | Code | Role |
|------|------|------|
| lucidia | `LUC` | Salesforce, blockchain |
| octavia | `OCT` | AI routing (Hailo-8) |
| aria | `ARI` | Agent orchestration |
| alice | `ALI` | K8s, mesh root |
| shellfish | `SHL` | Public gateway |
| cecilia | `CEC` | Dev (Mac) |
| arcadia | `ARC` | Mobile (iPhone) |

---

## Signal Flow

```
                    ┌─────────────┐
                    │   SIGNAL    │
                    │   PARSER    │
                    └──────┬──────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
         ▼                 ▼                 ▼
    ┌─────────┐      ┌─────────┐      ┌─────────┐
    │   📡    │      │   🎯    │      │   🔄    │
    │BROADCAST│      │TARGETED │      │  SYNC   │
    └────┬────┘      └────┬────┘      └────┬────┘
         │                │                │
         ▼                ▼                ▼
    ┌─────────┐      ┌─────────┐      ┌─────────┐
    │ ALL ORGS│      │SPECIFIC │      │BIDIRECT │
    │         │      │  ORG    │      │  SYNC   │
    └─────────┘      └─────────┘      └─────────┘
```

---

## The Morse Code Idea

Like actual morse, signals are:
- **Short** - minimal bytes
- **Unambiguous** - one meaning per signal
- **Chainable** - can sequence them

```
✔️✔️✔️ = All three steps done
⏳✔️❌ = Step 1 in progress, step 2 done, step 3 blocked
📡🔴 = Broadcast critical alert to all
🎯AI⬇️ = Push to BlackRoad-AI specifically
```

---

## Implementation (Future)

When we build the Operator, signals become:

```python
# In the operator
def signal(type: str, source: str, target: str, message: str):
    """
    Emit a signal to the mesh.
    """
    payload = {
        "ts": datetime.utcnow().isoformat(),
        "signal": type,
        "from": source,
        "to": target,
        "msg": message
    }

    if target == "ALL":
        broadcast(payload)
    else:
        route_to(target, payload)

    log_to_ledger(payload)  # Everything gets logged

# Usage
signal("✔️", "OS", "AI", "MEMORY.md updated")
signal("📡", "OS", "ALL", "New architecture decision")
signal("🎯", "OS", "HW", "Need octavia config")
```

---

## Current Signal Log

> Updated by agents as things happen

```
2026-01-27T00:00:00Z ✔️ OS → OS : Bridge established
2026-01-27T00:00:01Z ✔️ OS → OS : REPO_MAP.md created
2026-01-27T00:00:02Z ✔️ OS → OS : STREAMS.md created
2026-01-27T00:00:03Z ✔️ OS → OS : MEMORY.md created
2026-01-27T00:00:04Z ✔️ OS → OS : SIGNALS.md created
2026-01-27T00:00:05Z 📡 OS → ALL : Bridge is live, orgs can sync
```

---

*Signals are how the mesh thinks.*
