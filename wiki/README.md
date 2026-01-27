# BlackRoad Wiki Pages

This directory contains the source files for the BlackRoad Wiki.

## Structure

```
wiki/
├── Home.md                    ← Landing page
├── Getting-Started.md         ← Quick start guide
├── _Sidebar.md                ← Navigation menu
│
├── Architecture/
│   ├── Overview.md            ← The big picture
│   ├── Bridge.md              ← Central coordination
│   └── Operator.md            ← Routing engine
│
├── Orgs/
│   ├── BlackRoad-OS.md        ← 15 organization pages
│   ├── BlackRoad-AI.md
│   └── ...
│
└── Integrations/
    ├── Salesforce.md          ← Integration guides
    ├── Stripe.md
    └── ...
```

## Publishing to GitHub Wiki

GitHub Wikis are separate Git repositories. To publish these pages:

### Option 1: Manual Upload

1. Go to https://github.com/BlackRoad-OS/.github/wiki
2. Create each page via the web interface
3. Copy content from these files

### Option 2: Clone Wiki Repo

```bash
# Clone the wiki repo
git clone https://github.com/BlackRoad-OS/.github.wiki.git

# Copy files from this directory
cp -r wiki/* .github.wiki/

# Push to wiki
cd .github.wiki
git add .
git commit -m "Initialize wiki pages"
git push
```

## Navigation

The `_Sidebar.md` file creates the navigation menu visible on all wiki pages.

## Maintenance

- Keep pages in sync with main repository documentation
- Update organization pages as repos are created
- Add new integrations as they're implemented

---

*Documentation as code. Wiki as infrastructure.*
