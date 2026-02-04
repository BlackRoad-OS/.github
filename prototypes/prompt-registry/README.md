# Prompt Template Registry

> **Reusable, versioned prompt templates for the routing engine.**

Standardized prompt templates that can be shared across routes, versioned,
and optimized per-provider. Templates support variables, provider-specific
overrides, and usage tracking.

## Architecture

```
[Route Request]
      │
      ├── template_id: "code_review"
      ├── variables: { language: "python", code: "..." }
      │
      ▼
[Template Registry]
      │
      ├── Load template
      ├── Resolve variables
      ├── Apply provider overrides
      └── Return compiled prompt
```

## Files

| File | Purpose |
|------|---------|
| `registry.py` | Template storage, lookup, CRUD |
| `template.py` | Template model with variable resolution |
| `templates.yaml` | Default template library |

## Usage

```python
from registry import PromptRegistry

reg = PromptRegistry()
reg.load_defaults()

prompt = reg.render("code_review", {
    "language": "python",
    "code": "def foo(): pass",
    "focus": "security",
})
```
