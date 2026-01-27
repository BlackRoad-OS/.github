# Salesforce Sync

> **Sync Salesforce records to local storage. Runs on lucidia.**

```
Org: BlackRoad-Foundation
Node: lucidia (Pi 5 + Hailo)
API Limit: 15,000 calls/day
Sync: Bidirectional
```

---

## What It Does

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│  Salesforce │  ←───→  │   lucidia   │  ←───→  │  BlackRoad  │
│    Cloud    │   API   │  (Pi Node)  │  Mesh   │   Services  │
└─────────────┘         └─────────────┘         └─────────────┘
                              │
                              ▼
                        ┌─────────────┐
                        │  Local DB   │
                        │  (SQLite)   │
                        └─────────────┘
```

1. **Pull** records from Salesforce (Contacts, Leads, Accounts, Opportunities)
2. **Store** locally in SQLite for fast queries
3. **Sync** changes bidirectionally
4. **Signal** when records change
5. **Serve** data to other BlackRoad services

---

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set up credentials
cp .env.example .env
# Edit .env with your SF credentials

# Initialize database
python -m salesforce_sync.cli init

# Run initial sync
python -m salesforce_sync.cli sync

# Start sync daemon
python -m salesforce_sync.cli daemon
```

---

## Record Types

| Object | Fields Synced | Sync Frequency |
|--------|---------------|----------------|
| Contact | Name, Email, Phone, Account, Owner | 15 min |
| Lead | Name, Email, Company, Status, Owner | 15 min |
| Account | Name, Industry, Revenue, Owner | 1 hour |
| Opportunity | Name, Amount, Stage, CloseDate | 15 min |

---

## API Usage

```python
from salesforce_sync import SFSync, Contact, Lead

# Initialize
sync = SFSync()

# Get all contacts
contacts = sync.contacts.all()
for c in contacts:
    print(f"{c.name} <{c.email}>")

# Search
leads = sync.leads.search(company="Acme")

# Create (syncs to SF automatically)
new_contact = Contact(
    first_name="Jane",
    last_name="Doe",
    email="jane@example.com"
)
sync.contacts.create(new_contact)

# Update
contact = sync.contacts.get("003...")
contact.phone = "555-1234"
sync.contacts.update(contact)
```

---

## Signals Emitted

| Signal | When |
|--------|------|
| `✔️ FND → OS : sync_complete` | After successful sync |
| `📊 FND → OS : records_updated, count=N` | Records changed |
| `❌ FND → OS : sync_failed` | Sync error |
| `⚠️ FND → OS : api_limit_warning` | Approaching limit |

---

## Configuration

```yaml
# config.yaml
salesforce:
  instance_url: https://yourinstance.salesforce.com
  api_version: "58.0"

sync:
  interval_minutes: 15
  batch_size: 200
  objects:
    - Contact
    - Lead
    - Account
    - Opportunity

storage:
  type: sqlite
  path: ./data/salesforce.db

signals:
  enabled: true
  target: OS
```

---

## Directory Structure

```
salesforce-sync/
├── salesforce_sync/
│   ├── __init__.py
│   ├── models/           ← Data models
│   │   ├── base.py
│   │   ├── contact.py
│   │   ├── lead.py
│   │   ├── account.py
│   │   └── opportunity.py
│   ├── sync/             ← Sync engine
│   │   ├── engine.py
│   │   ├── puller.py
│   │   └── pusher.py
│   ├── storage/          ← Local storage
│   │   ├── sqlite.py
│   │   └── cache.py
│   ├── api/              ← SF API client
│   │   └── client.py
│   └── cli.py            ← CLI interface
├── config.yaml
├── requirements.txt
├── .env.example
└── README.md
```

---

*Your Salesforce, local and fast.*
