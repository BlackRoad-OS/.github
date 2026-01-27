# BlackRoad-Security Blueprint

> **The Guardian Layer**
> Code: `SEC`

---

## Mission

Trust nothing. Verify everything. Secure by default.

```
[Request] → [Validate] → [Authorize] → [Audit] → [Process]
```

---

## Core Principle

**Security is not a feature. It's the foundation.**

- Zero-trust architecture
- Principle of least privilege
- Defense in depth
- Everything logged, everything auditable

---

## What Lives Here

| Repo | Purpose | Priority |
|------|---------|----------|
| `auth` | Authentication, JWT, OAuth | P0 |
| `secrets` | Secret management, rotation | P0 |
| `audit` | Audit logging, compliance | P0 |
| `firewall` | Rate limiting, WAF rules | P1 |
| `scanner` | Vulnerability scanning | P1 |
| `policies` | Security policies, runbooks | P1 |

---

## Security Architecture

```
                    ┌─────────────────┐
                    │   CLOUDFLARE    │
                    │   WAF + DDoS    │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │     FIREWALL    │
                    │  Rate Limiting  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │      AUTH       │
                    │  JWT + OAuth    │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │    AUTHORIZE    │
                    │  RBAC + ABAC    │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │     AUDIT       │
                    │  Log Everything │
                    └────────┬────────┘
                             │
                             ▼
                        [Process]
```

---

## Authentication Flow

```
[User] → [Login] → [Validate Creds] → [Issue JWT] → [Return Token]
                         │
                         ▼
                  [Log Auth Event]
                         │
                         ▼
              [Check for Anomalies]
```

**JWT Claims:**
```json
{
  "sub": "user_id",
  "org": "org_id",
  "roles": ["admin", "user"],
  "permissions": ["read:*", "write:own"],
  "exp": 1234567890,
  "iat": 1234567800
}
```

---

## Secrets Management

| Secret Type | Storage | Rotation |
|-------------|---------|----------|
| API Keys | Cloudflare KV (encrypted) | 90 days |
| JWT Signing Keys | Hardware (alice) | 30 days |
| Database Creds | Vault/SOPS | 7 days |
| Node Certs | Tailscale (auto) | Auto |

---

## Audit Requirements

Every action logs:
```json
{
  "timestamp": "2026-01-27T12:00:00Z",
  "actor": "user_123",
  "action": "create",
  "resource": "project/456",
  "ip": "1.2.3.4",
  "user_agent": "...",
  "result": "success",
  "metadata": {}
}
```

**Retention:** 7 years (compliance)

---

## Integration Points

### Upstream (receives from)
- All orgs - security queries
- `CLD` - Firewall rule updates
- `OS` - Policy updates

### Downstream (sends to)
- `ARC` - Audit log archive
- All orgs - Security alerts
- `OS` - Incident reports

### Signals
```
🔐 SEC → ALL : Security advisory
🚨 SEC → OS : Incident detected
✔️ SEC → * : Auth approved
❌ SEC → * : Auth denied
🔄 SEC → OS : Secret rotation complete
```

---

## Incident Response

```
DETECT → CONTAIN → ERADICATE → RECOVER → LESSONS
   │         │          │          │         │
   ▼         ▼          ▼          ▼         ▼
 Alert    Isolate    Remove     Restore   Document
          affected   threat     service   & improve
```

---

*Security is invisible when it works. That's the goal.*
