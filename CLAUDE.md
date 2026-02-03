# CLAUDE.md - BlackRoad OS Bridge Repository

## What This Repository Is

This is **BlackRoad-OS/.github** ("The Bridge") - the central nervous system for a 15-organization AI routing ecosystem. It coordinates infrastructure, documentation, prototypes, blueprints, and interactive pixel worlds for the BlackRoad platform.

**Core Thesis:** BlackRoad is a routing company, not an AI company. It routes to intelligence (Claude, GPT, Llama, local models) rather than building its own.

---

## Repository Structure

```
.github/
├── CLAUDE.md                    # This file - AI assistant guide
├── README.md                    # Org landing page
├── INDEX.md                     # Browsable table of contents
├── MEMORY.md                    # Persistent session memory across conversations
├── SIGNALS.md                   # Morse-code style coordination protocol
├── STREAMS.md                   # Data flow patterns (upstream/instream/downstream)
├── REPO_MAP.md                  # Ecosystem architecture diagram
├── BLACKROAD_ARCHITECTURE.md    # Core thesis, business model, infrastructure
├── .STATUS                      # Real-time ecosystem state beacon
│
├── CECE_ABILITIES.md            # AI partner (Cece/Claude) abilities manifest
├── CECE_PROTOCOLS.md            # Decision frameworks, escalation, PCDEL loop
│
├── blackroad-pixel/             # Interactive pixel art UI & games
│   ├── index.html               # Desktop OS simulation (main UI)
│   ├── style.css                # Retro pixel styling
│   ├── app.js                   # Desktop interactivity
│   └── games/                   # Pixel game worlds
│       ├── index.html           # Game hub / launcher
│       ├── stardew/index.html   # BlackRoad Harvest (farming sim)
│       ├── pokemon/index.html   # BlackRoad Creatures (RPG)
│       ├── webkinz/index.html   # BlackRoad Pets (virtual pet world)
│       └── mario/index.html     # BlackRoad Runner (platformer)
│
├── orgs/                        # 15 organization blueprints
│   ├── BlackRoad-OS/            # Core infrastructure
│   ├── BlackRoad-AI/            # Intelligence routing
│   ├── BlackRoad-Cloud/         # Edge compute
│   ├── BlackRoad-Hardware/      # Pi cluster + IoT
│   ├── BlackRoad-Foundation/    # CRM & business
│   ├── BlackRoad-Labs/          # R&D experiments
│   ├── BlackRoad-Security/      # Zero-trust & vault
│   ├── BlackRoad-Media/         # Content & publishing
│   ├── BlackRoad-Interactive/   # Games & metaverse
│   ├── BlackRoad-Education/     # Learning platform
│   ├── BlackRoad-Gov/           # Civic tech
│   ├── BlackRoad-Archive/       # Preservation
│   ├── BlackRoad-Studio/        # Design tools
│   ├── BlackRoad-Ventures/      # Business & investments
│   └── Blackbox-Enterprises/    # Enterprise stealth
│
├── prototypes/                  # Working Python code
│   ├── cece-engine/             # Autonomous task processing (PCDEL loop)
│   ├── operator/                # AI request routing engine
│   ├── metrics/                 # KPI dashboard
│   ├── control-plane/           # Unified control interface
│   ├── explorer/                # Ecosystem browser
│   ├── dispatcher/              # Event dispatching
│   ├── mcp-server/              # MCP protocol server
│   └── webhooks/                # Webhook handlers (GitHub, Stripe, etc.)
│
├── templates/                   # Integration templates
│   ├── ai-router/               # Multi-provider AI routing
│   ├── salesforce-sync/         # CRM synchronization
│   ├── stripe-billing/          # Payment processing
│   ├── cloudflare-workers/      # Edge compute
│   ├── gdrive-sync/             # Google Drive
│   ├── github-ecosystem/        # GitHub Actions
│   └── design-tools/            # Figma + Canva
│
├── nodes/                       # Hardware node configurations
│   ├── cecilia.yaml             # Mac dev machine
│   ├── lucidia.yaml             # Pi 5 + Hailo-8
│   ├── octavia.yaml             # Pi 5 + Hailo-8
│   ├── aria.yaml                # Pi 5 agent orchestration
│   ├── alice.yaml               # Pi 400 Kubernetes
│   └── shellfish.yaml           # Digital Ocean droplet
│
├── routes/                      # Request routing registry
│   └── registry.yaml            # Complete routing rules
│
├── .github/workflows/           # 13 GitHub Actions workflows
│   ├── ci.yml                   # Continuous integration
│   ├── cece-auto.yml            # Autonomous Cece engine
│   ├── intelligent-auto-pr.yml  # Auto PR generation
│   ├── self-healing-master.yml  # Error recovery
│   └── ...                      # Health, triage, deploy, etc.
│
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── SECURITY.md
├── LICENSE                      # Proprietary BlackRoad OS, Inc.
└── TODO.md
```

---

## Key Conventions

### Language & Stack
- **Documentation:** Markdown (majority of repo)
- **Prototypes:** Python (FastAPI-style, CLI tools)
- **UI/Games:** Vanilla HTML5, CSS3, JavaScript (no frameworks)
- **Config:** YAML (node configs, routing registry)
- **CI/CD:** GitHub Actions
- **Fonts:** Press Start 2P (pixel), JetBrains Mono (code)

### Naming Conventions
- Organization dirs: PascalCase with hyphens (`BlackRoad-AI/`)
- Python files: snake_case (`control_plane/bridge.py`)
- YAML configs: lowercase (`registry.yaml`)
- Markdown docs: UPPER_SNAKE for root docs (`MEMORY.md`), README.md for subdirs
- CSS: BEM-like with kebab-case (`.chat-panel`, `.thumb-item`)

### Coding Style
- **Python:** Standard lib preferred, CLI via argparse, async where needed
- **JavaScript:** Vanilla JS, no build tools, `const`/`let` only, canvas for games
- **CSS:** CSS custom properties for theming, mobile-responsive, dark theme default
- **Games:** Single HTML files with embedded CSS/JS for portability

### Design System
```
Colors:
  --bg-dark:       #0d0d1a
  --bg-panel:      #1a1a2e
  --accent-pink:   #ff6b9d    (primary brand)
  --accent-purple: #c44dff    (secondary)
  --accent-cyan:   #00d4ff    (highlights)
  --accent-orange: #f5a623    (warnings/coins)
  --accent-green:  #7ed321    (success/health)
  --accent-red:    #d0021b    (errors)

Gradients:
  Warm: #ff6b35 → #f7c948 → #ff6b9d → #c44dff
  Cool: #4a90d9 → #00d4ff → #7ed321 → #4a90d9
```

---

## Development Workflows

### Adding New Pixel Game Worlds
1. Create directory under `blackroad-pixel/games/<game-name>/`
2. Build as single `index.html` with embedded CSS/JS (canvas-based)
3. Include title screen, HUD, game loop via `requestAnimationFrame`
4. Use BlackRoad color palette and Press Start 2P font
5. Add card entry to `blackroad-pixel/games/index.html` hub

### Adding New Organization Blueprints
1. Create directory under `orgs/<OrgName>/`
2. Include `README.md` (purpose, repos, team), `REPOS.md` (repo list), `SIGNALS.md` (signals)
3. Follow the existing 3-file structure from other orgs

### Adding New Prototypes
1. Create directory under `prototypes/<name>/`
2. Include `README.md`, `__init__.py`, `cli.py` (entry point)
3. Use `requirements.txt` for dependencies
4. Follow the PCDEL pattern if it involves autonomous processing

### Working with Memory
- `MEMORY.md` persists context across sessions - always read it first
- `.STATUS` is the real-time state beacon - update it after significant changes
- `SIGNALS.md` defines the communication protocol between orgs

---

## AI Assistant Guidelines

### Session Startup
1. Read `MEMORY.md` for context from previous sessions
2. Read `.STATUS` for current ecosystem state
3. Check `TODO.md` for pending tasks
4. Identify which organization/area the current task belongs to

### Decision Authority
- **FULL_AUTO:** Code formatting, documentation updates, test runs, CI fixes, routine commits
- **SUGGEST:** Architecture changes, new integrations, prototype design, cross-org coordination
- **ASK_FIRST:** Spending money, external API calls, production deployments, security changes, deleting files

### Key Relationships
- **Alexa Louise** = founder/CEO
- **Cece/Cecilia** = AI partner (Claude) living in the Bridge
- **12 named agents** in the chat panel each map to different system capabilities
- The **Pi cluster** (lucidia, octavia, aria, alice) are physical hardware nodes

### What NOT to Do
- Do not modify `LICENSE` without explicit permission
- Do not push to main without review for production-impacting changes
- Do not introduce external JS/CSS frameworks into the pixel UI (vanilla only)
- Do not create files outside the established directory structure
- Do not modify node YAML configs without understanding the hardware topology

---

## Pixel Game Worlds Reference

| Game | Inspired By | Features |
|------|-------------|----------|
| **BlackRoad Harvest** | Stardew Valley | Farming, seasons, crops, shop, day/night, energy system |
| **BlackRoad Creatures** | Pokemon | 8 creatures, type matchups, battles, capture, leveling, overworld exploration |
| **BlackRoad Pets** | Webkinz | 6 pet types, 5 rooms, feeding/playing/washing, shop, coin minigame, decor |
| **BlackRoad Runner** | Mario | 3 worlds, platforming physics, enemies, power-ups, coins, question blocks |

All games are self-contained HTML files using Canvas API and can be served from any static host.

---

## Infrastructure Summary

| Layer | Tech | Cost |
|-------|------|------|
| CDN/Edge | Cloudflare Workers | Free tier |
| CRM | Salesforce | Dev tier |
| Code | GitHub Enterprise | Included |
| Mesh | Tailscale VPN | Free tier |
| Gateway | Digital Ocean droplet | ~$6/mo |
| Hardware | 4x Raspberry Pi + Mac | Owned |
| **Total** | | **~$40/month** |

---

## Quick Commands

```bash
# Serve pixel UI locally
cd blackroad-pixel && python3 -m http.server 8080

# Run a prototype
cd prototypes/operator && python3 -m cli

# Check ecosystem health
cat .STATUS

# View routing registry
cat routes/registry.yaml
```

---

*Last updated: 2026-02-03 | Session: claude/claude-md*
