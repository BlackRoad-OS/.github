# BlackRoad Explorer

> **Navigate the entire ecosystem from the command line.**

```
Status: PROTOTYPE
Purpose: Browse orgs, repos, signals from CLI
```

---

## Quick Start

```bash
# List all orgs
python -m explorer.cli orgs

# View specific org
python -m explorer.cli org AI

# List repos for an org
python -m explorer.cli repos AI

# Interactive browser
python -m explorer.cli browse
```

---

## Commands

| Command | Description |
|---------|-------------|
| `orgs` | List all organizations |
| `org <code>` | View org details |
| `repos <code>` | List repos for org |
| `signals <code>` | View signals for org |
| `browse` | Interactive browser |
| `search <term>` | Search across everything |
| `tree` | Show directory tree |

---

## Example Session

```
$ python -m explorer.cli browse

🌉 BlackRoad Explorer
═══════════════════════════════════════

  1. [OS]  BlackRoad-OS        ← The Bridge
  2. [AI]  BlackRoad-AI        Intelligence routing
  3. [CLD] BlackRoad-Cloud     Edge compute
  4. [HW]  BlackRoad-Hardware  Pi cluster
  5. [LAB] BlackRoad-Labs      Experiments
  ...

Select org (1-15) or 'q' to quit: 2

═══════════════════════════════════════
  BlackRoad-AI
  "Route to intelligence, don't build it"
═══════════════════════════════════════

  Repos:
    • router      - The routing brain
    • prompts     - System prompts, Cece's personality
    • agents      - Autonomous agents
    • hailo       - Edge inference
    • models      - Model configs
    • eval        - Benchmarking

  [r] View repos  [s] View signals  [b] Back  [q] Quit
```

---

*Explore the universe without leaving your terminal.*
