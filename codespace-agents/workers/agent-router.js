/**
 * BlackRoad Agent Router - Cloudflare Worker
 * 
 * Routes requests to appropriate agent workers.
 */

const AGENT_URLS = {
  coder: 'https://coder-agent.blackroad.workers.dev',
  designer: 'https://designer-agent.blackroad.workers.dev',
  ops: 'https://ops-agent.blackroad.workers.dev',
  docs: 'https://docs-agent.blackroad.workers.dev',
  analyst: 'https://analyst-agent.blackroad.workers.dev',
};

export default {
  async fetch(request, env, ctx) {
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type',
        },
      });
    }

    const url = new URL(request.url);

    // Health check
    if (url.pathname === '/health') {
      return Response.json({
        service: 'agent-router',
        status: 'healthy',
        agents: Object.keys(AGENT_URLS),
        timestamp: new Date().toISOString(),
      });
    }

    // Route to specific agent
    if (url.pathname === '/ask' && request.method === 'POST') {
      try {
        const body = await request.json();
        const { task, agent } = body;

        if (!task) {
          return Response.json({ error: 'Task is required' }, { status: 400 });
        }

        // Auto-route if agent not specified
        const targetAgent = agent || routeTask(task);
        const agentUrl = AGENT_URLS[targetAgent];

        if (!agentUrl) {
          return Response.json(
            { error: `Unknown agent: ${targetAgent}` },
            { status: 400 }
          );
        }

        // Forward to agent
        const response = await fetch(`${agentUrl}/ask`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ task }),
        });

        const result = await response.json();

        // Add routing metadata
        result.routed_by = 'agent-router';
        result.selected_agent = targetAgent;

        return Response.json(result, {
          headers: {
            'Access-Control-Allow-Origin': '*',
          },
        });

      } catch (error) {
        return Response.json(
          { error: error.message },
          { status: 500 }
        );
      }
    }

    // List available agents
    if (url.pathname === '/agents') {
      return Response.json({
        agents: Object.keys(AGENT_URLS).map(id => ({
          id,
          url: AGENT_URLS[id],
        })),
      }, {
        headers: {
          'Access-Control-Allow-Origin': '*',
        },
      });
    }

    return Response.json(
      { error: 'Not found' },
      { status: 404 }
    );
  },
};

/**
 * Route task to appropriate agent based on keywords
 */
function routeTask(task) {
  const lower = task.toLowerCase();

  // Coder
  if (/code|function|class|bug|fix|refactor|implement|debug|test|python|javascript/.test(lower)) {
    return 'coder';
  }

  // Designer
  if (/design|ui|ux|color|palette|layout|component|style|css|accessibility/.test(lower)) {
    return 'designer';
  }

  // Ops
  if (/deploy|docker|kubernetes|ci\/cd|pipeline|infrastructure|server|cloud|monitoring/.test(lower)) {
    return 'ops';
  }

  // Docs
  if (/document|readme|tutorial|guide|api doc|documentation|explain|write|changelog/.test(lower)) {
    return 'docs';
  }

  // Analyst
  if (/analyze|metrics|data|statistics|report|trend|anomaly|performance|insights/.test(lower)) {
    return 'analyst';
  }

  // Default
  return 'coder';
}
