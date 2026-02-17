"""
BlackRoad MCP Server - Core server implementation.

Implements the Model Context Protocol for BlackRoad mesh access.
"""

import json
import sys
import asyncio
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

# Add prototypes to path for imports
PROTO_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROTO_ROOT / "operator"))
sys.path.insert(0, str(PROTO_ROOT / "dispatcher"))
sys.path.insert(0, str(PROTO_ROOT / "webhooks"))
sys.path.insert(0, str(PROTO_ROOT / "sessions"))


@dataclass
class Tool:
    """MCP Tool definition."""
    name: str
    description: str
    input_schema: Dict[str, Any]


@dataclass
class Resource:
    """MCP Resource definition."""
    uri: str
    name: str
    description: str
    mime_type: str = "application/json"


@dataclass
class MCPMessage:
    """MCP protocol message."""
    jsonrpc: str = "2.0"
    id: Optional[int] = None
    method: Optional[str] = None
    params: Optional[Dict[str, Any]] = None
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None


class BlackRoadMCP:
    """
    BlackRoad MCP Server.

    Provides AI assistants with access to the BlackRoad mesh
    through the Model Context Protocol.

    Capabilities:
    - Route queries to appropriate orgs
    - Dispatch requests to services
    - Check mesh health
    - Process webhooks
    - Access mesh resources
    """

    def __init__(self):
        """Initialize the MCP server."""
        self._operator = None
        self._dispatcher = None
        self._webhook_receiver = None
        self._session_registry = None
        self._collaboration_hub = None
        self._shared_memory = None
        self._signal_history: List[Dict[str, Any]] = []

        # Define tools
        self.tools = self._define_tools()

        # Define resources
        self.resources = self._define_resources()

    def _define_tools(self) -> List[Tool]:
        """Define available MCP tools."""
        return [
            Tool(
                name="route",
                description="Classify a query and determine which BlackRoad org should handle it. Returns the target org, confidence score, and classification details.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The query or request to classify"
                        },
                        "context": {
                            "type": "object",
                            "description": "Optional context for classification",
                            "additionalProperties": True
                        }
                    },
                    "required": ["query"]
                }
            ),
            Tool(
                name="dispatch",
                description="Dispatch a query to the BlackRoad mesh. Automatically routes to the appropriate org and service based on the query content.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The query or request to dispatch"
                        },
                        "data": {
                            "type": "object",
                            "description": "Additional data to send with the request",
                            "additionalProperties": True
                        }
                    },
                    "required": ["query"]
                }
            ),
            Tool(
                name="dispatch_to",
                description="Dispatch a request directly to a specific org and service. Use this when you know exactly where the request should go.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "org": {
                            "type": "string",
                            "description": "Target org code (OS, AI, FND, CLD, HW, LAB, SEC, MED, INT, EDU, GOV, ARC, STU, VEN, BBX)"
                        },
                        "service": {
                            "type": "string",
                            "description": "Target service name (optional, uses default if not specified)"
                        },
                        "data": {
                            "type": "object",
                            "description": "Data to send to the service",
                            "additionalProperties": True
                        }
                    },
                    "required": ["org"]
                }
            ),
            Tool(
                name="health_check",
                description="Check the health status of mesh services. Can check a specific org/service or all services.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "org": {
                            "type": "string",
                            "description": "Org code to check (optional, checks all if not specified)"
                        },
                        "service": {
                            "type": "string",
                            "description": "Service name to check (optional)"
                        }
                    }
                }
            ),
            Tool(
                name="list_orgs",
                description="List all BlackRoad organizations with their codes, names, and available services.",
                input_schema={
                    "type": "object",
                    "properties": {}
                }
            ),
            Tool(
                name="list_routes",
                description="List all available routes in the mesh, showing org, service, and endpoint mappings.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "org": {
                            "type": "string",
                            "description": "Filter routes by org code (optional)"
                        }
                    }
                }
            ),
            Tool(
                name="process_webhook",
                description="Process a webhook payload and convert it to a BlackRoad signal. Supports GitHub, Stripe, Salesforce, Cloudflare, Slack, Google Cloud, and Figma webhooks.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "provider": {
                            "type": "string",
                            "description": "Webhook provider (github, stripe, salesforce, cloudflare, slack, google, figma)"
                        },
                        "headers": {
                            "type": "object",
                            "description": "HTTP headers from the webhook request",
                            "additionalProperties": True
                        },
                        "body": {
                            "type": "object",
                            "description": "Webhook payload body",
                            "additionalProperties": True
                        }
                    },
                    "required": ["provider", "body"]
                }
            ),
            Tool(
                name="get_signals",
                description="Get recent signals that have flowed through the mesh. Useful for monitoring and debugging.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of signals to return (default: 10)"
                        },
                        "source": {
                            "type": "string",
                            "description": "Filter by signal source (optional)"
                        },
                        "target": {
                            "type": "string",
                            "description": "Filter by target org (optional)"
                        }
                    }
                }
            ),
            Tool(
                name="get_node_config",
                description="Get the configuration for a specific mesh node (lucidia, octavia, aria, alice, shellfish, cecilia, arcadia).",
                input_schema={
                    "type": "object",
                    "properties": {
                        "node": {
                            "type": "string",
                            "description": "Node name (lucidia, octavia, aria, alice, shellfish, cecilia, arcadia)"
                        }
                    },
                    "required": ["node"]
                }
            ),
            # Session Management Tools
            Tool(
                name="session_register",
                description="Register a new session in the mesh for discovery and collaboration.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "session_id": {
                            "type": "string",
                            "description": "Unique session identifier"
                        },
                        "agent_name": {
                            "type": "string",
                            "description": "Agent name (e.g., 'Cece', 'Agent-1')"
                        },
                        "agent_type": {
                            "type": "string",
                            "description": "Agent type (e.g., 'Claude', 'GPT-4')"
                        },
                        "human_user": {
                            "type": "string",
                            "description": "Associated human user"
                        },
                        "capabilities": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Session capabilities"
                        }
                    },
                    "required": ["session_id", "agent_name", "agent_type"]
                }
            ),
            Tool(
                name="session_list",
                description="List all active sessions in the mesh.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "include_offline": {
                            "type": "boolean",
                            "description": "Include offline sessions"
                        }
                    }
                }
            ),
            Tool(
                name="session_ping",
                description="Ping a session to check if it's alive and send a collaborative ping message.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "from_session": {
                            "type": "string",
                            "description": "Your session ID"
                        },
                        "to_session": {
                            "type": "string",
                            "description": "Target session ID to ping"
                        }
                    },
                    "required": ["from_session", "to_session"]
                }
            ),
            Tool(
                name="collab_send",
                description="Send a collaboration message to another session.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "from_session": {
                            "type": "string",
                            "description": "Your session ID"
                        },
                        "to_session": {
                            "type": "string",
                            "description": "Target session ID"
                        },
                        "message_type": {
                            "type": "string",
                            "enum": ["ping", "request", "response", "notification", "task_offer", "task_accept", "sync", "handoff"],
                            "description": "Type of message"
                        },
                        "subject": {
                            "type": "string",
                            "description": "Message subject"
                        },
                        "body": {
                            "type": "string",
                            "description": "Message body"
                        },
                        "data": {
                            "type": "object",
                            "description": "Additional data",
                            "additionalProperties": True
                        }
                    },
                    "required": ["from_session", "to_session", "subject", "body"]
                }
            ),
            Tool(
                name="collab_broadcast",
                description="Broadcast a message to all active sessions.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "from_session": {
                            "type": "string",
                            "description": "Your session ID"
                        },
                        "subject": {
                            "type": "string",
                            "description": "Message subject"
                        },
                        "body": {
                            "type": "string",
                            "description": "Message body"
                        }
                    },
                    "required": ["from_session", "subject", "body"]
                }
            ),
            Tool(
                name="collab_get_messages",
                description="Get collaboration messages for a session.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "session_id": {
                            "type": "string",
                            "description": "Session ID to get messages for"
                        },
                        "message_type": {
                            "type": "string",
                            "enum": ["ping", "request", "response", "broadcast", "notification", "task_offer", "task_accept", "sync", "handoff"],
                            "description": "Filter by message type"
                        }
                    },
                    "required": ["session_id"]
                }
            ),
            Tool(
                name="memory_set",
                description="Store a value in shared memory accessible by all sessions.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "session_id": {
                            "type": "string",
                            "description": "Your session ID"
                        },
                        "key": {
                            "type": "string",
                            "description": "Memory key"
                        },
                        "value": {
                            "description": "Value to store (any type)"
                        },
                        "memory_type": {
                            "type": "string",
                            "enum": ["state", "fact", "decision", "task", "context", "note", "config"],
                            "description": "Type of memory entry"
                        },
                        "tags": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Tags for searching"
                        }
                    },
                    "required": ["session_id", "key", "value"]
                }
            ),
            Tool(
                name="memory_get",
                description="Get a value from shared memory.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "key": {
                            "type": "string",
                            "description": "Memory key"
                        }
                    },
                    "required": ["key"]
                }
            ),
            Tool(
                name="memory_search",
                description="Search shared memory by pattern or tags.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "pattern": {
                            "type": "string",
                            "description": "Key pattern (supports * wildcard)"
                        },
                        "tags": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Tags to search for"
                        },
                        "session_id": {
                            "type": "string",
                            "description": "Filter by session ID"
                        }
                    }
                }
            ),
        ]

    def _define_resources(self) -> List[Resource]:
        """Define available MCP resources."""
        return [
            Resource(
                uri="mesh://status",
                name="Mesh Status",
                description="Current status of the BlackRoad mesh including health and statistics"
            ),
            Resource(
                uri="mesh://orgs",
                name="Organizations",
                description="List of all BlackRoad organizations and their details"
            ),
            Resource(
                uri="mesh://routes",
                name="Routes",
                description="Complete routing table for the mesh"
            ),
            Resource(
                uri="mesh://signals",
                name="Signals",
                description="Recent signals that have flowed through the mesh"
            ),
            Resource(
                uri="mesh://nodes/lucidia",
                name="Lucidia Node",
                description="Configuration for Lucidia (primary Pi node)"
            ),
            Resource(
                uri="mesh://nodes/octavia",
                name="Octavia Node",
                description="Configuration for Octavia (compute node)"
            ),
            Resource(
                uri="mesh://nodes/shellfish",
                name="Shellfish Node",
                description="Configuration for Shellfish (cloud gateway)"
            ),
        ]

    @property
    def operator(self):
        """Lazy load the Operator."""
        if self._operator is None:
            try:
                from routing.core.router import Operator
                self._operator = Operator()
            except ImportError as e:
                print(f"Warning: Could not load Operator: {e}", file=sys.stderr)
        return self._operator

    @property
    def dispatcher(self):
        """Lazy load the Dispatcher."""
        if self._dispatcher is None:
            try:
                from dispatcher.core import Dispatcher
                self._dispatcher = Dispatcher(mock=True)
            except ImportError as e:
                print(f"Warning: Could not load Dispatcher: {e}", file=sys.stderr)
        return self._dispatcher

    @property
    def webhook_receiver(self):
        """Lazy load the WebhookReceiver."""
        if self._webhook_receiver is None:
            try:
                from webhooks import WebhookReceiver
                self._webhook_receiver = WebhookReceiver()
            except ImportError as e:
                print(f"Warning: Could not load WebhookReceiver: {e}", file=sys.stderr)
        return self._webhook_receiver

    @property
    def session_registry(self):
        """Lazy load the Session Registry."""
        if self._session_registry is None:
            try:
                from sessions.registry import SessionRegistry
                self._session_registry = SessionRegistry()
            except ImportError as e:
                print(f"Warning: Could not load SessionRegistry: {e}", file=sys.stderr)
        return self._session_registry

    @property
    def collaboration_hub(self):
        """Lazy load the Collaboration Hub."""
        if self._collaboration_hub is None:
            try:
                from sessions.collaboration import CollaborationHub
                self._collaboration_hub = CollaborationHub(self.session_registry)
            except ImportError as e:
                print(f"Warning: Could not load CollaborationHub: {e}", file=sys.stderr)
        return self._collaboration_hub

    @property
    def shared_memory(self):
        """Lazy load the Shared Memory."""
        if self._shared_memory is None:
            try:
                from sessions.memory import SharedMemory
                self._shared_memory = SharedMemory()
            except ImportError as e:
                print(f"Warning: Could not load SharedMemory: {e}", file=sys.stderr)
        return self._shared_memory

    # =========================================================================
    # Tool Implementations
    # =========================================================================

    async def tool_route(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Route a query using the Operator."""
        if not self.operator:
            return {"error": "Operator not available"}

        result = self.operator.route(query, context=context)

        return {
            "destination": result.destination,
            "org": result.org,
            "org_code": result.org_code,
            "confidence": result.confidence,
            "category": result.classification.category if result.classification else None,
            "signal": result.signal,
        }

    async def tool_dispatch(self, query: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Dispatch a query to the mesh."""
        if not self.dispatcher:
            return {"error": "Dispatcher not available"}

        result = await self.dispatcher.dispatch(query, data=data)

        # Track signal
        self._signal_history.append({
            "type": "dispatch",
            "query": query,
            "org": result.org_code,
            "service": result.service,
            "success": result.success,
            "timestamp": datetime.utcnow().isoformat(),
        })

        return {
            "success": result.success,
            "org": result.org,
            "org_code": result.org_code,
            "service": result.service,
            "endpoint": result.endpoint,
            "latency_ms": result.latency_ms,
            "signal": result.signal,
            "error": result.error,
        }

    async def tool_dispatch_to(
        self,
        org: str,
        service: Optional[str] = None,
        data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Dispatch to a specific org/service."""
        if not self.dispatcher:
            return {"error": "Dispatcher not available"}

        result = await self.dispatcher.dispatch_to(org, service, data=data)

        # Track signal
        self._signal_history.append({
            "type": "dispatch_to",
            "org": result.org_code,
            "service": result.service,
            "success": result.success,
            "timestamp": datetime.utcnow().isoformat(),
        })

        return {
            "success": result.success,
            "org": result.org,
            "org_code": result.org_code,
            "service": result.service,
            "endpoint": result.endpoint,
            "latency_ms": result.latency_ms,
            "signal": result.signal,
            "error": result.error,
        }

    async def tool_health_check(
        self,
        org: Optional[str] = None,
        service: Optional[str] = None
    ) -> Dict[str, Any]:
        """Check health of services."""
        if not self.dispatcher:
            return {"error": "Dispatcher not available"}

        if org:
            status = await self.dispatcher.health_check(org, service)
            return {
                "org": org,
                "service": service,
                "status": status.value,
            }
        else:
            results = await self.dispatcher.health_check_all()
            return {
                "health": {
                    org_code: {
                        svc: status.value
                        for svc, status in services.items()
                    }
                    for org_code, services in results.items()
                }
            }

    async def tool_list_orgs(self) -> Dict[str, Any]:
        """List all organizations."""
        if not self.dispatcher:
            return {"error": "Dispatcher not available"}

        orgs = []
        for org in self.dispatcher.registry.list_orgs():
            orgs.append({
                "code": org.code,
                "name": org.name,
                "services": list(org.services.keys()),
            })

        return {"orgs": orgs}

    async def tool_list_routes(self, org: Optional[str] = None) -> Dict[str, Any]:
        """List all routes."""
        if not self.dispatcher:
            return {"error": "Dispatcher not available"}

        routes = self.dispatcher.list_routes()

        if org:
            routes = [r for r in routes if r["org"] == org]

        return {"routes": routes}

    async def tool_process_webhook(
        self,
        provider: str,
        body: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Process a webhook."""
        if not self.webhook_receiver:
            return {"error": "WebhookReceiver not available"}

        # Build headers based on provider if not provided
        if not headers:
            headers = self._build_webhook_headers(provider, body)

        result = self.webhook_receiver.process(
            headers=headers,
            body=json.dumps(body).encode(),
            provider_hint=provider,
        )

        if result.success and result.signal:
            # Track signal
            self._signal_history.append({
                "type": "webhook",
                "source": result.signal.source,
                "target": result.signal.target,
                "signal_type": result.signal.type.value,
                "timestamp": datetime.utcnow().isoformat(),
            })

            return {
                "success": True,
                "handler": result.handler,
                "signal": result.signal.to_dict(),
                "formatted": result.signal.format(),
            }
        else:
            return {
                "success": False,
                "error": result.error,
            }

    def _build_webhook_headers(self, provider: str, body: Dict) -> Dict[str, str]:
        """Build default headers for a webhook provider."""
        headers = {}

        if provider == "github":
            headers["X-GitHub-Event"] = body.get("action", "push")
        elif provider == "stripe":
            headers["Stripe-Signature"] = "t=0,v1=test"
        elif provider == "slack":
            headers["X-Slack-Signature"] = "v0=test"
            headers["X-Slack-Request-Timestamp"] = "0"
        elif provider == "cloudflare":
            headers["CF-Webhook-Auth"] = "test"
        elif provider == "figma":
            headers["X-Figma-Signature"] = "test"

        return headers

    async def tool_get_signals(
        self,
        limit: int = 10,
        source: Optional[str] = None,
        target: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get recent signals."""
        signals = self._signal_history[-limit:]

        if source:
            signals = [s for s in signals if s.get("source") == source]
        if target:
            signals = [s for s in signals if s.get("target") == target or s.get("org") == target]

        return {"signals": signals, "total": len(self._signal_history)}

    async def tool_get_node_config(self, node: str) -> Dict[str, Any]:
        """Get node configuration."""
        import yaml

        node_file = PROTO_ROOT.parent / "nodes" / f"{node}.yaml"

        if not node_file.exists():
            return {"error": f"Node config not found: {node}"}

        with open(node_file) as f:
            config = yaml.safe_load(f)

        return {"node": node, "config": config}

    # =========================================================================
    # Session Management Tool Implementations
    # =========================================================================

    async def tool_session_register(
        self,
        session_id: str,
        agent_name: str,
        agent_type: str,
        human_user: Optional[str] = None,
        capabilities: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Register a new session."""
        if not self.session_registry:
            return {"error": "Session registry not available"}

        session = self.session_registry.register(
            session_id=session_id,
            agent_name=agent_name,
            agent_type=agent_type,
            human_user=human_user,
            capabilities=capabilities or [],
        )

        return {
            "success": True,
            "session": session.to_dict(),
            "message": f"Registered session {session_id}",
        }

    async def tool_session_list(self, include_offline: bool = False) -> Dict[str, Any]:
        """List active sessions."""
        if not self.session_registry:
            return {"error": "Session registry not available"}

        sessions = self.session_registry.list_sessions(include_offline=include_offline)

        return {
            "sessions": [s.to_dict() for s in sessions],
            "count": len(sessions),
        }

    async def tool_session_ping(self, from_session: str, to_session: str) -> Dict[str, Any]:
        """Ping a session."""
        if not self.collaboration_hub:
            return {"error": "Collaboration hub not available"}

        # Update registry ping
        if self.session_registry:
            self.session_registry.ping(from_session)

        # Send collaboration ping
        message = self.collaboration_hub.ping_session(from_session, to_session)

        return {
            "success": True,
            "message": message.to_dict(),
            "signal": message.format_signal(),
        }

    async def tool_collab_send(
        self,
        from_session: str,
        to_session: str,
        subject: str,
        body: str,
        message_type: str = "request",
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Send a collaboration message."""
        if not self.collaboration_hub:
            return {"error": "Collaboration hub not available"}

        from sessions.collaboration import MessageType

        msg_type = MessageType(message_type)

        message = self.collaboration_hub.send(
            from_session=from_session,
            to_session=to_session,
            type=msg_type,
            subject=subject,
            body=body,
            data=data,
        )

        return {
            "success": True,
            "message": message.to_dict(),
            "signal": message.format_signal(),
        }

    async def tool_collab_broadcast(
        self,
        from_session: str,
        subject: str,
        body: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Broadcast a message to all sessions."""
        if not self.collaboration_hub:
            return {"error": "Collaboration hub not available"}

        message = self.collaboration_hub.broadcast(
            from_session=from_session,
            subject=subject,
            body=body,
            data=data,
        )

        return {
            "success": True,
            "message": message.to_dict(),
            "signal": message.format_signal(),
        }

    async def tool_collab_get_messages(
        self,
        session_id: str,
        message_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get messages for a session."""
        if not self.collaboration_hub:
            return {"error": "Collaboration hub not available"}

        from sessions.collaboration import MessageType

        msg_type = MessageType(message_type) if message_type else None

        messages = self.collaboration_hub.get_messages(
            session_id=session_id,
            message_type=msg_type,
        )

        return {
            "messages": [msg.to_dict() for msg in messages],
            "count": len(messages),
        }

    async def tool_memory_set(
        self,
        session_id: str,
        key: str,
        value: Any,
        memory_type: str = "state",
        tags: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Store a value in shared memory."""
        if not self.shared_memory:
            return {"error": "Shared memory not available"}

        from sessions.memory import MemoryType

        mem_type = MemoryType(memory_type)

        entry = self.shared_memory.set(
            session_id=session_id,
            key=key,
            value=value,
            type=mem_type,
            tags=tags or [],
        )

        return {
            "success": True,
            "entry": entry.to_dict(),
            "message": f"Stored {key} in shared memory",
        }

    async def tool_memory_get(self, key: str) -> Dict[str, Any]:
        """Get a value from shared memory."""
        if not self.shared_memory:
            return {"error": "Shared memory not available"}

        value = self.shared_memory.get(key)

        if value is None:
            return {"found": False, "key": key}

        return {
            "found": True,
            "key": key,
            "value": value,
        }

    async def tool_memory_search(
        self,
        pattern: Optional[str] = None,
        tags: Optional[List[str]] = None,
        session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Search shared memory."""
        if not self.shared_memory:
            return {"error": "Shared memory not available"}

        if pattern:
            entries = self.shared_memory.search(pattern)
        elif tags:
            entries = self.shared_memory.get_by_tags(tags)
        elif session_id:
            entries = self.shared_memory.get_by_session(session_id)
        else:
            return {"error": "Specify pattern, tags, or session_id"}

        return {
            "entries": [e.to_dict() for e in entries],
            "count": len(entries),
        }

    # =========================================================================
    # Resource Implementations
    # =========================================================================

    async def read_resource(self, uri: str) -> Dict[str, Any]:
        """Read a resource by URI."""
        if uri == "mesh://status":
            return await self._resource_status()
        elif uri == "mesh://orgs":
            return await self.tool_list_orgs()
        elif uri == "mesh://routes":
            return await self.tool_list_routes()
        elif uri == "mesh://signals":
            return await self.tool_get_signals(limit=50)
        elif uri.startswith("mesh://nodes/"):
            node = uri.split("/")[-1]
            return await self.tool_get_node_config(node)
        else:
            return {"error": f"Unknown resource: {uri}"}

    async def _resource_status(self) -> Dict[str, Any]:
        """Get mesh status."""
        status = {
            "timestamp": datetime.utcnow().isoformat(),
            "components": {
                "operator": self.operator is not None,
                "dispatcher": self.dispatcher is not None,
                "webhooks": self.webhook_receiver is not None,
            },
            "signals_processed": len(self._signal_history),
        }

        if self.dispatcher:
            status["stats"] = self.dispatcher.stats

        return status

    # =========================================================================
    # MCP Protocol Handler
    # =========================================================================

    async def handle_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle an MCP protocol message."""
        method = message.get("method")
        params = message.get("params", {})
        msg_id = message.get("id")

        try:
            if method == "initialize":
                result = await self._handle_initialize(params)
            elif method == "tools/list":
                result = await self._handle_tools_list()
            elif method == "tools/call":
                result = await self._handle_tools_call(params)
            elif method == "resources/list":
                result = await self._handle_resources_list()
            elif method == "resources/read":
                result = await self._handle_resources_read(params)
            elif method == "prompts/list":
                result = await self._handle_prompts_list()
            else:
                return self._error_response(msg_id, -32601, f"Unknown method: {method}")

            return self._success_response(msg_id, result)

        except Exception as e:
            return self._error_response(msg_id, -32603, str(e))

    async def _handle_initialize(self, params: Dict) -> Dict[str, Any]:
        """Handle initialize request."""
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {},
                "resources": {},
                "prompts": {},
            },
            "serverInfo": {
                "name": "blackroad-mcp",
                "version": "0.1.0",
            },
        }

    async def _handle_tools_list(self) -> Dict[str, Any]:
        """Handle tools/list request."""
        return {
            "tools": [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "inputSchema": tool.input_schema,
                }
                for tool in self.tools
            ]
        }

    async def _handle_tools_call(self, params: Dict) -> Dict[str, Any]:
        """Handle tools/call request."""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        # Map tool names to methods
        tool_map = {
            "route": self.tool_route,
            "dispatch": self.tool_dispatch,
            "dispatch_to": self.tool_dispatch_to,
            "health_check": self.tool_health_check,
            "list_orgs": self.tool_list_orgs,
            "list_routes": self.tool_list_routes,
            "process_webhook": self.tool_process_webhook,
            "get_signals": self.tool_get_signals,
            "get_node_config": self.tool_get_node_config,
            # Session management tools
            "session_register": self.tool_session_register,
            "session_list": self.tool_session_list,
            "session_ping": self.tool_session_ping,
            "collab_send": self.tool_collab_send,
            "collab_broadcast": self.tool_collab_broadcast,
            "collab_get_messages": self.tool_collab_get_messages,
            "memory_set": self.tool_memory_set,
            "memory_get": self.tool_memory_get,
            "memory_search": self.tool_memory_search,
        }

        if tool_name not in tool_map:
            raise ValueError(f"Unknown tool: {tool_name}")

        result = await tool_map[tool_name](**arguments)

        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(result, indent=2),
                }
            ]
        }

    async def _handle_resources_list(self) -> Dict[str, Any]:
        """Handle resources/list request."""
        return {
            "resources": [
                {
                    "uri": res.uri,
                    "name": res.name,
                    "description": res.description,
                    "mimeType": res.mime_type,
                }
                for res in self.resources
            ]
        }

    async def _handle_resources_read(self, params: Dict) -> Dict[str, Any]:
        """Handle resources/read request."""
        uri = params.get("uri")
        content = await self.read_resource(uri)

        return {
            "contents": [
                {
                    "uri": uri,
                    "mimeType": "application/json",
                    "text": json.dumps(content, indent=2),
                }
            ]
        }

    async def _handle_prompts_list(self) -> Dict[str, Any]:
        """Handle prompts/list request."""
        return {
            "prompts": [
                {
                    "name": "diagnose",
                    "description": "Diagnose issues with the BlackRoad mesh",
                    "arguments": [
                        {
                            "name": "symptom",
                            "description": "Description of the issue",
                            "required": True,
                        }
                    ],
                },
                {
                    "name": "deploy",
                    "description": "Guide through deploying to the mesh",
                    "arguments": [
                        {
                            "name": "service",
                            "description": "Service to deploy",
                            "required": True,
                        },
                        {
                            "name": "target",
                            "description": "Target environment",
                            "required": False,
                        }
                    ],
                },
            ]
        }

    def _success_response(self, msg_id: Optional[int], result: Any) -> Dict[str, Any]:
        """Build a success response."""
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": result,
        }

    def _error_response(self, msg_id: Optional[int], code: int, message: str) -> Dict[str, Any]:
        """Build an error response."""
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "error": {
                "code": code,
                "message": message,
            },
        }


def create_server() -> BlackRoadMCP:
    """Create a new MCP server instance."""
    return BlackRoadMCP()
