# Claude Code API Best Practices

> **Using Anthropic's Claude Code API effectively in the BlackRoad ecosystem**

---

## What is Claude Code API?

Claude Code API is Anthropic's API service that powers:
1. **Direct API calls** - Using the Anthropic Python/TypeScript SDK
2. **Claude Code IDE extension** - VS Code integration for development
3. **MCP (Model Context Protocol)** - Extensible tool integration

---

## API Configuration

### Environment Setup

```bash
# Set your Anthropic API key
export ANTHROPIC_API_KEY="sk-ant-api03-..."

# Verify it's set
echo $ANTHROPIC_API_KEY

# Optional: Set API version
export ANTHROPIC_API_VERSION="2023-06-01"
```

### Python SDK

```bash
# Install the official SDK
pip install anthropic

# For streaming support
pip install anthropic[streaming]
```

```python
# Basic usage
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude!"}
    ]
)

print(message.content[0].text)
```

### Async Usage

```python
from anthropic import AsyncAnthropic

client = AsyncAnthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

async def chat():
    message = await client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": "Hello!"}
        ]
    )
    return message.content[0].text
```

---

## Model Selection

### Recommended Models

| Use Case | Model | Why |
|----------|-------|-----|
| **Code Generation** | `claude-sonnet-4-20250514` | Best balance of quality and cost |
| **Code Review** | `claude-3-5-sonnet-20241022` | Fast and accurate |
| **Quick Tasks** | `claude-3-5-haiku-20241022` | Fastest, cheapest |
| **Complex Reasoning** | `claude-opus-4-20250514` | Most capable, expensive |

### Model Comparison

```yaml
claude-sonnet-4-20250514:
  context: 200K tokens
  cost_input: $3 per 1M tokens
  cost_output: $15 per 1M tokens
  latency: ~500ms
  best_for: General code tasks

claude-opus-4-20250514:
  context: 200K tokens
  cost_input: $15 per 1M tokens
  cost_output: $75 per 1M tokens
  latency: ~800ms
  best_for: Complex architecture

claude-3-5-haiku-20241022:
  context: 200K tokens
  cost_input: $0.80 per 1M tokens
  cost_output: $4 per 1M tokens
  latency: ~300ms
  best_for: Fast iterations
```

---

## BlackRoad Integration

### Using the AI Router

```python
from ai_router import Router

# Auto-route based on strategy
router = Router(strategy="cost")

# Will automatically use Claude for code tasks
result = await router.complete(
    "Write a Python function to parse YAML",
    capabilities=["code"]
)

print(result.content)
print(f"Provider: {result.provider}")  # anthropic
print(f"Cost: ${result.cost:.4f}")
```

### Using the Operator

```python
from operator import Operator

op = Operator()

# Classify and route
result = op.route("Generate API client code")

# Result will route to BlackRoad-AI
assert result.org_code == "AI"
assert "anthropic" in result.suggested_providers
```

### Using the MCP Server

```bash
# Start the MCP server
python -m blackroad_mcp

# In Claude Code, it will automatically connect
# and have access to BlackRoad tools
```

---

## Cost Management

### Track Usage

```python
from ai_router.tracking import CostTracker

tracker = CostTracker(storage_path=".anthropic-costs.json")
router = Router()

# Make a request
result = await router.complete("Hello", provider="anthropic")

# Track it
tracker.record_response(result.response)

# Get report
report = tracker.report(period="day")
print(f"Today's Anthropic cost: ${report.by_provider['anthropic']:.2f}")
```

### Set Budgets

```python
# In config.yaml
tracking:
  enabled: true
  alerts:
    - threshold: 5.00
      period: day
      provider: anthropic
    - threshold: 100.00
      period: month
      provider: anthropic
```

### Cost Optimization Tips

1. **Use Haiku for simple tasks** - 5x cheaper than Sonnet
2. **Cache system prompts** - Reduce repeated context
3. **Limit max_tokens** - Don't generate more than needed
4. **Use streaming** - Get partial results faster
5. **Batch requests** - Reduce overhead

```python
# Good: Specific max_tokens
response = await client.messages.create(
    model="claude-3-5-haiku-20241022",
    max_tokens=500,  # Only need a short response
    messages=[...]
)

# Bad: Unlimited tokens
response = await client.messages.create(
    model="claude-opus-4-20250514",
    max_tokens=4096,  # Might generate too much
    messages=[...]
)
```

---

## Best Practices

### 1. Error Handling

```python
from anthropic import APIError, RateLimitError

try:
    message = await client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}]
    )
except RateLimitError as e:
    # Implement exponential backoff
    await asyncio.sleep(e.retry_after or 60)
    # Retry...
except APIError as e:
    # Log the error
    logger.error(f"Anthropic API error: {e}")
    # Fall back to another provider
    result = await router.complete(prompt, chain=["ollama", "openai"])
```

### 2. Streaming for Long Responses

```python
async def stream_response(prompt: str):
    """Stream Claude's response for better UX."""
    async with client.messages.stream(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        async for text in stream.text_stream:
            print(text, end="", flush=True)
        
        # Get final message
        message = await stream.get_final_message()
        return message
```

### 3. System Prompts

```python
# Good: Clear system prompt
message = await client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system="You are a Python expert. Write clean, idiomatic code with type hints.",
    messages=[
        {"role": "user", "content": "Write a function to parse JSON"}
    ]
)

# Better: Context-rich system prompt
system_prompt = """
You are an expert Python developer working in the BlackRoad ecosystem.

Guidelines:
- Use Python 3.11+ features
- Include type hints
- Follow PEP 8 style
- Add docstrings
- Handle errors gracefully
"""

message = await client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system=system_prompt,
    messages=[{"role": "user", "content": prompt}]
)
```

### 4. Vision Capabilities

```python
# Analyze images with Claude
import base64

def encode_image(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

message = await client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": encode_image("diagram.png")
                    }
                },
                {
                    "type": "text",
                    "text": "Explain this architecture diagram"
                }
            ]
        }
    ]
)
```

### 5. Function Calling (Tool Use)

```python
# Define tools
tools = [
    {
        "name": "get_weather",
        "description": "Get weather for a location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {"type": "string"}
            },
            "required": ["location"]
        }
    }
]

message = await client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=tools,
    messages=[
        {"role": "user", "content": "What's the weather in SF?"}
    ]
)

# Handle tool calls
if message.stop_reason == "tool_use":
    tool_use = message.content[1]  # Get tool call
    # Execute the tool
    weather = get_weather(tool_use.input["location"])
    # Continue conversation with result
```

---

## Rate Limits

### Understanding Limits

```yaml
tier_1:  # Default
  requests: 50/min
  tokens: 40K/min
  
tier_2:  # Increased usage
  requests: 1000/min
  tokens: 80K/min
  
tier_3:  # High volume
  requests: 2000/min
  tokens: 160K/min
```

### Handling Rate Limits

```python
import asyncio
from anthropic import RateLimitError

async def call_with_backoff(prompt: str, max_retries: int = 3):
    """Call Claude with exponential backoff."""
    for attempt in range(max_retries):
        try:
            return await client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
        except RateLimitError as e:
            if attempt == max_retries - 1:
                raise
            
            wait_time = 2 ** attempt  # Exponential: 1s, 2s, 4s
            await asyncio.sleep(wait_time)
```

---

## Security

### API Key Management

```bash
# DO: Use environment variables
export ANTHROPIC_API_KEY="sk-ant-..."

# DO: Use secret management
# AWS Secrets Manager, HashiCorp Vault, etc.

# DON'T: Hardcode in code
api_key = "sk-ant-..."  # Never do this!

# DON'T: Commit to git
echo "ANTHROPIC_API_KEY=sk-ant-..." >> .env
git add .env  # Never do this!
```

### Best Practices

1. **Rotate keys regularly** - Every 90 days minimum
2. **Use separate keys per environment** - dev/staging/prod
3. **Limit key scope** - Restrict to necessary permissions
4. **Monitor usage** - Watch for anomalies
5. **Revoke compromised keys** - Immediately if exposed

---

## Monitoring & Logging

### Log Requests

```python
import logging

logger = logging.getLogger("anthropic")

async def logged_completion(prompt: str):
    """Make a request with logging."""
    start_time = time.time()
    
    try:
        message = await client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        
        latency = time.time() - start_time
        
        logger.info(
            f"Claude request successful",
            extra={
                "model": "claude-sonnet-4-20250514",
                "input_tokens": message.usage.input_tokens,
                "output_tokens": message.usage.output_tokens,
                "latency_ms": int(latency * 1000),
            }
        )
        
        return message
        
    except Exception as e:
        logger.error(f"Claude request failed: {e}")
        raise
```

### Emit Signals

```python
from signals import emit_signal

# Start signal
emit_signal("AI", "OS", "inference_start", {
    "provider": "anthropic",
    "model": "claude-sonnet-4-20250514"
})

# ... make request ...

# Complete signal
emit_signal("AI", "OS", "inference_complete", {
    "provider": "anthropic",
    "latency_ms": 450,
    "cost": 0.0032,
    "tokens": 1500
})
```

---

## Testing

### Mock API Calls

```python
from unittest.mock import AsyncMock, patch

async def test_claude_integration():
    """Test Claude API integration."""
    mock_message = AsyncMock()
    mock_message.content = [AsyncMock(text="Hello!")]
    mock_message.usage = AsyncMock(
        input_tokens=10,
        output_tokens=5
    )
    
    with patch("anthropic.AsyncAnthropic") as mock_client:
        mock_client.return_value.messages.create.return_value = mock_message
        
        result = await call_claude("Hello")
        assert result == "Hello!"
```

### Integration Tests

```bash
# Run integration tests (requires API key)
ANTHROPIC_API_KEY="sk-ant-test-..." pytest tests/test_anthropic.py

# Skip integration tests
pytest -m "not integration"
```

---

## Resources

### Official Documentation

- **API Reference:** https://docs.anthropic.com/
- **Python SDK:** https://github.com/anthropics/anthropic-sdk-python
- **MCP Protocol:** https://modelcontextprotocol.io/
- **Pricing:** https://www.anthropic.com/pricing

### BlackRoad Resources

- **AI Router Template:** [templates/ai-router/](../templates/ai-router/)
- **MCP Server:** [prototypes/mcp-server/](../prototypes/mcp-server/)
- **Operator:** [prototypes/operator/](../prototypes/operator/)
- **Integration Docs:** [INTEGRATIONS.md](../INTEGRATIONS.md)

### Community

- **Anthropic Discord:** https://discord.gg/anthropic
- **API Status:** https://status.anthropic.com/

---

## Troubleshooting

### Common Issues

**Issue:** "Invalid API key"
```bash
# Solution: Check environment variable
echo $ANTHROPIC_API_KEY
export ANTHROPIC_API_KEY="sk-ant-api03-..."
```

**Issue:** Rate limit errors
```python
# Solution: Implement exponential backoff
async def retry_with_backoff():
    for i in range(3):
        try:
            return await call_claude(prompt)
        except RateLimitError:
            await asyncio.sleep(2 ** i)
```

**Issue:** High costs
```python
# Solution: Switch to cheaper model
# Instead of: claude-opus-4-20250514 ($15/$75)
# Use: claude-3-5-haiku-20241022 ($0.80/$4)
```

---

*Using Claude Code API effectively in the BlackRoad ecosystem!*

📡 **Signal:** `docs → AI : best_practices_documented`
