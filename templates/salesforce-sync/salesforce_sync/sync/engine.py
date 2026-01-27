"""
Sync Engine - Bidirectional sync between Salesforce and local storage.

The heart of the salesforce-sync system.
"""

import sqlite3
import json
from typing import Dict, List, Type, Optional, Any
from datetime import datetime
from pathlib import Path

from ..models import Contact, Lead, Account, Opportunity, SFRecord
from ..api.client import SalesforceClient


class ObjectSync:
    """
    Sync handler for a single object type.

    Provides CRUD operations that sync with both local DB and Salesforce.
    """

    def __init__(
        self,
        model: Type[SFRecord],
        client: SalesforceClient,
        db: sqlite3.Connection
    ):
        self.model = model
        self.client = client
        self.db = db
        self._ensure_table()

    @property
    def table_name(self) -> str:
        return self.model.SF_OBJECT.lower()

    def _ensure_table(self):
        """Create table if not exists."""
        cursor = self.db.cursor()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                local_id INTEGER PRIMARY KEY AUTOINCREMENT,
                sf_id TEXT UNIQUE,
                data JSON NOT NULL,
                synced_at TIMESTAMP,
                is_dirty BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute(f"""
            CREATE INDEX IF NOT EXISTS idx_{self.table_name}_sf_id
            ON {self.table_name}(sf_id)
        """)
        self.db.commit()

    def all(self, limit: int = 1000) -> List[SFRecord]:
        """Get all records from local cache."""
        cursor = self.db.cursor()
        cursor.execute(
            f"SELECT data FROM {self.table_name} LIMIT ?",
            (limit,)
        )
        records = []
        for row in cursor.fetchall():
            data = json.loads(row[0])
            records.append(self.model.from_sf_dict(data))
        return records

    def get(self, sf_id: str) -> Optional[SFRecord]:
        """Get a single record by Salesforce ID."""
        cursor = self.db.cursor()
        cursor.execute(
            f"SELECT data FROM {self.table_name} WHERE sf_id = ?",
            (sf_id,)
        )
        row = cursor.fetchone()
        if row:
            data = json.loads(row[0])
            return self.model.from_sf_dict(data)
        return None

    def search(self, **kwargs) -> List[SFRecord]:
        """Search records by field values."""
        records = self.all()
        results = []
        for record in records:
            match = True
            for field, value in kwargs.items():
                record_value = getattr(record, field, None)
                if record_value is None:
                    match = False
                elif isinstance(value, str) and isinstance(record_value, str):
                    if value.lower() not in record_value.lower():
                        match = False
                elif record_value != value:
                    match = False
            if match:
                results.append(record)
        return results

    def create(self, record: SFRecord) -> SFRecord:
        """Create a new record (local + SF)."""
        # Create in Salesforce
        sf_data = record.to_sf_dict()
        sf_id = self.client.create(self.model.SF_OBJECT, sf_data)
        record.id = sf_id

        # Store locally
        self._save_local(record)
        record.mark_clean()

        return record

    def update(self, record: SFRecord) -> SFRecord:
        """Update a record (local + SF)."""
        if not record.id:
            raise ValueError("Cannot update record without SF ID")

        # Update in Salesforce
        sf_data = record.to_sf_dict()
        # Remove Id from update payload
        sf_data.pop("Id", None)
        self.client.update(self.model.SF_OBJECT, record.id, sf_data)

        # Update locally
        self._save_local(record)
        record.mark_clean()

        return record

    def delete(self, record: SFRecord) -> bool:
        """Delete a record (local + SF)."""
        if not record.id:
            raise ValueError("Cannot delete record without SF ID")

        # Delete from Salesforce
        self.client.delete(self.model.SF_OBJECT, record.id)

        # Delete locally
        cursor = self.db.cursor()
        cursor.execute(
            f"DELETE FROM {self.table_name} WHERE sf_id = ?",
            (record.id,)
        )
        self.db.commit()

        return True

    def sync_from_sf(self, since: Optional[datetime] = None) -> int:
        """
        Pull records from Salesforce.

        Args:
            since: Only sync records modified since this time

        Returns:
            Number of records synced
        """
        # Build query
        fields = list(self.model.SF_FIELDS.values())
        soql = f"SELECT {', '.join(fields)} FROM {self.model.SF_OBJECT}"

        if since:
            soql += f" WHERE LastModifiedDate > {since.isoformat()}Z"

        soql += " ORDER BY LastModifiedDate DESC LIMIT 2000"

        # Query Salesforce
        results = self.client.query_all(soql)

        # Save locally
        count = 0
        for sf_data in results:
            record = self.model.from_sf_dict(sf_data)
            self._save_local(record)
            count += 1

        return count

    def sync_to_sf(self) -> int:
        """
        Push dirty records to Salesforce.

        Returns:
            Number of records synced
        """
        cursor = self.db.cursor()
        cursor.execute(
            f"SELECT data FROM {self.table_name} WHERE is_dirty = 1"
        )

        count = 0
        for row in cursor.fetchall():
            data = json.loads(row[0])
            record = self.model.from_sf_dict(data)

            if record.id:
                self.update(record)
            else:
                self.create(record)

            count += 1

        return count

    def _save_local(self, record: SFRecord):
        """Save record to local database."""
        cursor = self.db.cursor()
        data = json.dumps(record.to_sf_dict())
        now = datetime.utcnow().isoformat()

        cursor.execute(f"""
            INSERT INTO {self.table_name} (sf_id, data, synced_at, is_dirty, updated_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(sf_id) DO UPDATE SET
                data = excluded.data,
                synced_at = excluded.synced_at,
                is_dirty = excluded.is_dirty,
                updated_at = excluded.updated_at
        """, (record.id, data, now, record.is_dirty, now))
        self.db.commit()

    def count(self) -> int:
        """Count local records."""
        cursor = self.db.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {self.table_name}")
        return cursor.fetchone()[0]


class SFSync:
    """
    Main sync engine.

    Provides access to all object syncs and orchestrates full syncs.

    Example:
        sync = SFSync()
        sync.connect()

        # Access objects
        contacts = sync.contacts.all()
        leads = sync.leads.search(company="Acme")

        # Full sync
        sync.sync_all()
    """

    def __init__(
        self,
        db_path: str = "./data/salesforce.db",
        **client_kwargs
    ):
        """
        Initialize sync engine.

        Args:
            db_path: Path to SQLite database
            **client_kwargs: Arguments passed to SalesforceClient
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self.db = sqlite3.connect(str(self.db_path))
        self.client = SalesforceClient(**client_kwargs)

        # Object syncs
        self._contacts: Optional[ObjectSync] = None
        self._leads: Optional[ObjectSync] = None
        self._accounts: Optional[ObjectSync] = None
        self._opportunities: Optional[ObjectSync] = None

        self._last_sync: Optional[datetime] = None

    def connect(self) -> bool:
        """Connect to Salesforce."""
        return self.client.connect()

    @property
    def contacts(self) -> ObjectSync:
        """Access Contact sync."""
        if self._contacts is None:
            self._contacts = ObjectSync(Contact, self.client, self.db)
        return self._contacts

    @property
    def leads(self) -> ObjectSync:
        """Access Lead sync."""
        if self._leads is None:
            self._leads = ObjectSync(Lead, self.client, self.db)
        return self._leads

    @property
    def accounts(self) -> ObjectSync:
        """Access Account sync."""
        if self._accounts is None:
            self._accounts = ObjectSync(Account, self.client, self.db)
        return self._accounts

    @property
    def opportunities(self) -> ObjectSync:
        """Access Opportunity sync."""
        if self._opportunities is None:
            self._opportunities = ObjectSync(Opportunity, self.client, self.db)
        return self._opportunities

    def sync_all(self, since: Optional[datetime] = None) -> Dict[str, int]:
        """
        Sync all object types.

        Returns dict of object -> count synced.
        """
        since = since or self._last_sync
        results = {}

        results["contacts"] = self.contacts.sync_from_sf(since)
        results["leads"] = self.leads.sync_from_sf(since)
        results["accounts"] = self.accounts.sync_from_sf(since)
        results["opportunities"] = self.opportunities.sync_from_sf(since)

        self._last_sync = datetime.utcnow()

        return results

    def push_all(self) -> Dict[str, int]:
        """Push all dirty records to Salesforce."""
        results = {}

        results["contacts"] = self.contacts.sync_to_sf()
        results["leads"] = self.leads.sync_to_sf()
        results["accounts"] = self.accounts.sync_to_sf()
        results["opportunities"] = self.opportunities.sync_to_sf()

        return results

    def stats(self) -> Dict[str, Any]:
        """Get sync statistics."""
        return {
            "contacts": self.contacts.count(),
            "leads": self.leads.count(),
            "accounts": self.accounts.count(),
            "opportunities": self.opportunities.count(),
            "last_sync": self._last_sync.isoformat() if self._last_sync else None,
            "api_calls": self.client.usage.calls_made,
            "api_remaining": self.client.usage.calls_remaining,
        }

    def close(self):
        """Close database connection."""
        self.db.close()
