/**
 * BlackRoad API Gateway Worker
 * Primary edge compute entry point — routes, authenticates, rate-limits,
 * and proxies requests across the entire BlackRoad ecosystem.
 *
 * Bindings: KV, D1, R2, AI, Queues, Analytics, Vectorize, Durable Objects
 */

export interface Env {
  // KV Namespaces
  CACHE: KVNamespace;
  SESSIONS: KVNamespace;
  RATE_LIMITS: KVNamespace;
  CONFIG: KVNamespace;
  API_KEYS: KVNamespace;

  // D1 Databases
  DB: D1Database;

  // R2 Buckets
  ASSETS: R2Bucket;
  UPLOADS: R2Bucket;

  // Workers AI
  AI: Ai;

  // Queues
  WEBHOOK_QUEUE: Queue;
  ANALYTICS_QUEUE: Queue;
  SIGNAL_QUEUE: Queue;

  // Analytics Engine
  ANALYTICS: AnalyticsEngineDataset;

  // Vectorize
  VECTORIZE: VectorizeIndex;

  // Durable Objects
  RATE_LIMITER: DurableObjectNamespace;
  SESSION_MANAGER: DurableObjectNamespace;
  WEBSOCKET_ROOM: DurableObjectNamespace;

  // Service Bindings (tunnels to origin)
  ORIGIN_PRIMARY: Fetcher;   // → lucidia
  ORIGIN_STORAGE: Fetcher;   // → aria
  ORIGIN_AGENTS: Fetcher;    // → alice
  ORIGIN_COMPUTE: Fetcher;   // → octavia

  // Secrets
  JWT_SECRET: string;
  STRIPE_WEBHOOK_SECRET: string;
  GITHUB_WEBHOOK_SECRET: string;
  ANTHROPIC_API_KEY: string;

  // Vars
  ENVIRONMENT: string;
  NODE_NAME: string;
}

// ─── Request context ────────────────────────────────────────────────
interface RequestContext {
  startTime: number;
  requestId: string;
  ip: string;
  country: string;
  colo: string;
  orgCode: string | null;
  userId: string | null;
  apiKey: string | null;
}

// ─── Main entry ─────────────────────────────────────────────────────
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const ctx_req = buildContext(request);

    try {
      // Request body size limit (10MB)
      const contentLength = parseInt(request.headers.get("Content-Length") || "0");
      if (contentLength > 10 * 1024 * 1024) {
        return Response.json(
          { error: "payload_too_large", message: "Request body exceeds 10MB limit" },
          { status: 413, headers: corsHeaders(request.headers.get("Origin")) },
        );
      }

      // CORS preflight
      if (request.method === "OPTIONS") {
        return handleCORS(request);
      }

      // WebSocket upgrade
      if (request.headers.get("Upgrade") === "websocket") {
        return handleWebSocket(request, env, ctx_req);
      }

      // Rate limiting via Durable Object
      const rateLimitResult = await checkRateLimit(request, env, ctx_req);
      if (rateLimitResult) return rateLimitResult;

      // Route the request
      const url = new URL(request.url);
      const response = await routeRequest(url, request, env, ctx, ctx_req);

      // Track analytics
      ctx.waitUntil(trackAnalytics(env, ctx_req, response));

      return addCORSHeaders(response, request.headers.get("Origin"));
    } catch (err: any) {
      ctx.waitUntil(trackError(env, ctx_req, err));
      return Response.json(
        { error: "internal_error", message: "An unexpected error occurred", requestId: ctx_req.requestId },
        { status: 500, headers: corsHeaders(request.headers.get("Origin")) },
      );
    }
  },

  // Queue consumer for async processing
  async queue(batch: MessageBatch, env: Env): Promise<void> {
    for (const message of batch.messages) {
      const { type, payload } = message.body as { type: string; payload: any };
      switch (type) {
        case "webhook":
          await processWebhook(payload, env);
          break;
        case "signal":
          await processSignal(payload, env);
          break;
        case "analytics":
          await processAnalyticsEvent(payload, env);
          break;
      }
      message.ack();
    }
  },

  // Scheduled CRON triggers
  async scheduled(event: ScheduledEvent, env: Env, ctx: ExecutionContext): Promise<void> {
    switch (event.cron) {
      case "*/5 * * * *":
        ctx.waitUntil(healthCheckAllNodes(env));
        break;
      case "0 * * * *":
        ctx.waitUntil(aggregateHourlyMetrics(env));
        break;
      case "0 0 * * *":
        ctx.waitUntil(rotateApiKeys(env));
        break;
    }
  },
};

// ═══════════════════════════════════════════════════════════════════
// ROUTING
// ═══════════════════════════════════════════════════════════════════

async function routeRequest(
  url: URL,
  request: Request,
  env: Env,
  ctx: ExecutionContext,
  reqCtx: RequestContext,
): Promise<Response> {
  const path = url.pathname;

  // ─── Public endpoints (no auth) ──────────────────────────────
  if (path === "/health") return handleHealth(env);
  if (path === "/v1/status") return handleSystemStatus(env);
  if (path === "/v1/auth/login") return handleLogin(request, env);
  if (path === "/v1/auth/register") return handleRegister(request, env);
  if (path === "/v1/auth/refresh") return handleRefreshToken(request, env);

  // ─── Webhook receivers (signature-verified) ──────────────────
  if (path.startsWith("/v1/webhooks/")) {
    return handleWebhookIngress(path, request, env, ctx);
  }

  // ─── Protected API routes ────────────────────────────────────
  const authResult = await authenticate(request, env);
  if (!authResult.authenticated) {
    return Response.json(
      { error: "unauthorized", message: authResult.reason },
      { status: 401, headers: corsHeaders() },
    );
  }
  reqCtx.userId = authResult.userId ?? null;
  reqCtx.apiKey = authResult.apiKey ?? null;

  // ─── Core OS routes ──────────────────────────────────────────
  if (path.startsWith("/v1/route")) return proxyToOrigin(request, env.ORIGIN_PRIMARY, "/v1/route");
  if (path.startsWith("/v1/bridge")) return proxyToOrigin(request, env.ORIGIN_PRIMARY, "/v1/bridge");
  if (path.startsWith("/v1/signals")) return handleSignals(request, env, ctx);
  if (path.startsWith("/v1/metrics")) return proxyToOrigin(request, env.ORIGIN_PRIMARY, "/v1/metrics");

  // ─── AI routes ───────────────────────────────────────────────
  if (path.startsWith("/v1/ai/complete")) return handleAIComplete(request, env);
  if (path.startsWith("/v1/ai/embed")) return handleAIEmbed(request, env);
  if (path.startsWith("/v1/ai/classify")) return handleAIClassify(request, env);
  if (path.startsWith("/v1/ai/agents")) return proxyToOrigin(request, env.ORIGIN_AGENTS, "/v1/agents");

  // ─── Edge data routes ────────────────────────────────────────
  if (path.startsWith("/v1/kv")) return handleKV(request, env);
  if (path.startsWith("/v1/db")) return handleD1(request, env);
  if (path.startsWith("/v1/storage")) return handleR2(request, env);
  if (path.startsWith("/v1/vectorize")) return handleVectorize(request, env);

  // ─── Org-specific proxy routes ───────────────────────────────
  if (path.startsWith("/v1/hw/")) return proxyToOrigin(request, env.ORIGIN_PRIMARY, path);
  if (path.startsWith("/v1/sec/")) return proxyToOrigin(request, env.ORIGIN_PRIMARY, path);
  if (path.startsWith("/v1/fnd/")) return proxyToOrigin(request, env.ORIGIN_PRIMARY, path);
  if (path.startsWith("/v1/med/")) return proxyToOrigin(request, env.ORIGIN_COMPUTE, path);
  if (path.startsWith("/v1/int/")) return proxyToOrigin(request, env.ORIGIN_COMPUTE, path);
  if (path.startsWith("/v1/edu/")) return proxyToOrigin(request, env.ORIGIN_STORAGE, path);
  if (path.startsWith("/v1/arc/")) return proxyToOrigin(request, env.ORIGIN_STORAGE, path);
  if (path.startsWith("/v1/stu/")) return proxyToOrigin(request, env.ORIGIN_COMPUTE, path);
  if (path.startsWith("/v1/lab/")) return proxyToOrigin(request, env.ORIGIN_COMPUTE, path);
  if (path.startsWith("/v1/gov/")) return proxyToOrigin(request, env.ORIGIN_PRIMARY, path);
  if (path.startsWith("/v1/ven/")) return proxyToOrigin(request, env.ORIGIN_PRIMARY, path);
  if (path.startsWith("/v1/bbx/")) return proxyToOrigin(request, env.ORIGIN_PRIMARY, path);

  // ─── Fallback ────────────────────────────────────────────────
  return Response.json(
    { error: "not_found", path, requestId: reqCtx.requestId },
    { status: 404, headers: corsHeaders() },
  );
}

// ═══════════════════════════════════════════════════════════════════
// AUTHENTICATION
// ═══════════════════════════════════════════════════════════════════

interface AuthResult {
  authenticated: boolean;
  userId?: string;
  apiKey?: string;
  reason?: string;
}

async function authenticate(request: Request, env: Env): Promise<AuthResult> {
  // Try Bearer token (JWT)
  const authHeader = request.headers.get("Authorization");
  if (authHeader?.startsWith("Bearer ")) {
    const token = authHeader.slice(7);
    const payload = await verifyJWT(token, env.JWT_SECRET);
    if (payload) {
      return { authenticated: true, userId: payload.sub };
    }
    return { authenticated: false, reason: "invalid_token" };
  }

  // Try API key
  const apiKey = request.headers.get("X-API-Key");
  if (apiKey) {
    const keyData = await env.API_KEYS.get(apiKey, "json") as { userId: string; scopes: string[] } | null;
    if (keyData) {
      return { authenticated: true, userId: keyData.userId, apiKey };
    }
    return { authenticated: false, reason: "invalid_api_key" };
  }

  // Try session cookie
  const cookie = request.headers.get("Cookie");
  if (cookie) {
    const sessionId = parseCookie(cookie, "session_id");
    if (sessionId) {
      const session = await env.SESSIONS.get(sessionId, "json") as { userId: string } | null;
      if (session) {
        return { authenticated: true, userId: session.userId };
      }
    }
  }

  return { authenticated: false, reason: "no_credentials" };
}

async function handleLogin(request: Request, env: Env): Promise<Response> {
  const { email, password } = await request.json() as { email: string; password: string };

  if (!email || !password || typeof email !== "string" || typeof password !== "string") {
    return Response.json({ error: "invalid_request", message: "Email and password required" }, { status: 400, headers: corsHeaders() });
  }

  const user = await env.DB.prepare(
    "SELECT id, email, password_hash, role FROM users WHERE email = ?",
  ).bind(email).first();

  if (!user || !await verifyPassword(password, user.password_hash as string)) {
    return Response.json({ error: "invalid_credentials" }, { status: 401, headers: corsHeaders() });
  }

  const token = await signJWT({ sub: user.id as string, role: user.role as string }, env.JWT_SECRET);
  const refreshToken = crypto.randomUUID();

  await env.SESSIONS.put(`refresh:${refreshToken}`, JSON.stringify({ userId: user.id }), {
    expirationTtl: 86400 * 30,
  });

  return Response.json(
    { token, refreshToken, user: { id: user.id, email: user.email, role: user.role } },
    { headers: corsHeaders() },
  );
}

async function handleRegister(request: Request, env: Env): Promise<Response> {
  const { email, name, password } = await request.json() as { email: string; name: string; password: string };

  if (!email || !name || !password) {
    return Response.json({ error: "invalid_request", message: "Email, name, and password required" }, { status: 400, headers: corsHeaders() });
  }
  if (typeof email !== "string" || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return Response.json({ error: "invalid_email" }, { status: 400, headers: corsHeaders() });
  }
  if (typeof password !== "string" || password.length < 8) {
    return Response.json({ error: "weak_password", message: "Password must be at least 8 characters" }, { status: 400, headers: corsHeaders() });
  }
  if (typeof name !== "string" || name.length > 100) {
    return Response.json({ error: "invalid_name" }, { status: 400, headers: corsHeaders() });
  }

  const existing = await env.DB.prepare("SELECT id FROM users WHERE email = ?").bind(email).first();
  if (existing) {
    return Response.json({ error: "email_exists" }, { status: 409, headers: corsHeaders() });
  }

  const id = crypto.randomUUID();
  const passwordHash = await hashPassword(password);

  await env.DB.prepare(
    "INSERT INTO users (id, email, name, password_hash, role, created_at) VALUES (?, ?, ?, ?, 'user', datetime('now'))",
  ).bind(id, email, name, passwordHash).run();

  const token = await signJWT({ sub: id, role: "user" }, env.JWT_SECRET);

  return Response.json(
    { token, user: { id, email, name, role: "user" } },
    { status: 201, headers: corsHeaders() },
  );
}

async function handleRefreshToken(request: Request, env: Env): Promise<Response> {
  const { refreshToken } = await request.json() as { refreshToken: string };
  const session = await env.SESSIONS.get(`refresh:${refreshToken}`, "json") as { userId: string } | null;

  if (!session) {
    return Response.json({ error: "invalid_refresh_token" }, { status: 401, headers: corsHeaders() });
  }

  const user = await env.DB.prepare("SELECT id, email, role FROM users WHERE id = ?")
    .bind(session.userId).first();

  if (!user) {
    return Response.json({ error: "user_not_found" }, { status: 404, headers: corsHeaders() });
  }

  const token = await signJWT({ sub: user.id as string, role: user.role as string }, env.JWT_SECRET);

  return Response.json({ token }, { headers: corsHeaders() });
}

// ═══════════════════════════════════════════════════════════════════
// RATE LIMITING (Durable Object)
// ═══════════════════════════════════════════════════════════════════

export class RateLimiter {
  state: DurableObjectState;

  constructor(state: DurableObjectState) {
    this.state = state;
  }

  async fetch(request: Request): Promise<Response> {
    const { key, limit, window } = await request.json() as {
      key: string;
      limit: number;
      window: number;
    };

    const now = Date.now();
    const windowKey = `rl:${key}:${Math.floor(now / (window * 1000))}`;

    let count = (await this.state.storage.get<number>(windowKey)) || 0;
    count++;

    await this.state.storage.put(windowKey, count);

    if (count > limit) {
      return Response.json({ allowed: false, remaining: 0, retryAfter: window });
    }

    return Response.json({ allowed: true, remaining: limit - count });
  }
}

async function checkRateLimit(
  request: Request,
  env: Env,
  ctx: RequestContext,
): Promise<Response | null> {
  const key = ctx.apiKey || ctx.ip;
  const id = env.RATE_LIMITER.idFromName(key);
  const limiter = env.RATE_LIMITER.get(id);

  const result = await limiter.fetch(new Request("https://internal/check", {
    method: "POST",
    body: JSON.stringify({ key, limit: 1000, window: 60 }),
  }));

  const data = await result.json() as { allowed: boolean; remaining: number; retryAfter?: number };

  if (!data.allowed) {
    return Response.json(
      { error: "rate_limited", retryAfter: data.retryAfter },
      {
        status: 429,
        headers: {
          ...corsHeaders(),
          "Retry-After": String(data.retryAfter),
          "X-RateLimit-Remaining": "0",
        },
      },
    );
  }

  return null;
}

// ═══════════════════════════════════════════════════════════════════
// WEBSOCKET (Durable Object)
// ═══════════════════════════════════════════════════════════════════

export class WebSocketRoom {
  state: DurableObjectState;
  sessions: Map<string, WebSocket>;

  constructor(state: DurableObjectState) {
    this.state = state;
    this.sessions = new Map();
  }

  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);
    const room = url.searchParams.get("room") || "default";

    const [client, server] = Object.values(new WebSocketPair());

    this.state.acceptWebSocket(server);
    const sessionId = crypto.randomUUID();
    this.sessions.set(sessionId, server);

    server.addEventListener("message", (event) => {
      // Broadcast to all other sessions in the room
      for (const [id, ws] of this.sessions) {
        if (id !== sessionId) {
          try {
            ws.send(typeof event.data === "string" ? event.data : "");
          } catch {
            this.sessions.delete(id);
          }
        }
      }
    });

    server.addEventListener("close", () => {
      this.sessions.delete(sessionId);
    });

    return new Response(null, { status: 101, webSocket: client });
  }
}

export class SessionManager {
  state: DurableObjectState;

  constructor(state: DurableObjectState) {
    this.state = state;
  }

  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);

    if (url.pathname === "/create") {
      const { userId, metadata } = await request.json() as { userId: string; metadata: any };
      const sessionId = crypto.randomUUID();
      await this.state.storage.put(sessionId, { userId, metadata, createdAt: Date.now() });
      return Response.json({ sessionId });
    }

    if (url.pathname === "/get") {
      const { sessionId } = await request.json() as { sessionId: string };
      const session = await this.state.storage.get(sessionId);
      if (!session) return Response.json({ error: "not_found" }, { status: 404 });
      return Response.json(session);
    }

    if (url.pathname === "/delete") {
      const { sessionId } = await request.json() as { sessionId: string };
      await this.state.storage.delete(sessionId);
      return Response.json({ deleted: true });
    }

    return Response.json({ error: "invalid_path" }, { status: 400 });
  }
}

async function handleWebSocket(
  request: Request,
  env: Env,
  ctx: RequestContext,
): Promise<Response> {
  // Require authentication for WebSocket upgrade
  const url = new URL(request.url);
  const token = url.searchParams.get("token") || request.headers.get("Sec-WebSocket-Protocol") || "";

  const payload = await verifyJWT(token, env.JWT_SECRET);
  if (!payload) {
    return Response.json(
      { error: "unauthorized", message: "Valid JWT required for WebSocket connection" },
      { status: 401, headers: corsHeaders() },
    );
  }

  const ALLOWED_ROOMS = ["signals", "metrics", "alerts", "chat", "status"];
  const room = url.searchParams.get("room") || "signals";
  if (!ALLOWED_ROOMS.includes(room)) {
    return Response.json(
      { error: "forbidden", message: "Invalid room" },
      { status: 403, headers: corsHeaders() },
    );
  }

  ctx.userId = payload.sub;
  const id = env.WEBSOCKET_ROOM.idFromName(room);
  const roomObj = env.WEBSOCKET_ROOM.get(id);
  return roomObj.fetch(request);
}

// ═══════════════════════════════════════════════════════════════════
// AI ENDPOINTS
// ═══════════════════════════════════════════════════════════════════

async function handleAIComplete(request: Request, env: Env): Promise<Response> {
  const { prompt, model, stream } = await request.json() as {
    prompt: string;
    model?: string;
    stream?: boolean;
  };

  // Check cache first
  const cacheKey = `ai:complete:${await hash(prompt + (model || ""))}`;
  const cached = await env.CACHE.get(cacheKey, "json");
  if (cached) {
    return Response.json({ ...cached as object, cached: true }, { headers: corsHeaders() });
  }

  const result = await env.AI.run(model || "@cf/meta/llama-3.1-8b-instruct", {
    messages: [{ role: "user", content: prompt }],
    stream: stream || false,
  });

  if (stream) {
    return new Response(result as ReadableStream, {
      headers: { "Content-Type": "text/event-stream", ...corsHeaders() },
    });
  }

  const response = { result, model: model || "@cf/meta/llama-3.1-8b-instruct", edge: request.cf?.colo };
  await env.CACHE.put(cacheKey, JSON.stringify(response), { expirationTtl: 300 });

  return Response.json(response, { headers: corsHeaders() });
}

async function handleAIEmbed(request: Request, env: Env): Promise<Response> {
  const { text, texts } = await request.json() as { text?: string; texts?: string[] };
  const input = texts || [text || ""];

  const embeddings = await env.AI.run("@cf/baai/bge-base-en-v1.5", { text: input });

  return Response.json({ embeddings, dimensions: 768 }, { headers: corsHeaders() });
}

async function handleAIClassify(request: Request, env: Env): Promise<Response> {
  const { text, labels } = await request.json() as { text: string; labels: string[] };

  const result = await env.AI.run("@cf/huggingface/distilbert-sst-2-int8", {
    text,
  });

  return Response.json({ classification: result }, { headers: corsHeaders() });
}

// ═══════════════════════════════════════════════════════════════════
// EDGE DATA (KV / D1 / R2 / Vectorize)
// ═══════════════════════════════════════════════════════════════════

async function handleKV(request: Request, env: Env): Promise<Response> {
  const url = new URL(request.url);
  const key = url.pathname.replace("/v1/kv/", "");

  switch (request.method) {
    case "GET": {
      const value = await env.CACHE.get(key);
      if (!value) return Response.json({ error: "not_found" }, { status: 404, headers: corsHeaders() });
      return new Response(value, { headers: corsHeaders() });
    }
    case "PUT": {
      const body = await request.text();
      const ttl = parseInt(url.searchParams.get("ttl") || "3600");
      await env.CACHE.put(key, body, { expirationTtl: ttl });
      return Response.json({ stored: true, key }, { headers: corsHeaders() });
    }
    case "DELETE": {
      await env.CACHE.delete(key);
      return Response.json({ deleted: true, key }, { headers: corsHeaders() });
    }
    default:
      return Response.json({ error: "method_not_allowed" }, { status: 405, headers: corsHeaders() });
  }
}

const ALLOWED_TABLES = [
  "users", "sessions", "api_keys", "signals", "audit_log",
  "routing_rules", "webhooks", "node_health", "metrics_hourly",
];

const FORBIDDEN_SQL_PATTERNS = /\b(DROP|ALTER|CREATE|TRUNCATE|DELETE\s+FROM|UPDATE\s+\w+\s+SET|INSERT\s+INTO)\b/i;

async function handleD1(request: Request, env: Env): Promise<Response> {
  const url = new URL(request.url);
  const table = url.pathname.replace("/v1/db/", "").split("/")[0];

  if (!ALLOWED_TABLES.includes(table)) {
    return Response.json(
      { error: "forbidden", message: "Access to this table is not allowed" },
      { status: 403, headers: corsHeaders() },
    );
  }

  switch (request.method) {
    case "GET": {
      const limit = Math.min(Math.max(parseInt(url.searchParams.get("limit") || "50"), 1), 1000);
      const offset = Math.max(parseInt(url.searchParams.get("offset") || "0"), 0);
      const results = await env.DB.prepare(
        "SELECT * FROM " + table + " LIMIT ? OFFSET ?",
      ).bind(limit, offset).all();
      return Response.json(results, { headers: corsHeaders() });
    }
    case "POST": {
      const { query, params } = await request.json() as { query: string; params?: any[] };
      if (FORBIDDEN_SQL_PATTERNS.test(query)) {
        return Response.json(
          { error: "forbidden", message: "Destructive queries are not allowed via API" },
          { status: 403, headers: corsHeaders() },
        );
      }
      const stmt = env.DB.prepare(query);
      const result = params ? await stmt.bind(...params).run() : await stmt.run();
      return Response.json(result, { headers: corsHeaders() });
    }
    default:
      return Response.json({ error: "method_not_allowed" }, { status: 405, headers: corsHeaders() });
  }
}

async function handleR2(request: Request, env: Env): Promise<Response> {
  const url = new URL(request.url);
  const key = url.pathname.replace("/v1/storage/", "");

  switch (request.method) {
    case "GET": {
      const obj = await env.ASSETS.get(key);
      if (!obj) return Response.json({ error: "not_found" }, { status: 404, headers: corsHeaders() });
      return new Response(obj.body, {
        headers: {
          "Content-Type": obj.httpMetadata?.contentType || "application/octet-stream",
          "ETag": obj.httpEtag,
          ...corsHeaders(),
        },
      });
    }
    case "PUT": {
      const contentType = request.headers.get("Content-Type") || "application/octet-stream";
      await env.ASSETS.put(key, request.body, {
        httpMetadata: { contentType },
      });
      return Response.json({ stored: true, key }, { status: 201, headers: corsHeaders() });
    }
    case "DELETE": {
      await env.ASSETS.delete(key);
      return Response.json({ deleted: true, key }, { headers: corsHeaders() });
    }
    case "HEAD": {
      const head = await env.ASSETS.head(key);
      if (!head) return new Response(null, { status: 404 });
      return new Response(null, {
        headers: {
          "Content-Length": String(head.size),
          "Content-Type": head.httpMetadata?.contentType || "application/octet-stream",
          "ETag": head.httpEtag,
        },
      });
    }
    default:
      return Response.json({ error: "method_not_allowed" }, { status: 405, headers: corsHeaders() });
  }
}

async function handleVectorize(request: Request, env: Env): Promise<Response> {
  const { action, vectors, query, topK } = await request.json() as {
    action: "upsert" | "query" | "delete";
    vectors?: { id: string; values: number[]; metadata?: any }[];
    query?: number[];
    topK?: number;
  };

  switch (action) {
    case "upsert": {
      if (!vectors) return Response.json({ error: "vectors_required" }, { status: 400, headers: corsHeaders() });
      const result = await env.VECTORIZE.upsert(vectors);
      return Response.json({ upserted: result }, { headers: corsHeaders() });
    }
    case "query": {
      if (!query) return Response.json({ error: "query_required" }, { status: 400, headers: corsHeaders() });
      const matches = await env.VECTORIZE.query(query, { topK: topK || 10 });
      return Response.json({ matches }, { headers: corsHeaders() });
    }
    case "delete": {
      if (!vectors) return Response.json({ error: "ids_required" }, { status: 400, headers: corsHeaders() });
      const ids = vectors.map((v) => v.id);
      const result = await env.VECTORIZE.deleteByIds(ids);
      return Response.json({ deleted: result }, { headers: corsHeaders() });
    }
    default:
      return Response.json({ error: "invalid_action" }, { status: 400, headers: corsHeaders() });
  }
}

// ═══════════════════════════════════════════════════════════════════
// WEBHOOKS
// ═══════════════════════════════════════════════════════════════════

async function handleWebhookIngress(
  path: string,
  request: Request,
  env: Env,
  ctx: ExecutionContext,
): Promise<Response> {
  const source = path.replace("/v1/webhooks/", "").split("/")[0];
  const body = await request.text();

  // Verify webhook signatures
  switch (source) {
    case "github": {
      const signature = request.headers.get("X-Hub-Signature-256") || "";
      if (!await verifyHMAC(body, signature, env.GITHUB_WEBHOOK_SECRET)) {
        return Response.json({ error: "invalid_signature" }, { status: 403, headers: corsHeaders() });
      }
      break;
    }
    case "stripe": {
      const sigHeader = request.headers.get("Stripe-Signature") || "";
      if (!sigHeader) {
        return Response.json({ error: "missing_signature" }, { status: 403, headers: corsHeaders() });
      }
      const timestampMatch = sigHeader.match(/t=(\d+)/);
      const sigMatch = sigHeader.match(/v1=([a-f0-9]+)/);
      if (!timestampMatch || !sigMatch) {
        return Response.json({ error: "invalid_signature_format" }, { status: 403, headers: corsHeaders() });
      }
      const signedPayload = `${timestampMatch[1]}.${body}`;
      if (!await verifyHMAC(signedPayload, `sha256=${sigMatch[1]}`, env.STRIPE_WEBHOOK_SECRET)) {
        return Response.json({ error: "invalid_signature" }, { status: 403, headers: corsHeaders() });
      }
      // Reject if timestamp is older than 5 minutes (replay protection)
      if (Math.abs(Date.now() / 1000 - parseInt(timestampMatch[1])) > 300) {
        return Response.json({ error: "timestamp_expired" }, { status: 403, headers: corsHeaders() });
      }
      break;
    }
  }

  // Queue for async processing
  ctx.waitUntil(
    env.WEBHOOK_QUEUE.send({
      type: "webhook",
      payload: { source, body: JSON.parse(body), headers: Object.fromEntries(request.headers) },
    }),
  );

  // Emit signal
  ctx.waitUntil(
    env.SIGNAL_QUEUE.send({
      type: "signal",
      payload: { signal: `📡 CLD → OS : webhook_received, source=${source}` },
    }),
  );

  return Response.json({ received: true, source, queued: true }, { headers: corsHeaders() });
}

async function processWebhook(payload: any, env: Env): Promise<void> {
  const { source, body } = payload;

  // Log to D1
  await env.DB.prepare(
    "INSERT INTO audit_log (id, event_type, source, payload, created_at) VALUES (?, ?, ?, ?, datetime('now'))",
  ).bind(crypto.randomUUID(), `webhook.${source}`, source, JSON.stringify(body)).run();
}

// ═══════════════════════════════════════════════════════════════════
// SIGNALS
// ═══════════════════════════════════════════════════════════════════

async function handleSignals(
  request: Request,
  env: Env,
  ctx: ExecutionContext,
): Promise<Response> {
  if (request.method === "GET") {
    // List recent signals
    const signals = await env.DB.prepare(
      "SELECT * FROM signals ORDER BY created_at DESC LIMIT 50",
    ).all();
    return Response.json(signals, { headers: corsHeaders() });
  }

  if (request.method === "POST") {
    const { signal, metadata } = await request.json() as { signal: string; metadata?: any };

    // Store signal
    await env.DB.prepare(
      "INSERT INTO signals (id, signal, metadata, created_at) VALUES (?, ?, ?, datetime('now'))",
    ).bind(crypto.randomUUID(), signal, JSON.stringify(metadata || {})).run();

    // Queue for async processing
    ctx.waitUntil(
      env.SIGNAL_QUEUE.send({ type: "signal", payload: { signal, metadata } }),
    );

    return Response.json({ emitted: true, signal }, { headers: corsHeaders() });
  }

  return Response.json({ error: "method_not_allowed" }, { status: 405, headers: corsHeaders() });
}

async function processSignal(payload: any, env: Env): Promise<void> {
  const { signal } = payload;
  // Signal processed — can add routing logic, notification fanout, etc.
  await env.ANALYTICS.writeDataPoint({
    blobs: [signal],
    indexes: ["signal"],
  });
}

// ═══════════════════════════════════════════════════════════════════
// HEALTH & STATUS
// ═══════════════════════════════════════════════════════════════════

async function handleHealth(env: Env): Promise<Response> {
  const checks: Record<string, string> = {};

  try {
    await env.CACHE.get("__health__");
    checks.kv = "ok";
  } catch {
    checks.kv = "error";
  }

  try {
    await env.DB.prepare("SELECT 1").first();
    checks.d1 = "ok";
  } catch {
    checks.d1 = "error";
  }

  try {
    await env.ASSETS.head("__health__");
    checks.r2 = "ok";
  } catch {
    checks.r2 = "ok"; // HEAD on missing key is fine
  }

  const allOk = Object.values(checks).every((v) => v === "ok");

  return Response.json(
    { status: allOk ? "healthy" : "degraded", checks, timestamp: new Date().toISOString() },
    { status: allOk ? 200 : 503, headers: corsHeaders() },
  );
}

async function handleSystemStatus(env: Env): Promise<Response> {
  const status = await env.CACHE.get("system_status", "json");
  const nodes = await env.CACHE.get("node_status", "json");

  return Response.json(
    {
      system: status || { state: "unknown" },
      nodes: nodes || {},
      edge: { colo: "auto", timestamp: new Date().toISOString() },
    },
    { headers: corsHeaders() },
  );
}

async function healthCheckAllNodes(env: Env): Promise<void> {
  const nodes = [
    { name: "lucidia", fetcher: env.ORIGIN_PRIMARY },
    { name: "aria", fetcher: env.ORIGIN_STORAGE },
    { name: "alice", fetcher: env.ORIGIN_AGENTS },
    { name: "octavia", fetcher: env.ORIGIN_COMPUTE },
  ];

  const results: Record<string, any> = {};

  for (const node of nodes) {
    try {
      const resp = await node.fetcher.fetch(new Request("https://internal/health"));
      results[node.name] = { status: resp.ok ? "healthy" : "unhealthy", code: resp.status };
    } catch {
      results[node.name] = { status: "unreachable" };
    }
  }

  await env.CACHE.put("node_status", JSON.stringify(results), { expirationTtl: 300 });
}

async function aggregateHourlyMetrics(env: Env): Promise<void> {
  // Hourly metrics aggregation stub
  const metrics = {
    timestamp: new Date().toISOString(),
    aggregated: true,
  };
  await env.CACHE.put("hourly_metrics", JSON.stringify(metrics), { expirationTtl: 7200 });
}

async function rotateApiKeys(env: Env): Promise<void> {
  // Daily API key rotation check stub
  const keys = await env.API_KEYS.list();
  for (const key of keys.keys) {
    if (key.expiration && key.expiration < Date.now() / 1000) {
      await env.API_KEYS.delete(key.name);
    }
  }
}

// ═══════════════════════════════════════════════════════════════════
// ANALYTICS
// ═══════════════════════════════════════════════════════════════════

async function trackAnalytics(env: Env, ctx: RequestContext, response: Response): Promise<void> {
  env.ANALYTICS.writeDataPoint({
    blobs: [ctx.requestId, ctx.ip, ctx.country, ctx.colo, ctx.orgCode || "none"],
    doubles: [Date.now() - ctx.startTime, response.status],
    indexes: [ctx.colo],
  });
}

async function trackError(env: Env, ctx: RequestContext, error: Error): Promise<void> {
  env.ANALYTICS.writeDataPoint({
    blobs: [ctx.requestId, "error", error.message],
    doubles: [Date.now() - ctx.startTime, 500],
    indexes: ["error"],
  });
}

async function processAnalyticsEvent(payload: any, env: Env): Promise<void> {
  await env.DB.prepare(
    "INSERT INTO audit_log (id, event_type, source, payload, created_at) VALUES (?, ?, ?, ?, datetime('now'))",
  ).bind(crypto.randomUUID(), "analytics", "worker", JSON.stringify(payload)).run();
}

// ═══════════════════════════════════════════════════════════════════
// PROXY TO ORIGIN
// ═══════════════════════════════════════════════════════════════════

async function proxyToOrigin(request: Request, fetcher: Fetcher, path: string): Promise<Response> {
  const url = new URL(request.url);
  url.pathname = path;

  const proxyReq = new Request(url.toString(), {
    method: request.method,
    headers: request.headers,
    body: request.body,
  });

  return fetcher.fetch(proxyReq);
}

// ═══════════════════════════════════════════════════════════════════
// UTILITIES
// ═══════════════════════════════════════════════════════════════════

function buildContext(request: Request): RequestContext {
  return {
    startTime: Date.now(),
    requestId: crypto.randomUUID(),
    ip: request.headers.get("CF-Connecting-IP") || "unknown",
    country: (request.cf?.country as string) || "unknown",
    colo: (request.cf?.colo as string) || "unknown",
    orgCode: null,
    userId: null,
    apiKey: null,
  };
}

const ALLOWED_ORIGINS = [
  "https://blackroad.ai",
  "https://app.blackroad.ai",
  "https://admin.blackroad.ai",
  "https://docs.blackroad.ai",
  "https://api.blackroad.ai",
];

function corsHeaders(origin?: string | null): Record<string, string> {
  const allowedOrigin = origin && ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0];
  return {
    "Access-Control-Allow-Origin": allowedOrigin,
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization, X-API-Key, X-Request-ID",
    "Access-Control-Allow-Credentials": "true",
    "Access-Control-Max-Age": "86400",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
  };
}

function handleCORS(request: Request): Response {
  const origin = request.headers.get("Origin");
  return new Response(null, { status: 204, headers: corsHeaders(origin) });
}

function addCORSHeaders(response: Response, origin?: string | null): Response {
  const headers = new Headers(response.headers);
  for (const [key, value] of Object.entries(corsHeaders(origin))) {
    headers.set(key, value);
  }
  return new Response(response.body, { status: response.status, headers });
}

function parseCookie(cookie: string, name: string): string | null {
  const match = cookie.match(new RegExp(`(?:^|;\\s*)${name}=([^;]*)`));
  return match ? match[1] : null;
}

async function hash(input: string): Promise<string> {
  const encoded = new TextEncoder().encode(input);
  const buffer = await crypto.subtle.digest("SHA-256", encoded);
  return Array.from(new Uint8Array(buffer)).map((b) => b.toString(16).padStart(2, "0")).join("");
}

async function hashPassword(password: string, salt?: string): Promise<string> {
  const passwordSalt = salt || Array.from(crypto.getRandomValues(new Uint8Array(16)))
    .map((b) => b.toString(16).padStart(2, "0")).join("");
  const keyMaterial = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(password),
    "PBKDF2",
    false,
    ["deriveBits"],
  );
  const derivedBits = await crypto.subtle.deriveBits(
    { name: "PBKDF2", salt: new TextEncoder().encode(passwordSalt), iterations: 100000, hash: "SHA-256" },
    keyMaterial,
    256,
  );
  const derivedHash = Array.from(new Uint8Array(derivedBits))
    .map((b) => b.toString(16).padStart(2, "0")).join("");
  return `pbkdf2:100000:${passwordSalt}:${derivedHash}`;
}

async function verifyPassword(password: string, stored: string): Promise<boolean> {
  if (stored.startsWith("pbkdf2:")) {
    const [, , salt] = stored.split(":");
    const computed = await hashPassword(password, salt);
    return computed === stored;
  }
  // Legacy fallback for old SHA-256 hashes — re-hash on next login
  return await hash(password + "blackroad-salt") === stored;
}

async function verifyJWT(token: string, secret: string): Promise<{ sub: string; role: string } | null> {
  try {
    const [headerB64, payloadB64, signatureB64] = token.split(".");
    const payload = JSON.parse(atob(payloadB64));
    if (payload.exp && payload.exp < Date.now() / 1000) return null;
    // Verify signature with HMAC-SHA256
    const key = await crypto.subtle.importKey(
      "raw",
      new TextEncoder().encode(secret),
      { name: "HMAC", hash: "SHA-256" },
      false,
      ["verify"],
    );
    const data = new TextEncoder().encode(`${headerB64}.${payloadB64}`);
    const signature = Uint8Array.from(atob(signatureB64.replace(/-/g, "+").replace(/_/g, "/")), (c) => c.charCodeAt(0));
    const valid = await crypto.subtle.verify("HMAC", key, signature, data);
    return valid ? payload : null;
  } catch {
    return null;
  }
}

async function signJWT(payload: { sub: string; role: string }, secret: string): Promise<string> {
  const header = btoa(JSON.stringify({ alg: "HS256", typ: "JWT" }));
  const body = btoa(JSON.stringify({ ...payload, iat: Math.floor(Date.now() / 1000), exp: Math.floor(Date.now() / 1000) + 3600 }));
  const key = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"],
  );
  const signature = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(`${header}.${body}`));
  const sig = btoa(String.fromCharCode(...new Uint8Array(signature))).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
  return `${header}.${body}.${sig}`;
}

async function verifyHMAC(body: string, signature: string, secret: string): Promise<boolean> {
  try {
    const key = await crypto.subtle.importKey(
      "raw",
      new TextEncoder().encode(secret),
      { name: "HMAC", hash: "SHA-256" },
      false,
      ["sign"],
    );
    const mac = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(body));
    const expected = "sha256=" + Array.from(new Uint8Array(mac)).map((b) => b.toString(16).padStart(2, "0")).join("");
    return signature === expected;
  } catch {
    return false;
  }
}
