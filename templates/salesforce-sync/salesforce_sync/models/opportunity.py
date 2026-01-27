"""
Opportunity model - SF Opportunity object.

Represents a potential deal/sale.
"""

from dataclasses import dataclass
from typing import Optional, ClassVar, Dict
from datetime import date
from enum import Enum
from .base import SFRecord


class OpportunityStage(Enum):
    """Standard opportunity stages."""
    PROSPECTING = "Prospecting"
    QUALIFICATION = "Qualification"
    NEEDS_ANALYSIS = "Needs Analysis"
    VALUE_PROPOSITION = "Value Proposition"
    ID_DECISION_MAKERS = "Id. Decision Makers"
    PERCEPTION_ANALYSIS = "Perception Analysis"
    PROPOSAL = "Proposal/Price Quote"
    NEGOTIATION = "Negotiation/Review"
    CLOSED_WON = "Closed Won"
    CLOSED_LOST = "Closed Lost"


@dataclass
class Opportunity(SFRecord):
    """
    Salesforce Opportunity record.

    Example:
        opp = Opportunity(
            name="Acme - 100 Widgets",
            account_id="001...",
            amount=50000,
            stage="Qualification",
            close_date=date(2026, 3, 15)
        )
    """

    # Basic info
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None  # New Business, Existing Business, etc.

    # Money
    amount: Optional[float] = None
    probability: Optional[int] = None  # 0-100
    expected_revenue: Optional[float] = None

    # Stage
    stage: Optional[str] = None
    forecast_category: Optional[str] = None

    # Dates
    close_date: Optional[date] = None
    next_step: Optional[str] = None

    # Relationships
    account_id: Optional[str] = None
    owner_id: Optional[str] = None
    contact_id: Optional[str] = None
    campaign_id: Optional[str] = None

    # Source
    lead_source: Optional[str] = None

    # Status
    is_closed: bool = False
    is_won: bool = False

    # Class config
    SF_OBJECT: ClassVar[str] = "Opportunity"
    SF_FIELDS: ClassVar[Dict[str, str]] = {
        "id": "Id",
        "name": "Name",
        "description": "Description",
        "type": "Type",
        "amount": "Amount",
        "probability": "Probability",
        "expected_revenue": "ExpectedRevenue",
        "stage": "StageName",
        "forecast_category": "ForecastCategory",
        "close_date": "CloseDate",
        "next_step": "NextStep",
        "account_id": "AccountId",
        "owner_id": "OwnerId",
        "contact_id": "ContactId",
        "campaign_id": "CampaignId",
        "lead_source": "LeadSource",
        "is_closed": "IsClosed",
        "is_won": "IsWon",
        "created_date": "CreatedDate",
        "last_modified_date": "LastModifiedDate",
    }

    @property
    def weighted_amount(self) -> float:
        """Get probability-weighted amount."""
        if not self.amount or not self.probability:
            return 0.0
        return self.amount * (self.probability / 100)

    @property
    def days_until_close(self) -> Optional[int]:
        """Get days until close date."""
        if not self.close_date:
            return None
        delta = self.close_date - date.today()
        return delta.days

    @property
    def is_late(self) -> bool:
        """Check if opportunity is past close date."""
        if not self.close_date:
            return False
        return self.close_date < date.today() and not self.is_closed

    @property
    def status_emoji(self) -> str:
        """Get status emoji."""
        if self.is_won:
            return "🎉"
        if self.is_closed:
            return "❌"
        if self.is_late:
            return "⚠️"
        if self.probability and self.probability >= 75:
            return "🔥"
        return "📊"

    def __str__(self) -> str:
        amount_str = f"${self.amount:,.0f}" if self.amount else "TBD"
        return f"Opportunity({self.name} - {amount_str})"

    def __repr__(self) -> str:
        return f"Opportunity(id={self.id!r}, name={self.name!r}, amount={self.amount!r}, stage={self.stage!r})"
