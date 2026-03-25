# Security Policy

## Supported Versions

Only the latest release on the default branch is actively maintained.

## Reporting a Vulnerability

**Do not open a public issue for security vulnerabilities.**

Email **security@blackroad.io** with:
- Description of the vulnerability
- Steps to reproduce
- Potential impact

We will acknowledge receipt within 48 hours and provide a timeline for a fix.

## Disclosure Policy

We follow coordinated disclosure. We ask that you give us 90 days to address the issue before public disclosure.

## Security Practices

- All commits to main/master require pull requests (enterprise ruleset)
- SHA pinning is required for all GitHub Actions
- Sensitive files (.env, *.pem, *.key) are blocked at the enterprise level
- Version tags (v*) are immutable once pushed
