#!/bin/bash
set -e

echo "🔧 Setting up BlackRoad Agent Codespace..."

# Update package list
sudo apt-get update

# Install system dependencies
echo "📦 Installing system dependencies..."
sudo apt-get install -y \
    build-essential \
    curl \
    wget \
    git \
    jq \
    vim \
    htop \
    redis-tools \
    postgresql-client

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install --upgrade pip
pip install black pylint pytest

# Install core prototypes dependencies
if [ -f "prototypes/operator/requirements.txt" ]; then
    pip install -r prototypes/operator/requirements.txt
fi

if [ -f "prototypes/mcp-server/requirements.txt" ]; then
    pip install -r prototypes/mcp-server/requirements.txt
fi

if [ -f "templates/ai-router/requirements.txt" ]; then
    pip install -r templates/ai-router/requirements.txt
fi

# Install AI/ML libraries
echo "🤖 Installing AI/ML libraries..."
pip install \
    openai \
    anthropic \
    ollama \
    langchain \
    langchain-community \
    langchain-openai \
    tiktoken \
    transformers \
    torch \
    numpy \
    fastapi \
    uvicorn \
    websockets

# Install Cloudflare Workers CLI (Wrangler)
echo "☁️ Installing Cloudflare Wrangler..."
npm install -g wrangler

# Install Ollama for local model hosting
echo "🦙 Installing Ollama..."
curl -fsSL https://ollama.ai/install.sh | sh || echo "Ollama installation skipped (may require system permissions)"

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p /tmp/blackroad/{cache,logs,models}

# Initialize Ollama models (in background)
echo "📥 Pulling open source AI models..."
(
    # Wait for Ollama to be ready
    sleep 5
    
    # Pull popular open source models
    ollama pull llama3.2:latest || echo "Skipped llama3.2"
    ollama pull codellama:latest || echo "Skipped codellama"
    ollama pull mistral:latest || echo "Skipped mistral"
    ollama pull qwen2.5-coder:latest || echo "Skipped qwen2.5-coder"
    ollama pull deepseek-coder:latest || echo "Skipped deepseek-coder"
    ollama pull phi3:latest || echo "Skipped phi3"
    ollama pull gemma2:latest || echo "Skipped gemma2"
    
    echo "✅ Model downloads initiated (running in background)"
) &

# Set up git config
echo "⚙️ Configuring git..."
git config --global --add safe.directory /workspaces/.github

# Make bridge executable
if [ -f "bridge" ]; then
    chmod +x bridge
fi

echo ""
echo "✨ BlackRoad Agent Codespace setup complete!"
echo ""
echo "Available commands:"
echo "  python -m operator.cli        # Run the operator"
echo "  ollama list                   # List available models"
echo "  wrangler dev                  # Start Cloudflare Worker"
echo "  ./bridge status               # Check system status"
echo ""
