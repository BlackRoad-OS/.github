"""
BlackRoad Dispatcher

Routes requests to the right service in the right org.

Usage:
    from dispatcher import Dispatcher

    d = Dispatcher()
    result = await d.dispatch("sync salesforce contacts")
    # → Routes to FND.salesforce service
"""

__version__ = "0.1.0"

from .core import Dispatcher, DispatchResult
from .registry import Registry, Org, Service
from .client import ServiceClient

__all__ = [
    "Dispatcher",
    "DispatchResult",
    "Registry",
    "Org",
    "Service",
    "ServiceClient",
]
