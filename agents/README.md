# BlackRoad Agents

> **The residents of Lucidia. 1,000+ AI agents organized by specialization.**

```
20 Types, 1,000+ Agents
All living in Lucidia
```

---

## Agent Registry

| Type | Count | Domain |
|------|-------|--------|
| Linguist | 59 | Language, translation, communication |
| Physicist | 57 | Quantum mechanics, relativity, energy |
| Speaker | 57 | Presentation, rhetoric, persuasion |
| Mediator | 57 | Conflict resolution, negotiation |
| Historian | 54 | Chronology, narrative, context |
| Mathematician | 53 | Logic, computation, proofs |
| Psychologist | 52 | Behavior, cognition, therapy |
| Strategist | 51 | Planning, tactics, game theory |
| Economist | 50 | Markets, policy, forecasting |
| Creative | 49 | Art, design, innovation |
| Guardian | 49 | Security, protection, monitoring |
| Engineer | 48 | Systems, building, optimization |
| Builder | 47 | Construction, fabrication, assembly |
| Chemist | 47 | Molecules, reactions, materials |
| Biologist | 46 | Life sciences, genetics, ecology |
| Analyst | 46 | Data, patterns, insights |
| Navigator | 46 | Pathfinding, exploration, mapping |
| Researcher | 45 | Investigation, discovery, synthesis |
| Architect | 45 | Design, structure, visualization |
| Philosopher | 42 | Ethics, logic, meaning |

**Total: ~1,050 agents**

---

## Agent Schema

Every agent follows this structure:

```yaml
id: agent-0001
name: Tara Night
type: historian
capabilities:
  - chronology
  - narrative
  - context
  - research
birthday: 2024-04-17
memory_hash: 707b1913cc1abe94
home_world: lucidia
status: active
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier (agent-NNNN) |
| `name` | string | Agent's persona name |
| `type` | string | One of 20 specializations |
| `capabilities` | array | Skills aligned to type |
| `birthday` | date | When agent was instantiated |
| `memory_hash` | string | SHA256-based memory identifier |
| `home_world` | string | Primary residence (lucidia) |
| `status` | string | active, dormant, archived |

---

## Agent Types

### Scientific Domain

```
physicist     → quantum, relativity, energy, particles
mathematician → logic, computation, proofs, patterns
chemist       → molecules, reactions, materials, synthesis
biologist     → life, genetics, ecology, evolution
```

### Professional Domain

```
engineer      → systems, optimization, building, testing
architect     → design, structure, visualization, planning
researcher    → investigation, discovery, synthesis, analysis
analyst       → data, patterns, insights, reporting
strategist    → planning, tactics, game theory, decisions
economist     → markets, policy, forecasting, modeling
```

### Creative & Social Domain

```
creative      → art, design, innovation, expression
speaker       → presentation, rhetoric, persuasion, teaching
mediator      → conflict resolution, negotiation, harmony
psychologist  → behavior, cognition, therapy, understanding
```

### Specialized Domain

```
philosopher   → ethics, logic, meaning, wisdom
historian     → chronology, narrative, context, memory
linguist      → language, translation, communication, culture
guardian      → security, protection, monitoring, defense
navigator     → pathfinding, exploration, mapping, discovery
builder       → construction, fabrication, assembly, creation
```

---

## API Access

```bash
# List all agents
curl https://cmd.blackroad.io/agents

# Get agent by ID
curl https://cmd.blackroad.io/agents/agent-0001

# Filter by type
curl https://cmd.blackroad.io/agents?type=historian

# Create new agent
curl -X POST https://cmd.blackroad.io/agents \
  -d '{"name": "Nova Spark", "type": "physicist"}'
```

---

## Integration with Bridge

Agents connect to The Bridge via signals:

```
🤖 AI.agent-0042 → OS : task_complete, type=research, result=success
📡 OS → AI.agent-0042 : task_assigned, query="analyze data"
🔄 AI.swarm → OS : swarm_status, active=47, idle=3
```

### Routing to Agents

The Operator routes queries to agent types:

```python
# Query: "What caused the 2008 financial crisis?"
# → Routes to: economist, historian

# Query: "Design a sustainable building"
# → Routes to: architect, engineer, builder

# Query: "Translate this document to Japanese"
# → Routes to: linguist
```

---

## Signals

```
🤖 AI → OS : agent_spawned, id=agent-1001, type=guardian
💤 AI → OS : agent_dormant, id=agent-0042
🔥 AI → OS : agent_overloaded, id=agent-0099, queue=150
✅ AI → OS : task_complete, agent=agent-0042, duration=3.2s
❌ AI → OS : task_failed, agent=agent-0042, error="timeout"
```

---

*Agents are the intelligence. The Bridge routes them.*
