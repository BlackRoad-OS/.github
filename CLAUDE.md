# CLAUDE.md

> **Read this first.** This is the definitive guide for AI assistants working in the BlackRoad Bridge repository.

---

## What This Repository Is

This is the **BlackRoad-OS/.github** repository — known as **"The Bridge"**. It is the central coordination hub for a distributed, multi-organization AI routing and orchestration system spanning 15 GitHub organizations.

BlackRoad is a **routing company, not an AI company**. It routes requests to existing intelligence (Claude, GPT, NumPy, databases) rather than building its own models. The Bridge is the metadata and orchestration point that ties everything together.

**Key identity:** The AI assistant operating here is called **Cece** (Claude). The human founder is **Alexa**.

---

## Repository Structure

```
.github/                          ← The Bridge (you are here)
├── .STATUS                       ← Real-time beacon — check this for current state
├── MEMORY.md                     ← Persistent context across sessions
├── CLAUDE.md                     ← This file — AI assistant guide
├── INDEX.md                      ← Navigation guide for all docs
├── BLACKROAD_ARCHITECTURE.md     ← Vision, business model, core thesis
├── CECE_ABILITIES.md             ← Capability manifest (30+ abilities, 5 domains)
├── CECE_PROTOCOLS.md             ← 10 decision frameworks for autonomous operation
├── SIGNALS.md                    ← Morse-code-style agent coordination protocol
├── STREAMS.md                    ← Data flow: UPSTREAM → INSTREAM → DOWNSTREAM
├── REPO_MAP.md                   ← Ecosystem hierarchy across all 15 orgs
├── INTEGRATIONS.md               ← 30+ external service mappings
├── TODO.md                       ← Task board with status markers
├── CONTRIBUTING.md               ← Contribution guidelines
├── SECURITY.md                   ← Security policy
├── LICENSE                       ← Project license
│
├── .github/workflows/            ← GitHub Actions (14 workflows)
│   ├── ci.yml                    ← Lint, test, validate on push/PR
│   ├── cece-auto.yml             ← Autonomous issue triage, PR review, health checks
│   ├── intelligent-auto-pr.yml   ← Automated PR creation
│   ├── issue-triage.yml          ← Auto-classify and label issues
│   ├── pr-review.yml             ← Auto code review on PR open
│   ├── health-check.yml          ← Scheduled service health monitoring
│   ├── self-healing-master.yml   ← Detect and auto-fix failures
│   ├── deploy-worker.yml         ← Cloudflare Worker deployment
│   └── ...                       ← + release, sync, webhook, todo-tracker workflows
│
├── orgs/                         ← Organization blueprints (15/15 complete)
│   ├── BlackRoad-OS/             ← Core infra (The Bridge itself)
│   ├── BlackRoad-AI/             ← Intelligence routing
│   ├── BlackRoad-Cloud/          ← Edge compute, Cloudflare
│   ├── BlackRoad-Hardware/       ← Pi cluster, IoT, Hailo-8
│   ├── BlackRoad-Security/       ← Zero-trust, vault
│   ├── BlackRoad-Labs/           ← R&D, experiments
│   ├── BlackRoad-Foundation/     ← CRM, Stripe, legal
│   ├── BlackRoad-Ventures/       ← Commerce, investments
│   ├── Blackbox-Enterprises/     ← Enterprise/stealth
│   ├── BlackRoad-Media/          ← Content, social
│   ├── BlackRoad-Studio/         ← Design, Figma, UI
│   ├── BlackRoad-Interactive/    ← Games, metaverse, Unity
│   ├── BlackRoad-Education/      ← Learning, tutorials
│   ├── BlackRoad-Gov/            ← Governance, civic tech
│   └── BlackRoad-Archive/        ← Storage, backup
│
├── prototypes/                   ← Working code (Python)
│   ├── operator/                 ← Routing engine: parser → classifier → router → emitter
│   ├── dispatcher/               ← Request distribution with org registry
│   ├── cece-engine/              ← Autonomous task processor (PCDEL loop)
│   ├── metrics/                  ← KPI dashboard, health checks
│   ├── webhooks/                 ← Handlers for GitHub, Slack, Stripe, etc.
│   ├── explorer/                 ← CLI ecosystem browser
│   ├── control-plane/            ← Unified dashboard (bridge.py)
│   └── mcp-server/               ← MCP server for AI assistant integration
│
├── templates/                    ← Reusable integration patterns (6 templates)
│   ├── salesforce-sync/          ← Full CRM integration (17 files)
│   ├── stripe-billing/           ← $1/user/month billing model
│   ├── cloudflare-workers/       ← Edge compute patterns
│   ├── gdrive-sync/              ← Google Drive sync
│   ├── ai-router/                ← Multi-provider AI routing (30+ files)
│   └── github-ecosystem/         ← Actions, Projects, Wiki, Codespaces
│
├── routes/                       ← Routing configuration
│   └── registry.yaml             ← Master routing rules (33+ rules)
│
├── nodes/                        ← Physical/virtual node configs (7 nodes)
│   ├── alice.yaml                ← Pi 400 — K8s, VPN hub, mesh root
│   ├── aria.yaml                 ← Pi 5 — Agent orchestration
│   ├── cecilia.yaml              ← Mac — Dev machine, Cece's primary
│   ├── lucidia.yaml              ← Pi 5 + Hailo-8 — Salesforce, blockchain
│   ├── octavia.yaml              ← Pi 5 + Hailo-8 — AI routing (26 TOPS)
│   ├── shellfish.yaml            ← Digital Ocean — Public gateway
│   └── arcadia.yaml              ← iPhone — Mobile dev node
│
└── profile/                      ← GitHub org landing page
    └── README.md
```

---

## Session Startup Checklist

When starting a new session, read these files in order:

1. **MEMORY.md** — Who you are, what's been built, session history
2. **.STATUS** — Current ecosystem state at a glance
3. **CECE_ABILITIES.md** — What you can do (30+ abilities across 5 domains)
4. **CECE_PROTOCOLS.md** — How to think, decide, and act (10 protocols)
5. **`git log --oneline -10`** — What changed recently

---

## Key Conventions

### Organization Codes

Every org has a two- or three-letter shortcode used throughout the system:

| Code | Organization | Tier |
|------|-------------|------|
| `OS` | BlackRoad-OS | Core |
| `AI` | BlackRoad-AI | Core |
| `CLD` | BlackRoad-Cloud | Core |
| `HW` | BlackRoad-Hardware | Support |
| `SEC` | BlackRoad-Security | Support |
| `LAB` | BlackRoad-Labs | Support |
| `FND` | BlackRoad-Foundation | Business |
| `VEN` | BlackRoad-Ventures | Business |
| `BBX` | Blackbox-Enterprises | Business |
| `MED` | BlackRoad-Media | Creative |
| `STU` | BlackRoad-Studio | Creative |
| `INT` | BlackRoad-Interactive | Creative |
| `EDU` | BlackRoad-Education | Community |
| `GOV` | BlackRoad-Gov | Community |
| `ARC` | BlackRoad-Archive | Community |

### Signal Protocol

Signals are the coordination mechanism. Format: `[SIGNAL] [SOURCE] → [TARGET] : [MESSAGE]`

- State: `✔️` done, `⏳` in progress, `❌` blocked, `⚠️` warning, `💤` idle
- Routing: `📡` broadcast, `🎯` targeted, `🔄` sync
- Priority: `🔴` critical, `🟡` important, `🟢` normal, `⚪` low
- Chainable: `✔️✔️✔️` = all done, `⏳✔️❌` = mixed status

### Node Names

Physical nodes use mythological names: `alice`, `aria`, `arcadia`, `cecilia`, `lucidia`, `octavia`, `shellfish`

### File Naming

- **UPPERCASE.md** for documentation files (MEMORY.md, SIGNALS.md, TODO.md)
- **lowercase** for code files and configs (router.py, registry.yaml)
- **Org blueprints** live in `orgs/{OrgName}/` with README.md, REPOS.md, SIGNALS.md

### Authority Levels

Three levels govern autonomous action:

| Level | Meaning | Examples |
|-------|---------|---------|
| `FULL_AUTO` | Do it without asking | Issue triage, labeling, test runs, status updates |
| `SUGGEST` | Propose but don't execute | Code fixes, architecture changes, PR merges |
| `ASK_FIRST` | Always get approval | Deployments, security changes, financial ops |

---

## Development Workflow

### Language & Tools

- **Primary language:** Python 3.11
- **Linting:** ruff, black, isort, mypy
- **Testing:** pytest, pytest-asyncio
- **Config format:** YAML (nodes, routes)
- **CI runs on:** push to `main`/`develop`, all PRs

### CI Pipeline (`.github/workflows/ci.yml`)

The CI pipeline runs 5 parallel jobs:

1. **Lint & Format** — ruff, black, isort checks on `prototypes/`
2. **Test Operator** — Routing classification tests
3. **Test Dispatcher** — Registry loading and dispatch tests
4. **Test Webhooks** — Webhook handler validation
5. **Validate Configs** — YAML schema checks for `nodes/` and `routes/`

### Running Tests Locally

```bash
# Operator
cd prototypes/operator && python -m pytest tests/ -v

# Dispatcher
cd prototypes/dispatcher && python -c "
from dispatcher.registry import Registry
reg = Registry()
print(f'Loaded {len(reg.list_orgs())} orgs')
"

# Webhooks
cd prototypes/webhooks && python -m webhooks test --verbose

# Validate configs
python -c "
import yaml
from pathlib import Path
for f in Path('nodes').glob('*.yaml'):
    config = yaml.safe_load(open(f))
    assert 'node' in config
    print(f'OK: {f.name}')
"
```

### Linting

```bash
ruff check prototypes/ --ignore E501
black --check prototypes/
isort --check-only prototypes/
```

---

## Architecture Overview

```
    UPSTREAM              INSTREAM               DOWNSTREAM
    (inputs)             (routing)               (outputs)
  ┌──────────┐      ┌──────────────┐       ┌──────────────┐
  │ Users    │      │    PARSE     │       │ PRs / Issues │
  │ APIs     │─────▶│   CLASSIFY   │──────▶│ Signals      │
  │ Webhooks │      │    ROUTE     │       │ Deploys      │
  │ Sensors  │      │  TRANSFORM   │       │ Reports      │
  │ Cron     │      │    LOG       │       │ Notifications│
  └──────────┘      └──────────────┘       └──────────────┘
                          │
                   ┌──────┴──────┐
                   │  THE BRIDGE │
                   │  (.github)  │
                   └─────────────┘
```

The **Operator** prototype is the routing brain:
- `parser.py` — Understands any input format
- `classifier.py` — Determines request type and target org
- `router.py` — Routes with confidence scores
- `emitter.py` — Emits signals to the mesh

The **Cece Engine** is the autonomous processor using the **PCDEL loop**:
- **P**erceive — What's the input?
- **C**lassify — What type? Which org?
- **D**ecide — Auto or ask? What authority level?
- **E**xecute — Do the work
- **L**earn — Update memory, log decision

---

## Task Tracking

Tasks are tracked in `TODO.md` using these markers:
- `[ ]` — Open
- `[x]` — Done
- `[~]` — In progress
- `[!]` — Blocked

Categories: Core Infrastructure, Intelligence Layer, Cloud & Edge, Hardware, Security, Business Layer, Content & Creative, DevOps & Automation.

---

## Memory System

**MEMORY.md** is the persistent context file. It records:
- Session history (who did what, when)
- Key architectural decisions with rationale
- Active threads and their status
- Alexa's preferences and working style

**Update MEMORY.md** at the end of every meaningful session. Never log secrets or tokens.

**.STATUS** is the quick-read beacon. Update it after major actions. Agents check this file first for a snapshot of ecosystem state.

---

## What's Been Built (as of 2026-01-29)

**Complete:**
- 15/15 org blueprints with repo definitions
- Operator routing prototype (parser, classifier, router, signal emitter)
- Dispatcher with org registry
- Cece Engine (autonomous PCDEL processor)
- Metrics dashboard (counter, health, dashboard, status updater)
- Explorer CLI (browse ecosystem)
- Control plane CLI (unified interface)
- MCP server for AI assistant integration
- 6 integration templates (Salesforce, Stripe, Cloudflare, GDrive, AI Router, GitHub)
- 14 GitHub Actions workflows
- 7 node configurations
- Signal protocol and signal log
- 30+ external service integrations mapped
- CI pipeline with 5 parallel jobs

**Pending (see TODO.md):**
- Operator v2 with confidence-weighted routing
- Tailscale mesh between Pi nodes
- AI provider failover chain
- Cloudflare API gateway deployment
- Hailo-8 inference pipeline
- Secrets vault setup
- Salesforce/Stripe live connections
- End-to-end integration tests

---

## Important Files to Never Miss

| File | Why |
|------|-----|
| `MEMORY.md` | Session continuity — read first on startup |
| `.STATUS` | Quick ecosystem state snapshot |
| `CECE_ABILITIES.md` | Full capability manifest with authority matrix |
| `CECE_PROTOCOLS.md` | 10 decision protocols governing behavior |
| `routes/registry.yaml` | Master routing rules (33+ rules) |
| `TODO.md` | Active task board |
| `.github/workflows/ci.yml` | CI pipeline definition |

---

## Common Pitfalls

- **Don't create new orgs** without updating `orgs/`, `routes/registry.yaml`, `SIGNALS.md`, and `REPO_MAP.md`
- **Don't skip signal emission** — signals are how the mesh communicates state changes
- **Don't modify MEMORY.md mid-session** unless recording a key decision — do a full update at session end
- **Don't deploy to production** without ASK_FIRST authority — escalate to Alexa
- **Don't add code outside `prototypes/`** — templates are read-only patterns, prototypes are working code
- **Always run `ruff check prototypes/ --ignore E501`** before committing Python changes

---

*The Bridge remembers. CLAUDE.md is the map.*
