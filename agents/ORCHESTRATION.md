# Agent Orchestration

> **How agents coordinate through the mesh. Swarms, tasks, and message passing.**

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        ORCHESTRATOR                              │
│                                                                  │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │   TASK      │    │   MESSAGE   │    │   MEMORY    │         │
│  │  SCHEDULER  │◄──►│     BUS     │◄──►│   SYSTEM    │         │
│  └──────┬──────┘    └──────┬──────┘    └─────────────┘         │
│         │                  │                                     │
└─────────┼──────────────────┼─────────────────────────────────────┘
          │                  │
    ┌─────┴─────┐      ┌─────┴─────┐
    │           │      │           │
┌───┴───┐ ┌───┴───┐ ┌───┴───┐ ┌───┴───┐
│Agent 1│ │Agent 2│ │Agent 3│ │Agent N│
│ type: │ │ type: │ │ type: │ │ type: │
│analyst│ │ engnr │ │ guard │ │  ...  │
└───────┘ └───────┘ └───────┘ └───────┘
```

---

## Components

### Task Scheduler

Distributes work to agents based on type and availability.

```yaml
task:
  id: task-001
  query: "Analyze market trends for Q1"
  assigned_to: [agent-0042, agent-0089]  # analysts
  priority: P1
  deadline: 2026-01-28T00:00:00Z
  status: in_progress
```

**Scheduling Strategies:**
- **Round Robin** - Distribute evenly across available agents
- **Capability Match** - Route to agents with required skills
- **Load Balance** - Send to least busy agent
- **Affinity** - Keep related tasks on same agent

### Message Bus

Central communication hub for all agents.

```
┌─────────────────────────────────────────┐
│              MESSAGE BUS                 │
├─────────────────────────────────────────┤
│  Topics:                                │
│    • tasks.new                          │
│    • tasks.complete                     │
│    • agents.status                      │
│    • swarm.coordinate                   │
│    • memory.sync                        │
└─────────────────────────────────────────┘
```

**Message Types:**
- `task_assigned` - New work for an agent
- `task_complete` - Agent finished work
- `task_failed` - Agent couldn't complete
- `status_update` - Health/load report
- `swarm_join` - Agent joining swarm
- `swarm_leave` - Agent leaving swarm

### Memory System

Persistent state for agents via `[MEMORY]` integration.

```yaml
agent_memory:
  agent_id: agent-0042
  memory_hash: 707b1913cc1abe94
  context:
    - session: session-001
      learned: ["user prefers concise answers"]
    - session: session-002
      learned: ["project uses Python 3.11"]
  long_term:
    expertise: ["data analysis", "visualization"]
    preferences: ["matplotlib over seaborn"]
```

---

## Swarm Operations

Multiple agents working together on complex tasks.

### Swarm Formation

```
User Query: "Research, analyze, and report on AI market"

          ┌────────────────┐
          │   ORCHESTRATOR │
          └───────┬────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
    ▼             ▼             ▼
┌────────┐   ┌────────┐   ┌────────┐
│RESEARCH│   │ANALYST │   │SPEAKER │
│ agent  │──►│ agent  │──►│ agent  │
│ (data) │   │(insight)   │(report)│
└────────┘   └────────┘   └────────┘
```

### Swarm Lifecycle

```bash
# 1. Initialize swarm
POST /swarm/create
{
  "task": "market_analysis",
  "agents": ["researcher", "analyst", "speaker"],
  "timeout": 300
}

# 2. Swarm coordinates
# Agents communicate via message bus
# Each completes their phase

# 3. Swarm completes
# Results aggregated
# Memory updated
```

### Swarm Signals

```
🔄 AI.swarm → OS : swarm_created, id=swarm-001, agents=3
📡 AI.agent-001 → AI.swarm : phase_complete, phase=research
📡 AI.agent-042 → AI.swarm : phase_complete, phase=analysis
📡 AI.agent-099 → AI.swarm : phase_complete, phase=report
✅ AI.swarm → OS : swarm_complete, id=swarm-001, duration=45s
```

---

## Model Support

Agents can use multiple AI backends:

| Provider | Models | Use Case |
|----------|--------|----------|
| **Ollama** | llama3, mistral, phi | Local inference |
| **OpenAI** | gpt-4, gpt-4o | Cloud, high capability |
| **Anthropic** | claude-3, claude-opus | Cloud, long context |
| **Hailo** | tinyllama, quantized | Edge, Pi cluster |

### Model Selection

```yaml
agent_config:
  id: agent-0042
  type: analyst
  model_preference:
    - provider: ollama
      model: llama3.2
      for: ["quick analysis", "simple queries"]
    - provider: openai
      model: gpt-4o
      for: ["complex analysis", "code generation"]
  fallback:
    provider: anthropic
    model: claude-3-sonnet
```

---

## Integration with Bridge

### Routing Flow

```
User → Operator → Agent Type Selection → Swarm/Single → Response

Example:
  "What caused inflation in 2024?"
  → Operator classifies: economics, history
  → Selects: economist + historian agents
  → Swarm coordinates research
  → Speaker agent formats response
  → Response to user
```

### API Endpoints

```bash
# Agent operations
GET  /agents                    # List all agents
GET  /agents/:id                # Get agent details
POST /agents/:id/task           # Assign task

# Swarm operations
POST /swarm/create              # Create swarm
GET  /swarm/:id/status          # Check swarm status
POST /swarm/:id/cancel          # Cancel swarm

# Memory operations
GET  /agents/:id/memory         # Get agent memory
POST /agents/:id/memory         # Update memory
```

---

## CLI Commands

```bash
# Agent management
blackroad agent list                    # List all agents
blackroad agent status agent-0042       # Check agent status
blackroad agent spawn --type=analyst    # Create new agent

# Swarm management
blackroad swarm create \
  --task="analyze data" \
  --agents=researcher,analyst,speaker

blackroad swarm status swarm-001
blackroad swarm logs swarm-001

# Task management
blackroad task assign agent-0042 "analyze Q1 data"
blackroad task status task-001
blackroad task cancel task-001
```

---

## Configuration

### Agent Config (`agent.yaml`)

```yaml
agent:
  id: agent-0042
  name: Nova Spark
  type: analyst

  resources:
    memory_limit: 512MB
    cpu_limit: 1.0
    timeout: 60s

  capabilities:
    - data_analysis
    - pattern_detection
    - visualization

  routing:
    keywords: ["analyze", "data", "patterns", "trends"]
    priority: 5
```

### Swarm Config (`swarm.yaml`)

```yaml
swarm:
  name: research_team

  composition:
    - type: researcher
      count: 2
    - type: analyst
      count: 1
    - type: speaker
      count: 1

  coordination:
    mode: pipeline  # or parallel, hybrid
    timeout: 300s

  output:
    format: markdown
    destination: /results
```

---

## Monitoring

### Health Checks

```bash
# Check all agents
blackroad health agents

# Output:
# agent-0001  ✅ active   cpu=12%  mem=45%
# agent-0002  ✅ active   cpu=8%   mem=32%
# agent-0003  💤 idle     cpu=0%   mem=12%
# agent-0004  ⚠️ overload cpu=95%  mem=88%
```

### Metrics

```yaml
metrics:
  agents:
    total: 1050
    active: 847
    idle: 189
    overloaded: 14

  tasks:
    completed_today: 12847
    failed_today: 23
    avg_duration: 4.2s

  swarms:
    active: 12
    completed_today: 89
    avg_size: 3.4
```

---

## Signals Reference

```
# Agent lifecycle
🤖 AI → OS : agent_spawned, id=X, type=Y
💤 AI → OS : agent_idle, id=X
🔥 AI → OS : agent_overloaded, id=X
💀 AI → OS : agent_terminated, id=X

# Task lifecycle
📋 OS → AI : task_assigned, agent=X, task=Y
⏳ AI → OS : task_started, agent=X, task=Y
✅ AI → OS : task_complete, agent=X, task=Y, duration=Zs
❌ AI → OS : task_failed, agent=X, task=Y, error=E

# Swarm lifecycle
🔄 AI → OS : swarm_created, id=X, agents=[...]
📡 AI → OS : swarm_phase_complete, id=X, phase=Y
✅ AI → OS : swarm_complete, id=X, duration=Zs
❌ AI → OS : swarm_failed, id=X, error=E
```

---

*Agents think. Swarms coordinate. The Bridge orchestrates.*
