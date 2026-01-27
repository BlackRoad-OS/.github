# AI Router

> **Route to intelligence, don't build it.**

```
Template: ai-router
Org: BlackRoad-AI (AI)
Status: READY
Version: 0.1.0
```

---

## What It Does

```
                    ┌─────────────────────────────────────┐
                    │           AI ROUTER                 │
                    │   Route to intelligence             │
                    └──────────────┬──────────────────────┘
                                   │
         ┌─────────────┬───────────┼───────────┬─────────────┐
         ▼             ▼           ▼           ▼             ▼
    ┌─────────┐   ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
    │ OpenAI  │   │Anthropic│ │ Hailo-8 │ │ Ollama  │ │  More   │
    │  GPT-4  │   │ Claude  │ │  Local  │ │  Local  │ │   ...   │
    └─────────┘   └─────────┘ └─────────┘ └─────────┘ └─────────┘
```

The AI Router provides:

1. **Unified API** - One interface for all providers
2. **Smart Routing** - Strategy-based provider selection
3. **Automatic Fallback** - If one fails, try the next
4. **Cost Tracking** - Know exactly what you're spending
5. **Signal Emission** - BlackRoad mesh integration

---

## Quick Start

```bash
# Install
pip install -r requirements.txt

# Set API keys
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."

# Run
python -m ai_router complete "What is 2+2?"

# With specific provider
python -m ai_router complete "Write code" --provider anthropic

# With fallback chain (try local first)
python -m ai_router complete "Analyze" --chain hailo,ollama,openai

# Interactive mode
python -m ai_router interactive
```

---

## Providers

| Provider | Type | Models | Cost |
|----------|------|--------|------|
| **OpenAI** | Cloud | GPT-4o, GPT-4o-mini, GPT-3.5 | $$ |
| **Anthropic** | Cloud | Claude Opus 4, Sonnet 4, Haiku | $$ |
| **Hailo** | Local | Quantized LLMs (Pi + Hailo-8) | FREE |
| **Ollama** | Local | Llama, Mistral, Phi, CodeLlama | FREE |

---

## Routing Strategies

```python
from ai_router import Router

# Cost optimized (default) - cheapest first
router = Router(strategy="cost")

# Latency optimized - fastest first
router = Router(strategy="latency")

# Quality optimized - best model first
router = Router(strategy="quality")

# Local first - always try local before cloud
router = Router(strategy="local_first")

# Cloud first - always try cloud for quality
router = Router(strategy="cloud_first")
```

### Strategy Priority

| Strategy | Priority Order |
|----------|----------------|
| cost | Hailo → Ollama → GPT-4o-mini → Claude Haiku |
| latency | Hailo → Ollama → GPT-4o-mini → Claude Haiku |
| quality | Claude Opus → GPT-4o → Claude Sonnet → Local |
| local_first | Hailo → Ollama → Any Cloud |
| cloud_first | Anthropic → OpenAI → Local |

---

## Python API

```python
from ai_router import Router

router = Router()

# Simple completion
result = await router.complete("What is the meaning of life?")
print(result.content)
print(f"Cost: ${result.total_cost:.4f}")

# With specific provider
result = await router.complete(
    "Write a Python function",
    provider="anthropic",
    model="claude-sonnet-4-20250514"
)

# With fallback chain
result = await router.complete(
    "Analyze this image",
    chain=["hailo", "ollama", "openai"]
)

# Stream response
async for chunk in router.complete_stream("Tell me a story"):
    print(chunk, end="", flush=True)

# Generate embeddings
embeddings = await router.embed("Hello world")
print(f"Dimensions: {embeddings.dimensions}")

# Check health
health = await router.health_check_all()
for provider, status in health.items():
    print(f"{provider}: {status.value}")
```

---

## Cost Tracking

```python
from ai_router import Router
from ai_router.tracking import CostTracker

tracker = CostTracker(storage_path=".costs.json")
router = Router()

# Track usage
result = await router.complete("Hello")
tracker.record_response(result.response)

# Get report
report = tracker.report(period="day")
print(report.summary())
# Cost Report: 2026-01-27 to 2026-01-28
# Total Cost:     $0.0234
# Total Tokens:   15,432
# Total Requests: 47
# By Provider:
#   anthropic: $0.0180 (23 requests)
#   openai: $0.0054 (24 requests)

# Set budget alerts
if tracker.total_cost > 10.0:
    print("Budget exceeded!")
```

---

## CLI Commands

```bash
# Complete a prompt
ai-router complete "What is 2+2?"
ai-router complete "Write code" --provider anthropic
ai-router complete "Analyze" --chain hailo,ollama,openai
ai-router complete "Hello" --strategy quality

# Stream response
ai-router stream "Tell me a story"

# Generate embeddings
ai-router embed "Hello world"
ai-router embed "Hello" --show-vector

# Check provider health
ai-router health

# Show cost report
ai-router costs --period day
ai-router costs --period week

# Interactive mode
ai-router interactive
```

---

## Directory Structure

```
ai-router/
├── ai_router/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── providers/
│   │   ├── __init__.py
│   │   ├── base.py          ← Provider interface
│   │   ├── openai.py        ← GPT-4, embeddings
│   │   ├── anthropic.py     ← Claude
│   │   ├── hailo.py         ← On-device (Hailo-8)
│   │   └── ollama.py        ← Local LLMs
│   ├── routing/
│   │   ├── __init__.py
│   │   ├── router.py        ← Main router
│   │   └── strategy.py      ← Routing strategies
│   ├── tracking/
│   │   ├── __init__.py
│   │   └── costs.py         ← Cost tracking
│   └── signals/
│       ├── __init__.py
│       └── emitter.py       ← Signal emission
├── config.yaml
├── requirements.txt
└── README.md
```

---

## Configuration

```yaml
# config.yaml
providers:
  openai:
    enabled: true
    default_model: gpt-4o-mini
    api_key: ${OPENAI_API_KEY}

  anthropic:
    enabled: true
    default_model: claude-3-5-haiku-20241022
    api_key: ${ANTHROPIC_API_KEY}

  hailo:
    enabled: true
    default_model: tinyllama-1b-q4
    base_url: http://lucidia:5000

  ollama:
    enabled: true
    default_model: llama3.2
    base_url: http://localhost:11434

routing:
  default_strategy: cost
  fallback_enabled: true
  max_retries: 3

tracking:
  enabled: true
  storage_path: .ai-router-costs.json

signals:
  enabled: true
  target: OS
```

---

## Signals

```
🧠 AI → OS : inference_start, provider=anthropic, model=claude-3.5-sonnet
✅ AI → OS : inference_complete, provider=anthropic, latency_ms=450, cost=$0.0032
❌ AI → OS : inference_failed, provider=hailo, error=device_busy
🔄 AI → OS : fallback_triggered, from=hailo, to=ollama
🟢 AI → OS : provider_healthy, provider=openai
🔴 AI → OS : provider_down, provider=hailo
💰 AI → OS : cost_alert, total=$10.50, period=day, threshold=$10.00
```

---

## Integration with BlackRoad

```python
# In the Operator
from ai_router import Router

router = Router(strategy="local_first")

async def handle_ai_query(query: str):
    # Route to the best AI provider
    result = await router.complete(query)

    # Emit signal
    print(result.signal())
    # 🧠 AI → OS : inference_complete, provider=hailo@lucidia, latency=85ms, cost=$0.00

    return result.content
```

---

## Adding a New Provider

```python
from ai_router.providers.base import Provider, ProviderConfig, CompletionResponse

class MyProvider(Provider):
    async def complete(self, request):
        # Your implementation
        return CompletionResponse(
            content="Hello!",
            model="my-model",
            provider=self.name,
            cost=0.001,
            latency_ms=100,
        )

    async def health_check(self):
        # Check if available
        return ProviderStatus.HEALTHY

# Register
router = Router(providers=[MyProvider(config)])
```

---

*Route to intelligence. Own the routing.*
