"""
Account model - SF Account object.

Represents a company/organization.
"""

from dataclasses import dataclass
from typing import Optional, ClassVar, Dict
from .base import SFRecord


@dataclass
class Account(SFRecord):
    """
    Salesforce Account record.

    Example:
        account = Account(
            name="Acme Corporation",
            industry="Technology",
            annual_revenue=1000000,
            type="Customer"
        )
    """

    # Basic info
    name: Optional[str] = None
    type: Optional[str] = None  # Prospect, Customer, Partner, etc.
    industry: Optional[str] = None
    description: Optional[str] = None

    # Size
    annual_revenue: Optional[float] = None
    number_of_employees: Optional[int] = None

    # Contact
    phone: Optional[str] = None
    fax: Optional[str] = None
    website: Optional[str] = None

    # Billing Address
    billing_street: Optional[str] = None
    billing_city: Optional[str] = None
    billing_state: Optional[str] = None
    billing_postal_code: Optional[str] = None
    billing_country: Optional[str] = None

    # Shipping Address
    shipping_street: Optional[str] = None
    shipping_city: Optional[str] = None
    shipping_state: Optional[str] = None
    shipping_postal_code: Optional[str] = None
    shipping_country: Optional[str] = None

    # Relationships
    parent_id: Optional[str] = None
    owner_id: Optional[str] = None

    # Other
    rating: Optional[str] = None  # Hot, Warm, Cold
    account_source: Optional[str] = None
    sic: Optional[str] = None  # Standard Industry Code
    ticker_symbol: Optional[str] = None

    # Class config
    SF_OBJECT: ClassVar[str] = "Account"
    SF_FIELDS: ClassVar[Dict[str, str]] = {
        "id": "Id",
        "name": "Name",
        "type": "Type",
        "industry": "Industry",
        "description": "Description",
        "annual_revenue": "AnnualRevenue",
        "number_of_employees": "NumberOfEmployees",
        "phone": "Phone",
        "fax": "Fax",
        "website": "Website",
        "billing_street": "BillingStreet",
        "billing_city": "BillingCity",
        "billing_state": "BillingState",
        "billing_postal_code": "BillingPostalCode",
        "billing_country": "BillingCountry",
        "shipping_street": "ShippingStreet",
        "shipping_city": "ShippingCity",
        "shipping_state": "ShippingState",
        "shipping_postal_code": "ShippingPostalCode",
        "shipping_country": "ShippingCountry",
        "parent_id": "ParentId",
        "owner_id": "OwnerId",
        "rating": "Rating",
        "account_source": "AccountSource",
        "sic": "Sic",
        "ticker_symbol": "TickerSymbol",
        "created_date": "CreatedDate",
        "last_modified_date": "LastModifiedDate",
    }

    @property
    def is_customer(self) -> bool:
        """Check if account is a customer."""
        return self.type == "Customer"

    @property
    def revenue_tier(self) -> str:
        """Get revenue tier."""
        if not self.annual_revenue:
            return "Unknown"
        if self.annual_revenue >= 10_000_000:
            return "Enterprise"
        if self.annual_revenue >= 1_000_000:
            return "Mid-Market"
        if self.annual_revenue >= 100_000:
            return "SMB"
        return "Startup"

    def __str__(self) -> str:
        return f"Account({self.name})"

    def __repr__(self) -> str:
        return f"Account(id={self.id!r}, name={self.name!r}, type={self.type!r})"
