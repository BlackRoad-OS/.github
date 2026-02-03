# Wiki Publishing Guide

## What We Built

Created a comprehensive Wiki structure with **27 pages**:

### Core Pages (3)
- `Home.md` - Landing page and navigation hub
- `Getting-Started.md` - Quick start guide for new users
- `_Sidebar.md` - Navigation menu (appears on all pages)

### Architecture (3)
- `Architecture/Overview.md` - The big picture of BlackRoad
- `Architecture/Bridge.md` - Central coordination details
- `Architecture/Operator.md` - Routing engine deep dive

### Organizations (15)
Complete pages for all 15 BlackRoad organizations:
- BlackRoad-OS (The Bridge)
- BlackRoad-AI (AI routing)
- BlackRoad-Cloud (Edge compute)
- BlackRoad-Hardware (Pi cluster)
- BlackRoad-Security (Auth & secrets)
- BlackRoad-Labs (R&D)
- BlackRoad-Foundation (CRM & billing)
- BlackRoad-Media (Content)
- BlackRoad-Studio (Design)
- BlackRoad-Interactive (Metaverse)
- BlackRoad-Education (Learning)
- BlackRoad-Gov (Governance)
- BlackRoad-Archive (Storage)
- BlackRoad-Ventures (Marketplace)
- Blackbox-Enterprises (Stealth)

### Integrations (5)
- Salesforce (CRM)
- Stripe (Billing)
- Cloudflare (Edge compute)
- Google Drive (Document sync)
- GitHub (Code & CI/CD)

---

## How to Publish

### Option 1: Manual (via GitHub Web UI)

1. Go to https://github.com/BlackRoad-OS/.github/wiki
2. Click "New Page" for each file
3. Copy the filename (without .md) as the page title
4. Copy the file content as the page body
5. Click "Save Page"

**Order to create pages:**
1. Home (must be first)
2. _Sidebar (enables navigation)
3. Getting-Started
4. Architecture pages (Overview, Bridge, Operator)
5. Organization pages (all 15)
6. Integration pages (all 5)

### Option 2: Git Clone (Recommended)

```bash
# Clone the wiki repository
git clone https://github.com/BlackRoad-OS/.github.wiki.git

# Copy all wiki files
cd /path/to/BlackRoad-OS/.github
cp -r wiki/* /path/to/.github.wiki/

# Push to wiki
cd /path/to/.github.wiki
git add .
git commit -m "Initialize BlackRoad Wiki with 27 pages"
git push origin master
```

### Option 3: Script

```bash
#!/bin/bash
# publish-wiki.sh

# Clone wiki repo
git clone https://github.com/BlackRoad-OS/.github.wiki.git /tmp/wiki

# Copy files
cp -r wiki/* /tmp/wiki/

# Commit and push
cd /tmp/wiki
git add .
git commit -m "Update wiki from main repository"
git push origin master

# Cleanup
rm -rf /tmp/wiki

echo "✔️ Wiki published successfully!"
```

---

## Verification

After publishing, verify:

1. **Home page loads**: https://github.com/BlackRoad-OS/.github/wiki
2. **Sidebar navigation works**: All links functional
3. **All 27 pages accessible**: No broken links
4. **Images/diagrams render**: ASCII art displays correctly

---

## Maintenance

To update the wiki in the future:

```bash
# 1. Make changes in wiki/ directory in main repo
vim wiki/Home.md

# 2. Commit to main repo
git add wiki/
git commit -m "Update wiki: ..."
git push

# 3. Sync to wiki repo (manual or via script)
git clone https://github.com/BlackRoad-OS/.github.wiki.git
cp -r wiki/* .github.wiki/
cd .github.wiki && git add . && git commit -m "Sync from main" && git push
```

**Pro Tip**: Set up a GitHub Action to auto-sync wiki/ directory changes to the wiki repository.

---

## Features of This Wiki

✅ **Complete Coverage**: All 15 organizations documented  
✅ **Architecture Docs**: Deep dives into Bridge and Operator  
✅ **Integration Guides**: Salesforce, Stripe, Cloudflare, etc.  
✅ **Navigation**: Sidebar for easy browsing  
✅ **Getting Started**: Quick onboarding guide  
✅ **Consistent Style**: Uniform formatting across all pages  
✅ **ASCII Diagrams**: Visual architecture representations  
✅ **Code Examples**: Practical implementation snippets  
✅ **Cross-linking**: Internal links between related pages  

---

## Next Steps

1. **Publish the wiki** using one of the methods above
2. **Enable wiki** in repository settings (if not already enabled)
3. **Share the link**: https://github.com/BlackRoad-OS/.github/wiki
4. **Iterate**: Update as organizations and integrations evolve

---

*Documentation complete. Ready to publish. 📚*
