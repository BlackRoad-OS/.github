# Getting Started with BlackRoad

> **From zero to productive in 15 minutes.**

---

## Prerequisites

- GitHub account
- Git installed locally
- Python 3.11+ (for prototypes)
- Node.js 18+ (optional, for frontend work)

---

## Step 1: Understand The Bridge

The Bridge is the central coordination point for all BlackRoad organizations.

```bash
# Clone The Bridge
git clone https://github.com/BlackRoad-OS/.github.git
cd .github

# Explore the structure
cat INDEX.md        # Table of contents
cat .STATUS         # Real-time beacon
cat MEMORY.md       # Persistent context
```

---

## Step 2: Choose Your Path

### Path A: Explore the Ecosystem

```bash
# Read the architecture
cat BLACKROAD_ARCHITECTURE.md

# Browse organizations
ls orgs/

# Check a specific org
cat orgs/BlackRoad-AI/README.md
```

### Path B: Run the Operator Prototype

The Operator is our routing engine - it determines which org should handle a request.

```bash
# Navigate to operator
cd prototypes/operator

# Install dependencies (if needed)
pip install -r requirements.txt 2>/dev/null || echo "No deps needed"

# Run a query
python -m operator.cli "What is the weather?"
# Output: BlackRoad-AI (95% confidence)

# Interactive mode
python -m operator.cli --interactive
```

### Path C: View Live Metrics

```bash
# Navigate to metrics
cd prototypes/metrics

# Install dependencies (if needed)
pip install -r requirements.txt 2>/dev/null || echo "No deps needed"

# View dashboard
python -m metrics.dashboard

# Compact view
python -m metrics.dashboard --compact

# Watch mode (live updates)
python -m metrics.dashboard --watch
```

---

## Step 3: Understand the Signal System

BlackRoad uses a morse code-style signal protocol for agent coordination.

### Signal Format

```
[ICON] [FROM] → [TO] : [ACTION], [metadata...]
```

### Examples

```bash
# Success signal
✔️ OS → OS : tests_passed, repo=operator, build=123

# Failure signal
❌ AI → OS : route_failed, reason=timeout, duration=5s

# Broadcast signal
📡 OS → ALL : status_update, health=5/5

# Targeted signal
🎯 CLD → OS : deploy_complete, worker=api, region=us-west
```

See [SIGNALS.md](https://github.com/BlackRoad-OS/.github/blob/main/SIGNALS.md) for full protocol.

---

## Step 4: Explore Organizations

Each organization has its own blueprint in the Bridge.

```bash
# List all orgs
ls orgs/

# Structure of each org
orgs/[ORG-NAME]/
├── README.md       # Mission & vision
├── REPOS.md        # Repository list
└── SIGNALS.md      # Signal patterns
```

### Tier 1: Core Infrastructure

```bash
cat orgs/BlackRoad-OS/README.md      # The Bridge, mesh, operator
cat orgs/BlackRoad-AI/README.md      # AI routing & intelligence
cat orgs/BlackRoad-Cloud/README.md   # Edge compute & Cloudflare
```

### Tier 2: Support Systems

```bash
cat orgs/BlackRoad-Hardware/README.md  # Pi cluster, Hailo-8
cat orgs/BlackRoad-Security/README.md  # Zero trust, vault
cat orgs/BlackRoad-Labs/README.md      # R&D experiments
```

---

## Step 5: Work with Templates

The Bridge includes templates for common integrations.

```bash
# List templates
ls templates/

# View a template
cat templates/github-ecosystem/README.md
cat templates/salesforce-sync/README.md
cat templates/stripe-billing/README.md
```

### Using a Template

```bash
# Copy template to your repo
cp -r templates/salesforce-sync/* /path/to/your/repo/

# Customize configuration
vim config.yml

# Follow the README
cat README.md
```

---

## Step 6: Check Routes

The Bridge defines routes for common patterns.

```bash
# List routes
ls routes/

# View routing logic
cat routes/README.md  # (if exists)
```

---

## Step 7: Contribute

### Making Changes

```bash
# Create a branch
git checkout -b feature/your-feature

# Make changes
vim orgs/BlackRoad-AI/README.md

# Commit with descriptive message
git commit -am "Update AI org blueprint"

# Push and create PR
git push origin feature/your-feature
gh pr create --title "Update AI org blueprint" --body "Description"
```

### Signal Your Changes

Include signals in your commit messages and PRs:

```
✔️ OS → OS : blueprint_updated, org=AI, files=1

Updated BlackRoad-AI blueprint with new repository structure.
```

---

## Common Tasks

### Task: Find where a feature should live

```bash
# Use the operator
cd prototypes/operator
python -m operator.cli "Where should authentication logic go?"
# Output: BlackRoad-Security (90%)
```

### Task: Check ecosystem health

```bash
# View metrics
cd prototypes/metrics
python -m metrics.dashboard --compact
```

### Task: Add a new integration

```bash
# Check existing templates
ls templates/

# If template exists, copy it
cp -r templates/[template]/ /path/to/repo/

# If no template, document it
vim INTEGRATIONS.md
```

### Task: Update organization structure

```bash
# Edit the org blueprint
vim orgs/BlackRoad-[ORG]/README.md

# Update repos list
vim orgs/BlackRoad-[ORG]/REPOS.md

# Document signals
vim orgs/BlackRoad-[ORG]/SIGNALS.md
```

---

## Development Workflow

### 1. Start with Memory

```bash
# Read context
cat MEMORY.md

# Check status
cat .STATUS
```

### 2. Make Changes

```bash
# Work in your area
vim orgs/BlackRoad-AI/README.md
```

### 3. Test Locally

```bash
# If code changes
python -m pytest  # or npm test

# If prototype changes
cd prototypes/operator
python -m operator.cli --test
```

### 4. Signal Success

```bash
git commit -m "✔️ AI → OS : blueprint_updated"
```

### 5. Update Memory (if significant)

```bash
# Document major changes
vim MEMORY.md

# Add to "What We've Built" section
```

---

## Key Files Reference

| File | Purpose | When to Use |
|------|---------|-------------|
| `INDEX.md` | Table of contents | Start here for navigation |
| `MEMORY.md` | Persistent context | Before/after sessions |
| `.STATUS` | Real-time beacon | Check current health |
| `SIGNALS.md` | Signal protocol | Learn coordination |
| `STREAMS.md` | Data flow patterns | Understand data movement |
| `REPO_MAP.md` | Ecosystem map | See all repos |
| `BLACKROAD_ARCHITECTURE.md` | The vision | Understand why |

---

## Getting Help

### Read the Docs

1. Start with [Architecture Overview](Architecture/Overview)
2. Check [organization pages](Orgs/BlackRoad-OS)
3. Review [integration guides](Integrations/Salesforce)

### Ask Questions

- Open a GitHub Discussion
- Create an issue with the `question` label
- Check existing documentation in `orgs/` directory

### Explore Examples

- Look at `prototypes/` for working code
- Check `templates/` for integration patterns
- Review `orgs/*/REPOS.md` for repository examples

---

## Next Steps

- **Architecture**: Read [Architecture Overview](Architecture/Overview)
- **Organizations**: Browse [BlackRoad-OS](Orgs/BlackRoad-OS)
- **Integrations**: Check [Salesforce Guide](Integrations/Salesforce)
- **Advanced**: Study [The Operator](Architecture/Operator)

---

*You're ready. Start building.*
