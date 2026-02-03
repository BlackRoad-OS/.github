# The Bridge

> **Central coordination. Memory. Routing. Everything connects here.**

---

## What is The Bridge?

The Bridge is the central coordination point for all BlackRoad organizations. It lives in `BlackRoad-OS/.github` and serves as:

1. **Coordination Hub**: Routes requests between organizations
2. **Memory System**: Maintains context across sessions
3. **Signal Router**: Coordinates agent communication
4. **Blueprint Storage**: Holds all organization specifications
5. **Status Beacon**: Provides real-time system health

---

## Why Git?

The Bridge lives in Git for several critical reasons:

### 1. Version Control
```bash
# See what changed
git log --oneline

# Compare states
git diff HEAD~1

# Rollback if needed
git revert abc123
```

### 2. Distributed by Default
- Every clone is a full backup
- No single point of failure
- Works offline

### 3. Human Readable
- Text files, not binary blobs
- Easy to inspect: `cat MEMORY.md`
- Diff-able changes

### 4. Survives Disconnects
```
Session 1: Update MEMORY.md → Commit → Push
[Disconnect]
Session 2: Pull → Read MEMORY.md → Continue
```

### 5. GitHub Integration
- Actions for automation
- Issues for tracking
- PRs for collaboration
- Wiki for documentation

---

## Bridge Components

```
BlackRoad-OS/.github/
│
├── Core Coordination
│   ├── .STATUS              ← Real-time beacon
│   ├── MEMORY.md            ← Persistent context
│   ├── SIGNALS.md           ← Coordination protocol
│   ├── STREAMS.md           ← Data flow patterns
│   └── INDEX.md             ← Navigation hub
│
├── Organization Blueprints
│   └── orgs/
│       ├── BlackRoad-OS/    ← 15 org specs
│       ├── BlackRoad-AI/
│       └── ...
│
├── Working Prototypes
│   └── prototypes/
│       ├── operator/        ← Routing engine
│       └── metrics/         ← KPI dashboard
│
├── Integration Templates
│   └── templates/
│       ├── salesforce-sync/
│       ├── stripe-billing/
│       └── ...
│
└── Configuration
    ├── routes/              ← Routing rules
    └── nodes/               ← Pi cluster config
```

---

## The Memory System

### Purpose
Maintain context across disconnects and sessions.

### Structure

```markdown
# MEMORY.md

## Current State
- Last updated
- Active session
- Participants

## What We've Built
- Completed features
- File counts
- Decisions made

## Active Threads
- Work in progress
- Future plans

## Conversation Context
- Recent discussions
- Key decisions
- Team dynamics
```

### Usage

**Before starting work:**
```bash
cat MEMORY.md          # Read context
git log --oneline -10  # See recent changes
cat .STATUS            # Check current health
```

**After significant work:**
```bash
vim MEMORY.md          # Update context
git commit -am "Update MEMORY: completed feature X"
git push
```

### Benefits

1. **Continuity**: New sessions pick up where old ones left off
2. **Knowledge Transfer**: Anyone can catch up quickly
3. **Accountability**: Clear record of decisions
4. **Learning**: Historical context for future work

---

## The Status Beacon

`.STATUS` is a real-time indicator of system health.

### Format

```yaml
status: operational
timestamp: 2026-01-27T19:43:32Z
health: 5/5
active_orgs: 15/15
bridge_version: v1.0.0
last_signal: ✔️ OS → OS : health_check_passed
```

### Update Mechanism

```python
# prototypes/metrics/status_updater.py
def update_status():
    health = calculate_health()
    status = {
        'status': 'operational' if health >= 4 else 'degraded',
        'timestamp': datetime.now().isoformat(),
        'health': f'{health}/5',
        'active_orgs': f'{count_active_orgs()}/15',
    }
    write_status_file(status)
    emit_signal('✔️ OS → OS : status_updated')
```

### Monitoring

```bash
# Watch status in real-time
watch -n 5 cat .STATUS

# Get status in CI
status=$(cat .STATUS | grep "^status:" | cut -d' ' -f2)
if [ "$status" != "operational" ]; then
    echo "Bridge degraded!"
    exit 1
fi
```

---

## Signal Routing

The Bridge routes signals between organizations.

### Signal Format

```
[ICON] [FROM] → [TO] : [ACTION], [metadata...]
```

### Routing Rules

```python
# Broadcast signals (📡) go to all orgs
if signal.icon == '📡':
    route_to_all_orgs(signal)

# Targeted signals (🎯) go to specific org
elif signal.icon == '🎯':
    route_to_org(signal.target, signal)

# Success/failure (✔️/❌) go back to caller
elif signal.icon in ['✔️', '❌']:
    route_to_caller(signal)
```

### Examples

```bash
# Broadcast: Everyone hears
📡 OS → ALL : maintenance_window, start=2026-01-28T00:00Z

# Targeted: Only AI receives
🎯 OS → AI : route_request, query="weather"

# Success: Back to caller
✔️ AI → OS : route_complete, service=openai

# Failure: Back to caller
❌ CLD → OS : deploy_failed, reason=timeout
```

---

## Organization Blueprints

### Blueprint Structure

```
orgs/BlackRoad-AI/
├── README.md       # Mission, vision, architecture
├── REPOS.md        # List of repositories
└── SIGNALS.md      # Signal patterns for this org
```

### README.md Template

```markdown
# BlackRoad-AI

> **Route to intelligence, don't build it.**

## Mission
AI/ML routing and aggregation

## Architecture
[Diagrams and details]

## Repositories
See [REPOS.md](REPOS.md)

## Signals
See [SIGNALS.md](SIGNALS.md)
```

### REPOS.md Template

```markdown
# BlackRoad-AI Repositories

| Repo | Purpose | Status |
|------|---------|--------|
| ai-router | Route to AI services | Active |
| ai-agents | Agent coordination | Planned |
| ai-prompts | Prompt templates | Active |
```

### SIGNALS.md Template

```markdown
# BlackRoad-AI Signals

## Emits
- ✔️ AI → OS : route_complete
- ❌ AI → OS : route_failed

## Receives
- 🎯 OS → AI : route_request
```

---

## The Operator

The Operator is the Bridge's routing engine.

### Components

1. **Parser**: Extract intent from request
2. **Classifier**: Score all orgs
3. **Router**: Select best org
4. **Emitter**: Send routing signal

### Flow

```
Request
  ↓
Parser
  ↓
Intent
  ↓
Classifier
  ↓
Scores
  ↓
Router
  ↓
Selected Org
  ↓
Emitter
  ↓
Signal
```

### Example

```bash
$ python -m operator.cli "Deploy my app"

Parsing: "Deploy my app"
Intent: deployment, infrastructure

Scoring organizations:
  - BlackRoad-Cloud: 95%
  - BlackRoad-OS: 70%
  - BlackRoad-Hardware: 30%

Routing to: BlackRoad-Cloud (95%)

Signal: 🎯 OS → CLD : route_request, intent=deploy
```

See [The Operator](Operator) for details.

---

## Metrics & Health

### Health Calculation

```python
def calculate_health():
    score = 0
    
    # All orgs blueprinted?
    if count_orgs() == 15:
        score += 1
    
    # Prototypes working?
    if test_operator() and test_metrics():
        score += 1
    
    # Recent commits?
    if commits_last_24h() > 0:
        score += 1
    
    # No broken links?
    if check_links() == 0:
        score += 1
    
    # Status file updated?
    if status_age_minutes() < 60:
        score += 1
    
    return score  # 0-5
```

### Dashboard

```bash
$ python -m metrics.dashboard

╔══════════════════════════════════════╗
║        BLACKROAD METRICS             ║
╚══════════════════════════════════════╝

Health:           🟢 5/5
Organizations:    15/15 active
Repositories:     86 defined
Files:            71 in Bridge
Lines:            ~10,000 total
Last Updated:     2026-01-27 19:43:32
Status:           operational

Recent Signals:
  ✔️ OS → OS : health_check_passed
  ✔️ OS → OS : metrics_calculated
  📡 OS → ALL : status_update
```

---

## Integration with GitHub

### Actions

```yaml
# .github/workflows/status-update.yml
name: Update Status

on:
  schedule:
    - cron: '*/5 * * * *'  # Every 5 minutes

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Update status
        run: |
          python -m metrics.status_updater
          git add .STATUS
          git commit -m "📡 OS → ALL : status_updated"
          git push
```

### Wiki

- Bridge documentation lives in Wiki
- Auto-generated from blueprints
- Updated via git

### Issues & PRs

- Feature requests → Issues
- Changes → PRs
- Signals in commit messages

---

## Bridge Operations

### Starting a Session

```bash
# 1. Pull latest
git pull

# 2. Read context
cat MEMORY.md
cat .STATUS

# 3. Check health
python -m metrics.dashboard --compact

# 4. Begin work
git checkout -b feature/new-feature
```

### During Work

```bash
# Signal progress
git commit -m "✔️ OS → OS : feature_started"

# Update memory if significant
vim MEMORY.md
```

### Ending a Session

```bash
# Update memory
vim MEMORY.md

# Final commit
git commit -am "📡 OS → ALL : session_complete"

# Push changes
git push

# Update status
python -m metrics.status_updater
```

---

## Best Practices

1. **Read MEMORY.md first**: Always catch up on context
2. **Check .STATUS**: Know the system health
3. **Use signals**: Communicate via protocol
4. **Update memory**: Document significant work
5. **Keep blueprints current**: Orgs evolve
6. **Test prototypes**: Ensure they work
7. **Emit signals**: Let others know what happened

---

## Troubleshooting

### Bridge is unhealthy

```bash
# Check what's wrong
python -m metrics.dashboard

# Review recent changes
git log --oneline -10

# Check for errors
grep "❌" .STATUS
```

### Memory is stale

```bash
# Pull latest
git pull

# Update MEMORY.md
vim MEMORY.md
git commit -am "Update MEMORY"
git push
```

### Signals not routing

```bash
# Check signal format
cat SIGNALS.md

# Verify organization blueprints
ls orgs/*/SIGNALS.md

# Test operator
cd prototypes/operator
python -m operator.cli --test
```

---

## Learn More

- **[Architecture Overview](Overview)** - The big picture
- **[The Operator](Operator)** - Routing engine details
- **[Organizations](../Orgs/BlackRoad-OS)** - Explore the 15 orgs

---

*The Bridge connects everything. Keep it healthy.*
