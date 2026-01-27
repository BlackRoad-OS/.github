# Sync to Organizations

This document explains how updates in the `.github` repository are synced to other BlackRoad organizations and repositories.

## Overview

The `.github` repository serves as the **central coordination hub** for all BlackRoad organizations. When changes are made here, they are automatically propagated to the appropriate target repositories through GitHub's repository dispatch system.

## How It Works

### 1. Workflow Triggers

The sync process is triggered in two ways:

**Automatic (on push to main):**
```yaml
on:
  push:
    branches: [main]
    paths:
      - 'templates/**'
      - '.github/workflows/**'
      - 'routes/registry.yaml'
```

**Manual dispatch:**
```bash
# Via GitHub UI: Actions → Sync to Orgs → Run workflow
# Or via gh CLI:
gh workflow run sync-to-orgs.yml -f target_orgs=OS,AI -f dry_run=false
```

### 2. Target Organizations

Organizations are defined in `routes/registry.yaml`. Only organizations with `status: active` receive sync updates.

Currently active orgs:
- **OS** (BlackRoad-OS) - Core infrastructure

To activate additional orgs, update their status in `routes/registry.yaml`:
```yaml
AI:
  name: BlackRoad-AI
  status: active  # Change from 'planned' to 'active'
  ...
```

### 3. Dispatch Process

For each active organization:

1. Load the organization's repository list from `routes/registry.yaml`
2. Send a `repository_dispatch` event to each repo:
   ```json
   {
     "event_type": "sync_from_bridge",
     "client_payload": {
       "source": "BlackRoad-OS/.github",
       "ref": "<commit-sha>",
       "timestamp": "<timestamp>"
     }
   }
   ```
3. Target repositories listen for this event and pull updates

### 4. Repository Setup

Target repositories must:

1. Have a workflow that listens for the dispatch event:
   ```yaml
   on:
     repository_dispatch:
       types: [sync_from_bridge]
   ```

2. Pull and apply updates from the bridge repository:
   ```yaml
   - name: Sync from bridge
     run: |
       # Pull workflow templates
       curl -o .github/workflows/shared.yml \
         https://raw.githubusercontent.com/BlackRoad-OS/.github/main/templates/workflows/shared.yml
   ```

## Testing

### Run Tests Locally

```bash
# Run all sync tests
python tests/test_sync.py

# Test with dry run (no actual dispatch)
gh workflow run sync-to-orgs.yml -f dry_run=true
```

### Verify Sync

After syncing, check:

1. **Workflow run logs**: Actions → Sync to Orgs → [latest run]
2. **Target repo webhooks**: Settings → Webhooks → Recent Deliveries
3. **Target repo workflows**: Should show triggered runs from dispatch

### Common Issues

**Issue**: "404 Repo not found or no dispatch workflow"
- **Solution**: Target repo either doesn't exist or hasn't set up a dispatch workflow

**Issue**: "401 Unauthorized"
- **Solution**: `GITHUB_TOKEN` lacks permission to dispatch to target org. Use a PAT with `repo` scope.

**Issue**: Sync runs but target repos don't update
- **Solution**: Target repos need to implement the dispatch handler workflow

## Auto-Merge to Main

PRs are automatically merged to `main` when:

1. ✅ All CI checks pass
2. ✅ PR is approved by a reviewer
3. ✅ PR has no merge conflicts

The auto-merge workflow:
- Triggers after CI completes successfully
- Checks PR approval status
- Enables auto-merge with squash commit
- Deletes the branch after merge

## CI Pipeline

Before any PR can be merged, it must pass:

- **Lint**: Ruff, Black, isort checks
- **Test Operator**: Routing logic tests
- **Test Dispatcher**: Registry and routing tests
- **Test Webhooks**: Webhook handling tests
- **Validate Config**: YAML validation
- **Test Sync**: Sync functionality validation ✨ (new)

## Monitoring

### Check Sync Status

```bash
# List recent workflow runs
gh run list --workflow=sync-to-orgs.yml

# View specific run details
gh run view <run-id>

# Watch a run in real-time
gh run watch <run-id>
```

### Check Active Orgs

```bash
# List active organizations
python -c "
import yaml
with open('routes/registry.yaml') as f:
    reg = yaml.safe_load(f)
    active = [code for code, org in reg['orgs'].items() if org.get('status') == 'active']
    print(f'Active orgs: {', '.join(active)}')
"
```

## Architecture

```
BlackRoad-OS/.github (Bridge)
    │
    ├─ Push to main
    │     │
    │     └─ Triggers sync-to-orgs.yml
    │           │
    │           ├─ Load routes/registry.yaml
    │           │
    │           └─ For each active org:
    │                 │
    │                 └─ For each repo:
    │                       │
    │                       └─ Send repository_dispatch
    │                             │
    │                             └─ Target repo receives event
    │                                   │
    │                                   └─ Pulls and applies updates
    │
    └─ PR approved + CI passes
          │
          └─ Triggers auto-merge.yml
                │
                └─ Merges to main
                      │
                      └─ Cycle continues...
```

## Contributing

When making changes that affect other orgs:

1. Create a feature branch
2. Make changes to templates, workflows, or configs
3. Run tests: `python tests/test_sync.py`
4. Create a PR to `main`
5. Get approval from a reviewer
6. CI will run automatically
7. Once approved + CI passes → auto-merge to main
8. Sync workflow dispatches to target orgs
9. Monitor target repos for successful application

## Security

- Use `GITHUB_TOKEN` for same-org dispatches
- Use PAT with minimal scope for cross-org dispatches
- Validate all payloads in target repos
- Never sync secrets or credentials
- Use dry-run mode when testing

## Troubleshooting

### Debug Mode

Enable verbose logging:
```yaml
env:
  ACTIONS_STEP_DEBUG: true
  ACTIONS_RUNNER_DEBUG: true
```

### Manual Dispatch

To sync specific orgs:
```bash
gh workflow run sync-to-orgs.yml -f target_orgs=OS,AI,CLD
```

To test without dispatching:
```bash
gh workflow run sync-to-orgs.yml -f dry_run=true
```

## Related Files

- `.github/workflows/sync-to-orgs.yml` - Main sync workflow
- `.github/workflows/auto-merge.yml` - Auto-merge workflow
- `.github/workflows/ci.yml` - CI pipeline with sync tests
- `routes/registry.yaml` - Organization registry
- `tests/test_sync.py` - Sync functionality tests
- `templates/` - Shared templates to sync
