"""
Contact model - SF Contact object.

Represents a person associated with an Account.
"""

from dataclasses import dataclass
from typing import Optional, ClassVar, Dict
from .base import SFRecord


@dataclass
class Contact(SFRecord):
    """
    Salesforce Contact record.

    Example:
        contact = Contact(
            first_name="Jane",
            last_name="Doe",
            email="jane@example.com",
            account_id="001..."
        )
    """

    # Name fields
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    salutation: Optional[str] = None  # Mr., Ms., Dr., etc.

    # Contact info
    email: Optional[str] = None
    phone: Optional[str] = None
    mobile_phone: Optional[str] = None
    fax: Optional[str] = None

    # Address
    mailing_street: Optional[str] = None
    mailing_city: Optional[str] = None
    mailing_state: Optional[str] = None
    mailing_postal_code: Optional[str] = None
    mailing_country: Optional[str] = None

    # Relationships
    account_id: Optional[str] = None
    reports_to_id: Optional[str] = None
    owner_id: Optional[str] = None

    # Other
    title: Optional[str] = None
    department: Optional[str] = None
    description: Optional[str] = None
    lead_source: Optional[str] = None

    # Class config
    SF_OBJECT: ClassVar[str] = "Contact"
    SF_FIELDS: ClassVar[Dict[str, str]] = {
        "id": "Id",
        "first_name": "FirstName",
        "last_name": "LastName",
        "salutation": "Salutation",
        "email": "Email",
        "phone": "Phone",
        "mobile_phone": "MobilePhone",
        "fax": "Fax",
        "mailing_street": "MailingStreet",
        "mailing_city": "MailingCity",
        "mailing_state": "MailingState",
        "mailing_postal_code": "MailingPostalCode",
        "mailing_country": "MailingCountry",
        "account_id": "AccountId",
        "reports_to_id": "ReportsToId",
        "owner_id": "OwnerId",
        "title": "Title",
        "department": "Department",
        "description": "Description",
        "lead_source": "LeadSource",
        "created_date": "CreatedDate",
        "last_modified_date": "LastModifiedDate",
    }

    @property
    def full_name(self) -> str:
        """Get full name."""
        parts = []
        if self.salutation:
            parts.append(self.salutation)
        if self.first_name:
            parts.append(self.first_name)
        if self.last_name:
            parts.append(self.last_name)
        return " ".join(parts)

    @property
    def mailing_address(self) -> str:
        """Get formatted mailing address."""
        parts = []
        if self.mailing_street:
            parts.append(self.mailing_street)
        city_state = []
        if self.mailing_city:
            city_state.append(self.mailing_city)
        if self.mailing_state:
            city_state.append(self.mailing_state)
        if city_state:
            line = ", ".join(city_state)
            if self.mailing_postal_code:
                line += f" {self.mailing_postal_code}"
            parts.append(line)
        if self.mailing_country:
            parts.append(self.mailing_country)
        return "\n".join(parts)

    def __str__(self) -> str:
        return f"Contact({self.full_name} <{self.email}>)"

    def __repr__(self) -> str:
        return f"Contact(id={self.id!r}, name={self.full_name!r}, email={self.email!r})"
