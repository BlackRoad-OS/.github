# Stripe Integration

> **Billing, payments, subscriptions. $1/user/month.**

---

## Overview

Stripe is BlackRoad's payment processor, managed by [BlackRoad-Foundation](../Orgs/BlackRoad-Foundation).

**Organization**: [BlackRoad-Foundation](../Orgs/BlackRoad-Foundation)  
**Status**: Planned

---

## Business Model

**Pricing**: $1/user/month

```python
# Subscription setup
stripe.Price.create(
    unit_amount=100,  # $1.00 in cents
    currency='usd',
    recurring={'interval': 'month'},
    product='prod_blackroad'
)
```

---

## Common Operations

### Create Customer

```python
import stripe

customer = stripe.Customer.create(
    email='user@example.com',
    name='John Doe',
    metadata={'source': 'signup'}
)
```

### Create Subscription

```python
subscription = stripe.Subscription.create(
    customer=customer.id,
    items=[{'price': 'price_1234'}],
    trial_period_days=7
)
```

### Handle Webhooks

```python
@app.route('/webhooks/stripe', methods=['POST'])
def stripe_webhook():
    event = stripe.Webhook.construct_event(
        request.data,
        request.headers['Stripe-Signature'],
        webhook_secret
    )
    
    if event.type == 'customer.subscription.created':
        # Handle new subscription
        emit(f"✔️ FND → OS : subscription_created")
    
    elif event.type == 'invoice.payment_failed':
        # Handle failed payment
        emit(f"❌ FND → OS : payment_failed")
    
    return {'status': 'ok'}
```

---

## Template

Full working template at: `templates/stripe-billing/`

```bash
# Use the template
cp -r templates/stripe-billing/* your-project/
vim config.yml  # Configure
python -m stripe_billing.cli test
```

---

## Learn More

- [BlackRoad-Foundation](../Orgs/BlackRoad-Foundation)
- [Salesforce Integration](Salesforce)

---

*Revenue engine. Simple billing.*
