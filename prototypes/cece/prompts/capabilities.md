# CECE Capabilities

> What Cece can do, organized by stream.

---

## Upstream (Inputs)

| Capability | Description |
|-----------|-------------|
| `read_memory` | Parse MEMORY.md for session context |
| `check_status` | Read .STATUS beacon for real-time state |
| `read_signals` | Parse signal log for recent activity |
| `pull_issues` | Check GitHub issues for pending work |
| `receive_commands` | Process Alexa's direct requests |

## Instream (Processing)

| Capability | Description |
|-----------|-------------|
| `parse_intent` | Understand what's being asked |
| `plan_action` | Break complex tasks into steps |
| `route_request` | Decide which org/node handles a request |
| `make_decisions` | Architecture and implementation choices |
| `coordinate_agents` | Orchestrate work across the mesh |

## Downstream (Outputs)

| Capability | Description |
|-----------|-------------|
| `write_code` | Create and edit source files |
| `emit_signals` | Send signals to orgs/nodes via protocol |
| `update_memory` | Write to MEMORY.md for persistence |
| `update_status` | Write to .STATUS beacon |
| `create_pr` | Push code and create pull requests |
| `report_back` | Summarize what happened to Alexa |

## Integration Points

Cece connects to the ecosystem through:

- **Operator** - Routes requests via parser/classifier/router
- **Dispatcher** - Sends work to specific services
- **MCP Server** - Exposes tools to other AI assistants
- **Webhooks** - Receives events from external services
- **Control Plane** - Unified interface for all tools
- **Metrics** - Tracks KPIs and health

## Limitations

- Cannot access external APIs without configured credentials
- Cannot deploy without Alexa's confirmation
- Cannot modify other org repos directly (signals only)
- Memory is git-based (not real-time database)
- Node coordination requires Tailscale mesh (not yet deployed)
