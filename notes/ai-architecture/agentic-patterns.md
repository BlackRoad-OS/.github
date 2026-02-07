# Agentic Architectures

## Single System vs Multi-Agent System

### Single System
```
User ──→ AI Agent ──→ Response
              │
           Memory
           Tools
```

### Multi-Agent System
```
User ──→ AI Agent ←──→ AI Agent
              │              │
           Memory          Tools
           Tools           Memory
```

Multiple agents collaborate, each with their own memory and tools.

## Patterns in Multi-Agent Systems

### 1. Parallel
```
         ┌─ AI Agent ─┐
In ──→───┤             ├───→ Out
         └─ AI Agent ─┘
```
Multiple agents process the same input simultaneously. Good for speed and redundancy.

### 2. Sequential
```
In ──→ AI Agent ──→ AI Agent ──→ Out
```
Each agent's output feeds into the next. Good for pipelines and staged processing.

### 3. Loop
```
In ──→ AI Agent ──→ AI Agent ──→ Out
          ▲              │
          └──────────────┘
```
Agents iterate until a condition is met. Good for refinement and self-correction.

### 4. Router
```
         ┌──→ Out
In ──→ AI Agent
         └──→ Out
```
One agent decides where to send the input. Good for classification and routing.

### 5. Aggregator
```
In ──→───┐
         AI Agent ──→ Out
In ──→───┘
```
Combines multiple inputs into a single output. Good for summarization and synthesis.

### 6. Network
```
         ┌─────────────┐
In ──→ AI Agent ←→ AI Agent ──→ Out
         └─→ AI Agent ←─┘
```
Fully connected agents that can communicate freely. Good for complex reasoning.

### 7. Hierarchical
```
              AI Agent (manager)
             /         \
      AI Agent       AI Agent
```
A manager agent delegates to worker agents. Good for task decomposition.

## Architecture Examples (with Tools)

### Hierarchical (with external services)
```
                    AI Agent (orchestrator)
                   /          |           \
            AI Agent      AI Agent      AI Agent
              |              |              |
         Vector Search   Web Search      Gmail
         Vector Search   Vector Search
```

### Human-in-the-Loop
```
User Input ──→ AI Agent ──→ Person ──→ Response
                  │                       │
               AI Agent ←─────────────────┘
```

### Shared Tools
```
User Input ──→ AI Agent ──→ Response
                  │
            ┌─────┼─────┐
      Vector Search  Web Search  Vector DB
```

### Database with Tools
```
User Input ──→ AI Agent ──→ Response
                  │
            ┌─────┼─────┐
        AI/KB   Web Search  Vector DB
                Data Transform
```

### Memory Transformation
```
User Input ──→ AI Agent ──→ Response
                  │
            ┌─────┼──────────┐
        Web Search  Vector Search  Vector DB
        AI Agent    Memory         Data Transform
```

## Relevance to BlackRoad

BlackRoad's architecture uses several of these patterns:
- **Router**: The Operator classifies and routes requests
- **Hierarchical**: Cece delegates to specialized tools/services
- **Sequential**: Request → classify → route → execute → respond
- **Shared Tools**: Multiple agents share NumPy, Claude, GPT, Hailo-8

## Connections

- Routing patterns connect to [DNS](../networking/dns.md) (hierarchical resolution)
- Agent memory relates to [Python Mutability](../programming/python-mutability.md) (shared vs. isolated state)
- The halting problem ([Halting Problem](../theoretical-cs/halting-problem.md)) limits what agents can decide
