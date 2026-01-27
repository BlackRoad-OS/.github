# BlackRoad Bridge

> **The central coordination hub for the BlackRoad ecosystem**

This repository (`.github`) serves as **The Bridge** - coordinating workflows, configurations, and updates across all 15 BlackRoad organizations.

## Key Features

- 🎯 **Central Routing**: Routes requests across 15 organizations
- 📡 **Auto-Sync**: Automatically pushes updates to target org repositories
- 🤖 **Auto-Merge**: PRs automatically merge to main after approval + CI pass
- ✅ **Comprehensive Testing**: Validates sync functionality and configurations
- 🔧 **Prototypes**: Working code for operator, dispatcher, webhooks, and more

## Quick Start

### Running Tests

```bash
# Run all sync tests
python tests/test_sync.py

# Run CI tests locally
python -m pytest prototypes/operator/tests/
```

### Syncing to Organizations

Updates are automatically synced when pushed to `main`. To manually trigger:

```bash
# Sync to all active orgs
gh workflow run sync-to-orgs.yml

# Sync to specific orgs
gh workflow run sync-to-orgs.yml -f target_orgs=OS,AI

# Test without actually dispatching (dry run)
gh workflow run sync-to-orgs.yml -f dry_run=true
```

See [docs/SYNC.md](docs/SYNC.md) for detailed documentation.

## Documentation

- [INDEX.md](INDEX.md) - Navigate the entire ecosystem
- [SYNC.md](docs/SYNC.md) - **How updates sync to other orgs** ✨
- [SIGNALS.md](SIGNALS.md) - Signal protocol for coordination
- [MEMORY.md](MEMORY.md) - Persistent context for agents
- [REPO_MAP.md](REPO_MAP.md) - All repos across all orgs
- [BLACKROAD_ARCHITECTURE.md](BLACKROAD_ARCHITECTURE.md) - Architecture vision

## Workflows

| Workflow | Purpose | Trigger |
|----------|---------|---------|
| **sync-to-orgs.yml** | Syncs updates to target orgs | Push to main, manual |
| **auto-merge.yml** | Auto-merges approved PRs | After CI passes |
| **ci.yml** | Runs tests and validation | Push, PR to main/develop |
| **sync-assets.yml** | Syncs from external sources | Every 6 hours, manual |
| **webhook-dispatch.yml** | Routes incoming webhooks | Repository dispatch |
| **deploy-worker.yml** | Deploys Cloudflare Workers | Push to main, manual |
| **release.yml** | Publishes releases | Push tags |
| **health-check.yml** | Monitors service health | Schedule, manual |

## Architecture

```
BlackRoad-OS/.github (The Bridge)
    │
    ├─── 15 Organizations
    │    ├─ OS (Core Infrastructure)
    │    ├─ AI (Intelligence Routing)
    │    ├─ CLD (Edge/Cloud)
    │    ├─ HW (Hardware/IoT)
    │    └─ ... 11 more
    │
    ├─── Prototypes
    │    ├─ operator (routing engine)
    │    ├─ dispatcher (org dispatcher)
    │    ├─ webhooks (event handling)
    │    └─ ... more
    │
    └─── Routes & Registry
         └─ routes/registry.yaml (master routing table)
```

## Contributing

1. Create a feature branch
2. Make changes
3. Run tests: `python tests/test_sync.py`
4. Create PR to `main`
5. Get approval
6. CI runs automatically
7. Auto-merge to main (after approval + CI pass)
8. Changes sync to target orgs automatically

## Testing & Validation

All PRs must pass:

- ✅ Lint (Ruff, Black, isort)
- ✅ Operator tests (routing logic)
- ✅ Dispatcher tests (org routing)
- ✅ Webhook tests (event handling)
- ✅ Config validation (YAML)
- ✅ **Sync tests (sync functionality)** ✨

## Organizations

15 orgs, 1 active (OS), 14 planned. See [routes/registry.yaml](routes/registry.yaml) for details.

**Active:**
- BlackRoad-OS (OS) - Core infrastructure, The Bridge

**Planned:**
- BlackRoad-AI (AI) - Intelligence routing
- BlackRoad-Cloud (CLD) - Edge/cloud computing
- BlackRoad-Hardware (HW) - Pi cluster, IoT
- BlackRoad-Security (SEC) - Auth, secrets
- BlackRoad-Labs (LAB) - R&D, experiments
- BlackRoad-Foundation (FND) - CRM, billing
- BlackRoad-Media (MED) - Content, social
- BlackRoad-Studio (STU) - Design, Figma
- BlackRoad-Interactive (INT) - Gaming, metaverse
- BlackRoad-Education (EDU) - Learning, tutorials
- BlackRoad-Gov (GOV) - Governance, voting
- BlackRoad-Archive (ARC) - Storage, backups
- BlackRoad-Ventures (VEN) - Marketplace
- Blackbox-Enterprises (BBX) - Enterprise

## Status

See [.STATUS](.STATUS) for real-time beacon.

---

**The Bridge is live. All systems nominal.**
