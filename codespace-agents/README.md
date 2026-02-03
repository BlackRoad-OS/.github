# BlackRoad AI Agents

> **Collaborative AI agents for code, design, and operations**

---

## Overview

This directory contains configuration and code for BlackRoad's collaborative AI agents. These agents work together to handle coding tasks, design work, infrastructure management, and more.

## Agent Architecture

```
┌─────────────────────────────────────────────────────┐
│              AGENT MESH NETWORK                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐         │
│  │  CODER  │───│ DESIGNER│───│   OPS   │         │
│  │  AGENT  │   │  AGENT  │   │  AGENT  │         │
│  └────┬────┘   └────┬────┘   └────┬────┘         │
│       │             │             │               │
│       └─────────────┼─────────────┘               │
│                     │                             │
│              ┌──────┴──────┐                      │
│              │  ORCHESTRATOR│                      │
│              │    (Router)  │                      │
│              └──────┬───────┘                      │
│                     │                             │
│         ┌───────────┼───────────┐                 │
│         ▼           ▼           ▼                 │
│    [Llama 3.2] [Mistral]  [CodeLlama]            │
│    [Qwen2.5]   [DeepSeek] [Phi-3]                │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## Available Agents

### 1. Coder Agent (`coder`)
- **Model**: CodeLlama, DeepSeek-Coder, Qwen2.5-Coder
- **Role**: Write, review, and refactor code
- **Capabilities**:
  - Code generation and completion
  - Bug fixes and debugging
  - Code review and suggestions
  - Documentation generation
  - Test case creation

### 2. Designer Agent (`designer`)
- **Model**: Llama 3.2, GPT-4 Vision
- **Role**: Design UI/UX, create assets
- **Capabilities**:
  - UI component design
  - Color palette generation
  - Layout suggestions
  - Accessibility checks
  - Design system maintenance

### 3. Ops Agent (`ops`)
- **Model**: Mistral, Llama 3.2
- **Role**: Infrastructure and deployment
- **Capabilities**:
  - DevOps automation
  - CI/CD pipeline management
  - Infrastructure as Code
  - Monitoring and alerts
  - Deployment strategies

### 4. Analyst Agent (`analyst`)
- **Model**: Llama 3.2, Phi-3
- **Role**: Data analysis and insights
- **Capabilities**:
  - Data processing
  - Metrics analysis
  - Report generation
  - Anomaly detection
  - Predictive analytics

### 5. Docs Agent (`docs`)
- **Model**: Gemma 2, Llama 3.2
- **Role**: Documentation and content
- **Capabilities**:
  - Technical documentation
  - API documentation
  - Tutorial creation
  - README generation
  - Knowledge base management

## Open Source Models

All agents use 100% open source, commercially-friendly AI models:

| Model | Size | Use Case | License |
|-------|------|----------|---------|
| **Llama 3.2** | 3B, 1B | General purpose, chat | Meta (Commercial OK) |
| **CodeLlama** | 7B, 13B | Code generation | Meta (Commercial OK) |
| **Mistral** | 7B | Instruction following | Apache 2.0 |
| **Qwen2.5-Coder** | 7B | Code generation | Apache 2.0 |
| **DeepSeek-Coder** | 6.7B | Code completion | MIT |
| **Phi-3** | 3.8B | Reasoning, analysis | MIT |
| **Gemma 2** | 2B, 9B | Text generation | Gemma Terms (Commercial OK) |

## Agent Communication

Agents communicate via:
- **MCP (Model Context Protocol)**: For tool use and context sharing
- **WebSockets**: For real-time collaboration
- **Cloudflare KV**: For persistent state
- **Signals**: For event notifications

## Quick Start

### Start All Agents
```bash
python -m agents.orchestrator start
```

### Chat with Specific Agent
```bash
# Code-related task
python -m agents.chat --agent coder "Refactor this function"

# Design task
python -m agents.chat --agent designer "Create a color palette"

# Ops task
python -m agents.chat --agent ops "Deploy to production"
```

### Group Collaboration
```bash
# Start a collaborative session
python -m agents.collaborate \
  --agents coder,designer,ops \
  --task "Build a new dashboard feature"
```

## Configuration

Each agent is configured in `agents/config/`:
- `coder.yaml` - Coder agent settings
- `designer.yaml` - Designer agent settings
- `ops.yaml` - Ops agent settings
- `analyst.yaml` - Analyst agent settings
- `docs.yaml` - Docs agent settings

## Development

### Adding a New Agent
1. Create configuration in `agents/config/new-agent.yaml`
2. Implement agent logic in `agents/new_agent.py`
3. Register in `agents/orchestrator.py`
4. Update this README

### Testing Agents
```bash
# Test individual agent
python -m agents.test --agent coder

# Test collaboration
python -m agents.test --scenario collaboration
```

## Integration with Cloudflare Workers

Agents can be deployed as edge workers:
```bash
cd agents/workers
wrangler deploy coder-agent
wrangler deploy designer-agent
wrangler deploy ops-agent
```

## Signals

Agents emit signals to the BlackRoad OS:
```
🤖 AI → OS : agent_started, agent=coder
💬 AI → OS : agent_response, agent=coder, task=complete
🔄 AI → OS : agent_collaboration, agents=[coder,designer]
📊 AI → OS : agent_metrics, tokens=1234, cost=0.01
```

## Architecture Notes

- **Local First**: All models run via Ollama locally when possible
- **Cloud Fallback**: Falls back to OpenAI/Anthropic APIs if needed
- **Cost Tracking**: Every request is logged with cost/token usage
- **Parallel Execution**: Agents can work on different tasks simultaneously
- **State Management**: Shared context via MCP and Cloudflare KV

---

*Agents that work together, build together.*
