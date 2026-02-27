# ✅ MERGE VERIFICATION CHECKLIST (TEMPLATE)

## How to use this document

Use this checklist to manually verify that a pull request is ready to be merged.  
This file is a reusable **template** and **does not, by itself, confirm that any PR has been approved or that checks have passed**.  
Copy this checklist into the PR description or a comment and tick items only after you have verified them.

---

## ✅ Quality Checks (to be verified per PR)

### Code Quality
- [ ] No whitespace errors detected
- [ ] No TODO/FIXME markers in code
- [ ] All files properly formatted
- [ ] Consistent style throughout

### Documentation Quality
- [ ] All required documentation pages created and complete
- [ ] Content is professional and clear
- [ ] No incomplete sections
- [ ] All internal links properly formatted
- [ ] Diagrams included where helpful
- [ ] Code examples provided where appropriate

### Content Coverage
- [ ] Home/landing page updated
- [ ] Getting Started / onboarding guide present
- [ ] Navigation sidebar and structure verified
- [ ] Architecture documentation in place
- [ ] Organization / domain pages cover required scope
- [ ] Integration guides for all supported integrations
- [ ] Publishing / deployment documentation available

### Git Status
- [ ] Working tree clean
- [ ] All intended changes committed
- [ ] All commits pushed to remote
- [ ] No merge conflicts
- [ ] Branch up to date with target branch

### File Structure
- [ ] Documentation directory organized (e.g., `wiki/` or `docs/`)
- [ ] Subdirectories created as needed (e.g., Architecture, Orgs, Integrations)
- [ ] Entry-point README present in documentation directory
- [ ] Publishing / deployment guide present
- [ ] Completion / overview summary available

---

## 🚀 Pre-Merge Summary (to be filled in per PR)

Fill this section out in the context of a specific pull request.

- [ ] All required quality checks above are completed
- [ ] All required automated CI checks have passed
- [ ] Changes have been reviewed by at least one maintainer
- [ ] Breaking changes (if any) are documented and communicated
- [ ] Release notes / changelog updated (if applicable)

**Final decision for this PR:**  
- [ ] Ready to merge  
- [ ] Needs changes  
- [ ] Blocked (describe blockers in the PR)

---

## 📋 Post-Merge Actions (optional checklist)

After merging, consider the following actions:

1. **Publish / Deploy Documentation**
   - [ ] Follow instructions in the relevant publishing guide (e.g., `WIKI_PUBLISHING.md`)
   - [ ] Verify all pages render correctly in the target environment
   - [ ] Confirm navigation and internal links work as expected

2. **Announce Changes**
   - [ ] Share documentation link with the team or stakeholders
   - [ ] Update main `README` to link to documentation (if needed)
   - [ ] Update any relevant dashboards, portals, or organizational profiles

3. **Maintain Documentation**
   - [ ] Keep documentation directory in sync with the live docs/wiki
   - [ ] Update pages as systems or organizations evolve
   - [ ] Add or revise integration guides as new integrations are added

---

## ✨ Template Metadata

This is a static template and should not be treated as proof that any particular PR has been reviewed, approved, or merged.  
For each PR, copy this checklist and complete it in that PR’s context.

_Last updated: ___________________  
Updated by: _______________________
