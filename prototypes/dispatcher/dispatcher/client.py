"""
Service Client - Make HTTP calls to services.

Handles retries, timeouts, and health checks.
"""

import asyncio
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum


class ServiceStatus(Enum):
    """Status of a service."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass
class ServiceResponse:
    """Response from a service call."""
    success: bool
    status_code: int
    data: Optional[Any] = None
    error: Optional[str] = None
    latency_ms: int = 0
    service: str = ""
    endpoint: str = ""
    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()


class ServiceClient:
    """
    HTTP client for calling services.

    Features:
    - Async HTTP calls
    - Automatic retries
    - Timeout handling
    - Health checks
    - Response parsing

    Usage:
        client = ServiceClient()

        # Call a service
        response = await client.call(
            endpoint="http://lucidia:8091/v1/salesforce/sync",
            method="POST",
            data={"objects": ["Contact"]}
        )

        # Health check
        healthy = await client.health_check("http://lucidia:8091/health")
    """

    def __init__(
        self,
        timeout: int = 30,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ):
        """
        Initialize the client.

        Args:
            timeout: Request timeout in seconds
            max_retries: Max retry attempts
            retry_delay: Delay between retries
        """
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self._session = None

    async def _get_session(self):
        """Get or create aiohttp session."""
        if self._session is None:
            import aiohttp
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            )
        return self._session

    async def close(self):
        """Close the session."""
        if self._session:
            await self._session.close()
            self._session = None

    async def call(
        self,
        endpoint: str,
        method: str = "POST",
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        service_name: str = "",
    ) -> ServiceResponse:
        """
        Call a service endpoint.

        Args:
            endpoint: Full URL to call
            method: HTTP method (GET, POST, etc.)
            data: JSON data to send
            headers: Additional headers
            service_name: Name for logging

        Returns:
            ServiceResponse with result
        """
        import aiohttp

        session = await self._get_session()
        start_time = datetime.now()

        # Default headers
        all_headers = {
            "Content-Type": "application/json",
            "User-Agent": "BlackRoad-Dispatcher/0.1.0",
        }
        if headers:
            all_headers.update(headers)

        last_error = None

        for attempt in range(self.max_retries):
            try:
                async with session.request(
                    method=method,
                    url=endpoint,
                    json=data,
                    headers=all_headers,
                ) as response:
                    latency_ms = int((datetime.now() - start_time).total_seconds() * 1000)

                    # Try to parse JSON
                    try:
                        response_data = await response.json()
                    except:
                        response_data = await response.text()

                    return ServiceResponse(
                        success=response.status < 400,
                        status_code=response.status,
                        data=response_data,
                        latency_ms=latency_ms,
                        service=service_name,
                        endpoint=endpoint,
                    )

            except asyncio.TimeoutError:
                last_error = "Timeout"
            except aiohttp.ClientError as e:
                last_error = str(e)
            except Exception as e:
                last_error = str(e)

            # Wait before retry
            if attempt < self.max_retries - 1:
                await asyncio.sleep(self.retry_delay * (attempt + 1))

        # All retries failed
        latency_ms = int((datetime.now() - start_time).total_seconds() * 1000)
        return ServiceResponse(
            success=False,
            status_code=0,
            error=last_error,
            latency_ms=latency_ms,
            service=service_name,
            endpoint=endpoint,
        )

    async def health_check(self, health_endpoint: str) -> ServiceStatus:
        """
        Check service health.

        Args:
            health_endpoint: Health check URL

        Returns:
            ServiceStatus
        """
        try:
            response = await self.call(
                endpoint=health_endpoint,
                method="GET",
                service_name="health",
            )

            if response.success:
                return ServiceStatus.HEALTHY
            elif response.status_code >= 500:
                return ServiceStatus.UNHEALTHY
            else:
                return ServiceStatus.DEGRADED

        except Exception:
            return ServiceStatus.UNKNOWN

    async def ping(self, endpoint: str) -> tuple:
        """
        Ping an endpoint and return latency.

        Returns:
            (reachable: bool, latency_ms: int)
        """
        response = await self.call(
            endpoint=endpoint,
            method="GET",
            service_name="ping",
        )
        return (response.success, response.latency_ms)


# Mock client for testing without real services
class MockServiceClient(ServiceClient):
    """Mock client that returns fake responses."""

    def __init__(self, responses: Optional[Dict[str, Any]] = None):
        super().__init__()
        self.responses = responses or {}
        self.calls: list = []

    async def call(
        self,
        endpoint: str,
        method: str = "POST",
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        service_name: str = "",
    ) -> ServiceResponse:
        """Return mock response."""
        self.calls.append({
            "endpoint": endpoint,
            "method": method,
            "data": data,
            "service": service_name,
        })

        # Check for predefined response
        if endpoint in self.responses:
            return ServiceResponse(
                success=True,
                status_code=200,
                data=self.responses[endpoint],
                latency_ms=50,
                service=service_name,
                endpoint=endpoint,
            )

        # Default mock response
        return ServiceResponse(
            success=True,
            status_code=200,
            data={"mock": True, "service": service_name},
            latency_ms=50,
            service=service_name,
            endpoint=endpoint,
        )

    async def health_check(self, health_endpoint: str) -> ServiceStatus:
        """Always return healthy for mock."""
        return ServiceStatus.HEALTHY
