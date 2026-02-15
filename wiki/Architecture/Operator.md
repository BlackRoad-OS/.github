# The Operator

> **The routing brain. Determines which organization handles each request.**

---

## What is The Operator?

The Operator is BlackRoad's routing engine. It analyzes incoming requests and determines which organization is best suited to handle them.

```
Request → Operator → Organization
```

**Location**: `prototypes/operator/`

---

## Architecture

```
┌─────────────────────────────────────────┐
│              THE OPERATOR               │
├─────────────────────────────────────────┤
│                                         │
│   Request                               │
│      ↓                                  │
│   ┌─────────┐                          │
│   │ Parser  │  Extract intent          │
│   └────┬────┘                          │
│        ↓                                │
│   ┌──────────┐                         │
│   │Classifier│  Score all orgs         │
│   └────┬─────┘                         │
│        ↓                                │
│   ┌─────────┐                          │
│   │ Router  │  Select best org         │
│   └────┬────┘                          │
│        ↓                                │
│   ┌─────────┐                          │
│   │ Emitter │  Send routing signal     │
│   └─────────┘                          │
│                                         │
└─────────────────────────────────────────┘
```

---

## Components

### 1. Parser

**Purpose**: Extract intent from natural language request.

**Input**: Raw request string
**Output**: Intent object with keywords, action, domain

```python
# operator/parser.py

def parse(request: str) -> Intent:
    """Extract intent from request."""
    keywords = extract_keywords(request)
    action = detect_action(request)
    domain = classify_domain(keywords)
    
    return Intent(
        raw=request,
        keywords=keywords,
        action=action,
        domain=domain
    )
```

**Examples:**

```python
parse("What's the weather in SF?")
# Intent(keywords=['weather', 'SF'], action='query', domain='ai')

parse("Deploy my app to production")
# Intent(keywords=['deploy', 'app', 'production'], action='deploy', domain='cloud')

parse("Create a new user in Salesforce")
# Intent(keywords=['create', 'user', 'salesforce'], action='create', domain='crm')
```

### 2. Classifier

**Purpose**: Score all organizations based on intent.

**Input**: Intent object
**Output**: Dict of org → confidence score

```python
# operator/classifier.py

def classify(intent: Intent) -> Dict[str, float]:
    """Score all organizations for this intent."""
    scores = {}
    
    for org in load_all_orgs():
        score = calculate_score(intent, org)
        scores[org.code] = score
    
    return scores
```

**Scoring Algorithm:**

```python
def calculate_score(intent: Intent, org: Organization) -> float:
    score = 0.0
    
    # Keyword matching
    for keyword in intent.keywords:
        if keyword in org.keywords:
            score += 0.2
    
    # Domain matching
    if intent.domain == org.domain:
        score += 0.4
    
    # Action matching
    if intent.action in org.actions:
        score += 0.3
    
    # Reputation (past success rate)
    score += org.reputation * 0.1
    
    return min(score, 1.0)  # Cap at 100%
```

**Examples:**

```python
classify(Intent(keywords=['deploy'], action='deploy', domain='cloud'))
# {
#   'CLD': 0.95,  # BlackRoad-Cloud
#   'OS': 0.70,   # BlackRoad-OS
#   'HW': 0.30,   # BlackRoad-Hardware
#   ...
# }

classify(Intent(keywords=['weather'], action='query', domain='ai'))
# {
#   'AI': 0.90,   # BlackRoad-AI
#   'OS': 0.50,
#   ...
# }
```

### 3. Router

**Purpose**: Select the best organization from scores.

**Input**: Scores dict
**Output**: Selected organization with confidence

```python
# operator/router.py

def route(scores: Dict[str, float]) -> Route:
    """Select best organization."""
    best_org = max(scores, key=scores.get)
    confidence = scores[best_org]
    
    # Require minimum confidence
    if confidence < 0.5:
        raise RoutingError("No org scored above 50%")
    
    return Route(
        org=best_org,
        confidence=confidence,
        alternatives=get_top_n(scores, n=3)
    )
```

**Route Object:**

```python
@dataclass
class Route:
    org: str              # 'AI', 'CLD', 'OS', etc.
    confidence: float     # 0.0 to 1.0
    alternatives: List[Tuple[str, float]]  # Backup options
```

### 4. Emitter

**Purpose**: Send routing signal to selected organization.

**Input**: Route object
**Output**: Signal string

```python
# operator/emitter.py

def emit(route: Route) -> str:
    """Emit routing signal."""
    signal = (
        f"🎯 OS → {route.org} : route_request, "
        f"confidence={route.confidence:.0%}"
    )
    
    log_signal(signal)
    return signal
```

---

## Usage

### Command Line

```bash
# Navigate to operator
cd prototypes/operator

# Single query
python -m operator.cli "What is the weather?"
# Output:
#   Parsing: "What is the weather?"
#   Intent: query, domain=ai
#   Routing to: BlackRoad-AI (90%)
#   Signal: 🎯 OS → AI : route_request

# Interactive mode
python -m operator.cli --interactive
# > What is the weather?
# AI (90%)
# > Deploy my app
# CLD (95%)
# > exit
```

### Python API

```python
from operator import Operator

# Initialize
op = Operator()

# Route a request
route = op.route("What is the weather?")
print(f"Organization: {route.org}")
print(f"Confidence: {route.confidence:.0%}")

# Get alternatives
for alt_org, alt_score in route.alternatives:
    print(f"  - {alt_org}: {alt_score:.0%}")
```

### REST API (Future)

```bash
curl -X POST https://bridge.blackroad.dev/route \
  -H "Content-Type: application/json" \
  -d '{"request": "What is the weather?"}'

# Response:
# {
#   "org": "AI",
#   "confidence": 0.90,
#   "signal": "🎯 OS → AI : route_request",
#   "alternatives": [
#     {"org": "OS", "confidence": 0.50},
#     {"org": "LAB", "confidence": 0.30}
#   ]
# }
```

---

## Organization Definitions

Organizations are defined in `orgs/` blueprints.

### Example: BlackRoad-AI

```python
# orgs/BlackRoad-AI/definition.py
{
    "code": "AI",
    "name": "BlackRoad-AI",
    "domain": "ai",
    "keywords": [
        "ai", "ml", "model", "intelligence",
        "weather", "translate", "analyze", "generate"
    ],
    "actions": [
        "query", "analyze", "generate", "translate"
    ],
    "reputation": 0.85  # 85% historical success rate
}
```

### Example: BlackRoad-Cloud

```python
# orgs/BlackRoad-Cloud/definition.py
{
    "code": "CLD",
    "name": "BlackRoad-Cloud",
    "domain": "cloud",
    "keywords": [
        "deploy", "cloudflare", "worker", "edge",
        "cdn", "dns", "function", "serverless"
    ],
    "actions": [
        "deploy", "scale", "monitor", "configure"
    ],
    "reputation": 0.92
}
```

---

## Routing Examples

### Example 1: AI Query

```bash
Request: "What's the weather in San Francisco?"

Parser:
  - Keywords: ['weather', 'san', 'francisco']
  - Action: query
  - Domain: ai

Classifier:
  - AI: 0.90 (keywords match, domain match)
  - OS: 0.50 (general capability)
  - LAB: 0.30 (experimental)

Router:
  - Selected: AI (90%)
  - Alternatives: OS (50%), LAB (30%)

Emitter:
  🎯 OS → AI : route_request, confidence=90%
```

### Example 2: Cloud Deployment

```bash
Request: "Deploy my API to production"

Parser:
  - Keywords: ['deploy', 'api', 'production']
  - Action: deploy
  - Domain: cloud

Classifier:
  - CLD: 0.95 (strong match)
  - OS: 0.70 (general infrastructure)
  - HW: 0.40 (physical deployment)

Router:
  - Selected: CLD (95%)
  - Alternatives: OS (70%), HW (40%)

Emitter:
  🎯 OS → CLD : route_request, confidence=95%
```

### Example 3: CRM Operation

```bash
Request: "Create a new customer in Salesforce"

Parser:
  - Keywords: ['create', 'customer', 'salesforce']
  - Action: create
  - Domain: crm

Classifier:
  - FND: 0.88 (Foundation handles CRM)
  - OS: 0.45
  - AI: 0.30

Router:
  - Selected: FND (88%)
  - Alternatives: OS (45%), AI (30%)

Emitter:
  🎯 OS → FND : route_request, confidence=88%
```

---

## Confidence Thresholds

| Confidence | Action |
|------------|--------|
| 90-100% | Route immediately |
| 70-89% | Route with warning |
| 50-69% | Route but suggest alternatives |
| 30-49% | Ask user to clarify |
| 0-29% | Cannot route, need more info |

```python
def handle_route(route: Route):
    if route.confidence >= 0.9:
        return route.org
    
    elif route.confidence >= 0.7:
        warn(f"Moderate confidence: {route.confidence:.0%}")
        return route.org
    
    elif route.confidence >= 0.5:
        print(f"Low confidence. Alternatives:")
        for alt_org, alt_score in route.alternatives:
            print(f"  - {alt_org}: {alt_score:.0%}")
        return route.org
    
    else:
        raise RoutingError("Cannot route with confidence < 50%")
```

---

## Testing

```bash
# Run tests
cd prototypes/operator
python -m pytest tests/

# Test parser
python -m operator.parser --test

# Test classifier
python -m operator.classifier --test

# Test router
python -m operator.router --test

# Integration test
python -m operator.cli --test
```

---

## Signals

### Emitted by Operator

```
🎯 OS → [ORG] : route_request, confidence=X%, intent=Y
✔️ OS → OS : routing_complete, org=X, latency=Yms
❌ OS → OS : routing_failed, reason=X
```

### Received by Operator

```
📡 [ORG] → OS : ready, capacity=X
📡 [ORG] → OS : busy, queue_length=X
📡 [ORG] → OS : offline, reason=maintenance
```

---

## Future Enhancements

### Machine Learning

Train classifier on historical data:

```python
# Learn from past routings
def train(history: List[Tuple[Intent, str]]):
    """Train classifier on routing history."""
    X = [intent_to_features(i) for i, _ in history]
    y = [org for _, org in history]
    
    model = RandomForestClassifier()
    model.fit(X, y)
    
    return model
```

### A/B Testing

```python
# Compare routing strategies
def route_with_experiment(intent: Intent) -> Route:
    if random() < 0.1:  # 10% experimental
        return experimental_router.route(intent)
    else:
        return standard_router.route(intent)
```

### Load Balancing

```python
# Consider org capacity
def route_with_load_balancing(scores: Dict[str, float]) -> Route:
    # Get org capacities
    capacities = get_org_capacities()
    
    # Adjust scores by capacity
    adjusted = {
        org: score * capacities[org]
        for org, score in scores.items()
    }
    
    return select_best(adjusted)
```

---

## Learn More

- **[Architecture Overview](Overview)** - The big picture
- **[The Bridge](Bridge)** - Central coordination
- **[Organizations](../Orgs/BlackRoad-OS)** - Explore the 15 orgs

---

*Route wisely. The right org for the right job.*
