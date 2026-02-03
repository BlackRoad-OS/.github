# Salesforce Integration

> **CRM, customer data, business operations.**

---

## Overview

Salesforce is BlackRoad's CRM platform, managed by [BlackRoad-Foundation](../Orgs/BlackRoad-Foundation).

**Organization**: [BlackRoad-Foundation](../Orgs/BlackRoad-Foundation)  
**Status**: Planned

---

## Architecture

```
┌─────────────────────────────────────────┐
│           SALESFORCE                    │
├─────────────────────────────────────────┤
│                                         │
│   Objects                               │
│   ├── Account     ← Companies          │
│   ├── Contact     ← People             │
│   ├── Opportunity ← Deals              │
│   └── Case        ← Support tickets    │
│                                         │
│   APIs                                  │
│   ├── REST API    ← CRUD operations    │
│   ├── SOAP API    ← Legacy             │
│   └── Bulk API    ← Large datasets     │
│                                         │
└─────────────────────────────────────────┘
```

---

## Authentication

```python
import requests

# OAuth 2.0
def authenticate():
    response = requests.post(
        'https://login.salesforce.com/services/oauth2/token',
        data={
            'grant_type': 'password',
            'client_id': SF_CLIENT_ID,
            'client_secret': SF_CLIENT_SECRET,
            'username': SF_USERNAME,
            'password': SF_PASSWORD
        }
    )
    return response.json()['access_token']
```

---

## Common Operations

### Create Account

```python
def create_account(name: str, email: str):
    """Create new Salesforce account."""
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'Name': name,
        'Email__c': email,
        'Type': 'Customer'
    }
    
    response = requests.post(
        f'{instance_url}/services/data/v58.0/sobjects/Account',
        headers=headers,
        json=data
    )
    
    return response.json()
```

### Query Accounts

```python
def query_accounts():
    """Query all accounts."""
    query = "SELECT Id, Name, Email__c FROM Account WHERE Type = 'Customer'"
    
    response = requests.get(
        f'{instance_url}/services/data/v58.0/query',
        headers={'Authorization': f'Bearer {access_token}'},
        params={'q': query}
    )
    
    return response.json()['records']
```

---

## Sync with Stripe

```python
def sync_sf_to_stripe(account_id: str):
    """Sync Salesforce account to Stripe customer."""
    
    # Get SF account
    sf_account = get_account(account_id)
    
    # Create Stripe customer
    stripe_customer = stripe.Customer.create(
        email=sf_account['Email__c'],
        name=sf_account['Name'],
        metadata={'sf_account_id': account_id}
    )
    
    # Update SF with Stripe ID
    update_account(account_id, {
        'Stripe_Customer_ID__c': stripe_customer.id
    })
    
    emit(f"✔️ FND → OS : sync_complete, sf={account_id}, stripe={stripe_customer.id}")
```

---

## Webhooks

```python
@app.route('/webhooks/salesforce', methods=['POST'])
def salesforce_webhook():
    """Handle Salesforce webhook."""
    event = request.json
    
    if event['type'] == 'Account.created':
        # Sync new account to Stripe
        sync_sf_to_stripe(event['data']['Id'])
    
    return {'status': 'ok'}
```

---

## Template

Full working template at: `templates/salesforce-sync/`

```bash
# Use the template
cp -r templates/salesforce-sync/* your-project/
vim config.yml  # Configure
python -m salesforce_sync.cli sync
```

---

## Signals

```
✔️ FND → OS : account_created, sf_id=001...
✔️ FND → OS : sync_complete, sf=001..., stripe=cus_...
❌ FND → OS : sync_failed, reason=timeout
```

---

## Learn More

- [BlackRoad-Foundation](../Orgs/BlackRoad-Foundation)
- [Stripe Integration](Stripe)

---

*CRM operations. Customer lifecycle.*
