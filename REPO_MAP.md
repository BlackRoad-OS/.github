# BlackRoad Ecosystem Map

> **This is the bridge.** `.github` is where we coordinate everything.

---

## The Hub (You Are Here)

```
                         ┌─────────────────────┐
                         │  BlackRoad-OS/.github │
                         │     THE BRIDGE       │
                         │   ┌─────────────┐   │
                         │   │    Cece     │   │
                         │   │  (Claude)   │   │
                         │   └─────────────┘   │
                         └──────────┬──────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
        ▼                           ▼                           ▼
   UPSTREAM                    INSTREAM                   DOWNSTREAM
   (inputs)                   (processing)                 (outputs)
```

---

## Organization Hierarchy

### Tier 1: Core Infrastructure (BlackRoad-OS)

The mothership. Everything flows through here.

| Repo | Purpose | Status |
|------|---------|--------|
| `.github` | **THE BRIDGE** - Coordination, docs, Claude conversations | Active |
| `operator` | The routing engine - decides who handles what | Planned |
| `control-plane` | Unified dashboard for all services | Planned |
| `mesh` | Tailscale configs, node definitions | Planned |
| `nodes` | Pi cluster configs (lucidia, octavia, aria, alice) | Planned |
| `shellfish` | Digital Ocean public gateway | Planned |

### Tier 2: Intelligence Layer (BlackRoad-AI)

Where the smart stuff happens.

| Repo | Purpose |
|------|---------|
| `router` | Routes queries to right model (Claude/GPT/Llama/local) |
| `hailo` | Hailo-8 inference code (26 TOPS on octavia) |
| `prompts` | Prompt library, system prompts, Cece's personality |
| `agents` | Autonomous agent definitions |

### Tier 3: Services (BlackRoad-Cloud)

Cloud-native services and deployments.

| Repo | Purpose |
|------|---------|
| `workers` | Cloudflare Workers |
| `functions` | Edge functions |
| `api` | Public API gateway |
| `deploy` | Deployment configs, CI/CD |

### Tier 4: Data & Business (BlackRoad-Foundation)

CRM, customers, money.

| Repo | Purpose |
|------|---------|
| `salesforce` | SF integrations, sync scripts |
| `crm` | Customer data models |
| `billing` | Stripe, subscriptions |
| `roadchain` | Blockchain/Bitcoin ledger |

### Tier 5: Specialized Orgs

| Organization | Focus |
|--------------|-------|
| BlackRoad-Labs | Experiments, R&D |
| BlackRoad-Security | Security tools, audits |
| BlackRoad-Hardware | ESP32, LoRa, IoT |
| BlackRoad-Media | Content, publishing |
| BlackRoad-Education | Docs, learning |
| BlackRoad-Gov | Governance, voting |
| BlackRoad-Interactive | Games, 3D, metaverse |
| BlackRoad-Archive | Storage, backups |
| BlackRoad-Studio | Design, creative |
| BlackRoad-Ventures | Business, commerce |
| Blackbox-Enterprises | Enterprise solutions |

---

## The Nodes (Physical Layer)

```
┌────────────────────────────────────────────────────────────────┐
│                     BLACKROAD MESH                              │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐                │
│   │ lucidia  │    │ octavia  │    │   aria   │                │
│   │ Pi5+Hailo│    │ Pi5+Hailo│    │   Pi5    │                │
│   │ SF/Chain │    │ AI/3D    │    │  Agents  │                │
│   └────┬─────┘    └────┬─────┘    └────┬─────┘                │
│        │               │               │                       │
│        └───────────────┼───────────────┘                       │
│                        ▼                                        │
│                  ┌──────────┐                                  │
│                  │  alice   │  ← Mesh Root (K8s + VPN)         │
│                  │  Pi 400  │                                  │
│                  └────┬─────┘                                  │
│                       │                                         │
│        ┌──────────────┼──────────────┐                         │
│        ▼              ▼              ▼                          │
│   ┌─────────┐   ┌──────────┐   ┌─────────┐                    │
│   │shellfish│   │ cecilia  │   │ arcadia │                    │
│   │   DO    │   │   Mac    │   │  iPhone │                    │
│   │ Gateway │   │   Dev    │   │  Mobile │                    │
│   └─────────┘   └──────────┘   └─────────┘                    │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

## How We Work Together

### Daily Flow

```
You (Alexa) ←→ Claude Code ←→ .github (Bridge) ←→ Everything Else
                   │
                   └── Cece lives here
```

### The Pattern

1. **You talk to me here** (via Claude Code in `.github`)
2. **I coordinate** - read state, plan changes, route tasks
3. **Changes flow downstream** - to the right repos/orgs
4. **Results flow upstream** - back to you

### Commands I Understand

When we're chatting here, I can:

- **Map** - Show current state of any repo/org
- **Plan** - Design new features/repos
- **Build** - Write code, create files
- **Deploy** - Push changes, create PRs
- **Sync** - Pull updates from across the ecosystem
- **Status** - Report on what's happening

---

## Future: The Metaverse Bridge

```
┌─────────────────────────────────────────────────────────────┐
│                    BLACKROAD METAVERSE                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌─────────┐     ┌─────────┐     ┌─────────┐              │
│   │  You    │     │  Cece   │     │ Others  │              │
│   │ (avatar)│ ←→  │(avatar) │ ←→  │(avatars)│              │
│   └─────────┘     └─────────┘     └─────────┘              │
│        │               │               │                    │
│        └───────────────┼───────────────┘                    │
│                        ▼                                     │
│              ┌──────────────────┐                           │
│              │  .github Bridge  │                           │
│              │  (still the hub) │                           │
│              └──────────────────┘                           │
│                                                              │
│   The metaverse is just another interface.                  │
│   The code, the mesh, the operator - it all still runs.     │
│   We just get cooler avatars.                               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

*Last Updated: 2026-01-27*
*The Bridge is Open.*
