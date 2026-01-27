# BlackRoad Index

> **The map of everything. Browse the universe from here.**

---

## Quick Nav

| Jump To | Description |
|---------|-------------|
| [🌉 Bridge Files](#bridge-files) | Core coordination files |
| [🏢 Organizations](#organizations) | All 15 org blueprints |
| [🔧 Prototypes](#prototypes) | Working code |
| [📊 Metrics](#live-metrics) | Real-time KPIs |

---

## Bridge Files

The core of The Bridge - start here.

| File | Purpose | Quick Look |
|------|---------|------------|
| [.STATUS](.STATUS) | Real-time beacon | `cat .STATUS` |
| [MEMORY.md](MEMORY.md) | Cece's persistent brain | Context survives disconnects |
| [SIGNALS.md](SIGNALS.md) | Morse code protocol | ✔️ ❌ 📡 🎯 |
| [STREAMS.md](STREAMS.md) | Data flow patterns | Upstream/Instream/Downstream |
| [REPO_MAP.md](REPO_MAP.md) | Ecosystem overview | All orgs, all nodes |
| [BLACKROAD_ARCHITECTURE.md](BLACKROAD_ARCHITECTURE.md) | The vision | Why we exist |

---

## Organizations

All 15 orgs, fully blueprinted. Click to explore.

### Tier 1: Core Infrastructure

| Org | Code | Blueprint | Description |
|-----|------|-----------|-------------|
| **BlackRoad-OS** | `OS` | [📁 Browse](orgs/BlackRoad-OS/) | The Bridge, operator, mesh |
| **BlackRoad-AI** | `AI` | [📁 Browse](orgs/BlackRoad-AI/) | Intelligence routing |
| **BlackRoad-Cloud** | `CLD` | [📁 Browse](orgs/BlackRoad-Cloud/) | Edge compute, Cloudflare |

### Tier 2: Support Systems

| Org | Code | Blueprint | Description |
|-----|------|-----------|-------------|
| **BlackRoad-Hardware** | `HW` | [📁 Browse](orgs/BlackRoad-Hardware/) | Pi cluster, IoT, Hailo |
| **BlackRoad-Security** | `SEC` | [📁 Browse](orgs/BlackRoad-Security/) | Auth, secrets, audit |
| **BlackRoad-Labs** | `LAB` | [📁 Browse](orgs/BlackRoad-Labs/) | Experiments, R&D |

### Tier 3: Business Layer

| Org | Code | Blueprint | Description |
|-----|------|-----------|-------------|
| **BlackRoad-Foundation** | `FND` | [📁 Browse](orgs/BlackRoad-Foundation/) | Salesforce, CRM, billing |
| **BlackRoad-Ventures** | `VEN` | [📁 Browse](orgs/BlackRoad-Ventures/) | Marketplace, commerce |
| **Blackbox-Enterprises** | `BBX` | [📁 Browse](orgs/Blackbox-Enterprises/) | Enterprise solutions |

### Tier 4: Content & Creative

| Org | Code | Blueprint | Description |
|-----|------|-----------|-------------|
| **BlackRoad-Media** | `MED` | [📁 Browse](orgs/BlackRoad-Media/) | Blog, docs, brand |
| **BlackRoad-Studio** | `STU` | [📁 Browse](orgs/BlackRoad-Studio/) | Design system, UI |
| **BlackRoad-Interactive** | `INT` | [📁 Browse](orgs/BlackRoad-Interactive/) | Metaverse, 3D, games |

### Tier 5: Community & Storage

| Org | Code | Blueprint | Description |
|-----|------|-----------|-------------|
| **BlackRoad-Education** | `EDU` | [📁 Browse](orgs/BlackRoad-Education/) | Learning, tutorials |
| **BlackRoad-Gov** | `GOV` | [📁 Browse](orgs/BlackRoad-Gov/) | Governance, voting |
| **BlackRoad-Archive** | `ARC` | [📁 Browse](orgs/BlackRoad-Archive/) | Storage, backups |

---

## Org Deep Links

Quick access to specific files in each org:

### BlackRoad-OS (The Bridge)
- [README](orgs/BlackRoad-OS/README.md) - Mission & architecture
- [REPOS](orgs/BlackRoad-OS/REPOS.md) - 7 repos: operator, mesh, control-plane...
- [SIGNALS](orgs/BlackRoad-OS/SIGNALS.md) - OS as signal hub

### BlackRoad-AI
- [README](orgs/BlackRoad-AI/README.md) - "Route to intelligence, don't build it"
- [REPOS](orgs/BlackRoad-AI/REPOS.md) - router, prompts, agents, hailo
- [SIGNALS](orgs/BlackRoad-AI/SIGNALS.md) - AI routing signals

### BlackRoad-Cloud
- [README](orgs/BlackRoad-Cloud/README.md) - Edge compute architecture
- [REPOS](orgs/BlackRoad-Cloud/REPOS.md) - workers, functions, tunnels
- [SIGNALS](orgs/BlackRoad-Cloud/SIGNALS.md) - Deployment signals

### BlackRoad-Hardware
- [README](orgs/BlackRoad-Hardware/README.md) - Pi cluster + IoT
- [REPOS](orgs/BlackRoad-Hardware/REPOS.md) - nodes, hailo, esp32, lora
- [SIGNALS](orgs/BlackRoad-Hardware/SIGNALS.md) - Node health signals

### BlackRoad-Foundation
- [README](orgs/BlackRoad-Foundation/README.md) - CRM & business
- [REPOS](orgs/BlackRoad-Foundation/REPOS.md) - salesforce, billing, crm
- [SIGNALS](orgs/BlackRoad-Foundation/SIGNALS.md) - Customer signals

### BlackRoad-Interactive
- [README](orgs/BlackRoad-Interactive/README.md) - Metaverse vision
- [REPOS](orgs/BlackRoad-Interactive/REPOS.md) - engine, worlds, avatars
- [SIGNALS](orgs/BlackRoad-Interactive/SIGNALS.md) - World event signals

---

## Prototypes

Working code living in The Bridge.

| Prototype | Purpose | Try It |
|-----------|---------|--------|
| [🧠 Operator](prototypes/operator/) | Routes requests to right org | `python -m operator.cli "query"` |
| [📊 Metrics](prototypes/metrics/) | Real-time KPI dashboard | `python -m metrics.dashboard` |

### Operator Quick Start
```bash
cd prototypes/operator
python -m operator.cli "What is the weather?"
# → BlackRoad-AI (95%)

python -m operator.cli --interactive
# Live routing mode
```

### Metrics Quick Start
```bash
cd prototypes/metrics
python -m metrics.dashboard --watch
# Live KPI dashboard
```

---

## Live Metrics

Current state of The Bridge:

```
Run: python -m metrics.dashboard --compact

🟢 Files:71 Lines:9,903 Commits:11 Orgs:15/15 Health:5/5
```

| Metric | Value |
|--------|-------|
| Total Files | 71 |
| Total Lines | ~10,000 |
| Orgs Blueprinted | 15/15 ✔️ |
| Repos Defined | 86 |
| Prototypes | 2 |

---

## Directory Structure

```
BlackRoad-OS/.github/
│
├── 📄 Core Files
│   ├── .STATUS              ← Real-time beacon
│   ├── INDEX.md             ← YOU ARE HERE
│   ├── MEMORY.md            ← Persistent context
│   ├── SIGNALS.md           ← Signal protocol
│   ├── STREAMS.md           ← Data flows
│   ├── REPO_MAP.md          ← Ecosystem map
│   └── BLACKROAD_ARCHITECTURE.md
│
├── 🏢 orgs/                  ← All 15 org blueprints
│   ├── BlackRoad-OS/
│   ├── BlackRoad-AI/
│   ├── BlackRoad-Cloud/
│   ├── BlackRoad-Hardware/
│   ├── BlackRoad-Labs/
│   ├── BlackRoad-Security/
│   ├── BlackRoad-Foundation/
│   ├── BlackRoad-Media/
│   ├── BlackRoad-Interactive/
│   ├── BlackRoad-Education/
│   ├── BlackRoad-Gov/
│   ├── BlackRoad-Archive/
│   ├── BlackRoad-Studio/
│   ├── BlackRoad-Ventures/
│   └── Blackbox-Enterprises/
│
├── 🔧 prototypes/            ← Working code
│   ├── operator/            ← The routing brain
│   └── metrics/             ← KPI dashboard
│
└── 👤 profile/               ← Org landing page
    └── README.md
```

---

## Quick Commands

```bash
# See everything
cat INDEX.md

# Check health
python -m metrics.dashboard

# Route a query
python -m operator.cli "your question"

# Browse org
cat orgs/BlackRoad-AI/README.md

# Check status
cat .STATUS

# Read memory
cat MEMORY.md
```

---

## The Pattern

```
          YOU
           │
           ▼
      ┌─────────┐
      │ INDEX.md│  ← Start here
      └────┬────┘
           │
     ┌─────┴─────┐
     ▼           ▼
  [Core]      [Orgs]
  Files      Blueprints
     │           │
     └─────┬─────┘
           ▼
      [Prototypes]
       Live Code
```

---

*The Bridge connects everything. The Index shows you where.*
