"""
Dispatcher Core - The routing brain.

Takes a request, figures out where it goes, sends it there.
"""

import sys
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List

from .registry import Registry, Org, Service
from .client import ServiceClient, ServiceResponse, ServiceStatus, MockServiceClient

# Add operator to path for classification
BRIDGE_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(BRIDGE_ROOT / "prototypes" / "operator"))


@dataclass
class DispatchResult:
    """Result of dispatching a request."""
    success: bool
    org: str
    org_code: str
    service: str
    endpoint: str
    response: Optional[ServiceResponse] = None
    classification: Optional[Any] = None
    error: Optional[str] = None
    latency_ms: int = 0
    timestamp: str = ""
    signal: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()
        if not self.signal:
            if self.success:
                self.signal = f"🎯 OS → {self.org_code} : dispatched, service={self.service}, latency={self.latency_ms}ms"
            else:
                self.signal = f"❌ OS → {self.org_code} : dispatch_failed, error={self.error}"


class Dispatcher:
    """
    The Dispatcher - Routes requests to services.

    Flow:
    1. Classify the request (using Operator)
    2. Look up the target org and service
    3. Call the service endpoint
    4. Return the result

    Usage:
        dispatcher = Dispatcher()

        # Dispatch a text query
        result = await dispatcher.dispatch("sync salesforce contacts")
        print(f"Routed to: {result.org}.{result.service}")
        print(f"Response: {result.response.data}")

        # Dispatch with explicit target
        result = await dispatcher.dispatch_to("FND", "salesforce", data={"action": "sync"})

        # Check all services
        health = await dispatcher.health_check_all()
    """

    def __init__(
        self,
        registry: Optional[Registry] = None,
        client: Optional[ServiceClient] = None,
        mock: bool = False,
    ):
        """
        Initialize the dispatcher.

        Args:
            registry: Routing registry (auto-loaded if None)
            client: Service client (created if None)
            mock: Use mock client (for testing)
        """
        self.registry = registry or Registry()

        if mock:
            self.client = MockServiceClient()
        else:
            self.client = client or ServiceClient()

        self._operator = None
        self._history: List[DispatchResult] = []

    @property
    def operator(self):
        """Lazy load the Operator for classification."""
        if self._operator is None:
            try:
                from routing.core.router import Operator
                self._operator = Operator()
            except ImportError:
                self._operator = None
        return self._operator

    async def dispatch(
        self,
        query: str,
        data: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> DispatchResult:
        """
        Dispatch a query to the appropriate service.

        Args:
            query: The query/request text
            data: Additional data to send
            context: Context for classification

        Returns:
            DispatchResult with response
        """
        start_time = datetime.now()

        # Step 1: Classify the request
        classification = None
        if self.operator:
            try:
                route_result = self.operator.route(query, context=context)
                org_code = route_result.org_code
                classification = route_result.classification
            except Exception as e:
                # Fallback to registry pattern matching
                org_code, _ = self.registry.match(query)
        else:
            # Use registry pattern matching
            org_code, matched_service = self.registry.match(query)

        # Step 2: Get org and service
        org = self.registry.get_org(org_code)
        if not org:
            return DispatchResult(
                success=False,
                org="Unknown",
                org_code=org_code,
                service="",
                endpoint="",
                error=f"Unknown org: {org_code}",
                latency_ms=int((datetime.now() - start_time).total_seconds() * 1000),
            )

        # Determine service
        if classification:
            # Use classification category to pick service
            service_name = self._category_to_service(org, classification.category)
        else:
            # Use default service
            service_name = self.registry.defaults.get("default_services", {}).get(org_code)

        service = org.get_service(service_name) if service_name else org.default_service()

        if not service:
            return DispatchResult(
                success=False,
                org=org.name,
                org_code=org_code,
                service="",
                endpoint="",
                error=f"No service found for {org_code}",
                latency_ms=int((datetime.now() - start_time).total_seconds() * 1000),
            )

        # Step 3: Call the service
        request_data = {
            "query": query,
            "context": context or {},
        }
        if data:
            request_data.update(data)

        response = await self.client.call(
            endpoint=service.endpoint,
            method="POST",
            data=request_data,
            service_name=f"{org_code}.{service.name}",
        )

        latency_ms = int((datetime.now() - start_time).total_seconds() * 1000)

        result = DispatchResult(
            success=response.success,
            org=org.name,
            org_code=org_code,
            service=service.name,
            endpoint=service.endpoint,
            response=response,
            classification=classification,
            error=response.error,
            latency_ms=latency_ms,
        )

        # Track history
        self._history.append(result)

        # Print signal
        print(f"  {result.signal}")

        return result

    async def dispatch_to(
        self,
        org_code: str,
        service_name: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> DispatchResult:
        """
        Dispatch directly to a specific org/service.

        Args:
            org_code: Target org code
            service_name: Target service (uses default if None)
            data: Data to send

        Returns:
            DispatchResult with response
        """
        start_time = datetime.now()

        org = self.registry.get_org(org_code)
        if not org:
            return DispatchResult(
                success=False,
                org="Unknown",
                org_code=org_code,
                service="",
                endpoint="",
                error=f"Unknown org: {org_code}",
            )

        if service_name:
            service = org.get_service(service_name)
        else:
            service = org.default_service()

        if not service:
            return DispatchResult(
                success=False,
                org=org.name,
                org_code=org_code,
                service="",
                endpoint="",
                error=f"Service not found: {service_name}",
            )

        response = await self.client.call(
            endpoint=service.endpoint,
            method="POST",
            data=data or {},
            service_name=f"{org_code}.{service.name}",
        )

        latency_ms = int((datetime.now() - start_time).total_seconds() * 1000)

        result = DispatchResult(
            success=response.success,
            org=org.name,
            org_code=org_code,
            service=service.name,
            endpoint=service.endpoint,
            response=response,
            error=response.error,
            latency_ms=latency_ms,
        )

        self._history.append(result)
        print(f"  {result.signal}")

        return result

    async def health_check(self, org_code: str, service_name: Optional[str] = None) -> ServiceStatus:
        """Check health of a service."""
        service = self.registry.get_service(org_code, service_name)
        if not service or not service.health:
            return ServiceStatus.UNKNOWN

        return await self.client.health_check(service.health)

    async def health_check_all(self) -> Dict[str, Dict[str, ServiceStatus]]:
        """Check health of all services."""
        results = {}

        for org in self.registry.list_orgs():
            results[org.code] = {}
            for name, service in org.services.items():
                if service.health:
                    status = await self.client.health_check(service.health)
                else:
                    status = ServiceStatus.UNKNOWN
                results[org.code][name] = status

        return results

    def _category_to_service(self, org: Org, category: str) -> Optional[str]:
        """Map classification category to service name."""
        # Direct mappings
        category_map = {
            "crm": "crm",
            "salesforce": "salesforce",
            "billing": "stripe",
            "payment": "stripe",
            "infrastructure": "worker",
            "storage": "storage",
            "ai": "router",
            "question": "router",
            "code": "router",
        }

        mapped = category_map.get(category.lower())
        if mapped and org.get_service(mapped):
            return mapped

        # Return first service as fallback
        return list(org.services.keys())[0] if org.services else None

    def list_routes(self) -> List[Dict[str, Any]]:
        """List all available routes."""
        routes = []
        for org in self.registry.list_orgs():
            for name, service in org.services.items():
                routes.append({
                    "org": org.code,
                    "org_name": org.name,
                    "service": name,
                    "endpoint": service.endpoint,
                    "type": service.type,
                })
        return routes

    @property
    def stats(self) -> Dict[str, Any]:
        """Get dispatch statistics."""
        if not self._history:
            return {"total": 0, "success_rate": 0, "by_org": {}}

        successful = [r for r in self._history if r.success]
        by_org: Dict[str, int] = {}

        for r in self._history:
            by_org[r.org_code] = by_org.get(r.org_code, 0) + 1

        return {
            "total": len(self._history),
            "success_rate": len(successful) / len(self._history),
            "by_org": by_org,
            "avg_latency_ms": sum(r.latency_ms for r in self._history) / len(self._history),
        }

    async def close(self):
        """Close the client."""
        await self.client.close()
