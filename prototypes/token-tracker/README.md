# Token Usage Tracker

> **Every token counted. Every dollar tracked. Per route, per provider, per minute.**

Tracks token consumption and cost across all AI providers and routes.
Provides real-time dashboards, budget alerts, and usage analytics.

## Architecture

```
[AI Provider Response]
        │
        ├── input_tokens: 150
        ├── output_tokens: 300
        ├── provider: "claude"
        ├── route: "code_review"
        │
        ▼
[Token Tracker]
        │
        ├── Record usage
        ├── Calculate cost
        ├── Update aggregates
        ├── Check budgets
        └── Emit alerts
```

## Files

| File | Purpose |
|------|---------|
| `tracker.py` | Core tracking engine with per-route/provider metrics |
| `budget.py` | Budget management and alerting |

## Usage

```python
from tracker import TokenTracker

tracker = TokenTracker()
tracker.record("code_review", "claude", input_tokens=150, output_tokens=300)
print(tracker.dashboard())
```
