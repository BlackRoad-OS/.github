"""
MCP Transport Layer

Handles communication over stdio (standard MCP transport).
"""

import sys
import json
import asyncio
from typing import Optional, Callable, Awaitable

from .server import BlackRoadMCP


class StdioTransport:
    """
    Standard I/O transport for MCP.

    Reads JSON-RPC messages from stdin and writes responses to stdout.
    This is the standard transport for MCP servers.
    """

    def __init__(self, server: BlackRoadMCP):
        """Initialize the transport."""
        self.server = server
        self._running = False

    async def start(self):
        """Start the transport loop."""
        self._running = True

        # Send server ready notification
        print(json.dumps({
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
        }), flush=True)

        while self._running:
            try:
                # Read line from stdin
                line = await asyncio.get_event_loop().run_in_executor(
                    None, sys.stdin.readline
                )

                if not line:
                    break

                line = line.strip()
                if not line:
                    continue

                # Parse JSON-RPC message
                try:
                    message = json.loads(line)
                except json.JSONDecodeError as e:
                    self._send_error(None, -32700, f"Parse error: {e}")
                    continue

                # Handle message
                response = await self.server.handle_message(message)

                # Send response (only if it has an id - not for notifications)
                if response.get("id") is not None:
                    self._send_response(response)

            except Exception as e:
                print(f"Transport error: {e}", file=sys.stderr)
                break

    def stop(self):
        """Stop the transport."""
        self._running = False

    def _send_response(self, response: dict):
        """Send a response to stdout."""
        print(json.dumps(response), flush=True)

    def _send_error(self, msg_id: Optional[int], code: int, message: str):
        """Send an error response."""
        self._send_response({
            "jsonrpc": "2.0",
            "id": msg_id,
            "error": {
                "code": code,
                "message": message,
            },
        })


class HTTPTransport:
    """
    HTTP transport for MCP (alternative to stdio).

    Useful for testing and web-based integrations.
    """

    def __init__(self, server: BlackRoadMCP, host: str = "localhost", port: int = 8090):
        """Initialize the transport."""
        self.server = server
        self.host = host
        self.port = port
        self._app = None

    async def start(self):
        """Start the HTTP server."""
        try:
            from aiohttp import web
        except ImportError:
            print("HTTP transport requires aiohttp. Install with: pip install aiohttp")
            return

        async def handle_mcp(request: web.Request) -> web.Response:
            """Handle MCP requests."""
            try:
                message = await request.json()
                response = await self.server.handle_message(message)
                return web.json_response(response)
            except Exception as e:
                return web.json_response({
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {"code": -32603, "message": str(e)},
                })

        async def handle_health(request: web.Request) -> web.Response:
            """Health check endpoint."""
            return web.json_response({"status": "healthy"})

        app = web.Application()
        app.router.add_post("/mcp", handle_mcp)
        app.router.add_get("/health", handle_health)

        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, self.host, self.port)
        await site.start()

        print(f"MCP HTTP server running on http://{self.host}:{self.port}")
        print("  POST /mcp - MCP endpoint")
        print("  GET /health - Health check")

        # Keep running
        while True:
            await asyncio.sleep(3600)


async def run_stdio():
    """Run MCP server with stdio transport."""
    server = BlackRoadMCP()
    transport = StdioTransport(server)
    await transport.start()


async def run_http(host: str = "localhost", port: int = 8090):
    """Run MCP server with HTTP transport."""
    server = BlackRoadMCP()
    transport = HTTPTransport(server, host, port)
    await transport.start()
