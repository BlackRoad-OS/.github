/**
 * BlackRoad API Gateway - Cloudflare Worker
 *
 * Edge-level API gateway handling:
 * - CORS
 * - Rate limiting (via KV)
 * - API key authentication
 * - Request routing
 * - Response caching
 * - Webhook receiving
 */

// ── Route Definitions ──────────────────────────────────────────────

const ROUTES = [
  { method: "POST", path: "/v1/route", handler: handleRoute },
  { method: "POST", path: "/v1/complete", handler: handleComplete },
  { method: "GET", path: "/v1/health", handler: handleHealth },
  { method: "GET", path: "/v1/status", handler: handleStatus },
  { method: "POST", path: "/v1/webhook/:provider", handler: handleWebhook },
  { method: "GET", path: "/v1/templates", handler: handleListTemplates },
];

// ── Main Entry Point ───────────────────────────────────────────────

export default {
  async fetch(request, env, ctx) {
    // CORS preflight
    if (request.method === "OPTIONS") {
      return handleCORS(env);
    }

    const url = new URL(request.url);
    const path = url.pathname;
    const method = request.method;

    // Health check (no auth required)
    if (path === "/v1/health" && method === "GET") {
      return corsResponse(await handleHealth(request, env), env);
    }

    // Match route
    const match = matchRoute(method, path);
    if (!match) {
      return corsResponse(
        jsonResponse({ error: "Not found", path }, 404),
        env
      );
    }

    // Rate limiting
    const rateLimitResult = await checkRateLimit(request, env);
    if (rateLimitResult) {
      return corsResponse(rateLimitResult, env);
    }

    // Authentication (skip for webhooks - they use signature verification)
    if (!path.startsWith("/v1/webhook")) {
      const authResult = authenticate(request, env);
      if (authResult) {
        return corsResponse(authResult, env);
      }
    }

    // Execute handler
    try {
      const response = await match.handler(request, env, match.params);
      return corsResponse(response, env);
    } catch (err) {
      return corsResponse(
        jsonResponse(
          { error: "Internal server error", message: err.message },
          500
        ),
        env
      );
    }
  },
};

// ── Route Matching ─────────────────────────────────────────────────

function matchRoute(method, path) {
  for (const route of ROUTES) {
    if (route.method !== method) continue;

    // Handle parameterized routes
    const routeParts = route.path.split("/");
    const pathParts = path.split("/");

    if (routeParts.length !== pathParts.length) continue;

    const params = {};
    let match = true;

    for (let i = 0; i < routeParts.length; i++) {
      if (routeParts[i].startsWith(":")) {
        params[routeParts[i].slice(1)] = pathParts[i];
      } else if (routeParts[i] !== pathParts[i]) {
        match = false;
        break;
      }
    }

    if (match) {
      return { handler: route.handler, params };
    }
  }
  return null;
}

// ── Authentication ─────────────────────────────────────────────────

function authenticate(request, env) {
  const authHeader = request.headers.get("Authorization");
  const apiKey = request.headers.get("X-API-Key");

  const key = apiKey || (authHeader?.startsWith("Bearer ") ? authHeader.slice(7) : null);

  if (!key) {
    return jsonResponse(
      { error: "Authentication required", hint: "Provide X-API-Key header or Bearer token" },
      401
    );
  }

  if (key !== env.BLACKROAD_API_KEY) {
    return jsonResponse({ error: "Invalid API key" }, 403);
  }

  return null; // Auth passed
}

// ── Rate Limiting ──────────────────────────────────────────────────

async function checkRateLimit(request, env) {
  if (!env.RATE_LIMIT) return null;

  const ip = request.headers.get("CF-Connecting-IP") || "unknown";
  const key = `rl:${ip}`;
  const limit = parseInt(env.RATE_LIMIT_REQUESTS || "60");
  const window = parseInt(env.RATE_LIMIT_WINDOW || "60");

  try {
    const current = await env.RATE_LIMIT.get(key);
    const count = current ? parseInt(current) : 0;

    if (count >= limit) {
      return jsonResponse(
        {
          error: "Rate limit exceeded",
          limit,
          window_seconds: window,
          retry_after: window,
        },
        429,
        { "Retry-After": String(window) }
      );
    }

    // Increment counter
    await env.RATE_LIMIT.put(key, String(count + 1), {
      expirationTtl: window,
    });
  } catch (e) {
    // If KV fails, allow the request (fail open)
    console.error("Rate limit check failed:", e.message);
  }

  return null;
}

// ── Route Handlers ─────────────────────────────────────────────────

async function handleRoute(request, env) {
  const body = await request.json();
  const { prompt, system, max_tokens, temperature, provider, tags } = body;

  if (!prompt) {
    return jsonResponse({ error: "prompt is required" }, 400);
  }

  // Forward to upstream BlackRoad router
  const upstream = env.UPSTREAM_URL || "http://localhost:8080";
  const response = await fetch(`${upstream}/route`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Gateway": "cloudflare",
      "X-Request-ID": crypto.randomUUID(),
      "CF-Connecting-IP": request.headers.get("CF-Connecting-IP") || "",
    },
    body: JSON.stringify({
      prompt,
      system,
      max_tokens: max_tokens || 1024,
      temperature: temperature || 0.7,
      preferred_provider: provider,
      required_tags: tags,
    }),
  });

  const data = await response.json();
  return jsonResponse(data, response.status);
}

async function handleComplete(request, env) {
  const body = await request.json();
  const { prompt, system, max_tokens, temperature, provider } = body;

  if (!prompt) {
    return jsonResponse({ error: "prompt is required" }, 400);
  }

  // Forward to upstream
  const upstream = env.UPSTREAM_URL || "http://localhost:8080";
  const response = await fetch(`${upstream}/complete`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Gateway": "cloudflare",
      "X-Request-ID": crypto.randomUUID(),
    },
    body: JSON.stringify({ prompt, system, max_tokens, temperature, provider }),
  });

  const data = await response.json();
  return jsonResponse(data, response.status);
}

async function handleHealth(request, env) {
  return jsonResponse({
    status: "healthy",
    gateway: "blackroad-edge",
    environment: env.ENVIRONMENT || "unknown",
    timestamp: new Date().toISOString(),
    edge_location: request.cf?.colo || "unknown",
    version: "1.0.0",
  });
}

async function handleStatus(request, env) {
  // Try to get upstream status
  let upstreamStatus = { status: "unknown" };
  try {
    const upstream = env.UPSTREAM_URL || "http://localhost:8080";
    const resp = await fetch(`${upstream}/status`, {
      headers: { "X-Gateway": "cloudflare" },
    });
    upstreamStatus = await resp.json();
  } catch (e) {
    upstreamStatus = { status: "unreachable", error: e.message };
  }

  return jsonResponse({
    gateway: {
      status: "healthy",
      environment: env.ENVIRONMENT,
      edge_location: request.cf?.colo || "unknown",
    },
    upstream: upstreamStatus,
    timestamp: new Date().toISOString(),
  });
}

async function handleWebhook(request, env, params) {
  const provider = params.provider;
  const body = await request.text();
  const headers = Object.fromEntries(request.headers.entries());

  // Forward to upstream webhook handler with all headers for verification
  const upstream = env.UPSTREAM_URL || "http://localhost:8080";
  const response = await fetch(`${upstream}/webhook/${provider}`, {
    method: "POST",
    headers: {
      "Content-Type": request.headers.get("Content-Type") || "application/json",
      "X-Gateway": "cloudflare",
      "X-Original-Headers": JSON.stringify(headers),
      "CF-Connecting-IP": request.headers.get("CF-Connecting-IP") || "",
      // Forward signature headers
      ...(headers["x-hub-signature-256"] && {
        "X-Hub-Signature-256": headers["x-hub-signature-256"],
      }),
      ...(headers["stripe-signature"] && {
        "Stripe-Signature": headers["stripe-signature"],
      }),
      ...(headers["x-slack-signature"] && {
        "X-Slack-Signature": headers["x-slack-signature"],
        "X-Slack-Request-Timestamp":
          headers["x-slack-request-timestamp"] || "",
      }),
    },
    body,
  });

  const data = await response.json();
  return jsonResponse(data, response.status);
}

async function handleListTemplates(request, env) {
  // Forward to upstream
  const upstream = env.UPSTREAM_URL || "http://localhost:8080";
  try {
    const response = await fetch(`${upstream}/templates`, {
      headers: { "X-Gateway": "cloudflare" },
    });
    const data = await response.json();
    return jsonResponse(data);
  } catch (e) {
    return jsonResponse({ error: "Upstream unavailable" }, 502);
  }
}

// ── CORS ───────────────────────────────────────────────────────────

function handleCORS(env) {
  return new Response(null, {
    status: 204,
    headers: corsHeaders(env),
  });
}

function corsHeaders(env) {
  return {
    "Access-Control-Allow-Origin": env.CORS_ORIGIN || "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
    "Access-Control-Allow-Headers":
      "Content-Type, Authorization, X-API-Key, X-Request-ID",
    "Access-Control-Max-Age": "86400",
  };
}

function corsResponse(response, env) {
  const headers = new Headers(response.headers);
  for (const [key, value] of Object.entries(corsHeaders(env))) {
    headers.set(key, value);
  }
  return new Response(response.body, {
    status: response.status,
    headers,
  });
}

// ── Utilities ──────────────────────────────────────────────────────

function jsonResponse(data, status = 200, extraHeaders = {}) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      "Content-Type": "application/json",
      "X-Powered-By": "BlackRoad",
      ...extraHeaders,
    },
  });
}
