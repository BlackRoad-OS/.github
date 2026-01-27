# BlackRoad-Security Repositories

> Repo specs for the Security org

---

## Repository List

### `auth` (P0 - Build First)

**Purpose:** Authentication and identity

**Structure:**
```
auth/
├── src/
│   ├── providers/
│   │   ├── password.py    ← Password auth
│   │   ├── oauth.py       ← OAuth providers
│   │   ├── magic-link.py  ← Email magic links
│   │   └── api-key.py     ← API key auth
│   ├── jwt/
│   │   ├── issuer.py      ← Token creation
│   │   ├── validator.py   ← Token validation
│   │   └── refresh.py     ← Token refresh
│   ├── mfa/
│   │   ├── totp.py        ← TOTP (Google Auth)
│   │   └── webauthn.py    ← Hardware keys
│   └── session/
│       └── manager.py
├── tests/
├── configs/
└── README.md
```

---

### `secrets` (P0 - Build First)

**Purpose:** Secret management and rotation

**Structure:**
```
secrets/
├── src/
│   ├── store/
│   │   ├── kv.py          ← Cloudflare KV
│   │   ├── sops.py        ← SOPS encryption
│   │   └── vault.py       ← HashiCorp Vault
│   ├── rotation/
│   │   ├── scheduler.py   ← Rotation schedule
│   │   ├── rotator.py     ← Rotation logic
│   │   └── notify.py      ← Rotation alerts
│   └── access/
│       └── policy.py      ← Access policies
├── configs/
│   └── rotation.yaml
└── README.md
```

---

### `audit` (P0 - Build First)

**Purpose:** Audit logging and compliance

**Structure:**
```
audit/
├── src/
│   ├── logger/
│   │   ├── writer.py      ← Write audit logs
│   │   └── format.py      ← Log formatting
│   ├── query/
│   │   └── search.py      ← Query audit logs
│   ├── compliance/
│   │   ├── soc2.py        ← SOC2 reports
│   │   └── gdpr.py        ← GDPR compliance
│   └── retention/
│       └── policy.py
├── schemas/
│   └── audit-event.json
└── README.md
```

---

### `firewall` (P1)

**Purpose:** Rate limiting and WAF

**Structure:**
```
firewall/
├── rules/
│   ├── rate-limits.yaml   ← Rate limit rules
│   ├── waf.yaml           ← WAF rules
│   └── blocklist.yaml     ← Blocked IPs/patterns
├── src/
│   ├── limiter.py         ← Rate limiter
│   └── waf.py             ← WAF logic
└── README.md
```

---

### `scanner` (P1)

**Purpose:** Vulnerability scanning

**Structure:**
```
scanner/
├── src/
│   ├── dependency/
│   │   └── scan.py        ← Dependency check
│   ├── code/
│   │   └── sast.py        ← Static analysis
│   ├── infra/
│   │   └── scan.py        ← Infrastructure scan
│   └── report/
│       └── generate.py
├── configs/
└── README.md
```

---

### `policies` (P1)

**Purpose:** Security policies and runbooks

**Structure:**
```
policies/
├── policies/
│   ├── access-control.md
│   ├── data-handling.md
│   ├── incident-response.md
│   └── password-policy.md
├── runbooks/
│   ├── incident/
│   │   ├── data-breach.md
│   │   └── ddos.md
│   └── operations/
│       ├── secret-rotation.md
│       └── access-review.md
└── README.md
```

---

## Security Checklist (for all repos)

- [ ] No secrets in code
- [ ] Dependencies scanned
- [ ] Input validation
- [ ] Output encoding
- [ ] Auth on all endpoints
- [ ] Audit logging enabled
- [ ] HTTPS only
- [ ] Rate limiting

---

*Security repos are the most boring and the most important.*
