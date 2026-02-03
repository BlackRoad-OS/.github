# CLAUDE.md

> Instructions and context for AI assistants working in the BlackRoad OS Bridge repository.

---

## Project Overview

This is **BlackRoad OS's `.github` repository**, known as **"The Bridge"** -- the central coordination hub for a 15-organization distributed intelligence routing platform. BlackRoad is a **routing company, not an AI company**. It connects users to existing intelligence (Claude, GPT, Llama, NumPy, databases, APIs) through an orchestration layer running on owned hardware.

**Owner:** BlackRoad OS, Inc. (CEO: Alexa Amundson)
**License:** Proprietary (testing/educational use only; see LICENSE)
**Contact:** blackroad.systems@gmail.com

---

## Repository Structure

```
.github/                        # The Bridge - central coordination
├── CLAUDE.md                   # This file - AI assistant instructions
├── MEMORY.md                   # Persistent context across sessions
├── .STATUS                     # Real-time state beacon for agents
├── BLACKROAD_ARCHITECTURE.md   # Core vision and architecture
├── CECE_PROTOCOLS.md           # Decision frameworks (PCDEL loop)
├── CECE_ABILITIES.md           # AI capability manifest (30+ abilities)
├── SIGNALS.md                  # Morse-code-style coordination protocol
├── STREAMS.md                  # Data flow patterns (upstream/instream/downstream)
├── REPO_MAP.md                 # Full ecosystem map
├── INDEX.md                    # Browsable table of contents
├── INTEGRATIONS.md             # 30+ external service mappings
├── SECURITY.md                 # Vulnerability reporting policy
├── CODE_OF_CONDUCT.md          # Community standards
├── CONTRIBUTING.md             # Contribution guidelines
├── TODO.md                     # Task board
├── LICENSE                     # Proprietary license
├── README.md                   # Repository intro
│
├── .github/workflows/          # 13 GitHub Actions workflows
│   ├── ci.yml                  # Continuous integration
│   ├── cece-auto.yml           # Autonomous Cece task automation
│   ├── issue-triage.yml        # Auto-classify and label issues
│   ├── pr-review.yml           # Automated code review
│   ├── health-check.yml        # Service health monitoring
│   ├── self-healing-master.yml # Error recovery automation
│   ├── intelligent-auto-pr.yml # Auto-generate PRs
│   ├── release.yml             # Release automation
│   ├── todo-tracker.yml        # Auto-create issues from TODOs
│   ├── webhook-dispatch.yml    # Webhook routing
│   ├── deploy-worker.yml       # Cloudflare Worker deployment
│   ├── sync-assets.yml         # Asset synchronization
│   └── test-auto-heal.yml      # Test automation recovery
│
├── profile/                    # GitHub organization profile
│   └── README.md
│
├── orgs/                       # 15 organization blueprints
│   ├── BlackRoad-OS/           # Core infrastructure (The Bridge)
│   ├── BlackRoad-AI/           # AI/ML routing
│   ├── BlackRoad-Cloud/        # Edge compute, Cloudflare
│   ├── BlackRoad-Hardware/     # Pi cluster, Hailo-8
│   ├── BlackRoad-Security/     # Zero trust, vault
│   ├── BlackRoad-Labs/         # R&D experiments
│   ├── BlackRoad-Foundation/   # CRM, billing, Salesforce, Stripe
│   ├── BlackRoad-Media/        # Content, social
│   ├── BlackRoad-Studio/       # Design, Figma, Canva
│   ├── BlackRoad-Interactive/  # Gaming, metaverse
│   ├── BlackRoad-Education/    # Learning platform
│   ├── BlackRoad-Gov/          # Governance, voting
│   ├── BlackRoad-Archive/      # Preservation, Drive sync
│   ├── BlackRoad-Ventures/     # Investments
│   └── Blackbox-Enterprises/   # Stealth projects
│
├── nodes/                      # Physical node configurations (YAML)
│   ├── cecilia.yaml            # Dev node (local laptop, ACTIVE)
│   ├── lucidia.yaml            # Primary (Pi 5 + Hailo-8)
│   ├── octavia.yaml            # Compute (Pi 5 + Hailo-8)
│   ├── aria.yaml               # Storage (Pi 5 + NVMe)
│   ├── alice.yaml              # Agents (Pi 5, K8s)
│   ├── shellfish.yaml          # Cloud gateway (Digital Ocean)
│   └── arcadia.yaml            # Mobile (iPhone)
│
├── routes/
│   └── registry.yaml           # 33+ routing rules mapping keywords to orgs
│
├── prototypes/                 # 8 working prototype modules
│   ├── operator/               # Routing engine (parser, classifier, router, emitter)
│   ├── metrics/                # KPI dashboard and health checks
│   ├── explorer/               # Ecosystem CLI browser
│   ├── cece-engine/            # PERCEIVE-CLASSIFY-DECIDE-EXECUTE-LEARN loop
│   ├── mcp-server/             # Model Context Protocol server
│   ├── dispatcher/             # Request dispatching
│   ├── control-plane/          # Unified dashboard
│   └── webhooks/               # Webhook handlers (GitHub, Stripe, Slack, etc.)
│
├── templates/                  # 7 reusable integration templates
│   ├── salesforce-sync/        # CRM sync engine
│   ├── ai-router/              # Multi-provider AI routing
│   ├── cloudflare-workers/     # Edge compute
│   ├── gdrive-sync/            # Google Drive sync
│   ├── stripe-billing/         # $1/user/month billing model
│   ├── github-ecosystem/       # GitHub Actions, Projects, etc.
│   └── design-tools/           # Figma, Canva integration
│
└── blackroad-pixel/            # Pixel art assets
```

---

## Key Concepts

### The Bridge

This repository (`.github`) is the central coordination point for the entire BlackRoad ecosystem. All signals, memory, routing rules, and org blueprints flow through here. Think of it as the nervous system connecting all 15 organizations.

### Routing, Not Building

BlackRoad does not train models or own GPUs. It routes requests to the right tool at the right time. The `Operator` pattern is:

```
[User Request] -> [Operator] -> [Route to Right Tool] -> [Answer]
```

### Organization Codes

15 orgs, each with a shortcode used in routing and signals:

| Code | Organization | Focus |
|------|-------------|-------|
| OS | BlackRoad-OS | Core infrastructure, The Bridge |
| AI | BlackRoad-AI | AI/ML routing |
| CLD | BlackRoad-Cloud | Edge compute, Cloudflare |
| HW | BlackRoad-Hardware | Pi cluster, Hailo-8, IoT |
| SEC | BlackRoad-Security | Zero trust, secrets, auth |
| LAB | BlackRoad-Labs | R&D experiments |
| FND | BlackRoad-Foundation | CRM, billing (Salesforce, Stripe) |
| MED | BlackRoad-Media | Content, social |
| STU | BlackRoad-Studio | Design (Figma, Canva) |
| INT | BlackRoad-Interactive | Gaming, metaverse |
| EDU | BlackRoad-Education | Learning platform |
| GOV | BlackRoad-Gov | Governance, voting |
| ARC | BlackRoad-Archive | Storage, backup |
| VEN | BlackRoad-Ventures | Investments |
| BBX | Blackbox-Enterprises | Stealth projects |

### Node Mesh

Physical hardware running specialized roles over Tailscale mesh networking:

| Node | Hardware | Role |
|------|----------|------|
| lucidia | Pi 5 + Hailo-8 | Primary: Salesforce sync, blockchain |
| octavia | Pi 5 + Hailo-8 | Compute: AI routing (26 TOPS) |
| aria | Pi 5 + NVMe | Storage: agent orchestration |
| alice | Pi 5 | Agents: K8s + VPN hub |
| shellfish | Digital Ocean | Cloud: public-facing gateway |
| cecilia | Local dev machine | Dev: Claude Code sessions |
| arcadia | iPhone | Mobile |

### Signal Protocol

Lightweight morse-code-style coordination between agents:

```
[TIMESTAMP] [SIGNAL] [SOURCE] -> [TARGET] : [MESSAGE]
```

Signals: `done`, `in-progress`, `blocked`, `broadcast`, `targeted`

### Data Flow Pattern (Streams)

```
UPSTREAM (input) -> INSTREAM (processing) -> DOWNSTREAM (output)
```

### PCDEL Processing Loop

All tasks follow: **PERCEIVE -> CLASSIFY -> DECIDE -> EXECUTE -> LEARN**

---

## Development Conventions

### Languages and Tools

- **Python** for prototypes and automation (pytest for tests)
- **JavaScript/TypeScript** for edge workers and web (vitest/jest for tests)
- **YAML** for configuration (nodes, routes, services)
- **Markdown** for documentation and protocols
- **Bash** for scripts and CLI tools
- **GitHub Actions** for CI/CD and automation

### Commit Message Format

```
<type>(<scope>): <subject>

Types: feat, fix, docs, style, refactor, test, chore
```

Examples:
```
feat(operator): Add keyword-based routing
fix(metrics): Resolve dashboard counter reset
docs(memory): Update session 3 summary
```

### File Naming

- Configuration: `*.yaml`
- Documentation: `README.md` in each directory, `UPPERCASE.md` for top-level docs
- State files: `.STATUS` (beacon), `MEMORY.md` (persistent context)
- Protocols: `CECE_PROTOCOLS.md`, `CECE_ABILITIES.md`

### Branch Naming

- Claude Code branches: `claude/<description>-<session-id>`
- Feature branches: `feature/<description>`

### Principles (from CONTRIBUTING.md)

- **Sovereignty**: Users own their data and infrastructure
- **Privacy**: No telemetry, tracking, or external dependencies
- **Offline-First**: Features should work without internet
- **No Vendor Lock-in**: Own the hardware, command the utilities
- **Route, Don't Build**: Connect to existing intelligence

### What NOT to Do

- No external analytics or telemetry
- No required internet connectivity for core features
- No vendor lock-in mechanisms
- No cloud-only functionality
- No compromising user privacy
- No committing secrets, tokens, or passwords

---

## Decision Authority (for AI Agents)

### FULL AUTO (no approval needed)

- Read any file/repo in the ecosystem
- Triage and label issues
- Comment on PRs with review
- Generate documentation
- Run tests and report results
- Update `.STATUS` beacon
- Generate reports

### SUGGEST (create PR, needs approval)

- Code changes to existing files
- New feature implementations
- Dependency updates
- Configuration changes
- Infrastructure modifications
- Security patches

### ASK FIRST (needs explicit command)

- Delete repos or branches
- Modify org settings
- Change access/permissions
- Deploy to production
- Financial operations (Stripe)
- External API key rotation

---

## Key Files to Read First

When starting a new session, read these in order:

1. **CLAUDE.md** (this file) -- instructions and conventions
2. **MEMORY.md** -- persistent session context, what has been built
3. **.STATUS** -- real-time ecosystem state
4. **BLACKROAD_ARCHITECTURE.md** -- the vision and architecture
5. **CECE_PROTOCOLS.md** -- decision frameworks and escalation paths
6. **REPO_MAP.md** -- full ecosystem structure

For deeper context, also check:

- `CECE_ABILITIES.md` -- full capability manifest
- `INTEGRATIONS.md` -- external service mappings
- `routes/registry.yaml` -- routing rules
- `orgs/*/README.md` -- individual org blueprints
- `nodes/*.yaml` -- hardware node configurations

---

## Infrastructure

Monthly cost: ~$40

| Service | Role |
|---------|------|
| Cloudflare | Edge/CDN, DNS, DDoS protection, Workers |
| Salesforce (Free Dev) | CRM, 15K API calls/day |
| GitHub Enterprise | 15 orgs, CI/CD, code hosting |
| Tailscale | Mesh networking between nodes |
| Digital Ocean | Cloud gateway (shellfish node) |

---

## Routing Registry

The routing registry (`routes/registry.yaml`) maps keywords to organizations and services. When classifying a request:

- `salesforce` -> FND (salesforce service)
- `stripe`, `billing`, `payment` -> FND (stripe service)
- `cloudflare`, `worker`, `edge` -> CLD (worker service)
- `hailo`, `inference` -> HW (hailo service)
- `figma`, `canva`, `design` -> STU (figma service)
- `gdrive`, `google drive` -> ARC (gdrive service)
- General questions -> AI (router service, fallback)
- Code/development -> AI (router service)

Default fallback org: **AI**

---

## Prototype Modules

Each prototype in `prototypes/` is a standalone module:

| Prototype | Purpose | Key Files |
|-----------|---------|-----------|
| operator | Request routing engine | parser.py, classifier.py, router.py, emitter.py |
| metrics | KPI dashboard | counter.py, health.py, dashboard.py, status_updater.py |
| explorer | Ecosystem CLI browser | browser.py, cli.py |
| cece-engine | Autonomous task processing | engine.py (PCDEL loop) |
| mcp-server | Model Context Protocol | server for AI tool integration |
| dispatcher | Async request dispatching | dispatcher with registry |
| control-plane | Unified dashboard | dashboard interface |
| webhooks | External event handlers | handlers for GitHub, Stripe, Slack, Salesforce, Cloudflare, Figma, Google, Discord |

---

## Business Model

- **Core Platform**: $1/user/month (mass market)
- **Enterprise**: Custom pricing
- **Marketplace**: 10% transaction fee on plugins/templates

---

## Session History Summary

| Session | Date | Highlights |
|---------|------|------------|
| 1 | 2026-01-27 | Bridge established, 15 org blueprints, 3 prototypes, 6 templates, 90+ files |
| 2 | 2026-01-27 | Continuity test -- memory system verified working |
| 3 | 2026-01-29 | Cece v2.0 enhancement: 30+ abilities, 10 protocols, autonomous engine |

---

*Last updated: 2026-02-03*
*BlackRoad OS, Inc. -- Proprietary and Confidential*
