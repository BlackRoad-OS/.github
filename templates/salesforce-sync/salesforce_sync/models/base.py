"""
Base Salesforce record model.

All SF objects inherit from SFRecord.
"""

from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any, List, ClassVar
from datetime import datetime
from enum import Enum
import json


class SFField:
    """Field descriptor for SF fields with metadata."""

    def __init__(
        self,
        sf_name: str,
        required: bool = False,
        readonly: bool = False,
        default: Any = None
    ):
        self.sf_name = sf_name
        self.required = required
        self.readonly = readonly
        self.default = default
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name, self.default)

    def __set__(self, obj, value):
        if self.readonly and self.name in obj.__dict__:
            raise AttributeError(f"{self.name} is readonly")
        obj.__dict__[self.name] = value


@dataclass
class SFRecord:
    """
    Base class for all Salesforce records.

    Provides common fields and serialization.
    """

    # Salesforce ID (18 char)
    id: Optional[str] = None

    # System fields (readonly)
    created_date: Optional[datetime] = None
    last_modified_date: Optional[datetime] = None
    created_by_id: Optional[str] = None
    last_modified_by_id: Optional[str] = None

    # Local tracking
    _synced_at: Optional[datetime] = field(default=None, repr=False)
    _is_dirty: bool = field(default=False, repr=False)
    _local_id: Optional[int] = field(default=None, repr=False)

    # Class-level config
    SF_OBJECT: ClassVar[str] = "SObject"
    SF_FIELDS: ClassVar[Dict[str, str]] = {}

    def __post_init__(self):
        """Mark as dirty if new."""
        if self.id is None:
            self._is_dirty = True

    @property
    def is_new(self) -> bool:
        """Check if record is new (not yet in SF)."""
        return self.id is None

    @property
    def is_dirty(self) -> bool:
        """Check if record has unsaved changes."""
        return self._is_dirty

    def mark_dirty(self):
        """Mark record as having changes."""
        self._is_dirty = True

    def mark_clean(self):
        """Mark record as synced."""
        self._is_dirty = False
        self._synced_at = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        data = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                if isinstance(value, datetime):
                    data[key] = value.isoformat()
                elif isinstance(value, Enum):
                    data[key] = value.value
                else:
                    data[key] = value
        return data

    def to_sf_dict(self) -> Dict[str, Any]:
        """Convert to Salesforce API format."""
        data = {}
        for local_name, sf_name in self.SF_FIELDS.items():
            value = getattr(self, local_name, None)
            if value is not None:
                if isinstance(value, datetime):
                    data[sf_name] = value.strftime("%Y-%m-%dT%H:%M:%S.000Z")
                elif isinstance(value, Enum):
                    data[sf_name] = value.value
                else:
                    data[sf_name] = value
        return data

    @classmethod
    def from_sf_dict(cls, data: Dict[str, Any]) -> "SFRecord":
        """Create from Salesforce API response."""
        kwargs = {}

        # Reverse mapping
        sf_to_local = {v: k for k, v in cls.SF_FIELDS.items()}

        for sf_name, value in data.items():
            local_name = sf_to_local.get(sf_name, sf_name.lower())
            if hasattr(cls, local_name) or local_name in ['id', 'created_date', 'last_modified_date']:
                # Parse dates
                if local_name.endswith('_date') and value:
                    try:
                        kwargs[local_name] = datetime.fromisoformat(value.replace('Z', '+00:00'))
                    except:
                        kwargs[local_name] = value
                else:
                    kwargs[local_name] = value

        record = cls(**kwargs)
        record._is_dirty = False
        record._synced_at = datetime.utcnow()
        return record

    def to_json(self) -> str:
        """Serialize to JSON."""
        return json.dumps(self.to_dict(), default=str)

    @classmethod
    def from_json(cls, json_str: str) -> "SFRecord":
        """Deserialize from JSON."""
        data = json.loads(json_str)
        return cls(**data)

    def __eq__(self, other):
        if not isinstance(other, SFRecord):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
