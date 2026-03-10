<p align="center">
  <img src="https://img.shields.io/badge/BlackRoad-OS-FF0066?style=for-the-badge&logo=github&logoColor=white" alt="BlackRoad OS"/>
</p>

# BlackRoad OS — The Bridge

[![GitHub](https://img.shields.io/badge/GitHub-BlackRoad--OS-purple?style=for-the-badge&logo=github)](https://github.com/BlackRoad-OS/.github)
[![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)](https://github.com/BlackRoad-OS/.github)
[![BlackRoad](https://img.shields.io/badge/BlackRoad-OS-black?style=for-the-badge)](https://blackroad.io)
[![CI](https://github.com/BlackRoad-OS/.github/actions/workflows/ci.yml/badge.svg)](https://github.com/BlackRoad-OS/.github/actions/workflows/ci.yml)

> **BlackRoad is a routing company, not an AI company.**
> We route requests to the right intelligence at the right time — Claude, GPT, Llama, Salesforce, local Hailo-8 inference — through an orchestration layer we own.

---

## What Is This Repository?

This is **The Bridge** — the central nervous system for the BlackRoad platform. It coordinates:

- **The Operator** — classifies any request and routes it to one of 15 specialized organizations
- **The Dispatcher** — takes classified requests and delivers them to real service endpoints
- **Webhook Receivers** — ingest events from GitHub, Stripe, Salesforce, Cloudflare, Slack, Figma, and Google
- **AI Failover Router** — chains Claude → GPT → Llama → local Hailo-8 with circuit breakers
- **Prompt Registry** — versioned prompt templates for all AI interactions
- **Token Tracker** — per-route token usage and cost accounting
- **Cece Engine** — autonomous task processing loop (PCDEL: Plan → Classify → Decide → Execute → Log)
- **MCP Server** — Model Context Protocol server for AI assistant integrations
- **API Gateway** — Cloudflare Worker fronting the entire platform
- **Pixel UI** — interactive desktop OS simulation and pixel game worlds

---

## Quick Start

```bash
# Clone and run the control plane CLI
git clone https://github.com/BlackRoad-OS/.github
cd .github
./bridge status       # Ecosystem health
./bridge route "sync salesforce contacts"  # Route a query
./bridge dashboard    # Full metrics dashboard
```

```bash
# Test the operator directly
cd prototypes/operator
python -c "
from routing.core.router import Operator
op = Operator()
result = op.route('What language model should I use?')
print(result)  # RouteResult(→ BlackRoad-AI [AI], conf=0.85)
"
```

```bash
# Run the webhook test suite
cd prototypes/webhooks
python -m webhooks test --verbose
# Results: 12 passed, 0 failed
```

---

## Repository Structure

```
.github/
├── prototypes/          # Working Python implementations
│   ├── operator/        # Request classification & routing core
│   ├── dispatcher/      # Route requests to service endpoints
│   ├── webhooks/        # Webhook receivers (GitHub, Stripe, etc.)
│   ├── ai-failover/     # AI provider failover chain
│   ├── cece-engine/     # Autonomous task processing (PCDEL loop)
│   ├── audit-log/       # Structured audit trail
│   ├── metrics/         # KPI dashboard and counters
│   ├── mcp-server/      # MCP protocol server for AI tools
│   ├── prompt-registry/ # Versioned prompt template registry
│   └── token-tracker/   # Token usage and cost tracking
│
├── templates/           # Integration templates
│   ├── ai-router/       # Multi-provider AI routing
│   ├── salesforce-sync/ # CRM synchronization
│   ├── stripe-billing/  # Payment processing
│   └── cloudflare-workers/ # Edge compute
│
├── workers/             # Cloudflare Workers
│   └── api-gateway/     # Public-facing API gateway (TypeScript)
│
├── blackroad-pixel/     # Interactive pixel art OS UI
│   └── games/           # Stardew, Pokemon, Webkinz, Mario clones
│
├── orgs/                # 15 organization blueprints
├── nodes/               # Hardware node configurations (Pi cluster)
├── routes/              # Routing registry (15 orgs, 21 rules)
├── tunnels/             # Cloudflare tunnel configs
└── .github/workflows/   # CI/CD pipelines
```

---

## The Routing Model

```
[Any Request]
      │
      ▼
 ┌──────────┐        ┌──────────────────────┐
 │ OPERATOR │───────►│  15 Organizations    │
 └──────────┘        ├──────────────────────┤
      │              │ OS  → Infrastructure │
      │              │ AI  → Language tasks │
      │              │ FND → CRM / billing  │
      │              │ SEC → Security       │
      │              │ CLD → Edge compute   │
      │              │ HW  → IoT / Pi       │
      │              │ ... → 9 more         │
      ▼              └──────────────────────┘
 ┌──────────┐
 │DISPATCHER│──► Real endpoints (Salesforce, Claude, Cloudflare...)
 └──────────┘
```

---

## Infrastructure (~$40/month)

| Layer | Service | Cost |
|-------|---------|------|
| Edge/CDN | Cloudflare Workers | Free tier |
| CRM | Salesforce Dev Edition | Free |
| Code/CI | GitHub | Included |
| Mesh | Tailscale VPN | Free tier |
| Gateway | Digital Ocean (Shellfish) | ~$6/mo |
| Compute | 4× Raspberry Pi + Mac | Owned hardware |

---

## Development

```bash
# Lint (must pass before merge)
ruff check prototypes/ --ignore E501

# Run operator tests
cd prototypes/operator && python -m pytest tests/ -v

# Run dispatcher tests
cd prototypes/dispatcher && python -m pytest tests/ -v

# Run webhook tests
cd prototypes/webhooks && python -m pytest tests/ -v
# or: python -m webhooks test --verbose

# Serve the pixel UI locally
cd blackroad-pixel && python3 -m http.server 8080
```

---

## Organization Map

| Code | Organization | Focus |
|------|-------------|-------|
| OS | BlackRoad-OS | Core infrastructure, operator, this repo |
| AI | BlackRoad-AI | AI routing, model inference |
| CLD | BlackRoad-Cloud | Cloudflare Workers, edge compute |
| HW | BlackRoad-Hardware | Raspberry Pi cluster, IoT, ESP32 |
| LAB | BlackRoad-Labs | R&D, experiments |
| SEC | BlackRoad-Security | Zero-trust, secrets, audit |
| FND | BlackRoad-Foundation | Salesforce CRM, Stripe billing |
| MED | BlackRoad-Media | Content, publishing |
| INT | BlackRoad-Interactive | Games, metaverse |
| EDU | BlackRoad-Education | Learning platform |
| GOV | BlackRoad-Gov | Civic tech, governance |
| ARC | BlackRoad-Archive | Storage, backup |
| STU | BlackRoad-Studio | Design tools |
| VEN | BlackRoad-Ventures | Commerce, investments |
| BBX | Blackbox-Enterprises | Enterprise solutions |

---

*BlackRoad OS, Inc. — Proprietary and Confidential*
