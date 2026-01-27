# BlackRoad-Cloud Repositories

> Repo specs for the Cloud org

---

## Repository List

### `workers` (P0 - Build First)

**Purpose:** Cloudflare Workers - edge compute

**Structure:**
```
workers/
├── src/
│   ├── gateway/
│   │   ├── index.ts      ← Main API gateway
│   │   └── routes.ts     ← Route definitions
│   ├── router/
│   │   └── index.ts      ← Internal routing logic
│   ├── auth/
│   │   ├── index.ts      ← Auth worker
│   │   └── jwt.ts        ← JWT handling
│   └── shared/
│       ├── utils.ts
│       └── types.ts
├── wrangler.toml         ← Cloudflare config
├── package.json
└── README.md
```

**Key Features:**
- TypeScript
- Hono framework (fast, lightweight)
- KV for caching
- Durable Objects for state (if needed)

---

### `deploy` (P0 - Build First)

**Purpose:** CI/CD and deployment configs

**Structure:**
```
deploy/
├── github-actions/
│   ├── deploy-workers.yml
│   ├── deploy-pages.yml
│   └── test.yml
├── scripts/
│   ├── deploy.sh
│   ├── rollback.sh
│   └── health-check.sh
├── environments/
│   ├── production.env
│   ├── staging.env
│   └── development.env
└── README.md
```

---

### `api` (P1)

**Purpose:** API definitions and documentation

**Structure:**
```
api/
├── openapi/
│   └── spec.yaml         ← OpenAPI 3.0 spec
├── schemas/
│   ├── request.json
│   └── response.json
├── examples/
│   └── ...
└── README.md
```

---

### `dns` (P1)

**Purpose:** DNS and routing configuration

**Structure:**
```
dns/
├── zones/
│   ├── blackroad.dev.json
│   └── ...
├── rules/
│   ├── redirects.json
│   └── page-rules.json
└── README.md
```

---

### `tunnel` (P1)

**Purpose:** Cloudflare Tunnel to Pi mesh

**Structure:**
```
tunnel/
├── configs/
│   ├── alice.yaml        ← Main tunnel config
│   └── shellfish.yaml    ← Backup tunnel
├── scripts/
│   ├── setup-tunnel.sh
│   └── rotate-creds.sh
└── README.md
```

**Key Insight:** Tunnels connect Cloudflare edge to our Pi mesh without exposing ports.

---

### `pages` (P2)

**Purpose:** Static site deployments

**Structure:**
```
pages/
├── sites/
│   ├── landing/          ← Marketing site
│   ├── docs/             ← Documentation
│   └── status/           ← Status page
├── build-configs/
└── README.md
```

---

## Repo Creation Order

```
1. workers    ← Core edge compute
2. deploy     ← CI/CD pipeline
3. api        ← API documentation
4. dns        ← Routing rules
5. tunnel     ← Mesh connectivity
6. pages      ← Static sites
```

---

*Deploy once, run everywhere.*
