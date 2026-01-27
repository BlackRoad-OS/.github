"""
Salesforce API Client.

Handles authentication and API calls to Salesforce.
"""

import os
import json
from typing import Dict, List, Any, Optional, Type
from datetime import datetime
from dataclasses import dataclass

# Note: In production, use `simple_salesforce` library
# pip install simple-salesforce


@dataclass
class APIUsage:
    """Track API usage."""
    calls_made: int = 0
    daily_limit: int = 15000
    last_reset: Optional[datetime] = None

    @property
    def calls_remaining(self) -> int:
        return self.daily_limit - self.calls_made

    @property
    def usage_percent(self) -> float:
        return (self.calls_made / self.daily_limit) * 100

    def increment(self):
        self.calls_made += 1


class SalesforceClient:
    """
    Client for Salesforce REST API.

    Example:
        client = SalesforceClient(
            instance_url="https://yourinstance.salesforce.com",
            access_token="your_token"
        )

        # Query
        results = client.query("SELECT Id, Name FROM Contact LIMIT 10")

        # Get record
        contact = client.get("Contact", "003...")

        # Create record
        result = client.create("Contact", {"FirstName": "Jane", "LastName": "Doe"})

        # Update record
        client.update("Contact", "003...", {"Phone": "555-1234"})

        # Delete record
        client.delete("Contact", "003...")
    """

    def __init__(
        self,
        instance_url: Optional[str] = None,
        access_token: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        security_token: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        api_version: str = "58.0"
    ):
        """
        Initialize client.

        Can authenticate via:
        1. Access token (if you already have one)
        2. Username/password + security token
        3. OAuth client credentials
        """
        self.instance_url = instance_url or os.getenv("SF_INSTANCE_URL")
        self.access_token = access_token or os.getenv("SF_ACCESS_TOKEN")
        self.api_version = api_version
        self.usage = APIUsage()

        # Store credentials for re-auth
        self._username = username or os.getenv("SF_USERNAME")
        self._password = password or os.getenv("SF_PASSWORD")
        self._security_token = security_token or os.getenv("SF_SECURITY_TOKEN")
        self._client_id = client_id or os.getenv("SF_CLIENT_ID")
        self._client_secret = client_secret or os.getenv("SF_CLIENT_SECRET")

        # Will be set after connection
        self._sf = None

    @property
    def base_url(self) -> str:
        """Get API base URL."""
        return f"{self.instance_url}/services/data/v{self.api_version}"

    def connect(self) -> bool:
        """
        Connect to Salesforce.

        Returns True if connection successful.
        """
        try:
            # Try to import simple_salesforce
            from simple_salesforce import Salesforce

            if self.access_token and self.instance_url:
                # Use existing token
                self._sf = Salesforce(
                    instance_url=self.instance_url,
                    session_id=self.access_token
                )
            elif self._username and self._password:
                # Username/password auth
                self._sf = Salesforce(
                    username=self._username,
                    password=self._password,
                    security_token=self._security_token or ""
                )
                self.instance_url = self._sf.sf_instance
                self.access_token = self._sf.session_id
            else:
                raise ValueError("No valid credentials provided")

            return True

        except ImportError:
            print("Warning: simple_salesforce not installed. Using mock mode.")
            return self._mock_connect()

        except Exception as e:
            print(f"Connection failed: {e}")
            return False

    def _mock_connect(self) -> bool:
        """Mock connection for development."""
        print("Running in mock mode - no actual SF connection")
        return True

    def query(self, soql: str) -> List[Dict[str, Any]]:
        """
        Execute SOQL query.

        Args:
            soql: SOQL query string

        Returns:
            List of record dictionaries
        """
        self.usage.increment()

        if self._sf:
            result = self._sf.query(soql)
            return result.get("records", [])
        else:
            # Mock response
            return self._mock_query(soql)

    def query_all(self, soql: str) -> List[Dict[str, Any]]:
        """
        Execute SOQL query and fetch all results (handles pagination).
        """
        self.usage.increment()

        if self._sf:
            result = self._sf.query_all(soql)
            return result.get("records", [])
        else:
            return self._mock_query(soql)

    def get(self, sobject: str, record_id: str) -> Dict[str, Any]:
        """
        Get a single record by ID.

        Args:
            sobject: Object type (Contact, Lead, etc.)
            record_id: Salesforce record ID

        Returns:
            Record dictionary
        """
        self.usage.increment()

        if self._sf:
            obj = getattr(self._sf, sobject)
            return obj.get(record_id)
        else:
            return self._mock_get(sobject, record_id)

    def create(self, sobject: str, data: Dict[str, Any]) -> str:
        """
        Create a new record.

        Args:
            sobject: Object type
            data: Field values

        Returns:
            New record ID
        """
        self.usage.increment()

        if self._sf:
            obj = getattr(self._sf, sobject)
            result = obj.create(data)
            return result["id"]
        else:
            return self._mock_create(sobject, data)

    def update(self, sobject: str, record_id: str, data: Dict[str, Any]) -> bool:
        """
        Update an existing record.

        Args:
            sobject: Object type
            record_id: Record ID
            data: Fields to update

        Returns:
            True if successful
        """
        self.usage.increment()

        if self._sf:
            obj = getattr(self._sf, sobject)
            obj.update(record_id, data)
            return True
        else:
            return self._mock_update(sobject, record_id, data)

    def delete(self, sobject: str, record_id: str) -> bool:
        """
        Delete a record.

        Args:
            sobject: Object type
            record_id: Record ID

        Returns:
            True if successful
        """
        self.usage.increment()

        if self._sf:
            obj = getattr(self._sf, sobject)
            obj.delete(record_id)
            return True
        else:
            return self._mock_delete(sobject, record_id)

    def describe(self, sobject: str) -> Dict[str, Any]:
        """Get object metadata/schema."""
        self.usage.increment()

        if self._sf:
            obj = getattr(self._sf, sobject)
            return obj.describe()
        else:
            return {"name": sobject, "fields": []}

    # Mock methods for development without SF connection

    def _mock_query(self, soql: str) -> List[Dict]:
        """Return mock data for queries."""
        if "Contact" in soql:
            return [
                {"Id": "003MOCK001", "FirstName": "Jane", "LastName": "Doe", "Email": "jane@example.com"},
                {"Id": "003MOCK002", "FirstName": "John", "LastName": "Smith", "Email": "john@example.com"},
            ]
        if "Lead" in soql:
            return [
                {"Id": "00QMOCK001", "FirstName": "Alice", "LastName": "Wong", "Company": "Acme Corp"},
            ]
        return []

    def _mock_get(self, sobject: str, record_id: str) -> Dict:
        return {"Id": record_id, "Name": f"Mock {sobject}"}

    def _mock_create(self, sobject: str, data: Dict) -> str:
        import random
        prefix = {"Contact": "003", "Lead": "00Q", "Account": "001", "Opportunity": "006"}.get(sobject, "000")
        return f"{prefix}MOCK{random.randint(1000, 9999)}"

    def _mock_update(self, sobject: str, record_id: str, data: Dict) -> bool:
        return True

    def _mock_delete(self, sobject: str, record_id: str) -> bool:
        return True
