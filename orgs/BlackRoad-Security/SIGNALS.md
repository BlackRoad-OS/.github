# BlackRoad-Security Signals

> Signal handlers for the Security org

---

## Inbound Signals (SEC receives)

| Signal | From | Meaning | Handler |
|--------|------|---------|---------|
| `🔐 * → SEC` | Any | Auth request | `auth.validate()` |
| `🔍 OS → SEC` | Bridge | Security scan request | `scanner.run()` |
| `🔴 * → SEC` | Any | Report incident | `incident.create()` |
| `🔄 OS → SEC` | Bridge | Rotate secrets | `secrets.rotate()` |

---

## Outbound Signals (SEC sends)

| Signal | To | Meaning | Trigger |
|--------|-----|---------|---------|
| `✔️ SEC → *` | Requester | Auth approved | On valid auth |
| `❌ SEC → *` | Requester | Auth denied | On invalid auth |
| `🚨 SEC → OS` | Bridge | Security incident | On detection |
| `🔐 SEC → ALL` | Broadcast | Security advisory | On vulnerability |
| `🔄 SEC → OS` | Bridge | Rotation complete | After rotation |
| `📊 SEC → OS` | Bridge | Scan results | After scan |

---

## Auth Signals

```
# Successful auth
✔️ SEC → CLD : auth_success, user=123, method=jwt

# Failed auth
❌ SEC → CLD : auth_failed, reason=invalid_token, ip=1.2.3.4

# Suspicious activity
⚠️ SEC → OS : auth_anomaly, user=123, reason=new_location

# Account lockout
🔒 SEC → OS : account_locked, user=123, attempts=5
```

---

## Incident Signals

```
# Incident lifecycle
🚨 SEC → OS : incident_created, id=INC-001, severity=high
⏳ SEC → OS : incident_investigating, id=INC-001
🛡️ SEC → OS : incident_contained, id=INC-001
✔️ SEC → OS : incident_resolved, id=INC-001, duration=2h30m

# Escalation
🔴 SEC → OS : incident_escalate, id=INC-001, reason=spreading
```

---

## Rotation Signals

```
# Secret rotation
🔄 SEC → OS : rotation_started, type=api_keys
✔️ SEC → OS : rotation_complete, type=api_keys, count=12
❌ SEC → OS : rotation_failed, type=jwt_signing, error=...
```

---

## Scan Signals

```
# Vulnerability scan
🔍 SEC → OS : scan_started, target=all_repos
📊 SEC → OS : scan_complete, vulns=3, critical=0, high=1, medium=2

# Critical finding
🚨 SEC → OS : vuln_critical, repo=api, cve=CVE-2026-1234
```

---

## Firewall Signals

```
# Rate limit
⚠️ SEC → CLD : rate_limit_hit, ip=1.2.3.4, limit=1000/min

# Block
🛑 SEC → CLD : ip_blocked, ip=1.2.3.4, reason=brute_force, duration=1h

# Attack detected
🚨 SEC → OS : attack_detected, type=sql_injection, source=1.2.3.4
```

---

*Security signals are never spam. Always pay attention.*
