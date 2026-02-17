# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| latest  | :white_check_mark: |
| main    | :white_check_mark: |

## Reporting a Vulnerability

**DO NOT open a public GitHub issue for security vulnerabilities.**

Email: **security@blackroad.io**

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fixes (optional)

### Response Timeline

| Stage | SLA |
|-------|-----|
| Acknowledgment | 48 hours |
| Severity assessment | 72 hours |
| Fix for CRITICAL | 7 days |
| Fix for HIGH | 14 days |
| Fix for MEDIUM | 30 days |
| Disclosure coordination | After fix deployed |

## Security Architecture

### Edge Security (Cloudflare Workers)

| Control | Status | Details |
|---------|--------|---------|
| CORS origin whitelist | :white_check_mark: Active | Only `blackroad.ai` subdomains allowed |
| HSTS | :white_check_mark: Active | `max-age=31536000; includeSubDomains; preload` |
| Content Security | :white_check_mark: Active | `X-Content-Type-Options`, `X-Frame-Options`, `X-XSS-Protection` |
| Rate limiting | :white_check_mark: Active | Durable Object sliding window, 1000 req/min per key |
| Request size limit | :white_check_mark: Active | 10MB max body |
| SQL injection protection | :white_check_mark: Active | Table whitelist + destructive query blocking |

### Authentication

| Method | Status | Details |
|--------|--------|---------|
| JWT (Bearer) | :white_check_mark: Active | HMAC-SHA256, 1-hour expiry |
| API Keys | :white_check_mark: Active | KV-stored, scoped, daily expiry check |
| Session cookies | :white_check_mark: Active | 30-day refresh tokens |
| WebSocket auth | :white_check_mark: Active | JWT required for upgrade, room whitelist |
| Password hashing | :white_check_mark: Active | PBKDF2 with 100k iterations, random salt |

### Webhook Verification

| Provider | Status | Method |
|----------|--------|--------|
| GitHub | :white_check_mark: | HMAC-SHA256 (`X-Hub-Signature-256`) |
| Stripe | :white_check_mark: | HMAC-SHA256 + timestamp replay protection (5 min window) |
| Salesforce | :construction: Planned | OAuth certificate verification |
| Slack | :construction: Planned | Signing secret verification |

### Network Security

| Control | Status | Details |
|---------|--------|---------|
| Cloudflare Tunnels | :white_check_mark: Active | 4 tunnels, no open inbound ports |
| Tailscale ACL | :white_check_mark: Active | Role-based: admin/operator/dev/mobile |
| Tailscale SSH | :white_check_mark: Active | Key-based auth, admin-only |
| Tunnel failover | :white_check_mark: Active | Automatic failover chains + self-healing |
| MagicDNS | :white_check_mark: Active | Internal resolution for mesh nodes |

### CI/CD Security

| Control | Status | Details |
|---------|--------|---------|
| CodeQL SAST | :white_check_mark: Active | JavaScript/TypeScript + Python, weekly + on PR |
| Secret scanning | :white_check_mark: Active | TruffleHog + Gitleaks + custom patterns |
| Dependency audit | :white_check_mark: Active | npm audit (critical/high fail gate) |
| Dependabot | :white_check_mark: Active | Weekly updates for npm, pip, GitHub Actions |
| SBOM generation | :white_check_mark: Active | CycloneDX format, 90-day retention |
| License compliance | :white_check_mark: Active | GPL-3.0/AGPL-3.0/SSPL-1.0 blocked |
| Workflow security lint | :white_check_mark: Active | Permission audit, injection detection |
| Infrastructure scan | :white_check_mark: Active | Tunnel config + Tailscale ACL audit |
| CODEOWNERS enforcement | :white_check_mark: Active | Security team reviews auth, workflows, tunnels |
| Secret rotation reminders | :white_check_mark: Active | Monthly automated issue creation |

### Secret Management

| Secret | Rotation Period | Storage |
|--------|----------------|---------|
| `JWT_SECRET` | 90 days | Cloudflare Workers env |
| `GITHUB_WEBHOOK_SECRET` | 180 days | GitHub + Workers |
| `STRIPE_WEBHOOK_SECRET` | 180 days | Stripe + Workers |
| `ANTHROPIC_API_KEY` | 90 days | Workers env |
| `CLOUDFLARE_API_TOKEN` | 90 days | GitHub secrets |
| `TAILSCALE_AUTH_KEY` | 90 days | GitHub secrets |

## Best Practices

When contributing:

1. **Never** commit secrets, API keys, or credentials
2. **Always** use parameterized queries for database access
3. **Always** validate and sanitize user input at system boundaries
4. **Always** verify webhook signatures before processing
5. **Never** use `Access-Control-Allow-Origin: *` in production
6. **Always** enforce authentication on WebSocket upgrades
7. **Never** log sensitive data (passwords, tokens, PII)
8. **Always** use PBKDF2/bcrypt/scrypt for password hashing (never plain SHA-256)
9. Keep dependencies up to date — review Dependabot PRs promptly
10. Review security audit workflow results weekly

## Bug Bounty

We currently do not have a formal bug bounty program, but we acknowledge contributors who help improve our security posture.

---

**BlackRoad OS** — Secure by default, hardened by design
