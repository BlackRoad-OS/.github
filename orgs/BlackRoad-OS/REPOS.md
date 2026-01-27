# BlackRoad-OS Repositories

> All repos that should exist in the core OS org

---

## Repository Map

```
BlackRoad-OS/
├── .github          ← THE BRIDGE (you're here!) ✔️ EXISTS
├── operator         ← The routing engine
├── control-plane    ← Unified dashboard
├── mesh             ← Tailscale + node configs
├── infra            ← Infrastructure as code
├── cli              ← Command line tools
└── sdk              ← Developer SDK
```

---

## Detailed Repo Specs

### 1. `.github` (THE BRIDGE) ✔️ EXISTS

**Status:** Active - you're reading this from inside it

**Purpose:** Central coordination point for the entire ecosystem

**Contents:**
```
.github/
├── .STATUS                    ← Real-time state beacon
├── BLACKROAD_ARCHITECTURE.md  ← The vision document
├── MEMORY.md                  ← Cece's persistent brain
├── REPO_MAP.md                ← Ecosystem overview
├── SIGNALS.md                 ← Morse code protocol
├── STREAMS.md                 ← Data flow patterns
├── orgs/                      ← Blueprints for ALL 15 orgs
│   ├── BlackRoad-AI/
│   ├── BlackRoad-OS/          ← This very blueprint!
│   └── ... (all 15)
└── profile/
    └── README.md              ← Org landing page
```

---

### 2. `operator`

**Status:** Planned (P0 - Critical)

**Purpose:** The brain that routes requests to the right destination

**Structure:**
```
operator/
├── src/
│   ├── parser/        ← Parse incoming requests
│   ├── classifier/    ← Classify request type
│   ├── router/        ← Route to destination
│   ├── signals/       ← Emit/receive signals
│   └── failover/      ← Handle failures
├── config/
│   ├── routes.yaml    ← Routing rules
│   └── providers.yaml ← Provider configs
├── tests/
└── README.md
```

**Key Features:**
- Parse any input (HTTP, webhook, CLI, signal)
- Classify intent (AI query, CRM lookup, storage, etc.)
- Route to correct org/service
- Handle failures gracefully
- Emit signals for observability

**Tech:** Python or Rust, stateless, runs on any node

---

### 3. `control-plane`

**Status:** Planned (P1)

**Purpose:** Unified dashboard to see and control everything

**Structure:**
```
control-plane/
├── frontend/          ← React/Next.js dashboard
│   ├── components/
│   ├── pages/
│   │   ├── overview/  ← System health at a glance
│   │   ├── nodes/     ← Pi cluster status
│   │   ├── orgs/      ← Org health
│   │   ├── signals/   ← Signal stream viewer
│   │   └── logs/      ← Audit log viewer
│   └── styles/
├── backend/           ← API for dashboard
│   ├── routes/
│   └── services/
└── README.md
```

**Key Features:**
- Real-time node health (lucidia, octavia, aria, alice, shellfish)
- Signal stream visualization
- Org status overview
- Log aggregation and search
- Alerting configuration

---

### 4. `mesh`

**Status:** Planned (P0 - Critical)

**Purpose:** Network configuration for all nodes

**Structure:**
```
mesh/
├── tailscale/
│   ├── acls.json      ← Access control lists
│   └── dns.json       ← DNS configuration
├── nodes/
│   ├── lucidia.yaml   ← Pi 5 + Hailo (Salesforce)
│   ├── octavia.yaml   ← Pi 5 + Hailo (AI routing)
│   ├── aria.yaml      ← Pi 5 (agents)
│   ├── alice.yaml     ← Pi 400 (K8s master)
│   ├── shellfish.yaml ← Digital Ocean (gateway)
│   ├── cecilia.yaml   ← Mac (dev)
│   └── arcadia.yaml   ← iPhone (mobile)
├── topology/
│   └── mesh.yaml      ← Overall network topology
└── README.md
```

**Key Features:**
- Tailscale VPN configuration
- Node definitions (hostname, IP, role, capabilities)
- Access control between nodes
- DNS for internal service discovery

---

### 5. `infra`

**Status:** Planned (P1)

**Purpose:** Infrastructure as code

**Structure:**
```
infra/
├── terraform/
│   ├── digitalocean/  ← Shellfish droplet
│   ├── cloudflare/    ← DNS, workers, tunnels
│   └── github/        ← Org settings, repos
├── ansible/
│   ├── playbooks/     ← Node setup playbooks
│   └── inventory/     ← Node inventory
├── docker/
│   └── compose/       ← Docker compose files
├── k8s/
│   └── manifests/     ← Kubernetes manifests (alice)
└── README.md
```

**Key Features:**
- Reproducible infrastructure
- Node provisioning automation
- Secret management
- Backup configuration

---

### 6. `cli`

**Status:** Planned (P2)

**Purpose:** Command line interface for BlackRoad

**Structure:**
```
cli/
├── src/
│   ├── commands/
│   │   ├── status.rs   ← br status
│   │   ├── route.rs    ← br route <query>
│   │   ├── signal.rs   ← br signal <msg>
│   │   └── org.rs      ← br org <name>
│   └── main.rs
├── Cargo.toml
└── README.md
```

**Example Commands:**
```bash
br status              # Show system status
br route "What is X?"  # Route a query
br signal "✔️ done"    # Send a signal
br org ai status       # Check AI org status
br nodes               # List all nodes
```

---

### 7. `sdk`

**Status:** Planned (P2)

**Purpose:** Developer SDK for building on BlackRoad

**Structure:**
```
sdk/
├── python/
│   └── blackroad/
│       ├── client.py
│       ├── signals.py
│       └── router.py
├── typescript/
│   └── src/
│       ├── client.ts
│       ├── signals.ts
│       └── router.ts
├── examples/
└── README.md
```

**Example Usage:**
```python
from blackroad import Client

client = Client()
response = client.route("What is the weather?")
client.signal("✔️", "OS", "AI", "Query complete")
```

---

## Priority Order

| Priority | Repo | Why |
|----------|------|-----|
| P0 | `.github` | ✔️ Done - The Bridge is live |
| P0 | `operator` | Core routing - nothing works without it |
| P0 | `mesh` | Network config - nodes need to talk |
| P1 | `control-plane` | Visibility - need to see what's happening |
| P1 | `infra` | Reproducibility - can rebuild anything |
| P2 | `cli` | Developer experience |
| P2 | `sdk` | External developers |

---

## Repo Creation Checklist

When creating each repo:

- [ ] Initialize with README.md from this spec
- [ ] Add .github/CODEOWNERS
- [ ] Set up branch protection
- [ ] Add to control-plane monitoring
- [ ] Signal to Bridge: `✔️ OS → OS : repo created`

---

*These repos are the foundation. Everything else builds on top.*
