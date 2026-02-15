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
if curl -fsSL https://ollama.ai/install.sh | sh; then
    echo "✅ Ollama installed successfully"
    OLLAMA_INSTALLED=true
else
    echo "⚠️  Ollama installation skipped (may require system permissions)"
    OLLAMA_INSTALLED=false
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p /tmp/blackroad/{cache,logs,models}

# Initialize Ollama models (in background) only if Ollama was installed
if [ "$OLLAMA_INSTALLED" = true ] && command -v ollama >/dev/null 2>&1; then
    echo "📥 Pulling open source AI models..."
    (
        LOG_FILE="/tmp/blackroad/logs/ollama_model_pull.log"
        
        # Wait for Ollama to be ready
        sleep 5
        
        echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] Starting Ollama model pulls..." > "$LOG_FILE" 2>&1
        
        # Pull popular open source models
        ollama pull llama3.2:latest >> "$LOG_FILE" 2>&1 || echo "Skipped llama3.2"
        ollama pull codellama:latest >> "$LOG_FILE" 2>&1 || echo "Skipped codellama"
        ollama pull mistral:latest >> "$LOG_FILE" 2>&1 || echo "Skipped mistral"
        ollama pull qwen2.5-coder:latest >> "$LOG_FILE" 2>&1 || echo "Skipped qwen2.5-coder"
        ollama pull deepseek-coder:latest >> "$LOG_FILE" 2>&1 || echo "Skipped deepseek-coder"
        ollama pull phi3:latest >> "$LOG_FILE" 2>&1 || echo "Skipped phi3"
        ollama pull gemma2:latest >> "$LOG_FILE" 2>&1 || echo "Skipped gemma2"
        
        echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] Model downloads complete" >> "$LOG_FILE" 2>&1
        echo "✅ Model downloads initiated (check /tmp/blackroad/logs/ollama_model_pull.log for details)"
    ) &
else
    echo "⚠️  Ollama is not installed; skipping model downloads."
fi

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
