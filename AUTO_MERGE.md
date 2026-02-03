# Auto-Merge

> **Automatic PR merging when all checks pass**

---

## What It Does

The auto-merge workflow automatically merges pull requests when:
1. ✅ All required checks pass (Tests, PR Review, etc.)
2. ✅ PR is from a `copilot/**` branch OR has `auto-merge` label
3. ✅ PR is not a draft
4. ✅ PR has no merge conflicts
5. ✅ No checks are pending or failed

---

## How to Enable

### Option 1: Use Copilot Branches

PRs from branches starting with `copilot/` are automatically eligible:

```bash
git checkout -b copilot/my-feature
# Make changes
git push origin copilot/my-feature
# Create PR - will auto-merge when checks pass!
```

### Option 2: Add Auto-Merge Label

Add the `auto-merge` or `automerge` label to any PR:

```bash
# Via GitHub UI: Add "auto-merge" label to the PR

# Via CLI
gh pr edit <PR_NUMBER> --add-label "auto-merge"
```

---

## Workflow

```
┌─────────────────┐
│  PR Created or  │
│  Pushed         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Run Checks:    │
│  - Tests        │
│  - PR Review    │
│  - Linting      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  All Checks     │
│  Passed?        │
└────┬──────┬─────┘
     │ No   │ Yes
     ▼      ▼
   Wait   Check Eligibility
          ├─ copilot/** branch?
          ├─ auto-merge label?
          ├─ Not draft?
          └─ No conflicts?
               │
               ▼
          ┌──────────┐
          │ Enable   │
          │ Auto-    │
          │ Merge    │
          └────┬─────┘
               │
               ▼
          ┌──────────┐
          │ Merge PR │
          │ (Squash) │
          └──────────┘
```

---

## Triggers

Auto-merge checks run when:

1. **Workflow Completion** - After Tests or PR Review workflows complete
2. **PR Labeled** - When `auto-merge` label is added
3. **PR Updated** - When new commits are pushed (synchronize)
4. **Manual** - Via workflow_dispatch (for testing/troubleshooting)

---

## Merge Strategy

**Squash and Merge** is used by default:
- All commits are squashed into a single commit
- Cleaner git history
- Commit message includes PR title and number

---

## Requirements

For auto-merge to work, the PR must:

### ✅ Required Conditions

- [ ] PR state is `open`
- [ ] PR is not a draft
- [ ] Branch has no merge conflicts
- [ ] All status checks have passed
- [ ] No checks are pending
- [ ] Branch is either:
  - From `copilot/**` namespace, OR
  - Has `auto-merge` or `automerge` label

### ❌ Auto-Merge Blocked If

- PR is a draft
- PR has merge conflicts
- Any required checks failed
- Any checks are still pending
- Branch is not eligible (not copilot/* and no label)
- PR is already closed/merged

---

## Examples

### Copilot Branch (Auto-Eligible)

```bash
# Create copilot branch
git checkout -b copilot/add-testing-infrastructure

# Make changes and push
git add .
git commit -m "Add comprehensive testing"
git push origin copilot/add-testing-infrastructure

# Create PR
gh pr create --title "Add testing infrastructure" --body "Details..."

# Auto-merge will activate automatically when checks pass! ✅
```

### Regular Branch (Needs Label)

```bash
# Create regular branch
git checkout -b feature/new-feature

# Make changes and push
git add .
git commit -m "Add new feature"
git push origin feature/new-feature

# Create PR
gh pr create --title "New feature" --body "Details..."

# Add auto-merge label
gh pr edit --add-label "auto-merge"

# Auto-merge will activate when checks pass! ✅
```

---

## Monitoring

### Check Auto-Merge Status

```bash
# View PR details
gh pr view <PR_NUMBER>

# Check workflow runs
gh run list --workflow=auto-merge.yml

# View specific run
gh run view <RUN_ID>
```

### GitHub UI

1. Go to PR page
2. Scroll to bottom - you'll see "Auto-merge enabled" if active
3. Check "Checks" tab to see workflow status

---

## Notifications

When auto-merge is enabled, the workflow will:

1. ✅ Enable GitHub's native auto-merge feature
2. 💬 Add a comment to the PR with details
3. 📊 Add workflow summary
4. 📡 Emit signal: `auto-merge → branch : enabled`

Example comment:

```
🤖 Auto-merge enabled

All checks have passed! This PR will be automatically merged when ready.

- Branch: copilot/add-feature
- Merge method: Squash and merge
- Triggered by: workflow_run

This is an automated action by the BlackRoad auto-merge system.

📡 auto-merge → copilot/add-feature : enabled
```

---

## Troubleshooting

### Auto-Merge Not Triggering

**Check eligibility:**
```bash
# Is it a copilot branch?
git branch --show-current
# Should start with "copilot/"

# Does it have the label?
gh pr view <PR_NUMBER> --json labels

# Are all checks passing?
gh pr checks <PR_NUMBER>
```

**Common issues:**
- ❌ Branch doesn't start with `copilot/`
- ❌ Missing `auto-merge` label
- ❌ PR is a draft
- ❌ Checks are still running
- ❌ Some checks failed
- ❌ Merge conflicts exist

### Manual Trigger

```bash
# Manually trigger auto-merge check
gh workflow run auto-merge.yml -f pr_number=<PR_NUMBER>

# Check the run
gh run list --workflow=auto-merge.yml --limit 1
```

### Disable Auto-Merge

```bash
# Remove auto-merge label
gh pr edit <PR_NUMBER> --remove-label "auto-merge"

# Or via API
gh api repos/:owner/:repo/pulls/<PR_NUMBER>/auto-merge -X DELETE
```

---

## Security

### Permissions

The workflow requires:
- `pull-requests: write` - To enable auto-merge
- `contents: write` - To merge PRs
- `checks: read` - To verify check status

### Safety Checks

Auto-merge will **NOT** proceed if:
- Any required checks fail
- PR has conflicts
- PR is in draft state
- Branch protection rules are not satisfied

---

## Configuration

### Required Workflows

These workflows must complete successfully:
- `Tests` - Unit and integration tests
- `PR Review` - Code quality checks

### Customization

Edit `.github/workflows/auto-merge.yml` to:

**Change merge method:**
```yaml
mergeMethod: SQUASH  # Options: MERGE, SQUASH, REBASE
```

**Add more required workflows:**
```yaml
workflow_run:
  workflows:
    - "Tests"
    - "PR Review"
    - "Security Scan"  # Add custom workflows
```

**Change branch pattern:**
```yaml
# Check for different branch pattern
const isEligibleBranch = pr.head.ref.startsWith('feature/');
```

---

## Best Practices

### ✅ Do

- Use `copilot/**` branches for automated work
- Ensure tests are comprehensive
- Add clear PR descriptions
- Wait for all checks before expecting merge
- Monitor auto-merge comments

### ❌ Don't

- Force push to branches with open PRs (breaks checks)
- Add auto-merge label to PRs with known issues
- Skip writing tests
- Ignore failed checks
- Use on PRs that need manual review

---

## Integration with BlackRoad

Auto-merge is designed for:

1. **Copilot Branches** - AI-assisted development
2. **Automated Updates** - Dependabot, renovate
3. **Prototype Work** - Fast iteration on prototypes
4. **Documentation** - Low-risk doc updates

For sensitive changes (security, core infrastructure), manual review is still recommended even if auto-merge is eligible.

---

## Signals

Auto-merge emits BlackRoad signals:

```
📡 auto-merge → branch : checking
📡 auto-merge → branch : eligible
📡 auto-merge → branch : enabled
📡 auto-merge → branch : merged
📡 auto-merge → branch : blocked, reason=conflicts
```

---

## FAQ

**Q: Will this merge without human review?**
A: Yes, if all checks pass and conditions are met. Use manual review for critical changes.

**Q: Can I disable auto-merge for a specific PR?**
A: Yes, don't use copilot/* branches and don't add the auto-merge label.

**Q: What if I want to add more commits?**
A: Just push - auto-merge will wait for new checks to complete.

**Q: Does this work with branch protection?**
A: Yes, all branch protection rules still apply.

**Q: Can I see which PRs have auto-merge enabled?**
A: Check PR labels for "auto-merge" or look for the auto-merge status on the PR page.

---

*Auto-merge intelligently. Merge with confidence.* 🚀

📡 **Signal:** `docs → auto-merge : documented`
