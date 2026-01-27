"""
BlackRoad Metrics - Real-time KPIs for the ecosystem.

Usage:
    from metrics import Dashboard, Counter, Health

    dashboard = Dashboard()
    dashboard.show()
"""

from .counter import Counter, CodeMetrics
from .health import HealthChecker, HealthStatus
from .dashboard import Dashboard

__version__ = "0.1.0"
__all__ = ["Counter", "CodeMetrics", "HealthChecker", "HealthStatus", "Dashboard"]
