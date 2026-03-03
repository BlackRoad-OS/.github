# Security Policy

## Supported Versions

We actively support the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| latest  | :white_check_mark: |
| main    | :white_check_mark: |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security issue, please report it responsibly.

### How to Report

**Please DO NOT open a public GitHub issue for security vulnerabilities.**

Instead, please email: **security@blackroad.io**

In your report, please include:

- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact
- Any suggested fixes (optional)

### What to Expect

- **Acknowledgment**: We'll acknowledge your report within 48 hours
- **Assessment**: We'll assess the vulnerability and determine its severity
- **Updates**: We'll keep you informed of our progress
- **Resolution**: We'll work on a fix and coordinate disclosure timing with you
- **Credit**: With your permission, we'll credit you in our security advisories

### Security Features

This repository is protected with:

- Dependabot vulnerability scanning (weekly schedule, npm + pip + GitHub Actions)
- Automated security updates
- GitHub secret scanning
- CodeQL code analysis (JavaScript/TypeScript, Python)
- Dependency review on pull requests
- Pinned GitHub Actions to commit SHAs (supply chain protection)
- Minimal workflow permissions (principle of least privilege)

### Security Architecture

**API Gateway (Cloudflare Worker)**
- PBKDF2 password hashing (100,000 iterations, random salt)
- HMAC-SHA256 JWT with algorithm validation
- Webhook signature verification (GitHub HMAC, Stripe timestamp + HMAC)
- SQL injection protection via table allowlists and query restrictions
- Input validation on all public endpoints (length limits, format checks)
- Rate limiting via Durable Objects
- Path traversal prevention on KV/R2 key operations
- CORS restricted to approved origins
- Error messages sanitized in production (no stack traces)

**Workflow Security**
- All third-party GitHub Actions pinned to full commit SHAs
- Minimal permissions declared on every workflow
- User-controlled input passed via environment variables, never interpolated in shell
- No secrets logged or exposed in step outputs

### Best Practices

When contributing to this project:

- Never commit secrets, API keys, or credentials
- Keep dependencies up to date
- Follow secure coding guidelines
- Review Dependabot alerts promptly
- Pin all action references to commit SHAs
- Declare minimal permissions on workflows

## Bug Bounty Program

We currently do not have a formal bug bounty program, but we greatly appreciate responsible disclosure and will acknowledge contributors who help improve our security posture.

---

**BlackRoad OS, Inc.** - Building secure, scalable systems
