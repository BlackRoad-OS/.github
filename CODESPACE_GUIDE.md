# Getting Started with BlackRoad Agent Codespace

This guide will help you get started with the BlackRoad Agent Codespace and collaborative AI agents.

## Quick Start

### 1. Open in Codespace

Click the "Code" button on GitHub and select "Create codespace on main" (or your branch).

The devcontainer will automatically:
- Install Python, Node.js, and Go
- Set up Ollama for local AI models
- Install Cloudflare Wrangler CLI
- Pull open source AI models in the background
- Configure all dependencies

### 2. Wait for Setup

The initial setup takes 5-10 minutes as it downloads AI models. You can monitor progress:

```bash
# Check if Ollama is ready
ollama list

# See what models are downloading
ps aux | grep ollama
```

### 3. Test the Orchestrator

```bash
# Test agent routing
python -m codespace_agents.orchestrator

# You should see:
# ✅ Loaded agent: Coder (coder)
# ✅ Loaded agent: Designer (designer)
# ✅ Loaded agent: Ops (ops)
# ✅ Loaded agent: Docs (docs)
# ✅ Loaded agent: Analyst (analyst)
```

## Usage Examples

### Example 1: Chat with Coder Agent

```bash
# Ask a coding question
python -m codespace_agents.chat --agent coder "Write a Python function to reverse a string"

# Interactive mode
python -m codespace_agents.chat --agent coder
```

### Example 2: Auto-Route Task

```bash
# Let the orchestrator choose the right agent
python -m codespace_agents.chat "Design a color palette for a dashboard"
# → Routes to Designer agent

python -m codespace_agents.chat "Deploy the app to Cloudflare"
# → Routes to Ops agent
```

### Example 3: Collaborative Session

```bash
# Start a group chat with all agents
python -m codespace_agents.collaborate

# Work with specific agents
python -m codespace_agents.collaborate --agents coder,designer,ops

# Broadcast a task to all agents
python -m codespace_agents.collaborate \
  --mode broadcast \
  --task "Create a new feature: user profile page"

# Sequential handoff (agents work in order)
python -m codespace_agents.collaborate \
  --mode sequential \
  --agents designer,coder,ops \
  --task "Build and deploy a contact form"
```

## Common Workflows

### Workflow 1: Feature Development

```bash
# 1. Design phase
python -m codespace_agents.chat --agent designer \
  "Design a user profile page with avatar, bio, and social links"

# 2. Implementation
python -m codespace_agents.chat --agent coder \
  "Implement the user profile page in React with Tailwind CSS"

# 3. Documentation
python -m codespace_agents.chat --agent docs \
  "Create documentation for the user profile component"

# 4. Deployment
python -m codespace_agents.chat --agent ops \
  "Deploy to Cloudflare Pages"
```

### Workflow 2: Bug Fix

```bash
# 1. Analyze the issue
python -m codespace_agents.chat --agent analyst \
  "Why is the login page slow?"

# 2. Fix the code
python -m codespace_agents.chat --agent coder \
  "Optimize the authentication flow"

# 3. Update docs
python -m codespace_agents.chat --agent docs \
  "Update changelog with performance improvements"
```

### Workflow 3: Collaborative Development

```bash
# Start a group session
python -m codespace_agents.collaborate

# Then in the chat:
You: We need to build a real-time chat feature
Coder: I'll implement the WebSocket backend
Designer: I'll create the chat UI components
Ops: I'll set up the Cloudflare Durable Objects
Docs: I'll document the API
```

## Model Configuration

Models are configured in `codespace-agents/config/`:

```yaml
# codespace-agents/config/coder.yaml
models:
  primary: "qwen2.5-coder:latest"
  fallback:
    - "deepseek-coder:latest"
    - "codellama:latest"
```

You can modify these to use different models.

## Cloud Fallback

If local models are unavailable, agents fall back to cloud APIs:

```bash
# Set API keys (optional)
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
```

Without API keys, only local Ollama models are used.

## Cloudflare Workers

Deploy agents as edge workers:

```bash
cd codespace-agents/workers

# Deploy the router
wrangler deploy agent-router.js

# Deploy coder agent
wrangler deploy coder-agent.js

# Test
curl https://agent-router.YOUR-SUBDOMAIN.workers.dev/health
```

## Troubleshooting

### Models not found

```bash
# Pull models manually
ollama pull qwen2.5-coder
ollama pull llama3.2
ollama pull mistral
ollama pull phi3
ollama pull gemma2

# Check available models
ollama list
```

### Ollama not running

```bash
# Start Ollama service
ollama serve &

# Or check if it's running
ps aux | grep ollama
```

### Port conflicts

If ports are in use, modify `.devcontainer/devcontainer.json`:

```json
"forwardPorts": [
  8080,  // Change if needed
  11434  // Ollama port
]
```

## Tips

1. **Multiple agents**: Run multiple agents in parallel by opening multiple terminals
2. **Cost tracking**: Check `codespace_agents/config/*.yaml` for cost settings
3. **Context**: Agents maintain context within a session but not across sessions
4. **Collaboration**: Agents can request help from each other automatically
5. **Performance**: Smaller models (1B-3B) are faster, larger (7B+) are more capable

## Next Steps

- Explore agent configurations in `codespace-agents/config/`
- Read about available models in `codespace-agents/MODELS.md`
- Try collaborative sessions with multiple agents
- Deploy agents to Cloudflare Workers
- Customize agent prompts and behaviors

## Get Help

- Check agent status: `python -m codespace_agents.orchestrator`
- List models: `ollama list`
- View logs: Check terminal output for errors
- Read docs: All docs in `codespace-agents/`

---

Happy coding with your AI agent team! 🤖✨
