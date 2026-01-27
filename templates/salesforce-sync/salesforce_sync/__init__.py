"""
Salesforce Sync - Local sync for Salesforce records.

Usage:
    from salesforce_sync import SFSync, Contact, Lead, Account, Opportunity

    sync = SFSync()
    contacts = sync.contacts.all()
"""

from .models import Contact, Lead, Account, Opportunity, SFRecord
from .sync.engine import SFSync
from .api.client import SalesforceClient

__version__ = "0.1.0"
__all__ = [
    "SFSync",
    "SalesforceClient",
    "Contact",
    "Lead",
    "Account",
    "Opportunity",
    "SFRecord"
]
