# BlackRoad Integrations

> **Every service we connect to. The full universe.**

---

## Integration Map

```
                              ┌─────────────────┐
                              │   BLACKROAD     │
                              │    BRIDGE       │
                              └────────┬────────┘
                                       │
        ┌──────────────────────────────┼──────────────────────────────┐
        │                              │                              │
        ▼                              ▼                              ▼
   ┌─────────┐                   ┌─────────┐                   ┌─────────┐
   │ BUSINESS│                   │   DEV   │                   │ CONTENT │
   └────┬────┘                   └────┬────┘                   └────┬────┘
        │                              │                              │
   ┌────┴────┐                   ┌────┴────┐                   ┌────┴────┐
   │Salesforce│                  │ GitHub  │                   │ Figma   │
   │ Stripe  │                   │Cloudflare│                  │ Canva   │
   │ HubSpot │                   │ Vercel  │                   │ Google  │
   └─────────┘                   └─────────┘                   └─────────┘
```

---

## Quick Reference

| Integration | Org | Status | Template |
|-------------|-----|--------|----------|
| [Salesforce](#salesforce) | FND | ✔️ Template | [salesforce-sync](templates/salesforce-sync/) |
| [Stripe](#stripe) | FND | ✔️ Template | [stripe-billing](templates/stripe-billing/) |
| [Cloudflare](#cloudflare) | CLD | ✔️ Template | [cloudflare-workers](templates/cloudflare-workers/) |
| [Google Drive](#google-drive) | ARC | ✔️ Template | [gdrive-sync](templates/gdrive-sync/) |
| [GitHub](#github) | OS | 📋 Mapped | Built-in |
| [Figma](#figma) | STU | 📋 Mapped | API only |
| [Canva](#canva) | STU | 📋 Mapped | Export only |
| [Notion](#notion) | MED | 📋 Mapped | API |
| [Slack](#slack) | OS | 📋 Mapped | Webhooks |
| [Discord](#discord) | EDU | 📋 Mapped | Bot |

---

## Business Integrations

### Salesforce
```yaml
service: Salesforce
org: BlackRoad-Foundation (FND)
node: lucidia
template: templates/salesforce-sync/

purpose: CRM, customer data, pipeline
objects:
  - Contact
  - Lead
  - Account
  - Opportunity

api:
  type: REST
  auth: OAuth 2.0 / Username-Password
  limit: 15,000 calls/day
  docs: https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/

signals:
  - "✔️ FND → OS : sf_sync_complete"
  - "📊 FND → OS : pipeline_update"
  - "🎉 FND → OS : deal_closed"
```

### Stripe
```yaml
service: Stripe
org: BlackRoad-Foundation (FND)
node: lucidia
template: templates/stripe-billing/

purpose: Payments, subscriptions, invoicing
objects:
  - Customer
  - Subscription
  - Invoice
  - PaymentIntent
  - Price
  - Product

api:
  type: REST
  auth: API Key (sk_live_xxx)
  limit: 100 requests/sec
  docs: https://stripe.com/docs/api

webhooks:
  - customer.created
  - customer.subscription.created
  - invoice.paid
  - payment_intent.succeeded

signals:
  - "💰 FND → OS : payment_received"
  - "📦 FND → OS : subscription_started"
  - "⚠️ FND → OS : payment_failed"
```

### HubSpot
```yaml
service: HubSpot
org: BlackRoad-Foundation (FND)
purpose: Marketing automation, forms, email

api:
  type: REST
  auth: OAuth 2.0 / API Key
  docs: https://developers.hubspot.com/docs/api/overview

objects:
  - Contact
  - Company
  - Deal
  - Form
  - Email
```

---

## Developer Integrations

### GitHub
```yaml
service: GitHub
org: BlackRoad-OS (OS)
purpose: Code, issues, PRs, actions, wiki

components:
  repos:
    description: Code repositories
    api: REST + GraphQL

  actions:
    description: CI/CD workflows
    location: .github/workflows/
    triggers:
      - push
      - pull_request
      - schedule
      - workflow_dispatch

  projects:
    description: Project boards
    api: GraphQL (ProjectV2)

  wiki:
    description: Documentation
    type: Git-backed markdown

  discussions:
    description: Community Q&A
    api: GraphQL

  codespaces:
    description: Cloud dev environments
    config: .devcontainer/

api:
  type: REST + GraphQL
  auth: GitHub App / PAT / OAuth
  cli: gh
  docs: https://docs.github.com/en/rest

signals:
  - "📝 OS → OS : pr_created"
  - "✔️ OS → OS : pr_merged"
  - "🐛 OS → OS : issue_opened"
```

### Cloudflare
```yaml
service: Cloudflare
org: BlackRoad-Cloud (CLD)
node: shellfish
template: templates/cloudflare-workers/

purpose: Edge compute, CDN, DNS, tunnels

components:
  workers:
    description: Edge functions
    runtime: V8 isolates
    language: JavaScript/TypeScript/Rust/Python

  pages:
    description: Static site hosting
    build: Git-connected

  r2:
    description: Object storage (S3 compatible)

  d1:
    description: Edge SQLite database

  kv:
    description: Key-value storage

  tunnels:
    description: Secure tunnels to origin
    use: Connect Pi cluster to edge

  dns:
    description: DNS management

  access:
    description: Zero-trust access

api:
  type: REST
  auth: API Token
  cli: wrangler
  docs: https://developers.cloudflare.com/

signals:
  - "🚀 CLD → OS : worker_deployed"
  - "🌐 CLD → OS : tunnel_connected"
  - "📊 CLD → OS : traffic_spike"
```

### Vercel
```yaml
service: Vercel
org: BlackRoad-Cloud (CLD)
purpose: Frontend deployment, serverless

api:
  type: REST
  auth: Bearer Token
  cli: vercel
  docs: https://vercel.com/docs/rest-api
```

### Railway
```yaml
service: Railway
org: BlackRoad-Cloud (CLD)
purpose: App deployment, ephemeral test environments for feature branches

api:
  type: GraphQL
  auth: API Token
  cli: railway
  docs: https://docs.railway.app/reference/cli-api

capabilities:
  - Deploy ephemeral environments per feature branch
  - Database provisioning (Postgres, Redis, MySQL)
  - Automatic HTTPS and custom domains

signals:
  - "🚂 CLD → OS : railway_deployed"
  - "🔄 CLD → OS : environment_created"
```

### DigitalOcean
```yaml
service: DigitalOcean
org: BlackRoad-Cloud (CLD)
node: shellfish
purpose: Droplet management, infrastructure lifecycle

api:
  type: REST
  auth: API Token
  cli: doctl
  docs: https://docs.digitalocean.com/reference/doctl/

capabilities:
  - Droplet lifecycle management (create, rebuild, scale)
  - Managed Kubernetes clusters
  - Spaces object storage (S3-compatible)

actions:
  - chrisjsimpson/droplet-rebuild-action (GitHub Action for droplet rebuilds)
  - doctl compute droplet create/rebuild/delete

signals:
  - "🌊 CLD → OS : droplet_rebuilt"
  - "📈 CLD → OS : droplet_scaled"
```

---

## Storage & Files

### Google Drive
```yaml
service: Google Drive
org: BlackRoad-Archive (ARC)
template: templates/gdrive-sync/

purpose: Document storage, sharing, collaboration

objects:
  - File
  - Folder
  - Permission
  - Comment
  - Revision

api:
  type: REST
  auth: OAuth 2.0 / Service Account
  scopes:
    - drive.readonly
    - drive.file
    - drive.metadata
  docs: https://developers.google.com/drive/api

signals:
  - "📁 ARC → OS : file_uploaded"
  - "🔄 ARC → OS : file_modified"
  - "📤 ARC → OS : file_shared"
```

### Google Sheets
```yaml
service: Google Sheets
org: BlackRoad-Archive (ARC)
purpose: Spreadsheet data, simple databases

api:
  type: REST
  auth: OAuth 2.0
  docs: https://developers.google.com/sheets/api
```

### Dropbox
```yaml
service: Dropbox
org: BlackRoad-Archive (ARC)
purpose: File backup, sync

api:
  type: REST
  auth: OAuth 2.0
```

### AWS S3
```yaml
service: AWS S3
org: BlackRoad-Archive (ARC)
purpose: Object storage, backups

api:
  type: REST (S3 protocol)
  auth: IAM / Access Keys
  compatible:
    - Cloudflare R2
    - MinIO
    - Backblaze B2
```

---

## Design & Content

### Figma
```yaml
service: Figma
org: BlackRoad-Studio (STU)
purpose: UI/UX design, prototypes, design system

api:
  type: REST
  auth: OAuth 2.0 / Personal Access Token
  docs: https://www.figma.com/developers/api

capabilities:
  - Read files and components
  - Export images (PNG, SVG, PDF)
  - Read comments
  - Access design tokens
  - Get file versions

signals:
  - "🎨 STU → OS : design_updated"
  - "💬 STU → OS : comment_added"
  - "📤 STU → OS : assets_exported"
```

### Canva
```yaml
service: Canva
org: BlackRoad-Studio (STU)
purpose: Quick graphics, social media assets

api:
  type: REST (limited)
  auth: OAuth 2.0
  docs: https://www.canva.dev/docs/connect/

capabilities:
  - Create designs from templates
  - Export designs
  - Brand kit access
```

### Adobe Creative Cloud
```yaml
service: Adobe CC
org: BlackRoad-Studio (STU)
purpose: Professional design, video, photography

apps:
  - Photoshop
  - Illustrator
  - Premiere Pro
  - After Effects
  - XD

api:
  type: REST
  auth: OAuth 2.0
  docs: https://developer.adobe.com/
```

---

## Communication

### Slack
```yaml
service: Slack
org: BlackRoad-OS (OS)
purpose: Team communication, notifications

api:
  type: REST + WebSocket
  auth: Bot Token / OAuth
  docs: https://api.slack.com/

capabilities:
  - Send messages
  - Create channels
  - Slash commands
  - Interactive components
  - Webhooks

signals:
  - "💬 OS → Slack : notification"
  - "🚨 OS → Slack : alert"
```

### Discord
```yaml
service: Discord
org: BlackRoad-Education (EDU)
purpose: Community, support, announcements

api:
  type: REST + WebSocket
  auth: Bot Token
  docs: https://discord.com/developers/docs

capabilities:
  - Bot messages
  - Slash commands
  - Embeds
  - Reactions
  - Voice (limited)
```

### Email (SendGrid/Postmark)
```yaml
service: SendGrid / Postmark
org: BlackRoad-Media (MED)
purpose: Transactional email, newsletters

api:
  type: REST
  auth: API Key
```

---

## Documentation & Knowledge

### Notion
```yaml
service: Notion
org: BlackRoad-Media (MED)
purpose: Documentation, wikis, databases

api:
  type: REST
  auth: Integration Token
  docs: https://developers.notion.com/

objects:
  - Page
  - Database
  - Block
  - User

capabilities:
  - Create/update pages
  - Query databases
  - Search content
```

### Confluence
```yaml
service: Confluence
org: BlackRoad-Media (MED)
purpose: Enterprise documentation

api:
  type: REST
  auth: API Token
```

### GitBook
```yaml
service: GitBook
org: BlackRoad-Education (EDU)
purpose: Public documentation

api:
  type: REST
  auth: API Token
  sync: Git
```

---

## AI & ML

### OpenAI
```yaml
service: OpenAI
org: BlackRoad-AI (AI)
purpose: GPT models, embeddings, DALL-E

api:
  type: REST
  auth: API Key
  models:
    - gpt-4
    - gpt-3.5-turbo
    - text-embedding-ada-002
    - dall-e-3
```

### Anthropic (Claude)
```yaml
service: Anthropic
org: BlackRoad-AI (AI)
purpose: Claude models

api:
  type: REST
  auth: API Key
  models:
    - claude-3-opus
    - claude-3-sonnet
    - claude-3-haiku
```

### Hugging Face
```yaml
service: Hugging Face
org: BlackRoad-AI (AI)
purpose: Model hosting, inference endpoints, specialized reasoning

api:
  type: REST
  auth: HF_TOKEN (Bearer)
  docs: https://huggingface.co/docs/huggingface_hub/guides/inference

capabilities:
  - Programmatic deployment of dedicated inference endpoints
  - High-compute tasks exceeding local Pi cluster capacity
  - GGUF model hosting via Ollama integration

signals:
  - "🤗 AI → OS : inference_complete"
  - "⚠️ AI → OS : rate_limit_hit"
```

### Ollama
```yaml
service: Ollama
org: BlackRoad-AI (AI)
node: lucidia
purpose: Local LLM inference via Cloudflare Tunnel

api:
  type: REST (OpenAI-compatible)
  auth: Cloudflare Access (service token or mTLS required)
  endpoint: http://lucidia:11434
  tunnel: Cloudflare Tunnel (connectivity only; auth via Cloudflare Access) → lucidia:11434
  docs: https://github.com/ollama/ollama/blob/main/docs/api.md

models:
  - bartowski/Llama-3.2-3B-Instruct-GGUF
  - gemma:2b
  - tinyllama

capabilities:
  - Local private inference (no data leaves network)
  - Copilot offloading via LiteLLM proxy
  - Quantized GGUF model support

signals:
  - "🧠 AI → OS : local_inference_complete"
  - "📊 AI → OS : model_loaded"
```

### Replicate
```yaml
service: Replicate
org: BlackRoad-AI (AI)
purpose: Open source model hosting

api:
  type: REST
  auth: API Token
```

---

## Automation

### Zapier
```yaml
service: Zapier
org: BlackRoad-OS (OS)
purpose: No-code automation between services

api:
  type: REST (webhooks)
  auth: Webhook URLs
```

### Make (Integromat)
```yaml
service: Make
org: BlackRoad-OS (OS)
purpose: Visual automation workflows

api:
  type: REST
  auth: API Key
```

### n8n
```yaml
service: n8n
org: BlackRoad-OS (OS)
purpose: Self-hosted workflow automation

deployment: Self-hosted on alice
api:
  type: REST
```

---

## Analytics

### Google Analytics
```yaml
service: Google Analytics
org: BlackRoad-Media (MED)
purpose: Web analytics

api:
  type: REST
  auth: OAuth 2.0
  version: GA4
```

### Mixpanel
```yaml
service: Mixpanel
org: BlackRoad-Media (MED)
purpose: Product analytics

api:
  type: REST
  auth: API Secret
```

### Plausible
```yaml
service: Plausible
org: BlackRoad-Media (MED)
purpose: Privacy-friendly analytics

api:
  type: REST
  auth: API Key
  deployment: Self-hosted option
```

---

## Integration Patterns

### Webhook Pattern
```
External Service → Webhook → Operator → Route → Handler
                                ↓
                            Signal to OS
```

### Polling Pattern
```
Scheduler → Poll Service → Compare → Update Local
                              ↓
                        Signal if changed
```

### Real-time Pattern
```
WebSocket/SSE → Event Stream → Process → Signal
```

---

## Signal Reference

All integrations emit signals to OS:

| Signal | Meaning |
|--------|---------|
| `✔️ [ORG] → OS : [action]_complete` | Action succeeded |
| `❌ [ORG] → OS : [action]_failed` | Action failed |
| `📊 [ORG] → OS : [metric]_update` | Metric changed |
| `🔔 [ORG] → OS : [event]_received` | External event |
| `⚠️ [ORG] → OS : [limit]_warning` | Approaching limit |

---

*Every service. One Bridge.*
