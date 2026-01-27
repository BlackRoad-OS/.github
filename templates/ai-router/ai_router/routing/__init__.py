"""Routing logic - The brain that picks the right provider."""

from .router import Router, Route, RouteResult
from .strategy import (
    RoutingStrategy,
    CostOptimized,
    LatencyOptimized,
    QualityOptimized,
    LocalFirst,
    CloudFirst,
)

__all__ = [
    "Router",
    "Route",
    "RouteResult",
    "RoutingStrategy",
    "CostOptimized",
    "LatencyOptimized",
    "QualityOptimized",
    "LocalFirst",
    "CloudFirst",
]
