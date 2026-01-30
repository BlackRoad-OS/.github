# GitHub Ecosystem

> **Integration Guide** — architectural reference for future implementation. Code snippets below are illustrative, not runnable.

> **Actions, Projects, Wiki, Codespaces, Discussions. The full suite.**

```
Org: BlackRoad-OS (OS)
Platform: github.com/BlackRoad-OS
CLI: gh
```

---

## The GitHub Stack

```
┌─────────────────────────────────────────────────────────────┐
│                     GITHUB ECOSYSTEM                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   │
│   │  Repos  │   │ Actions │   │Projects │   │  Wiki   │   │
│   │  Code   │   │  CI/CD  │   │ Boards  │   │  Docs   │   │
│   └─────────┘   └─────────┘   └─────────┘   └─────────┘   │
│                                                             │
│   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   │
│   │ Issues  │   │  PRs    │   │Codespace│   │Discuss- │   │
│   │ Tracker │   │ Review  │   │  Dev    │   │  ions   │   │
│   └─────────┘   └─────────┘   └─────────┘   └─────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 1. GitHub Actions

### Workflow Triggers

```yaml
# .github/workflows/main.yml
name: BlackRoad CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight
  workflow_dispatch:      # Manual trigger
    inputs:
      environment:
        description: 'Deploy environment'
        required: true
        default: 'staging'
```

### Standard Workflows

#### CI Pipeline
```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install deps
        run: pip install -r requirements.txt

      - name: Run tests
        run: pytest

      - name: Signal success
        if: success()
        run: echo "✔️ OS → OS : tests_passed"
```

#### Deploy to Cloudflare
```yaml
name: Deploy Worker

on:
  push:
    branches: [main]
    paths: ['workers/**']

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Cloudflare
        uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CF_API_TOKEN }}
          workingDirectory: 'workers/api'
```

#### Sync to External
```yaml
name: Sync Salesforce

on:
  schedule:
    - cron: '*/15 * * * *'  # Every 15 minutes

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run sync
        env:
          SF_USERNAME: ${{ secrets.SF_USERNAME }}
          SF_PASSWORD: ${{ secrets.SF_PASSWORD }}
        run: python -m salesforce_sync.cli sync
```

### Custom Actions

```yaml
# .github/actions/signal/action.yml
name: 'Emit Signal'
description: 'Emit a BlackRoad signal'
inputs:
  signal:
    description: 'Signal string'
    required: true
  target:
    description: 'Target org'
    default: 'OS'
runs:
  using: 'composite'
  steps:
    - run: echo "${{ inputs.signal }}"
      shell: bash
```

---

## 2. GitHub Projects (V2)

### Project Structure

```
BlackRoad Roadmap
├── 📋 Backlog
│   └── Ideas, future features
├── 🎯 Ready
│   └── Spec'd and ready to start
├── 🚧 In Progress
│   └── Currently being worked on
├── 👀 In Review
│   └── PRs open, awaiting review
└── ✅ Done
    └── Shipped!
```

### Custom Fields

| Field | Type | Values |
|-------|------|--------|
| Priority | Single select | P0, P1, P2, P3 |
| Org | Single select | OS, AI, CLD, HW, ... |
| Size | Single select | XS, S, M, L, XL |
| Sprint | Iteration | 2-week sprints |

### GraphQL API

```graphql
# Get project items
query {
  organization(login: "BlackRoad-OS") {
    projectV2(number: 1) {
      items(first: 100) {
        nodes {
          content {
            ... on Issue {
              title
              state
            }
          }
          fieldValues(first: 10) {
            nodes {
              ... on ProjectV2ItemFieldSingleSelectValue {
                name
                field { ... on ProjectV2SingleSelectField { name } }
              }
            }
          }
        }
      }
    }
  }
}
```

### CLI Commands

```bash
# List projects
gh project list --owner BlackRoad-OS

# View project
gh project view 1 --owner BlackRoad-OS

# Add issue to project
gh project item-add 1 --owner BlackRoad-OS --url https://github.com/BlackRoad-OS/repo/issues/123
```

---

## 3. GitHub Wiki

### Wiki Structure

```
wiki/
├── Home.md                    ← Landing page
├── Getting-Started.md
├── Architecture/
│   ├── Overview.md
│   ├── Bridge.md
│   └── Operator.md
├── Orgs/
│   ├── BlackRoad-OS.md
│   ├── BlackRoad-AI.md
│   └── ...
├── Integrations/
│   ├── Salesforce.md
│   ├── Stripe.md
│   └── Cloudflare.md
└── _Sidebar.md               ← Navigation
```

### Sidebar Template

```markdown
<!-- _Sidebar.md -->
# BlackRoad Wiki

**Getting Started**
- [[Home]]
- [[Installation]]
- [[Quick Start]]

**Architecture**
- [[Bridge]]
- [[Operator]]
- [[Signals]]

**Organizations**
- [[OS]] | [[AI]] | [[Cloud]]
- [[Hardware]] | [[Labs]]

**Integrations**
- [[Salesforce]] | [[Stripe]]
- [[Cloudflare]] | [[Google]]
```

### Git-based Wiki

```bash
# Clone wiki
git clone https://github.com/BlackRoad-OS/.github.wiki.git

# Edit locally
cd .github.wiki
echo "# New Page" > New-Page.md

# Push changes
git add .
git commit -m "Add new page"
git push
```

---

## 4. GitHub Codespaces

### Devcontainer Config

```json
// .devcontainer/devcontainer.json
{
  "name": "BlackRoad Dev",
  "image": "mcr.microsoft.com/devcontainers/python:3.11",

  "features": {
    "ghcr.io/devcontainers/features/node:1": {},
    "ghcr.io/devcontainers/features/github-cli:1": {},
    "ghcr.io/devcontainers/features/docker-in-docker:2": {}
  },

  "postCreateCommand": "pip install -r requirements.txt",

  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "github.copilot",
        "esbenp.prettier-vscode"
      ],
      "settings": {
        "python.defaultInterpreterPath": "/usr/local/bin/python"
      }
    }
  },

  "forwardPorts": [8000, 3000],

  "secrets": {
    "SF_USERNAME": {
      "description": "Salesforce username"
    },
    "STRIPE_KEY": {
      "description": "Stripe API key"
    }
  }
}
```

### Codespace Prebuilds

```yaml
# .github/workflows/codespaces-prebuild.yml
name: Codespaces Prebuild

on:
  push:
    branches: [main]
    paths:
      - '.devcontainer/**'
      - 'requirements.txt'
  workflow_dispatch:

jobs:
  prebuild:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: devcontainers/ci@v0.3
        with:
          push: always
```

---

## 5. GitHub Discussions

### Categories

| Category | Purpose |
|----------|---------|
| 📣 Announcements | Official updates |
| 💡 Ideas | Feature requests |
| 🙏 Q&A | Questions and answers |
| 🙌 Show and Tell | Share what you've built |
| 💬 General | Everything else |

### Discussion Templates

```markdown
<!-- .github/DISCUSSION_TEMPLATE/ideas.yml -->
title: "[Idea] "
labels: ["enhancement", "idea"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for sharing your idea!

  - type: textarea
    id: problem
    attributes:
      label: Problem
      description: What problem does this solve?
    validations:
      required: true

  - type: textarea
    id: solution
    attributes:
      label: Proposed Solution
      description: How would you solve it?
```

---

## 6. Issue & PR Templates

### Issue Templates

```yaml
# .github/ISSUE_TEMPLATE/bug_report.yml
name: Bug Report
description: Report something that's broken
title: "[Bug] "
labels: ["bug", "triage"]
body:
  - type: textarea
    id: description
    attributes:
      label: What happened?
      placeholder: Describe the bug...
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: Expected behavior

  - type: dropdown
    id: org
    attributes:
      label: Which org?
      options:
        - OS (Bridge)
        - AI
        - Cloud
        - Hardware
        - Other
```

### PR Template

```markdown
<!-- .github/PULL_REQUEST_TEMPLATE.md -->
## Summary
<!-- What does this PR do? -->

## Changes
<!-- List of changes -->
-
-

## Testing
<!-- How was this tested? -->
- [ ] Unit tests
- [ ] Integration tests
- [ ] Manual testing

## Signals
<!-- What signals will this emit? -->
- `✔️ OS → OS : feature_shipped`

## Checklist
- [ ] Tests pass
- [ ] Docs updated
- [ ] No secrets committed
```

---

## CLI Reference

```bash
# Issues
gh issue create --title "Bug" --body "Description"
gh issue list --label bug
gh issue close 123

# PRs
gh pr create --title "Feature" --body "Description"
gh pr list --state open
gh pr merge 123

# Actions
gh run list
gh run watch
gh workflow run deploy.yml

# Projects
gh project list
gh project item-add 1 --url ISSUE_URL

# Codespaces
gh codespace create
gh codespace list
gh codespace ssh

# Releases
gh release create v1.0.0 --generate-notes
```

---

## Signals

```
📝 OS → OS : issue_created, repo=.github, number=123
🔀 OS → OS : pr_merged, repo=operator, branch=feature/routing
✔️ OS → OS : workflow_success, name=CI, run=456
🚀 OS → OS : release_published, tag=v1.0.0
💬 OS → OS : discussion_answered, category=Q&A
```

---

*GitHub is the foundation. Build on it.*
