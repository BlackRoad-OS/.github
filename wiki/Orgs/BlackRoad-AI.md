# BlackRoad-AI

> **Route to intelligence, don't build it.**

**Code**: `AI`  
**Tier**: Core Infrastructure  
**Status**: Active

---

## Mission

BlackRoad-AI aggregates and routes to AI/ML services. We don't host models - we connect users to the best intelligence for their needs.

---

## Philosophy

**Traditional Approach:**
```
Build Model → Train Model → Host Model → Maintain Model
```

**BlackRoad Approach:**
```
Route to OpenAI OR Anthropic OR Cohere OR Local Model
```

**Why?** Intelligence is commoditizing. The value is in knowing which service to use and when.

---

## Architecture

```
┌─────────────────────────────────────────────┐
│            BLACKROAD-AI (AI)                │
├─────────────────────────────────────────────┤
│                                             │
│   Router                                    │
│   ├── OpenAI          ← GPT-4, ChatGPT    │
│   ├── Anthropic       ← Claude             │
│   ├── Cohere          ← Command            │
│   ├── Google          ← Gemini, PaLM       │
│   ├── HuggingFace     ← Open models        │
│   └── Local (Hailo)   ← On-device          │
│                                             │
│   Aggregator                                │
│   ├── Combine responses                    │
│   ├── Confidence scoring                   │
│   └── Best answer selection                │
│                                             │
│   Agent System                              │
│   ├── Code agents                          │
│   ├── Research agents                      │
│   └── Assistant agents                     │
│                                             │
└─────────────────────────────────────────────┘
```

---

## Repositories

| Repository | Purpose | Status |
|------------|---------|--------|
| ai-router | Route to AI services | Planned 🔜 |
| ai-agents | Agent coordination | Planned 🔜 |
| ai-prompts | Prompt templates | Planned 🔜 |
| hailo-integration | Local inference on Hailo-8 | Planned 🔜 |

---

## Routing Logic

```python
def route_ai_request(query: str) -> Response:
    """Route AI request to best service."""
    
    # Classify request type
    request_type = classify(query)
    
    # Select service
    if request_type == 'code':
        service = 'openai'  # GPT-4 for code
    elif request_type == 'creative':
        service = 'anthropic'  # Claude for writing
    elif request_type == 'fast':
        service = 'hailo'  # Local for speed
    else:
        service = 'openai'  # Default
    
    # Make request
    response = call_service(service, query)
    
    # Emit signal
    emit(f"✔️ AI → OS : route_complete, service={service}")
    
    return response
```

---

## Signals

### Emits

```
✔️ AI → OS : route_complete, service=openai, latency=234ms
❌ AI → OS : route_failed, service=anthropic, reason=timeout
📡 AI → ALL : service_down, provider=cohere
```

### Receives

```
🎯 OS → AI : route_request, query="...", context={}
📡 ALL → AI : rate_limit_warning, provider=openai
```

---

## Integration Points

- **OpenAI**: GPT-4, ChatGPT, DALL-E
- **Anthropic**: Claude (various models)
- **Cohere**: Command, Embed
- **Google**: Gemini, PaLM
- **HuggingFace**: Open-source models
- **Hailo-8**: Local inference on hardware

---

## Learn More

- **[BlackRoad-Hardware](BlackRoad-Hardware)** - Hailo-8 integration
- **[Architecture Overview](../Architecture/Overview)** - The big picture

---

*Intelligence is everywhere. We route to it.*
