# BlackRoad Agent Codespace

> **Collaborative AI agents powered by open source models**

This repository includes a complete GitHub Codespaces configuration with AI agents that work together on coding projects.

## 🚀 Quick Start

1. **Open in Codespace**: Click "Code" → "Create codespace"
2. **Wait for setup**: AI models will download automatically (~5-10 min)
3. **Start collaborating**: Use the agent CLI tools

```bash
# Chat with an agent
python -m codespace_agents.chat --agent coder "Write a function to sort a list"

# Start a group session
python -m codespace_agents.collaborate
```

## 🤖 Available Agents

- **Coder**: Code generation, review, debugging (Qwen2.5-Coder)
- **Designer**: UI/UX design, accessibility (Llama 3.2)
- **Ops**: DevOps, deployment, infrastructure (Mistral)
- **Docs**: Technical documentation, tutorials (Gemma 2)
- **Analyst**: Data analysis, metrics, insights (Phi-3)

## 📚 Documentation

- [Codespace Guide](CODESPACE_GUIDE.md) - Getting started
- [Agent Documentation](codespace_agents/README.md) - Agent details
- [Model Information](codespace_agents/MODELS.md) - Open source models

## ✨ Features

✅ 100% open source AI models  
✅ Commercially friendly licenses  
✅ Local-first (no API costs)  
✅ Cloud fallback (optional)  
✅ Collaborative sessions  
✅ Cloudflare Workers deployment  
✅ GitHub Copilot compatible  

---
