"""
Lead model - SF Lead object.

Represents a potential customer/prospect.
"""

from dataclasses import dataclass
from typing import Optional, ClassVar, Dict
from enum import Enum
from .base import SFRecord


class LeadStatus(Enum):
    """Standard lead statuses."""
    OPEN = "Open - Not Contacted"
    WORKING = "Working - Contacted"
    CLOSED_CONVERTED = "Closed - Converted"
    CLOSED_NOT_CONVERTED = "Closed - Not Converted"


class LeadSource(Enum):
    """Lead sources."""
    WEB = "Web"
    PHONE = "Phone Inquiry"
    PARTNER = "Partner Referral"
    PURCHASED_LIST = "Purchased List"
    OTHER = "Other"


@dataclass
class Lead(SFRecord):
    """
    Salesforce Lead record.

    Example:
        lead = Lead(
            first_name="John",
            last_name="Smith",
            company="Acme Corp",
            email="john@acme.com",
            status=LeadStatus.OPEN
        )
    """

    # Name
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    salutation: Optional[str] = None

    # Company
    company: Optional[str] = None
    title: Optional[str] = None
    industry: Optional[str] = None
    annual_revenue: Optional[float] = None
    number_of_employees: Optional[int] = None

    # Contact
    email: Optional[str] = None
    phone: Optional[str] = None
    mobile_phone: Optional[str] = None
    website: Optional[str] = None

    # Address
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None

    # Status
    status: Optional[str] = None
    rating: Optional[str] = None  # Hot, Warm, Cold
    lead_source: Optional[str] = None

    # Relationships
    owner_id: Optional[str] = None
    converted_account_id: Optional[str] = None
    converted_contact_id: Optional[str] = None
    converted_opportunity_id: Optional[str] = None
    is_converted: bool = False

    # Other
    description: Optional[str] = None

    # Class config
    SF_OBJECT: ClassVar[str] = "Lead"
    SF_FIELDS: ClassVar[Dict[str, str]] = {
        "id": "Id",
        "first_name": "FirstName",
        "last_name": "LastName",
        "salutation": "Salutation",
        "company": "Company",
        "title": "Title",
        "industry": "Industry",
        "annual_revenue": "AnnualRevenue",
        "number_of_employees": "NumberOfEmployees",
        "email": "Email",
        "phone": "Phone",
        "mobile_phone": "MobilePhone",
        "website": "Website",
        "street": "Street",
        "city": "City",
        "state": "State",
        "postal_code": "PostalCode",
        "country": "Country",
        "status": "Status",
        "rating": "Rating",
        "lead_source": "LeadSource",
        "owner_id": "OwnerId",
        "converted_account_id": "ConvertedAccountId",
        "converted_contact_id": "ConvertedContactId",
        "converted_opportunity_id": "ConvertedOpportunityId",
        "is_converted": "IsConverted",
        "description": "Description",
        "created_date": "CreatedDate",
        "last_modified_date": "LastModifiedDate",
    }

    @property
    def full_name(self) -> str:
        """Get full name."""
        parts = []
        if self.first_name:
            parts.append(self.first_name)
        if self.last_name:
            parts.append(self.last_name)
        return " ".join(parts) or "Unknown"

    @property
    def is_hot(self) -> bool:
        """Check if lead is hot."""
        return self.rating == "Hot"

    def __str__(self) -> str:
        return f"Lead({self.full_name} @ {self.company})"

    def __repr__(self) -> str:
        return f"Lead(id={self.id!r}, name={self.full_name!r}, company={self.company!r}, status={self.status!r})"
