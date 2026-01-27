# Support

> **Need help with BlackRoad?** You're in the right place.

---

## Getting Support

### 1. 📖 Documentation

Start with our comprehensive documentation:

- **[INDEX.md](INDEX.md)** - Complete map of the ecosystem
- **[BLACKROAD_ARCHITECTURE.md](BLACKROAD_ARCHITECTURE.md)** - Architecture overview
- **[REPO_MAP.md](REPO_MAP.md)** - All repositories and organizations
- **[STREAMS.md](STREAMS.md)** - Data flow patterns
- **[SIGNALS.md](SIGNALS.md)** - Communication protocol
- **[INTEGRATIONS.md](INTEGRATIONS.md)** - External service integrations
- **[Organization Blueprints](orgs/)** - Detailed specs for all 15 orgs

### 2. 💬 Community Discussions

Ask questions and discuss with the community:

**GitHub Discussions:** [BlackRoad-OS/discussions](https://github.com/orgs/BlackRoad-OS/discussions)

- General questions
- Feature discussions
- Best practices
- Show and tell

### 3. 🐛 Issue Tracker

Found a bug or have a specific problem?

**Create an issue:** Use our [issue templates](.github/ISSUE_TEMPLATE/)

- [Bug Report](.github/ISSUE_TEMPLATE/bug_report.yml) - Report bugs
- [Feature Request](.github/ISSUE_TEMPLATE/feature_request.yml) - Suggest features
- [Organization Setup](.github/ISSUE_TEMPLATE/organization_setup.yml) - Request new repos

### 4. 🏢 Organization-Specific Support

Different organizations have different support channels:

#### BlackRoad-OS (Core Infrastructure)
- **Scope:** The Bridge, operator, mesh networking
- **Docs:** [orgs/BlackRoad-OS/](orgs/BlackRoad-OS/)
- **Issues:** General infrastructure issues

#### BlackRoad-AI (Intelligence Routing)
- **Scope:** AI routing, model integrations, Hailo
- **Docs:** [orgs/BlackRoad-AI/](orgs/BlackRoad-AI/)
- **Issues:** Routing logic, AI features

#### BlackRoad-Cloud (Edge Compute)
- **Scope:** Cloudflare Workers, edge functions
- **Docs:** [orgs/BlackRoad-Cloud/](orgs/BlackRoad-Cloud/)
- **Issues:** Deployment, edge compute

#### BlackRoad-Hardware (Physical Infrastructure)
- **Scope:** Raspberry Pi cluster, IoT, Hailo-8
- **Docs:** [orgs/BlackRoad-Hardware/](orgs/BlackRoad-Hardware/)
- **Issues:** Hardware setup, node configuration

#### BlackRoad-Security (Security & Auth)
- **Scope:** Authentication, secrets, compliance
- **Docs:** [orgs/BlackRoad-Security/](orgs/BlackRoad-Security/)
- **Security:** See [SECURITY.md](SECURITY.md)

#### BlackRoad-Foundation (Business & CRM)
- **Scope:** Salesforce, Stripe, billing
- **Docs:** [orgs/BlackRoad-Foundation/](orgs/BlackRoad-Foundation/)
- **Issues:** Business operations, integrations

---

## Common Questions

### General

**Q: What is BlackRoad?**
A: BlackRoad is a routing company that connects users to intelligence (AI models, APIs, databases) without owning the intelligence itself. Read [BLACKROAD_ARCHITECTURE.md](BLACKROAD_ARCHITECTURE.md) for details.

**Q: How many organizations are there?**
A: 15 specialized organizations across 5 tiers (Core, Support, Business, Creative, Community). See [INDEX.md](INDEX.md) for the complete list.

**Q: What is "The Bridge"?**
A: This `.github` repository - the central coordination point where all architecture decisions are made and organization blueprints live.

### Technical

**Q: How do I run the Operator?**
A: 
```bash
cd prototypes/operator
python -m operator.cli "your query here"
```

**Q: How do I check system health?**
A:
```bash
python -m metrics.dashboard
cat .STATUS
```

**Q: What's the signal protocol?**
A: Signals are emoji-based messages for agent coordination. Read [SIGNALS.md](SIGNALS.md) for the complete protocol.

### Contributing

**Q: How can I contribute?**
A: See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

**Q: Which organization should I contribute to?**
A: Review the organization blueprints in [orgs/](orgs/) to find the right fit for your contribution.

**Q: Do you accept pull requests?**
A: Yes! Follow the [PR template](.github/PULL_REQUEST_TEMPLATE.md) and guidelines in [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Response Times

We aim for:

- **Discussions:** Response within 24-48 hours
- **Bug Reports:** Triage within 48 hours
- **Feature Requests:** Review within 1 week
- **Security Issues:** Response within 48 hours (see [SECURITY.md](SECURITY.md))

Note: Response times may vary based on maintainer availability and issue complexity.

---

## Self-Help Resources

### Quick Commands

```bash
# See everything
cat INDEX.md

# Check health
python -m metrics.dashboard

# Route a query
python -m operator.cli "your question"

# Browse an organization
cat orgs/BlackRoad-AI/README.md

# Check current status
cat .STATUS

# Read persistent memory
cat MEMORY.md

# List all repositories
cat REPO_MAP.md

# View integrations
cat INTEGRATIONS.md
```

### Prototypes

Try our working prototypes:

```bash
# Operator - Routes queries to correct org
cd prototypes/operator
python -m operator.cli --interactive

# Metrics - Real-time KPI dashboard
cd prototypes/metrics
python -m metrics.dashboard --watch

# Explorer - Browse the ecosystem
cd prototypes/explorer
python -m explorer.cli
```

### Templates

Explore integration templates:

- **Salesforce Sync:** [templates/salesforce-sync/](templates/salesforce-sync/)
- **Stripe Billing:** [templates/stripe-billing/](templates/stripe-billing/)
- **Cloudflare Workers:** [templates/cloudflare-workers/](templates/cloudflare-workers/)
- **Google Drive Sync:** [templates/gdrive-sync/](templates/gdrive-sync/)
- **GitHub Ecosystem:** [templates/github-ecosystem/](templates/github-ecosystem/)
- **Design Tools:** [templates/design-tools/](templates/design-tools/)

---

## Commercial Support

For enterprise support or custom implementations:

- **Email:** support@blackroad.dev *(configure when available)*
- **Org:** [Blackbox-Enterprises](orgs/Blackbox-Enterprises/) - Enterprise solutions
- **Consulting:** Available for large-scale deployments

---

## Educational Resources

### Learning Paths

**Beginner:**
1. Read [BLACKROAD_ARCHITECTURE.md](BLACKROAD_ARCHITECTURE.md)
2. Explore [INDEX.md](INDEX.md)
3. Try the Operator prototype
4. Browse organization blueprints

**Intermediate:**
1. Study [STREAMS.md](STREAMS.md) and [SIGNALS.md](SIGNALS.md)
2. Review [INTEGRATIONS.md](INTEGRATIONS.md)
3. Contribute to prototypes
4. Implement a template

**Advanced:**
1. Design new organization blueprints
2. Build cross-org integrations
3. Optimize routing algorithms
4. Contribute to infrastructure

### Tutorials

Check [BlackRoad-Education](orgs/BlackRoad-Education/) for:
- Getting started guides
- Integration tutorials
- Best practices
- Video walkthroughs

---

## Troubleshooting

### Common Issues

**Issue: Operator not routing correctly**
```bash
# Check the operator configuration
cat prototypes/operator/routing/config.yaml

# Test with verbose output
python -m operator.cli "query" --verbose
```

**Issue: Can't find a specific file**
```bash
# Use the index
grep -r "filename" INDEX.md

# Search the repo map
grep -r "repo-name" REPO_MAP.md
```

**Issue: Understanding data flow**
```bash
# Read the streams documentation
cat STREAMS.md

# Check signal definitions
cat SIGNALS.md
```

---

## Staying Updated

### Release Notes

Watch for releases in individual repositories:
- Check GitHub Releases for each repo
- Review CHANGELOG files
- Follow release signals

### Community Updates

- **GitHub Discussions** - Announcements
- **Repository Watch** - Enable notifications
- **MEMORY.md** - Check for session updates

---

## Contact

### Public Channels

- **GitHub Issues** - Bug reports and features
- **GitHub Discussions** - General questions
- **Documentation** - Self-service help

### Private Channels

- **Security Issues** - See [SECURITY.md](SECURITY.md)
- **Business Inquiries** - support@blackroad.dev *(configure when available)*

---

## Contributing to Support

Help us improve support:

- Answer questions in Discussions
- Improve documentation
- Create tutorials
- Share your solutions
- Report documentation issues

---

*We're here to help! 🤝*

📡 **Signal:** `user → support : help_requested`
