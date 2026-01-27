# The Bridge

> **BlackRoad-OS/.github** - The central coordination point for all BlackRoad organizations

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Organizations](https://img.shields.io/badge/organizations-15-green.svg)](orgs/)
[![Status](https://img.shields.io/badge/status-active-success.svg)](.STATUS)
[![AI](https://img.shields.io/badge/AI-Claude%20Code%20API-blue.svg)](CLAUDE_CODE_API.md)

---

## What Is This?

This repository is **The Bridge** - where all BlackRoad architecture, blueprints, and coordination happens.

```
[User Request] → [Operator] → [Right Tool] → [Answer]
```

BlackRoad is a routing company. We don't build intelligence, we route to it.

---

## Quick Start

### 📖 New Here? Start With These

1. **[INDEX.md](INDEX.md)** - Complete map of everything
2. **[BLACKROAD_ARCHITECTURE.md](BLACKROAD_ARCHITECTURE.md)** - Our vision and architecture
3. **[REPO_MAP.md](REPO_MAP.md)** - All 15 orgs and 86+ repos
4. **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute

### 🏢 Explore Organizations

Browse the 15 specialized organizations:

| Tier | Organizations |
|------|---------------|
| **Core** | [BlackRoad-OS](orgs/BlackRoad-OS/) · [BlackRoad-AI](orgs/BlackRoad-AI/) · [BlackRoad-Cloud](orgs/BlackRoad-Cloud/) |
| **Support** | [BlackRoad-Hardware](orgs/BlackRoad-Hardware/) · [BlackRoad-Security](orgs/BlackRoad-Security/) · [BlackRoad-Labs](orgs/BlackRoad-Labs/) |
| **Business** | [BlackRoad-Foundation](orgs/BlackRoad-Foundation/) · [BlackRoad-Ventures](orgs/BlackRoad-Ventures/) · [Blackbox-Enterprises](orgs/Blackbox-Enterprises/) |
| **Creative** | [BlackRoad-Media](orgs/BlackRoad-Media/) · [BlackRoad-Studio](orgs/BlackRoad-Studio/) · [BlackRoad-Interactive](orgs/BlackRoad-Interactive/) |
| **Community** | [BlackRoad-Education](orgs/BlackRoad-Education/) · [BlackRoad-Gov](orgs/BlackRoad-Gov/) · [BlackRoad-Archive](orgs/BlackRoad-Archive/) |

### 🔧 Try the Prototypes

```bash
# Route a query
cd prototypes/operator
python -m operator.cli "What is the weather?"

# View ecosystem metrics
cd prototypes/metrics
python -m metrics.dashboard

# Browse the ecosystem
cd prototypes/explorer
python -m explorer.cli
```

---

## Core Files

| File | Purpose |
|------|---------|
| [.STATUS](.STATUS) | Real-time system beacon |
| [INDEX.md](INDEX.md) | Navigation hub |
| [MEMORY.md](MEMORY.md) | Persistent AI context |
| [SIGNALS.md](SIGNALS.md) | Agent coordination protocol |
| [STREAMS.md](STREAMS.md) | Data flow patterns |
| [INTEGRATIONS.md](INTEGRATIONS.md) | External services (30+) |
| [CLAUDE_CODE_API.md](CLAUDE_CODE_API.md) | Claude Code API best practices |

---

## The Stack

| Layer | Technology |
|-------|------------|
| **Edge** | Cloudflare Workers, WAF |
| **Compute** | Raspberry Pi 4 Cluster (4 nodes) + Hailo-8 AI |
| **Network** | Tailscale (WireGuard VPN) |
| **CRM** | Salesforce |
| **Billing** | Stripe ($1/user/month model) |
| **Code** | GitHub (you're here) |
| **AI/Intelligence** | Claude Code API (Anthropic), GPT (OpenAI), Llama (Local) |
| **Development** | Claude Code IDE, MCP Server, AI Router |

---

## Directory Structure

```
BlackRoad-OS/.github/
│
├── 📄 Core Files
│   ├── .STATUS              ← Real-time beacon
│   ├── INDEX.md             ← Start here!
│   ├── MEMORY.md            ← Persistent context
│   ├── SIGNALS.md           ← Communication protocol
│   ├── STREAMS.md           ← Data flows
│   ├── REPO_MAP.md          ← Ecosystem map
│   ├── INTEGRATIONS.md      ← External services
│   └── BLACKROAD_ARCHITECTURE.md
│
├── 🏢 orgs/                  ← All 15 org blueprints
│   ├── BlackRoad-OS/
│   ├── BlackRoad-AI/
│   ├── BlackRoad-Cloud/
│   └── ... (12 more)
│
├── 🔧 prototypes/            ← Working code
│   ├── operator/            ← Routing brain
│   ├── metrics/             ← KPI dashboard
│   └── explorer/            ← Ecosystem browser
│
├── 📦 templates/             ← Integration patterns
│   ├── salesforce-sync/
│   ├── stripe-billing/
│   ├── cloudflare-workers/
│   └── ... (3 more)
│
├── 👤 profile/               ← Org landing page
│   └── README.md
│
└── ⚙️ .github/               ← GitHub automation
    ├── workflows/           ← CI/CD
    ├── ISSUE_TEMPLATE/      ← Issue forms
    └── ...
```

---

## Contributing

We welcome contributions! Please read:

1. **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines
2. **[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)** - Community standards
3. **[SECURITY.md](SECURITY.md)** - Security policy
4. **[SUPPORT.md](SUPPORT.md)** - Getting help

### Quick Contribution Flow

```bash
# 1. Fork and clone
git clone https://github.com/YOUR_USERNAME/.github.git

# 2. Create a branch
git checkout -b feat/org-name/feature-description

# 3. Make changes, test, commit
git commit -m "feat(org-ai): add feature"

# 4. Push and create PR
git push origin your-branch-name
```

---

## Key Concepts

### The Operator

The routing brain that classifies queries and routes them to the right organization.

```python
from operator.core import Operator

op = Operator()
result = op.route("Deploy a Cloudflare Worker")
# → Routes to BlackRoad-Cloud with 95% confidence
```

### Signals

Emoji-based protocol for agent coordination:

- ✔️ Success
- ❌ Error  
- 📡 Data transmission
- 🎯 Goal achieved

See [SIGNALS.md](SIGNALS.md) for the complete protocol.

### Streams

Data flow patterns:

- **Upstream** - External → BlackRoad
- **Instream** - Internal processing
- **Downstream** - BlackRoad → External

See [STREAMS.md](STREAMS.md) for details.

---

## Community

- **Discussions** - [Ask questions](https://github.com/orgs/BlackRoad-OS/discussions)
- **Issues** - [Report bugs or request features](.github/ISSUE_TEMPLATE/)
- **Support** - [Get help](SUPPORT.md)

---

## License

[MIT License](LICENSE) - See LICENSE file for details.

---

## Status

```bash
cat .STATUS
```

Current state:
- 🟢 **Organizations:** 15/15 blueprinted
- 🟢 **Repositories:** 86 defined
- 🟢 **Prototypes:** 3 working
- 🟢 **Templates:** 6 available
- 🟢 **Health:** 5/5

---

## The Vision

> "We route intelligence. We don't build it."

BlackRoad connects users to the intelligence that already exists - AI models, databases, APIs, and more. We don't train models. We don't buy GPUs. We route requests to the right tool at the right time.

**Scale:** $1/user/month × millions of users = sustainable routing company

Read [BLACKROAD_ARCHITECTURE.md](BLACKROAD_ARCHITECTURE.md) for the complete vision.

---

## Quick Commands

```bash
# Check everything
cat INDEX.md

# System health
python -m metrics.dashboard

# Route a query
python -m operator.cli "your question"

# Current status
cat .STATUS

# Browse organizations
ls orgs/

# View integrations
cat INTEGRATIONS.md
```

---

## Links

- **Organization Profile:** [github.com/BlackRoad-OS](https://github.com/BlackRoad-OS)
- **Main Website:** blackroad.dev *(coming soon)*
- **Documentation:** This repository
- **Support:** [SUPPORT.md](SUPPORT.md)

---

*The Bridge connects everything. Start exploring.*

📡 **Signal:** `visitor → bridge : connected`
