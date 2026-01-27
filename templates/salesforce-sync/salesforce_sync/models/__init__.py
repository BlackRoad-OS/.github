"""Salesforce data models."""

from .base import SFRecord, SFField
from .contact import Contact
from .lead import Lead
from .account import Account
from .opportunity import Opportunity

__all__ = [
    "SFRecord",
    "SFField",
    "Contact",
    "Lead",
    "Account",
    "Opportunity"
]
