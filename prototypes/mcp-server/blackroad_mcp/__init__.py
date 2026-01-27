"""
BlackRoad MCP Server

Model Context Protocol server for the BlackRoad mesh.
Allows AI assistants to interact with the entire ecosystem.

Tools:
- route: Classify and route a query
- dispatch: Send request to a service
- dispatch_to: Send to specific org/service
- health_check: Check service health
- list_orgs: List all organizations
- list_routes: List all routes
- process_webhook: Process a webhook payload
- get_signals: Get recent signals

Resources:
- mesh://status - Current mesh status
- mesh://orgs - Organization list
- mesh://routes - Routing table
- mesh://signals - Recent signals
- mesh://nodes/{node} - Node configuration

Usage:
    # Start the server
    python -m blackroad_mcp

    # Or use with Claude Code
    claude --mcp-server "python -m blackroad_mcp"
"""

__version__ = "0.1.0"

from .server import BlackRoadMCP, create_server

__all__ = ["BlackRoadMCP", "create_server"]
