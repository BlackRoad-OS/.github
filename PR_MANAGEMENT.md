# Pull Request Management

> **Automated PR handling system for the BlackRoad .github repository**

---

## Overview

The BlackRoad PR Handler provides automated triage, labeling, and management of pull requests across the organization. It helps maintainers quickly assess and process incoming PRs with intelligent categorization and status tracking.

---

## Current Open PRs

### High Priority

#### PR #7: Update MEMORY.md
- **Status**: Ready for review (not draft)
- **Type**: Documentation update
- **Summary**: Marks completed roadmap items through dispatcher
- **Changes**: 1101 additions, 5 deletions, 6 files
- **Action Needed**: Final review and merge

#### PR #12: Add CLAUDE.md
- **Status**: Draft
- **Type**: Documentation
- **Summary**: AI assistant guide for BlackRoad Bridge
- **Changes**: 340 additions, 1 file
- **Action Needed**: Finalize and mark ready for review

### Infrastructure & Testing

#### PR #2: Infrastructure Setup
- **Status**: Ready for review (not draft)
- **Type**: Infrastructure
- **Summary**: Testing, CI/CD, auto-merge, Claude Code API integration
- **Changes**: 7267 additions, 21 deletions, 38 files
- **Scope**: Comprehensive testing framework (97 tests, 73% coverage)
- **Action Needed**: Review and merge - foundational infrastructure

### Feature Development

#### PR #3: Wiki Documentation
- **Status**: Draft
- **Type**: Documentation
- **Summary**: Comprehensive Wiki documentation structure (27 pages, 3,522 lines)
- **Changes**: 3853 additions, 30 files
- **Action Needed**: Review wiki structure and publishing plan

#### PR #4: AI Agent Codespace
- **Status**: Ready for review (not draft)
- **Type**: AI Feature
- **Summary**: Collaborative AI agent codespace with open source models
- **Changes**: 3771 additions, 1 deletion, 23 files
- **Action Needed**: Test agent collaboration features

#### PR #5: Org Sync System
- **Status**: Ready for review (not draft) [WIP in title]
- **Type**: Infrastructure
- **Summary**: Updates pushing to other orgs and repos
- **Changes**: 1216 additions, 2 deletions, 8 files
- **Action Needed**: Complete security scan

#### PR #6: Collaboration & Memory
- **Status**: Ready for review (not draft) [WIP in title]
- **Type**: Core Feature
- **Summary**: Collaboration and memory functions for sessions
- **Changes**: 3665 additions, 15 files
- **Action Needed**: Update main Bridge documentation

### Current PR (This One)

#### PR #18: Handle Incoming PRs
- **Status**: Work in Progress
- **Type**: Workflow/Automation
- **Summary**: PR handling workflow and management system
- **Action Needed**: Complete implementation

---

## PR Handling Workflow

### Automatic Processing

When a PR is opened or updated, the PR Handler workflow automatically:

1. **Analyzes** the PR
   - Detects WIP status
   - Categorizes type (workflow, documentation, testing, infrastructure, ai-feature, core-feature)
   - Identifies org scope
   - Checks merge readiness

2. **Labels** the PR
   - Type labels (workflows, documentation, testing, etc.)
   - Status labels (work-in-progress, ready-for-review)
   - Org scope labels (org:os, org:ai, multi-org, etc.)

3. **Comments** on the PR
   - Analysis summary
   - Next steps checklist
   - Type-specific guidance
   - Merge readiness status

4. **Requests Reviews**
   - Assigns appropriate reviewers
   - Notifies maintainers

5. **Tracks Status**
   - Monitors CI checks
   - Updates merge readiness
   - Provides status summary

### PR Types and Handling

#### 🔧 Workflow PRs
- **Security Focus**: Extra scrutiny for permissions and secrets
- **Testing**: Validate YAML syntax and workflow logic
- **Deployment**: Test in safe environment first

#### 📚 Documentation PRs
- **Content Review**: Check accuracy and completeness
- **Links**: Verify all links work
- **Style**: Ensure consistent formatting

#### 🧪 Testing PRs
- **Coverage**: Verify adequate test coverage
- **Quality**: Check test quality and assertions
- **Integration**: Ensure tests work in CI

#### 🏗️ Infrastructure PRs
- **Production Ready**: Review for production deployment
- **Dependencies**: Check for security vulnerabilities
- **Backwards Compat**: Ensure no breaking changes

#### 🤖 AI Feature PRs
- **Testing**: Test with various scenarios
- **Performance**: Check resource usage
- **Integration**: Verify works with existing AI systems

#### ⭐ Core Feature PRs
- **Comprehensive Review**: Requires thorough examination
- **Testing**: Extensive test coverage needed
- **Documentation**: Must update docs

---

## PR Review Checklist

For reviewers, use this checklist when reviewing PRs:

### All PRs
- [ ] Code quality meets standards
- [ ] Changes are focused and minimal
- [ ] No unintended changes included
- [ ] Commit messages are clear
- [ ] CI checks pass

### Code Changes
- [ ] Tests added/updated
- [ ] No security vulnerabilities
- [ ] Error handling is appropriate
- [ ] Logging is adequate
- [ ] Performance impact is acceptable

### Documentation Changes
- [ ] Information is accurate
- [ ] Examples work as shown
- [ ] Links are valid
- [ ] Formatting is consistent

### Workflow Changes
- [ ] Permissions are minimal
- [ ] Secrets are properly referenced
- [ ] Triggers are appropriate
- [ ] Error handling is robust

---

## Merging Strategy

### Auto-Merge Eligible
PRs from `copilot/**` branches can auto-merge when:
- Not marked as draft or WIP
- All CI checks pass
- No merge conflicts
- At least one approval (if required)

### Manual Merge Required
- PRs modifying workflow files
- PRs from external contributors
- Breaking changes
- Major feature additions

### Merge Methods
- **Squash Merge**: Default for feature branches (preserves clean history)
- **Rebase Merge**: For linear history preservation
- **Merge Commit**: For keeping all commits (rarely used)

---

## Labels

### Type Labels
- `workflows` - GitHub Actions workflows
- `documentation` - Documentation changes
- `testing` - Test additions/changes
- `infrastructure` - Infrastructure setup
- `ai-enhancement` - AI/ML features
- `enhancement` - Core feature additions
- `bug` - Bug fixes
- `dependencies` - Dependency updates
- `security` - Security fixes

### Status Labels
- `work-in-progress` - Still being worked on
- `ready-for-review` - Ready for maintainer review
- `needs-changes` - Changes requested
- `approved` - Approved for merge
- `blocked` - Blocked by something

### Priority Labels
- `priority-high` - Needs immediate attention
- `priority-medium` - Normal priority
- `priority-low` - Can wait

### Org Scope Labels
- `org:os` - BlackRoad-OS
- `org:ai` - BlackRoad-AI
- `org:cloud` - BlackRoad-Cloud
- `multi-org` - Affects multiple orgs
- `all-orgs` - Affects all organizations

---

## Commands

### PR Management Script

Use the PR management script for quick PR operations:

```bash
# List all open PRs
./scripts/pr_manager.py list

# Show PR statistics
./scripts/pr_manager.py status

# Show details for a specific PR
./scripts/pr_manager.py show <number>

# Add a label to a PR
./scripts/pr_manager.py label <number> <label>

# Request review for a PR
./scripts/pr_manager.py review <number>

# Merge a PR (when ready)
./scripts/pr_manager.py merge <number>
```

### PR Comment Commands (Future)

Maintainers can use these commands in PR comments:

- `/merge` - Merge the PR (if eligible)
- `/rebase` - Rebase the PR
- `/label <label>` - Add a label
- `/assign @user` - Assign to user
- `/review` - Request review
- `/wip` - Mark as work in progress
- `/ready` - Mark as ready for review

---

## Metrics

Track PR handling efficiency:

- **Average Time to Review**: Target < 24 hours
- **Average Time to Merge**: Target < 48 hours for ready PRs
- **PR Backlog**: Current open PRs
- **Auto-Merge Rate**: Percentage of PRs auto-merged
- **Review Coverage**: Percentage of PRs reviewed

---

## Best Practices

### For PR Authors

1. **Clear Title**: Use descriptive, action-oriented titles
2. **Detailed Description**: Explain what, why, and how
3. **Small PRs**: Keep changes focused and minimal
4. **Tests**: Add tests for new functionality
5. **Documentation**: Update docs with code changes
6. **Draft First**: Use draft PRs for work in progress
7. **Link Issues**: Reference related issues

### For Reviewers

1. **Timely Reviews**: Review within 24 hours
2. **Constructive Feedback**: Be specific and helpful
3. **Test Locally**: Run and test the changes
4. **Check CI**: Ensure all checks pass
5. **Security**: Look for security issues
6. **Approve or Request Changes**: Don't leave pending

---

## Automation

### Workflows

1. **PR Handler** (`pr-handler.yml`)
   - Automatic PR analysis and labeling
   - Comment generation
   - Reviewer assignment
   - Status tracking

2. **PR Review** (`pr-review.yml`)
   - Code quality checks
   - Security scanning
   - Test validation

3. **Auto-Merge** (part of PR Handler)
   - Automatic merging for eligible PRs
   - Status check verification
   - Conflict detection

### Integrations

- **GitHub Actions**: Workflow automation
- **Codecov**: Test coverage tracking
- **Dependabot**: Dependency updates
- **CodeQL**: Security scanning

---

## Troubleshooting

### PR Won't Merge
- Check for merge conflicts
- Verify CI checks pass
- Ensure not marked as draft
- Check branch protection rules

### Labels Not Applied
- Check PR Handler workflow logs
- Verify permissions are correct
- Ensure labels exist in repository

### Reviewer Not Assigned
- Check if reviewer is valid collaborator
- Verify PR Handler workflow ran
- Check workflow permissions

---

## Future Enhancements

- [ ] Automatic PR prioritization
- [ ] Smart reviewer assignment based on file changes
- [ ] PR dependency tracking
- [ ] Integration with project boards
- [ ] Slack/Discord notifications
- [ ] PR analytics dashboard
- [ ] Automatic changelog generation
- [ ] Release note automation

---

*Part of the BlackRoad Autonomy System - Making PR management effortless*
