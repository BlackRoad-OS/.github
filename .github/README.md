# .github Directory

This directory contains GitHub-specific configurations for the BlackRoad-OS/.github repository, which serves as **The Bridge** - the central coordination point for all BlackRoad organizations.

---

## Purpose

The `.github` directory in a special `.github` repository serves two purposes:

1. **Repository Configuration** - Settings for this specific repository
2. **Organization Defaults** - Default settings inherited by all repositories in the BlackRoad-OS organization

---

## Structure

```
.github/
├── ISSUE_TEMPLATE/          # Issue templates
│   ├── bug_report.yml       # Bug report template
│   ├── config.yml           # Issue template configuration
│   ├── feature_request.yml  # Feature request template
│   └── organization_setup.yml # Org setup template
│
├── workflows/               # GitHub Actions workflows
│   ├── ci.yml              # Continuous integration
│   ├── deploy-worker.yml   # Cloudflare Worker deployment
│   ├── health-check.yml    # System health monitoring
│   ├── issue-triage.yml    # Auto-triage issues
│   ├── pr-review.yml       # PR automation
│   ├── release.yml         # Release management
│   ├── sync-assets.yml     # Asset sync
│   └── webhook-dispatch.yml # Webhook handling
│
├── CODEOWNERS              # Code review assignments
├── dependabot.yml          # Dependency update automation
├── FUNDING.yml             # Sponsorship configuration
└── PULL_REQUEST_TEMPLATE.md # PR template
```

---

## Files Explained

### Issue Templates

**ISSUE_TEMPLATE/**

GitHub issue forms that provide structured bug reports and feature requests. All templates include organization selection to route issues correctly.

- `bug_report.yml` - Structured bug reporting
- `feature_request.yml` - Feature suggestions
- `organization_setup.yml` - New repository setup requests
- `config.yml` - Links to docs and discussions

### Workflows

**workflows/**

Automated GitHub Actions for CI/CD, monitoring, and automation.

Key workflows:
- `issue-triage.yml` - Uses the Operator prototype to auto-classify and label issues
- `ci.yml` - Runs tests and linting
- `health-check.yml` - Monitors system health
- `deploy-worker.yml` - Deploys Cloudflare Workers

### Code Review

**CODEOWNERS**

Defines default reviewers for different parts of the repository:
- Core files require core team approval
- Organization blueprints route to org-specific teams
- Security files require security team approval

### Dependency Management

**dependabot.yml**

Configures Dependabot to automatically:
- Update GitHub Actions weekly
- Update Python dependencies in prototypes
- Create PRs for security updates

### Funding

**FUNDING.yml**

Placeholder for future sponsorship options (GitHub Sponsors, custom URLs).

### Pull Requests

**PULL_REQUEST_TEMPLATE.md**

Template for all pull requests with:
- Description guidelines
- Type of change checkboxes
- Organization selection
- Testing checklist
- Signal notation

---

## How It Works

### As a .github Repository

This repository is special because it's named `.github` in the BlackRoad-OS organization. This means:

1. **Organization-wide defaults** - Files here apply to all repos without their own versions
2. **Profile README** - The `profile/README.md` appears on the org's GitHub page
3. **Shared workflows** - Can be reused across repositories

### Auto-triage System

The `issue-triage.yml` workflow uses the Operator prototype to:
1. Parse issue title and body
2. Route to appropriate organization (OS, AI, Cloud, etc.)
3. Apply relevant labels
4. Add auto-classification comment

### Code Review Flow

When a PR is created:
1. CODEOWNERS assigns reviewers based on changed files
2. CI workflows run automated checks
3. Security scans execute
4. Human reviewers approve
5. Auto-merge if conditions met

---

## Customization

### Adding a New Issue Template

1. Create a new `.yml` file in `ISSUE_TEMPLATE/`
2. Follow the GitHub issue forms syntax
3. Include organization dropdown for routing
4. Test with a real issue

### Adding a New Workflow

1. Create a new `.yml` file in `workflows/`
2. Define triggers (push, PR, schedule, etc.)
3. Add jobs and steps
4. Test in a branch before merging

### Updating CODEOWNERS

1. Edit `.github/CODEOWNERS`
2. Add patterns and team mentions
3. Ensure teams exist in GitHub org settings

---

## Best Practices

### Issue Templates

- Keep forms concise but comprehensive
- Use dropdowns for structured data
- Make critical fields required
- Include help text and examples

### Workflows

- Pin action versions for security
- Use secrets for credentials
- Add timeout limits
- Fail fast for quick feedback

### CODEOWNERS

- More specific patterns at the bottom
- Use teams instead of individuals
- Require reviews for sensitive files
- Document ownership reasons

---

## Inheritance

Repositories in BlackRoad-OS without their own `.github` directory will inherit:

- Issue templates
- Pull request template
- Community health files (CODE_OF_CONDUCT, CONTRIBUTING, etc.)
- Funding configuration

Repositories can override by creating their own versions.

---

## Testing

### Test Issue Templates

1. Go to "New Issue" in this repository
2. Verify all templates appear
3. Test form validation
4. Check auto-triage workflow runs

### Test Workflows

1. Create a test branch
2. Make changes that trigger workflows
3. Check Actions tab for results
4. Verify notifications work

### Test CODEOWNERS

1. Create a test PR
2. Verify correct reviewers assigned
3. Check review requirements

---

## Maintenance

### Regular Tasks

- **Weekly** - Review Dependabot PRs
- **Monthly** - Update workflow versions
- **Quarterly** - Review CODEOWNERS accuracy
- **Yearly** - Audit all templates and docs

### Monitoring

Check these regularly:
- Failed workflow runs
- Unassigned issues (triage failures)
- Dependabot alerts
- Security advisories

---

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [About CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- [Dependabot Configuration](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file)
- [Issue Forms Syntax](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms)

---

## Questions?

See [SUPPORT.md](../SUPPORT.md) for help options.

---

*This directory is the automation heart of BlackRoad.*

📡 **Signal:** `.github → automation : configured`
