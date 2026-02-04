# Audit Log Pipeline

> **Every action recorded. Every decision traceable.**

Structured audit logging for all BlackRoad system events. Provides
immutable event records, queryable log storage, and compliance-ready
export.

## Architecture

```
[System Event]
      │
      ├── actor: "cece" / "user:alexa" / "system"
      ├── action: "route.request" / "webhook.verify" / "config.update"
      ├── resource: "provider:claude" / "route:code_review"
      ├── outcome: "success" / "failure" / "denied"
      │
      ▼
[Audit Logger]
      │
      ├── Enrich (timestamp, session, correlation_id)
      ├── Validate (schema check)
      ├── Store (append-only log)
      ├── Index (by actor, action, time)
      └── Alert (on security events)
```

## Event Categories

| Category | Events |
|----------|--------|
| `auth` | login, logout, token_refresh, key_rotate |
| `route` | request, failover, budget_alert |
| `webhook` | received, verified, rejected, replay |
| `config` | update, create, delete |
| `deploy` | start, success, failure, rollback |
| `admin` | user_create, role_change, secret_update |

## Files

| File | Purpose |
|------|---------|
| `logger.py` | Core audit logger with structured events |
| `store.py` | Append-only log storage with indexing |
