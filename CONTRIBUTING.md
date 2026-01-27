# Contributing to BlackRoad

> **Welcome to The Bridge!** We're building a routing company that connects users to intelligence without owning the intelligence itself.

---

## Getting Started

Before contributing, please:

1. **Read the architecture** - [BLACKROAD_ARCHITECTURE.md](BLACKROAD_ARCHITECTURE.md)
2. **Understand the ecosystem** - [INDEX.md](INDEX.md) and [REPO_MAP.md](REPO_MAP.md)
3. **Learn the signal protocol** - [SIGNALS.md](SIGNALS.md)
4. **Review the streams model** - [STREAMS.md](STREAMS.md)

---

## How to Contribute

### 1. Choose Your Organization

BlackRoad operates across 15 specialized organizations. Identify which one your contribution relates to:

| Organization | Focus Area | Blueprint |
|--------------|-----------|-----------|
| BlackRoad-OS | Core infrastructure, The Bridge | [Browse](orgs/BlackRoad-OS/) |
| BlackRoad-AI | Intelligence routing, ML | [Browse](orgs/BlackRoad-AI/) |
| BlackRoad-Cloud | Edge compute, Cloudflare | [Browse](orgs/BlackRoad-Cloud/) |
| BlackRoad-Hardware | Pi cluster, IoT, Hailo | [Browse](orgs/BlackRoad-Hardware/) |
| BlackRoad-Security | Auth, secrets, audit | [Browse](orgs/BlackRoad-Security/) |
| BlackRoad-Labs | Experiments, R&D | [Browse](orgs/BlackRoad-Labs/) |
| BlackRoad-Foundation | CRM, finance, Stripe | [Browse](orgs/BlackRoad-Foundation/) |
| BlackRoad-Ventures | Marketplace, commerce | [Browse](orgs/BlackRoad-Ventures/) |
| Blackbox-Enterprises | Enterprise solutions | [Browse](orgs/Blackbox-Enterprises/) |
| BlackRoad-Media | Content, social media | [Browse](orgs/BlackRoad-Media/) |
| BlackRoad-Studio | Design system, UI | [Browse](orgs/BlackRoad-Studio/) |
| BlackRoad-Interactive | Metaverse, 3D, games | [Browse](orgs/BlackRoad-Interactive/) |
| BlackRoad-Education | Learning, tutorials | [Browse](orgs/BlackRoad-Education/) |
| BlackRoad-Gov | Governance, voting | [Browse](orgs/BlackRoad-Gov/) |
| BlackRoad-Archive | Storage, backups | [Browse](orgs/BlackRoad-Archive/) |

### 2. Types of Contributions

We welcome:

- 🐛 **Bug fixes** - Fix issues in existing code
- ✨ **New features** - Add functionality to an organization
- 📚 **Documentation** - Improve docs, add examples
- 🏢 **Organization blueprints** - Enhance org specifications
- 🔧 **Infrastructure** - Workflows, templates, tools
- 🧪 **Tests** - Add or improve test coverage
- ⚡ **Performance** - Optimize existing code
- 🎨 **Design** - UI/UX improvements

### 3. Contribution Workflow

#### Step 1: Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/.github.git
cd .github
```

#### Step 2: Create a Branch

```bash
# Use a descriptive branch name
git checkout -b feat/org-name/feature-description
# or
git checkout -b fix/org-name/bug-description
```

#### Step 3: Make Your Changes

- Follow existing code style and patterns
- Add tests if applicable
- Update documentation if needed
- Keep commits focused and atomic

#### Step 4: Test Your Changes

```bash
# Run relevant tests
python -m pytest prototypes/

# Check linting (if applicable)
# Verify builds pass
```

#### Step 5: Commit with Clear Messages

```bash
git add .
git commit -m "feat(org-ai): add new routing algorithm

- Implement fuzzy matching for queries
- Add confidence scoring
- Update tests

Signal: AI → OS : feature_added"
```

**Commit Message Format:**
```
<type>(<scope>): <subject>

<body>

Signal: <from> → <to> : <signal>
```

**Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

#### Step 6: Push and Create Pull Request

```bash
git push origin your-branch-name
```

Then create a pull request on GitHub using our [PR template](.github/PULL_REQUEST_TEMPLATE.md).

---

## Code Style Guidelines

### Python

- Use Python 3.11+
- Follow PEP 8 style guide
- Use type hints where possible
- Document functions with docstrings
- Keep functions small and focused

### Markdown

- Use consistent heading levels
- Include code examples in fenced blocks
- Add emojis for readability (sparingly)
- Keep line length reasonable

### YAML

- Use 2 spaces for indentation
- Quote strings when necessary
- Comment complex configurations

---

## Signal Protocol

All contributions should follow the signal protocol documented in [SIGNALS.md](SIGNALS.md).

When your contribution creates cross-org communication, emit appropriate signals:

```python
# Example: Emit a signal when work completes
emit_signal(
    from_org="AI",
    to_org="OS",
    signal="query_routed",
    confidence=0.95
)
```

---

## Testing

### Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test
python -m pytest prototypes/operator/tests/test_router.py

# Run with coverage
python -m pytest --cov
```

### Writing Tests

- Write tests for new features
- Maintain or improve test coverage
- Use descriptive test names
- Test edge cases

---

## Documentation

### When to Update Docs

- Adding new features or APIs
- Changing existing behavior
- Adding new organization
- Creating new templates

### Where to Add Docs

- **README files** - In each organization blueprint
- **INTEGRATIONS.md** - For external service integrations
- **Code comments** - For complex logic
- **Examples** - In templates/ directory

---

## Pull Request Guidelines

### Before Submitting

- [ ] Code follows project style
- [ ] Tests pass locally
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] Branch is up to date with main
- [ ] No unnecessary files included

### PR Description

Use the [PR template](.github/PULL_REQUEST_TEMPLATE.md) and include:

- Clear description of changes
- Type of change
- Related organization(s)
- Testing performed
- Screenshots (if UI changes)

### Review Process

1. Automated checks run (CI/CD)
2. Auto-triage assigns labels
3. Maintainers review code
4. Feedback addressed
5. PR merged

---

## Organization-Specific Guidelines

### BlackRoad-OS (The Bridge)

- Changes affect all orgs - be careful
- Update MEMORY.md for significant changes
- Keep .STATUS current
- Coordinate with other org maintainers

### BlackRoad-AI

- Router changes need performance tests
- Document classification logic
- Include confidence thresholds

### BlackRoad-Cloud

- Test on Cloudflare Workers environment
- Verify edge compute performance
- Check cold start times

### BlackRoad-Hardware

- Test on Raspberry Pi if possible
- Document hardware requirements
- Consider power consumption

---

## Getting Help

- 💬 **Discussions** - Ask questions in GitHub Discussions
- 📖 **Documentation** - Read [INDEX.md](INDEX.md) and org blueprints
- 🐛 **Issues** - Check existing issues or create a new one
- 📊 **Dashboard** - Run `python -m metrics.dashboard` for ecosystem health

---

## Code of Conduct

This project follows our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold this code.

---

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

## Recognition

Contributors will be:

- Listed in CONTRIBUTORS.md
- Credited in release notes
- Given appropriate GitHub permissions

---

## Questions?

- Check [SUPPORT.md](SUPPORT.md) for support options
- Review [SECURITY.md](SECURITY.md) for security issues
- Browse organization blueprints in [orgs/](orgs/)

---

*Thank you for contributing to BlackRoad! 🚀*

📡 **Signal:** `contributor → OS : contribution_started`
