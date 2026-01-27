# BlackRoad MCP Server

Model Context Protocol server for the BlackRoad mesh. Allows AI assistants to interact with the entire ecosystem.

## Quick Start

```bash
# Run the MCP server (stdio mode for MCP clients)
python -m blackroad_mcp

# Or run in HTTP mode for testing
python -m blackroad_mcp --http --port 8090

# Interactive mode
python -m blackroad_mcp interactive
```

## Available Tools

| Tool | Description |
|------|-------------|
| `route` | Classify a query and determine the target org |
| `dispatch` | Dispatch a query (auto-routes) |
| `dispatch_to` | Dispatch to specific org/service |
| `health_check` | Check service health |
| `list_orgs` | List all organizations |
| `list_routes` | List routing table |
| `process_webhook` | Process a webhook payload |
| `get_signals` | Get recent signals |
| `get_node_config` | Get node configuration |

## Available Resources

| URI | Description |
|-----|-------------|
| `mesh://status` | Current mesh status |
| `mesh://orgs` | Organization list |
| `mesh://routes` | Routing table |
| `mesh://signals` | Recent signals |
| `mesh://nodes/{name}` | Node configuration |

## Usage with Claude Code

Add to your MCP configuration:

```json
{
  "mcpServers": {
    "blackroad": {
      "command": "python",
      "args": ["-m", "blackroad_mcp"],
      "cwd": "/path/to/.github/prototypes/mcp-server"
    }
  }
}
```

Then in Claude Code:

```
> Route "sync salesforce contacts"
> List all BlackRoad organizations
> Check health of FND services
> Get the configuration for lucidia node
```

## Testing

```bash
# Run test suite
python -m blackroad_mcp test --verbose

# Call tools directly
python -m blackroad_mcp call route "sync salesforce"
python -m blackroad_mcp call list_orgs
python -m blackroad_mcp call get_node_config node=lucidia
```

## Architecture

```
Claude Code / AI Assistant
         │
         ▼
    ┌─────────────┐
    │  MCP Server │
    └─────────────┘
         │
    ┌────┼────┐
    ▼    ▼    ▼
Operator Dispatcher Webhooks
    │         │         │
    └────┬────┴────┬────┘
         ▼         ▼
    BlackRoad Mesh Services
```

## Signal Flow

```
User Query → MCP Server → Operator (classify) → Dispatcher (route) → Service
                ↓
            Signal emitted
                ↓
            Logged to history
```
