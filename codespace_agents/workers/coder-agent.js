/**
 * BlackRoad Coder Agent - Cloudflare Worker
 * 
 * Edge-deployed coder agent for code generation and review.
 */

export default {
  async fetch(request, env, ctx) {
    // Handle CORS
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
        agent: 'coder',
        status: 'healthy',
        model: 'qwen2.5-coder',
        timestamp: new Date().toISOString(),
      });
    }

    // Main endpoint
    if (url.pathname === '/ask' && request.method === 'POST') {
      try {
        const body = await request.json();
        const { task } = body;

        if (!task) {
          return Response.json({ error: 'Task is required' }, { status: 400 });
        }

        // TODO: Implement actual model inference by integrating with:
        // - Ollama API running on a backend server
        // - Cloudflare Workers AI
        // - OpenAI/Anthropic APIs
        // For now, return mock response
        const response = {
          agent: 'coder',
          task,
          response: `[Mock Response] I would help you with: ${task}. Note: Actual model inference not yet implemented.`,
          model: 'qwen2.5-coder:latest',
          timestamp: new Date().toISOString(),
          // In production, would include:
          // - Code generation
          // - Code review
          // - Test cases
          // - Documentation
        };

        // Store in KV for history (optional)
        if (env.AGENT_KV) {
          const key = `coder:${Date.now()}`;
          await env.AGENT_KV.put(key, JSON.stringify(response), {
            expirationTtl: 86400, // 24 hours
          });
        }

        return Response.json(response, {
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

    // List recent tasks
    if (url.pathname === '/history' && env.AGENT_KV) {
      try {
        const list = await env.AGENT_KV.list({ prefix: 'coder:' });
        const keys = list.keys.slice(0, 10); // Last 10
        
        const history = [];
        for (const { name } of keys) {
          const value = await env.AGENT_KV.get(name);
          if (value) {
            history.push(JSON.parse(value));
          }
        }

        return Response.json({ history }, {
          headers: {
            'Access-Control-Allow-Origin': '*',
          },
        });
      } catch (error) {
        return Response.json({ error: error.message }, { status: 500 });
      }
    }

    return Response.json(
      { error: 'Not found' },
      { status: 404 }
    );
  },
};
