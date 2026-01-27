# Google Drive Sync

> **Docs, sheets, files. Your knowledge base in the cloud.**

```
Org: BlackRoad-Archive (ARC)
Node: aria (agents)
Storage: Unlimited (Workspace)
```

---

## What It Does

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Google    │  ←───→  │  BlackRoad  │  ←───→  │    Local    │
│    Drive    │   API   │    Sync     │         │   Storage   │
└─────────────┘         └─────────────┘         └─────────────┘
                              │
                        ┌─────┴─────┐
                        │  Index &  │
                        │  Search   │
                        └───────────┘
```

1. **Sync** - Mirror folders locally
2. **Index** - Full-text search
3. **Watch** - Real-time change notifications
4. **Export** - Convert Google Docs to markdown
5. **Backup** - Archive important files

---

## Quick Start

```bash
# Install
pip install -r requirements.txt

# Authenticate (opens browser)
python -m gdrive_sync.cli auth

# List files
python -m gdrive_sync.cli ls

# Sync a folder
python -m gdrive_sync.cli sync --folder "BlackRoad Docs" --local ./docs

# Watch for changes
python -m gdrive_sync.cli watch
```

---

## Folder Structure

```
Google Drive/
├── BlackRoad/
│   ├── 📁 Architecture/
│   │   ├── 📄 System Design.gdoc
│   │   ├── 📄 API Spec.gdoc
│   │   └── 📊 Metrics Dashboard.gsheet
│   ├── 📁 Business/
│   │   ├── 📄 Pitch Deck.gslides
│   │   ├── 📊 Financial Model.gsheet
│   │   └── 📄 Contracts/
│   ├── 📁 Engineering/
│   │   ├── 📄 Runbooks/
│   │   ├── 📄 Postmortems/
│   │   └── 📄 RFCs/
│   └── 📁 Media/
│       ├── 🖼️ Logos/
│       ├── 🖼️ Screenshots/
│       └── 🎥 Videos/
```

---

## Data Models

### File
```python
@dataclass
class DriveFile:
    id: str                     # Google file ID
    name: str
    mime_type: str              # application/vnd.google-apps.document
    parents: List[str]          # Parent folder IDs
    size: Optional[int]         # bytes (not for Google Docs)
    created_time: datetime
    modified_time: datetime
    web_view_link: str
    owners: List[str]
    shared: bool

    @property
    def is_google_doc(self) -> bool:
        return self.mime_type.startswith("application/vnd.google-apps")

    @property
    def extension(self) -> str:
        MIME_TO_EXT = {
            "application/vnd.google-apps.document": ".gdoc",
            "application/vnd.google-apps.spreadsheet": ".gsheet",
            "application/vnd.google-apps.presentation": ".gslides",
            "application/vnd.google-apps.folder": "",
        }
        return MIME_TO_EXT.get(self.mime_type, "")
```

### Folder
```python
@dataclass
class DriveFolder:
    id: str
    name: str
    path: str                   # /BlackRoad/Architecture
    parent_id: Optional[str]
    children: List[DriveFile]
```

### Change
```python
@dataclass
class DriveChange:
    file_id: str
    file: Optional[DriveFile]   # None if deleted
    removed: bool
    time: datetime
    change_type: str            # created, modified, deleted, moved
```

---

## Export Formats

| Google Type | Export As |
|-------------|-----------|
| Document | Markdown, DOCX, PDF, HTML |
| Spreadsheet | CSV, XLSX, JSON |
| Presentation | PDF, PPTX |
| Drawing | PNG, SVG, PDF |

```python
# Export Google Doc as Markdown
content = client.export(file_id, mime_type="text/markdown")

# Export Sheet as JSON
data = client.export(file_id, mime_type="application/json")
```

---

## API Usage

```python
from gdrive_sync import DriveClient, DriveFile

client = DriveClient()

# List files
files = client.list_files(
    folder_id="root",
    query="name contains 'BlackRoad'"
)

for f in files:
    print(f"{f.name} ({f.mime_type})")

# Get file metadata
file = client.get_file("file_id")

# Download file
content = client.download(file.id)
with open(file.name, "wb") as f:
    f.write(content)

# Export Google Doc as Markdown
md_content = client.export(file.id, "text/markdown")

# Upload file
new_file = client.upload(
    name="report.pdf",
    content=pdf_bytes,
    folder_id="folder_id",
    mime_type="application/pdf"
)

# Create folder
folder = client.create_folder(
    name="New Project",
    parent_id="parent_folder_id"
)

# Watch for changes
for change in client.watch(folder_id="xxx"):
    print(f"{change.change_type}: {change.file.name}")
    # Signal to OS
    emit_signal(f"📁 ARC → OS : file_{change.change_type}")
```

---

## Sync Engine

```python
from gdrive_sync import SyncEngine

sync = SyncEngine(
    remote_folder="BlackRoad Docs",
    local_path="./docs",
    export_format="markdown"  # Convert gdocs to md
)

# Initial sync
sync.pull()  # Download all files

# Push local changes
sync.push()  # Upload modified files

# Bidirectional sync
sync.sync()  # Both directions

# Watch and auto-sync
sync.watch(interval=60)  # Check every 60s
```

---

## CLI Commands

```bash
# Authenticate
gdrive auth

# List files
gdrive ls
gdrive ls --folder "BlackRoad"
gdrive ls --query "modifiedTime > '2024-01-01'"

# Download
gdrive download FILE_ID
gdrive download FILE_ID --format markdown

# Upload
gdrive upload ./file.pdf --folder "Reports"

# Sync folder
gdrive sync --remote "BlackRoad Docs" --local ./docs

# Watch for changes
gdrive watch --folder "BlackRoad"

# Search
gdrive search "architecture diagram"

# Export all docs as markdown
gdrive export --folder "Docs" --format markdown --output ./markdown/
```

---

## Directory Structure

```
gdrive-sync/
├── gdrive_sync/
│   ├── __init__.py
│   ├── models/
│   │   ├── file.py
│   │   ├── folder.py
│   │   └── change.py
│   ├── client.py         ← Google API wrapper
│   ├── sync.py           ← Sync engine
│   ├── export.py         ← Format converters
│   ├── watch.py          ← Change detection
│   ├── index.py          ← Local search index
│   └── cli.py
├── config.yaml
├── credentials.json      ← OAuth credentials
└── requirements.txt
```

---

## Signals

```
📁 ARC → OS : file_created, name="Design Doc.gdoc", folder="/Architecture"
📝 ARC → OS : file_modified, name="API Spec.gdoc", editor="alexa@blackroad.ai"
🗑️ ARC → OS : file_deleted, name="old-draft.docx"
📤 ARC → OS : file_shared, name="Pitch Deck", with="investor@vc.com"
🔄 ARC → OS : sync_complete, files=156, changed=12
```

---

## Integration with BlackRoad

```python
# Auto-sync architecture docs to .github
sync = SyncEngine(
    remote_folder="BlackRoad/Architecture",
    local_path="/path/to/.github/docs/",
    export_format="markdown",
    on_change=lambda f: emit_signal(f"📁 ARC → OS : doc_updated, {f.name}")
)

# Index all docs for AI context
from gdrive_sync import Indexer

indexer = Indexer()
indexer.index_folder("BlackRoad Docs")

# Search
results = indexer.search("operator routing logic")
for r in results:
    print(f"{r.file.name}: {r.snippet}")
```

---

*Your docs, everywhere.*
