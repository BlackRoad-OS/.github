# Operator Prototype

> **The brain that routes everything.**

```
Status: PROTOTYPE (living in the Bridge)
Future home: BlackRoad-OS/operator
```

---

## What It Does

```
[Any Input] → [Parser] → [Classifier] → [Router] → [Destination]
                                            ↓
                                       [Signals]
```

1. **Parse** - Understand any input (text, HTTP, webhook, signal)
2. **Classify** - What type of request is this? (AI, CRM, storage, etc.)
3. **Route** - Send to the right org/service
4. **Signal** - Emit signals for observability

---

## Quick Start

```bash
cd prototypes/operator

# Install deps
pip install -r requirements.txt

# Run a test query
python -m operator.cli "What is the weather?"

# Start the server
python -m operator.server
```

---

## Usage

### As a Library

```python
from operator import Operator

op = Operator()

# Route a query
result = op.route("What is the weather?")
print(result)
# → RouteResult(destination="AI", org="BlackRoad-AI", confidence=0.95)

# Route with context
result = op.route("Update customer record", context={"user": "alexa"})
# → RouteResult(destination="FND", org="BlackRoad-Foundation", confidence=0.88)
```

### As a CLI

```bash
# Simple query
br route "What is the weather?"
# → Routed to: BlackRoad-AI (confidence: 0.95)

# With verbose output
br route -v "Store this file"
# → Classification: storage
# → Destination: BlackRoad-Archive
# → Confidence: 0.82
# → Signal: 🎯 OS → ARC : route request
```

### As a Server

```bash
# Start server
python -m operator.server --port 8080

# Send request
curl -X POST http://localhost:8080/route \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the weather?"}'
```

---

## Configuration

Routes are configured in `config/routes.yaml`:

```yaml
routes:
  - pattern: "weather|forecast|temperature"
    destination: AI
    org: BlackRoad-AI

  - pattern: "customer|contact|lead|salesforce"
    destination: FND
    org: BlackRoad-Foundation

  - pattern: "store|save|backup|archive"
    destination: ARC
    org: BlackRoad-Archive
```

---

## Architecture

```
operator/
├── __init__.py
├── core/
│   ├── parser.py      ← Parse any input format
│   ├── classifier.py  ← Classify request type
│   └── router.py      ← Route to destination
├── signals/
│   └── emitter.py     ← Emit signals to mesh
├── config/
│   ├── routes.yaml    ← Routing rules
│   └── orgs.yaml      ← Org definitions
├── cli.py             ← Command line interface
└── server.py          ← HTTP server
```

---

## Signals Emitted

| Signal | When |
|--------|------|
| `🎯 OS → [ORG]` | Request routed |
| `✔️ OS → OS` | Route complete |
| `❌ OS → OS` | Route failed |
| `⚠️ OS → OS` | Low confidence route |

---

*The Operator is the nervous system. It decides where everything goes.*
