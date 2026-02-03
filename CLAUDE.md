# CLAUDE.md

> Instructions for AI assistants working in **BlackRoad-OS/.github** (The Bridge).

---

## What This Repository Is

This is the **organization-level GitHub configuration repository** for the BlackRoad ecosystem. It serves as "The Bridge" - the central coordination hub for a 15-organization distributed system. BlackRoad is a **routing company**: it connects users to existing intelligence (Claude, GPT, Llama, NumPy, legal databases, etc.) rather than building or training models itself.

**Core thesis:** Own the routing layer, not the intelligence. Control plane runs on owned hardware (Raspberry Pi cluster with Hailo-8 accelerators). Target: $1/user/month at scale.

---

## Repository Structure

```
.github/
├── CLAUDE.md                 ← You are here
├── MEMORY.md                 ← Persistent context across sessions (read first)
├── .STATUS                   ← Real-time state beacon (check on startup)
├── INDEX.md                  ← Navigable table of contents
├── BLACKROAD_ARCHITECTURE.md ← Vision, business model, infrastructure
├── SIGNALS.md                ← Morse-code-style coordination protocol
├── STREAMS.md                ← Upstream/Instream/Downstream data flows
├── REPO_MAP.md               ← Full ecosystem map (all orgs, repos)
├── INTEGRATIONS.md           ← 30+ external services mapped
├── CECE_PROTOCOLS.md         ← 10 decision & escalation frameworks
├── CECE_ABILITIES.md         ← 30+ capabilities manifest
├── SECURITY.md               ← Security policy
├── CONTRIBUTING.md           ← Contributing guidelines
├── CODE_OF_CONDUCT.md        ← Community standards
│
├── orgs/                     ← 15 organization blueprints
│   ├── BlackRoad-OS/         ← Core infrastructure (The Bridge)
│   ├── BlackRoad-AI/         ← Intelligence routing
│   ├── BlackRoad-Cloud/      ← Edge compute, Cloudflare
│   ├── BlackRoad-Hardware/   ← Pi cluster, IoT, Hailo
│   ├── BlackRoad-Security/   ← Auth, secrets, audit
│   ├── BlackRoad-Labs/       ← R&D experiments
│   ├── BlackRoad-Foundation/ ← Salesforce, CRM, billing
│   ├── BlackRoad-Media/      ← Content, publishing
│   ├── BlackRoad-Interactive/← Games, metaverse, 3D
│   ├── BlackRoad-Education/  ← Learning platform
│   ├── BlackRoad-Gov/        ← Governance, voting
│   ├── BlackRoad-Archive/    ← Storage, backups
│   ├── BlackRoad-Studio/     ← Design, creative tools
│   ├── BlackRoad-Ventures/   ← Commerce, investments
│   └── Blackbox-Enterprises/ ← Stealth/enterprise solutions
│
├── prototypes/               ← Working code (Python)
│   ├── operator/             ← Routing engine (parser, classifier, router, emitter)
│   ├── metrics/              ← KPI dashboard (counter, health, status)
│   ├── explorer/             ← Ecosystem browser CLI
│   ├── cece-engine/          ← Autonomous task processing (PERCEIVE-CLASSIFY-DECIDE-EXECUTE-LEARN)
│   ├── control-plane/        ← Unified dashboard/CLI
│   ├── dispatcher/           ← Request distribution engine
│   ├── mcp-server/           ← Model Context Protocol server
│   └── webhooks/             ← Event handlers (GitHub, Stripe, Salesforce, etc.)
│
├── templates/                ← Reusable integration patterns
│   ├── salesforce-sync/      ← Full Salesforce package (17 files)
│   ├── stripe-billing/       ← $1/user/month subscription model
│   ├── cloudflare-workers/   ← Edge compute deployment
│   ├── gdrive-sync/          ← Document synchronization
│   ├── github-ecosystem/     ← Actions, Projects, Wiki integration
│   ├── design-tools/         ← Figma, Canva integration
│   └── ai-router/            ← AI routing template
│
├── routes/
│   └── registry.yaml         ← Master org routing rules (pattern-matched)
│
├── nodes/                    ← Hardware node YAML configs
├── profile/                  ← GitHub org profile page
│
└── .github/workflows/        ← 13 GitHub Actions workflows
    ├── ci.yml                ← Lint (ruff, black, isort) + test + validate
    ├── cece-auto.yml         ← Autonomous issue triage, PR review, health checks
    ├── intelligent-auto-pr.yml ← Auto dependency/security/quality PRs
    ├── issue-triage.yml      ← Auto-classify and label issues
    ├── pr-review.yml         ← Automated code review
    ├── health-check.yml      ← Node & service monitoring (every 15 min)
    ├── self-healing-master.yml ← Failure detection and auto-recovery
    ├── release.yml           ← Automated release drafting
    ├── deploy-worker.yml     ← Cloudflare Worker deployment
    ├── sync-assets.yml       ← Asset synchronization
    ├── todo-tracker.yml      ← TODO item management
    ├── webhook-dispatch.yml  ← Webhook event routing
    └── test-auto-heal.yml    ← Self-healing test suite
```

---

## Key Concepts

### Organization Shortcodes

Every org has a 2-3 letter code used in signals, routing, and configuration:

| Code | Organization | Domain |
|------|-------------|--------|
| OS | BlackRoad-OS | Core infrastructure, The Bridge |
| AI | BlackRoad-AI | Intelligence routing |
| CLD | BlackRoad-Cloud | Edge compute, Cloudflare |
| HW | BlackRoad-Hardware | Pi cluster, Hailo-8, IoT |
| SEC | BlackRoad-Security | Auth, secrets, vault |
| LAB | BlackRoad-Labs | R&D, experiments |
| FND | BlackRoad-Foundation | CRM, billing, Salesforce, Stripe |
| MED | BlackRoad-Media | Content, social, marketing |
| INT | BlackRoad-Interactive | Games, metaverse, VR/AR |
| EDU | BlackRoad-Education | Learning, courses |
| GOV | BlackRoad-Gov | Governance, voting |
| ARC | BlackRoad-Archive | Storage, backups |
| STU | BlackRoad-Studio | Design, Figma, Canva |
| VEN | BlackRoad-Ventures | Commerce, investments |
| BBX | Blackbox-Enterprises | Enterprise, stealth projects |

### Signal Protocol

Inter-component communication uses a structured format:

```
[EMOJI] [SOURCE] → [TARGET] : [MESSAGE]
```

Emojis: `✔️` done, `⏳` in progress, `❌` blocked, `📡` broadcast, `🎯` targeted

Example: `✔️ OS → AI : MEMORY.md updated, sync context`

### Streams Model

All data flow follows three stages:
- **UPSTREAM:** Inputs (requests, API data, webhooks, cron, user commands)
- **INSTREAM:** Processing (parse, route, transform, validate, enrich, log)
- **DOWNSTREAM:** Outputs (responses, API updates, node commands, storage)

### Hardware Nodes

Named nodes in the Raspberry Pi mesh (all female names):
`lucidia`, `octavia`, `aria`, `alice`, `shellfish`, `cecilia`, `arcadia`

---

## Development Workflows

### CI Pipeline (`ci.yml`)

Triggered on push/PR to `main` or `develop`. Runs:

1. **Linting:** `ruff`, `black --check`, `isort --check`
2. **Testing:** Operator, dispatcher, and webhook prototype tests
3. **Validation:** YAML config file validation

### Running Tests Locally

All prototype code is Python. From the repo root:

```bash
# Lint
ruff check prototypes/
black --check prototypes/
isort --check prototypes/

# Test specific prototypes
python -m pytest prototypes/operator/
python -m pytest prototypes/dispatcher/
python -m pytest prototypes/webhooks/
```

### Routing Registry

Routing rules live in `routes/registry.yaml`. Each org entry defines:
- Services with endpoints and health checks
- Pattern-based routing rules with priorities
- Default fallback org: `AI`

---

## Conventions

### File Organization

- **Org blueprints:** `orgs/{OrgName}/README.md`, `REPOS.md`, `SIGNALS.md`
- **Prototypes:** `prototypes/{name}/` as Python packages
- **Templates:** `templates/{integration}/` with full working code
- **Documentation:** Root-level `.md` files

### Naming

- Repositories: `kebab-case` (e.g., `salesforce-sync`, `stripe-billing`)
- Python packages: `snake_case` modules inside prototype directories
- Workflow files: descriptive kebab-case (e.g., `intelligent-auto-pr.yml`)
- Commit messages: emoji prefix + description (e.g., `🤖 Deploy Intelligent Auto-PR System`)

### Commit Message Style

Recent commits use emoji prefixes:
```
🤖 Deploy Intelligent Auto-PR System
🤖 Autonomy deployment - Push to 100!
```

### Authority Levels (for AI agents)

- **LEVEL 1 - FULL AUTO:** Read, triage, label, comment, generate code, run tests, emit signals, update `.STATUS`
- **LEVEL 2 - SUGGEST:** Code changes via PR (needs human approval)
- **LEVEL 3 - ASK FIRST:** Delete operations, org settings, permissions, deployments, financial actions, API key rotation

---

## Session Startup Protocol

When beginning work on this repository, follow this sequence:

1. Read `MEMORY.md` - understand session history and what has been built
2. Read `.STATUS` - check current state of all systems
3. Read `CECE_ABILITIES.md` - understand available capabilities
4. Read `CECE_PROTOCOLS.md` - understand decision frameworks
5. Check `git log --oneline -10` - see recent changes

---

## Important Files to Read First

| File | Purpose |
|------|---------|
| `MEMORY.md` | Session history, what's been built, key decisions |
| `.STATUS` | Real-time beacon: bridge/org/node status |
| `INDEX.md` | Navigable table of contents for all docs |
| `BLACKROAD_ARCHITECTURE.md` | Full vision, business model, infrastructure |
| `routes/registry.yaml` | Master routing rules for the entire ecosystem |

---

## What NOT to Do

- Do not commit secrets, `.env` files, or credentials
- Do not deploy to production without explicit approval (Level 3 action)
- Do not delete files or change org settings without asking (Level 3 action)
- Do not add telemetry or tracking - privacy-first design
- Do not introduce vendor lock-in - the system is designed to be portable
- Do not modify `MEMORY.md` or `.STATUS` casually - these are critical state files updated at session boundaries

---

## Architecture Principles

1. **Route, don't build.** Use existing intelligence; own the orchestration layer.
2. **Own, don't rent.** Hardware is owned (Pi cluster), infrastructure costs ~$40/month.
3. **Offline-first.** Core functionality works without internet where possible.
4. **Privacy-first.** No telemetry, no tracking, user data stays local.
5. **No vendor lock-in.** Every external dependency has a migration path.
