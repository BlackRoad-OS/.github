#!/bin/bash
#
# BlackRoad Agent Quick Start
# Run this after opening the codespace to verify everything works
#

set -e

echo "🤖 BlackRoad Agent Quick Start"
echo "================================"
echo ""

# Check Python
echo "✓ Checking Python..."
python --version

# Check Ollama
echo "✓ Checking Ollama..."
if command -v ollama &> /dev/null; then
    echo "  Ollama installed"
    
    # Start Ollama if not running
    if ! pgrep -x "ollama" > /dev/null; then
        echo "  Starting Ollama..."
        ollama serve > /tmp/ollama.log 2>&1 &
        sleep 3
    fi
    
    # List available models
    echo "  Available models:"
    ollama list | head -10
else
    echo "  ⚠️  Ollama not installed yet. Run .devcontainer/setup.sh"
fi

# Check Wrangler
echo "✓ Checking Wrangler (Cloudflare CLI)..."
if command -v wrangler &> /dev/null; then
    wrangler --version
else
    echo "  ⚠️  Wrangler not installed"
fi

# Test agent orchestrator
echo ""
echo "✓ Testing Agent Orchestrator..."
python -m codespace_agents.orchestrator > /tmp/agent-test.log 2>&1
if [ $? -eq 0 ]; then
    echo "  All agents loaded successfully!"
    echo ""
    echo "  Available agents:"
    grep "Loaded agent:" /tmp/agent-test.log | sed 's/.*Loaded/  -/'
else
    echo "  ⚠️  Agent orchestrator test failed"
    cat /tmp/agent-test.log
fi

# Show next steps
echo ""
echo "================================"
echo "✨ Setup Complete!"
echo ""
echo "Next steps:"
echo ""
echo "  1. Chat with an agent:"
echo "     python -m codespace_agents.chat --agent coder 'Write a hello world function'"
echo ""
echo "  2. Try the examples:"
echo "     python -m codespace_agents.examples"
echo ""
echo "  3. Start a collaborative session:"
echo "     python -m codespace_agents.collaborate"
echo ""
echo "  4. Deploy to Cloudflare:"
echo "     cd codespace-agents/workers && wrangler deploy"
echo ""
echo "📚 Documentation:"
echo "  - Getting Started: CODESPACE_GUIDE.md"
echo "  - Agent Docs: codespace-agents/README.md"
echo "  - Models: codespace-agents/MODELS.md"
echo ""
echo "================================"
