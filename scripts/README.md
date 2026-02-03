# Scripts Directory

Management and automation scripts for BlackRoad-OS/.github repository.

## PR Manager

### Usage

```bash
# List all open PRs
./scripts/pr_manager.py list

# Show PR statistics
./scripts/pr_manager.py status

# Show details for a specific PR
./scripts/pr_manager.py show 18

# Add a label to a PR
./scripts/pr_manager.py label 18 enhancement

# Request review for a PR
./scripts/pr_manager.py review 18

# Merge a PR (when ready)
./scripts/pr_manager.py merge 18
```

### Features

- List all open PRs with status and category
- Show detailed PR information
- Add labels to PRs
- Request reviews
- Merge PRs with safety checks
- Display PR statistics and breakdown

### Requirements

- Python 3.7+
- GitHub CLI (`gh`) for actual PR operations

### Note

The script provides GitHub CLI commands for actual operations. To execute these commands automatically, you would need to integrate with the GitHub API using a token.

## Future Scripts

- `deploy.py` - Deployment automation
- `sync_orgs.py` - Sync configurations across organizations
- `metrics.py` - Generate repository metrics
- `release.py` - Release management

---

*Part of the BlackRoad Autonomy System*
