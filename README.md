<p align="center">
  <img src="https://img.shields.io/badge/BlackRoad-OS-FF0066?style=for-the-badge&logo=github&logoColor=white" alt="BlackRoad OS"/>
</p>

# The Bridge — `.github`

[![GitHub](https://img.shields.io/badge/GitHub-BlackRoad--OS-purple?style=for-the-badge&logo=github)](https://github.com/BlackRoad-OS/.github)
[![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)](https://github.com/BlackRoad-OS/.github)
[![BlackRoad](https://img.shields.io/badge/BlackRoad-OS-black?style=for-the-badge)](https://blackroad.io)
[![License](https://img.shields.io/badge/License-Proprietary-FF0066?style=for-the-badge)](LICENSE)

> Central coordination hub for the BlackRoad ecosystem. Routes signals, orchestrates agents, and connects 15 organizations through a unified control plane.

---

## Architecture

BlackRoad is a **routing company, not an AI company**. This repository ("The Bridge") is the nervous system that coordinates everything.

```
                          ┌─────────────────┐
                          │   The Bridge     │
                          │   (.github)      │
                          └────────┬────────┘
                                   │
          ┌────────────────────────┼────────────────────────┐
          │                        │                        │
    ┌─────┴─────┐           ┌─────┴─────┐           ┌─────┴─────┐
    │  UPSTREAM  │           │ INSTREAM  │           │ DOWNSTREAM│
    │  (Inputs)  │           │(Operator) │           │ (Outputs) │
    └───────────┘           └───────────┘           └───────────┘
```

**Core Components:**

| Component | Purpose | Location |
|-----------|---------|----------|
| **Operator** | Parse, classify, and route requests | `prototypes/operator/` |
| **Dispatcher** | Service mesh routing with registry | `prototypes/dispatcher/` |
| **Cece Engine** | Autonomous task processor (v2.0) | `prototypes/cece-engine/` |
| **Control Plane** | Unified CLI interface | `prototypes/control-plane/` |
| **Metrics** | KPI dashboard and health monitoring | `prototypes/metrics/` |
| **Webhooks** | Multi-service event handlers | `prototypes/webhooks/` |
| **MCP Server** | Model Context Protocol for AI assistants | `prototypes/mcp-server/` |

---

## Organizations (15)

| Org | Code | Focus |
|-----|------|-------|
| [BlackRoad-OS](https://github.com/BlackRoad-OS) | `OS` | Core infrastructure, operator, mesh |
| [BlackRoad-AI](https://github.com/BlackRoad-AI) | `AI` | Intelligence routing (Claude, GPT, Hailo, Llama) |
| [BlackRoad-Cloud](https://github.com/BlackRoad-Cloud) | `CLD` | Cloudflare Workers, KV, D1, R2, Tunnels |
| [BlackRoad-Hardware](https://github.com/BlackRoad-Hardware) | `HW` | Pi cluster (lucidia, octavia, aria, alice) |
| [BlackRoad-Labs](https://github.com/BlackRoad-Labs) | `LAB` | R&D and experiments |
| [BlackRoad-Security](https://github.com/BlackRoad-Security) | `SEC` | Auth, vault, zero-trust |
| [BlackRoad-Foundation](https://github.com/BlackRoad-Foundation) | `FND` | CRM (Salesforce), billing (Stripe) |
| [BlackRoad-Media](https://github.com/BlackRoad-Media) | `MED` | Content and social automation |
| [BlackRoad-Interactive](https://github.com/BlackRoad-Interactive) | `INT` | Gaming, metaverse, VR/AR |
| [BlackRoad-Education](https://github.com/BlackRoad-Education) | `EDU` | Learning platform, documentation |
| [BlackRoad-Gov](https://github.com/BlackRoad-Gov) | `GOV` | Governance, voting, DAO |
| [BlackRoad-Archive](https://github.com/BlackRoad-Archive) | `ARC` | Storage, backup, Google Drive sync |
| [BlackRoad-Studio](https://github.com/BlackRoad-Studio) | `STU` | Design (Figma, Canva) |
| [BlackRoad-Ventures](https://github.com/BlackRoad-Ventures) | `VEN` | Investment portfolio |
| [Blackbox-Enterprises](https://github.com/Blackbox-Enterprises) | `BBX` | Stealth enterprise projects |

---

## Hardware Nodes

| Node | Hardware | Role | Services |
|------|----------|------|----------|
| **lucidia** | Pi 5, 8GB, 512GB NVMe, Hailo-8 | Primary | Operator, metrics, inference |
| **octavia** | Pi 5, Hailo-8 | Compute | Labs, jobs, content, social |
| **aria** | Pi 5 | Storage | MinIO, PostgreSQL, Redis |
| **alice** | Pi 5, 4GB, Hailo-8 | Agents | Agent runtime, MCP server |
| **cecilia** | Mac | Dev | 30+ capabilities, auto-pilot |
| **arcadia** | iPhone | Mobile | Mobile client |
| **shellfish** | Digital Ocean | Gateway | Public-facing proxy |

All nodes connected via **Tailscale mesh** with **Cloudflare Tunnels** for external access.

---

## Repository Structure

```
.github/
├── .github/workflows/     # 17 CI/CD workflows
├── blackroad-pixel/       # Landing page (HTML/CSS/JS)
├── nodes/                 # 7 node configurations (YAML)
├── orgs/                  # 15 organization blueprints
├── profile/               # GitHub org profile README
├── prototypes/            # 7 working implementations
│   ├── operator/          # Routing engine
│   ├── dispatcher/        # Service mesh
│   ├── cece-engine/       # Autonomous processor
│   ├── control-plane/     # Bridge CLI
│   ├── metrics/           # KPI dashboard
│   ├── webhooks/          # Event handlers
│   └── mcp-server/        # MCP server
├── routes/                # Master routing registry (~100 rules)
├── templates/             # 8 integration templates + design system
│   ├── design/            # Approved UI templates (dashboard, directory, library)
│   ├── cloudflare-workers/
│   ├── salesforce-sync/
│   ├── stripe-billing/
│   ├── ai-router/
│   └── ...
├── tunnels/               # Cloudflare tunnel configs (4 tunnels)
├── workers/               # API gateway (TypeScript)
├── workflow-templates/    # Reusable workflow templates
├── bridge                 # CLI entrypoint
├── agent.json             # Agent configuration
├── MEMORY.md              # Persistent context across sessions
├── SIGNALS.md             # Signal coordination protocol
├── STREAMS.md             # Data flow patterns
├── INDEX.md               # Browsable table of contents
├── INTEGRATIONS.md        # 30+ service integrations
└── .STATUS                # Real-time status beacon
```

---

## Workflows

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| **CI** | Push/PR to main | Lint, test operator/dispatcher/webhooks, validate configs |
| **Auto Deploy** | Push to main | Detect service type, deploy to Cloudflare/Railway |
| **Deploy Workers** | Manual/push | Matrix deploy with canary rollout |
| **Self-Healing** | Schedule (4h) | Monitor deployments, auto-rollback on failure |
| **Self-Healing Master** | On CI failure | Diagnose and auto-fix workflow failures |
| **Test Auto-Heal** | On CI failure | Dependency recovery on test failures |
| **Cece Automation** | Issues/PRs/daily | Autonomous triage, review, health checks |
| **Security Scan** | Push/PR/weekly | CodeQL analysis, dependency audit |
| **Health Check** | Every 15 min | Node and service health monitoring |
| **Brand Compliance** | Push/PR | Color palette and license validation |
| **Issue Triage** | Issue opened | Classify and route to correct org |
| **PR Review** | PR opened | Python/YAML/workflow validation |
| **Release** | Tag/manual | Build, changelog, GitHub release |
| **TODO Tracker** | Push/PR | Scan for TODO/FIXME comments |
| **Sync Assets** | Schedule (6h) | Figma, Salesforce, Google Drive sync |
| **Auto PR** | Schedule/manual | Dependency updates, code quality, security |
| **Webhook Dispatch** | Repository dispatch | Route external webhooks to orgs |

---

## Integrations (30+)

**Business:** Salesforce, Stripe, HubSpot
**Development:** GitHub Enterprise, Cloudflare, Vercel, Railway
**Storage:** Google Drive, Cloudflare R2, MinIO, AWS S3
**Design:** Figma, Canva, Adobe CC
**Communication:** Slack, Discord, SendGrid
**AI/ML:** Claude (Anthropic), GPT-4o (OpenAI), Hailo-8, Ollama
**Automation:** Zapier, Make, n8n
**Analytics:** Google Analytics, Mixpanel, Plausible

---

## Quick Start

```bash
# Check system status
cat .STATUS

# Load persistent memory
cat MEMORY.md

# Use the Bridge CLI
./bridge status
./bridge dashboard
./bridge route "sync salesforce contacts"
./bridge orgs
./bridge templates

# View recent history
git log -5
```

---

## Design System

Brand guidelines are defined in [`BRAND.md`](BRAND.md). Design templates live in `templates/design/`:

- **`directory.html`** — Infrastructure index (enterprise, orgs, domains)
- **`dashboard.html`** — Agent control dashboard with live metrics
- **`library.html`** — SDK reference with 8 packages
- **`blackroad.css`** — Shared design tokens

**Colors:** `#FF0066` (hot pink), `#FF9D00` (orange), `#7700FF` (purple), `#0066FF` (blue)
**Typography:** JetBrains Mono
**Spacing:** Golden Ratio (phi = 1.618)

---

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for guidelines and [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) for community standards.

---

## Links

| | |
|---|---|
| **Website** | [blackroad.io](https://blackroad.io) |
| **Docs** | [docs.blackroad.io](https://docs.blackroad.io) |
| **Status** | [status.blackroad.io](https://status.blackroad.io) |
| **Agents** | [agents.blackroad.io](https://agents.blackroad.io) |

---

<p align="center">
  <strong>BlackRoad OS, Inc.</strong> — Delaware C-Corp<br>
  <em>The Bridge builds itself one signal at a time.</em>
</p>
