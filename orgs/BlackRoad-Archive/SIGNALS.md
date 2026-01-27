# BlackRoad-Archive Signals

> Signal handlers for the Archive org

---

## Inbound Signals (ARC receives)

| Signal | From | Meaning | Handler |
|--------|------|---------|---------|
| `📦 * → ARC` | Any | Store this | `storage.store()` |
| `🔍 * → ARC` | Any | Search for | `search.query()` |
| `🗑️ * → ARC` | Any | Delete (soft) | `retention.soft_delete()` |
| `⚖️ SEC → ARC` | Security | Legal hold | `retention.hold()` |

---

## Outbound Signals (ARC sends)

| Signal | To | Meaning | Trigger |
|--------|-----|---------|---------|
| `📦 ARC → OS` | Bridge | Data archived | On store |
| `🔍 ARC → *` | Requester | Search results | On query |
| `♻️ ARC → OS` | Bridge | Tier migration | On migrate |
| `⚠️ ARC → OS` | Bridge | Storage alert | On threshold |
| `✅ ARC → OS` | Bridge | Backup complete | On backup |

---

## Storage Signals

```
# Store data
📦 ARC → OS : stored, type=log, size=1.2MB, tier=warm, id=abc123

# Retrieve
🔍 ARC → SEC : retrieved, id=abc123, requestor=audit_system

# Tier migration
♻️ ARC → OS : migrated, count=1000, from=warm, to=cold, saved=$12
```

---

## Backup Signals

```
# Backup started
⏳ ARC → OS : backup_started, type=database, target=r2

# Progress
📊 ARC → OS : backup_progress, type=database, progress=45%

# Complete
✅ ARC → OS : backup_complete, type=database, size=2.3GB, duration=5m

# Verification
✔️ ARC → OS : backup_verified, id=backup_123, integrity=pass

# Failed
❌ ARC → OS : backup_failed, type=database, error="connection timeout"
```

---

## Retention Signals

```
# Policy applied
🗓️ ARC → OS : retention_applied, policy=logs, archived=5000, deleted=0

# Legal hold
⚖️ ARC → OS : legal_hold_applied, scope=user_123, reason="litigation"

# GDPR deletion
🗑️ ARC → OS : gdpr_deleted, user=456, records=23
```

---

## Alert Signals

```
# Storage threshold
⚠️ ARC → OS : storage_alert, tier=hot, usage=85%, threshold=80%

# Backup age
⚠️ ARC → OS : backup_stale, type=database, age=26h, max=24h

# Integrity issue
🚨 ARC → OS : integrity_alert, backup=xyz, issue="checksum_mismatch"
```

---

*Archive signals preserve history.*
