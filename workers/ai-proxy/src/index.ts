/**
 * BlackRoad AI Proxy Worker
 *
 * Unified proxy for all AI vendor APIs.  No client ever calls OpenAI,
 * Anthropic, or any other vendor directly — every request flows through
 * this Cloudflare Worker so BlackRoad owns the traffic path.
 *
 * Supported vendor routes (all behind api.blackroad.ai/v1/ai/):
 *   /v1/ai/openai/*    → api.openai.com
 *   /v1/ai/anthropic/* → api.anthropic.com
 *   /v1/ai/local/*     → Cloudflare Workers AI (on-edge, no external call)
 *   /v1/ai/complete    → smart router: tries local → openai → anthropic
 *   /v1/ai/embed       → smart router: local embeddings first
 *
 * Auth: every inbound request must carry a valid BlackRoad JWT
 *       (issued by api.blackroad.ai/v1/auth/login).
 */

export interface Env {
  // KV
  API_KEYS: KVNamespace;
  RATE_LIMITS: KVNamespace;

  // Workers AI (Cloudflare on-edge inference)
  AI: Ai;

  // Analytics
  ANALYTICS: AnalyticsEngineDataset;

  // Secrets
  OPENAI_API_KEY: string;
  ANTHROPIC_API_KEY: string;
  BLACKROAD_JWT_SECRET: string;

  // Vars
  ENVIRONMENT: string;
  AI_PROVIDER_PRIORITY: string;
}

// ─── Vendor upstream bases ────────────────────────────────────────
const VENDORS: Record<string, string> = {
  openai: "https://api.openai.com",
  anthropic: "https://api.anthropic.com",
};

// ─── Entry point ─────────────────────────────────────────────────
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    if (request.method === "OPTIONS") return corsResponse();

    const url = new URL(request.url);
    const path = url.pathname;

    // ── Health check (public) ─────────────────────────────────────
    if (path === "/health" || path === "/v1/ai/health") {
      return jsonResponse({ status: "ok", service: "blackroad-ai-proxy" });
    }

    // ── Auth: require valid BlackRoad JWT ─────────────────────────
    const authError = await validateAuth(request, env);
    if (authError) return authError;

    // ── Route to vendor ───────────────────────────────────────────
    const segments = path.replace(/^\/v1\/ai\//, "").split("/");
    const vendor = segments[0];

    try {
      if (vendor === "local") {
        return await handleLocal(request, env, segments.slice(1));
      }
      if (vendor === "complete") {
        return await handleSmartComplete(request, env, ctx);
      }
      if (vendor === "embed") {
        return await handleSmartEmbed(request, env);
      }
      if (vendor in VENDORS) {
        return await proxyToVendor(request, env, vendor, segments.slice(1));
      }
    } catch (err: any) {
      return jsonResponse({ error: err.message }, 502);
    }

    return jsonResponse({ error: "Unknown AI vendor route", path }, 404);
  },
};

// ─── Auth validation ─────────────────────────────────────────────
async function validateAuth(request: Request, env: Env): Promise<Response | null> {
  const authHeader = request.headers.get("Authorization") ?? "";
  const token = authHeader.startsWith("Bearer ") ? authHeader.slice(7) : null;

  // API-key auth (stored in KV)
  const xApiKey = request.headers.get("x-blackroad-api-key");
  if (xApiKey) {
    const valid = await env.API_KEYS.get(`key:${xApiKey}`);
    if (valid) return null;
  }

  if (!token) {
    return jsonResponse({ error: "Unauthorized — BlackRoad JWT required" }, 401);
  }

  // Lightweight JWT signature check (HS256)
  const ok = await verifyJwt(token, env.BLACKROAD_JWT_SECRET);
  if (!ok) {
    return jsonResponse({ error: "Unauthorized — invalid or expired token" }, 401);
  }

  return null;
}

// ─── Proxy to an external vendor ─────────────────────────────────
async function proxyToVendor(
  request: Request,
  env: Env,
  vendor: string,
  pathSegments: string[]
): Promise<Response> {
  const base = VENDORS[vendor];
  const vendorPath = "/" + pathSegments.join("/");
  const url = new URL(request.url);
  const targetUrl = `${base}${vendorPath}${url.search}`;

  // Build forwarded headers — inject vendor auth, strip client auth
  const headers = new Headers(request.headers);
  headers.delete("Authorization");
  headers.delete("x-blackroad-api-key");
  headers.set("User-Agent", "BlackRoad-AI-Proxy/1.0");

  if (vendor === "openai") {
    headers.set("Authorization", `Bearer ${env.OPENAI_API_KEY}`);
  } else if (vendor === "anthropic") {
    headers.set("x-api-key", env.ANTHROPIC_API_KEY);
    headers.set("anthropic-version", "2023-06-01");
  }

  const upstream = await fetch(targetUrl, {
    method: request.method,
    headers,
    body: request.method !== "GET" && request.method !== "HEAD" ? request.body : null,
  });

  // Forward the upstream response, adding CORS headers
  const response = new Response(upstream.body, upstream);
  response.headers.set("Access-Control-Allow-Origin", "*");
  response.headers.set("x-blackroad-vendor", vendor);
  response.headers.set("x-blackroad-proxy", "1");
  return response;
}

// ─── Local inference (Cloudflare Workers AI) ─────────────────────
async function handleLocal(
  request: Request,
  env: Env,
  pathSegments: string[]
): Promise<Response> {
  const action = pathSegments[0] ?? "complete";
  const body = await request.json<Record<string, unknown>>();

  if (action === "complete" || action === "chat" || action === "completions") {
    const messages = (body.messages as Array<{ role: string; content: string }>) ?? [
      { role: "user", content: String(body.prompt ?? body.input ?? "") },
    ];
    const result = await env.AI.run("@cf/meta/llama-3.1-8b-instruct", { messages });
    return jsonResponse({ provider: "cloudflare-workers-ai", ...result });
  }

  if (action === "embed" || action === "embeddings") {
    const text = String(body.input ?? body.text ?? "");
    const result = await env.AI.run("@cf/baai/bge-base-en-v1.5", { text });
    return jsonResponse({ provider: "cloudflare-workers-ai", ...result });
  }

  return jsonResponse({ error: `Unknown local action: ${action}` }, 400);
}

// ─── Smart completion router ─────────────────────────────────────
// Priority: local (Workers AI) → openai → anthropic
async function handleSmartComplete(
  request: Request,
  env: Env,
  ctx: ExecutionContext
): Promise<Response> {
  const priority = env.AI_PROVIDER_PRIORITY.split(",").map((s) => s.trim());
  const body = await request.json<Record<string, unknown>>();

  for (const provider of priority) {
    try {
      if (provider === "local") {
        return await handleLocal(
          new Request(request.url, { method: "POST", headers: request.headers, body: JSON.stringify(body) }),
          env,
          ["complete"]
        );
      }
      if (provider in VENDORS) {
        // Map to the vendor's standard chat completions path
        const vendorPath =
          provider === "anthropic" ? ["v1", "messages"] : ["v1", "chat", "completions"];
        return await proxyToVendor(
          new Request(request.url, { method: "POST", headers: request.headers, body: JSON.stringify(body) }),
          env,
          provider,
          vendorPath
        );
      }
    } catch {
      // Provider failed — try next
      continue;
    }
  }

  return jsonResponse({ error: "All AI providers unavailable" }, 503);
}

// ─── Smart embedding router ───────────────────────────────────────
async function handleSmartEmbed(request: Request, env: Env): Promise<Response> {
  const body = await request.json<Record<string, unknown>>();
  try {
    return await handleLocal(
      new Request(request.url, { method: "POST", headers: request.headers, body: JSON.stringify(body) }),
      env,
      ["embed"]
    );
  } catch {
    return await proxyToVendor(
      new Request(request.url, { method: "POST", headers: request.headers, body: JSON.stringify(body) }),
      env,
      "openai",
      ["v1", "embeddings"]
    );
  }
}

// ─── JWT verification (HS256) ─────────────────────────────────────
async function verifyJwt(token: string, secret: string): Promise<boolean> {
  try {
    const parts = token.split(".");
    if (parts.length !== 3) return false;

    const enc = new TextEncoder();
    const key = await crypto.subtle.importKey(
      "raw",
      enc.encode(secret),
      { name: "HMAC", hash: "SHA-256" },
      false,
      ["verify"]
    );

    const data = enc.encode(`${parts[0]}.${parts[1]}`);
    const sig = Uint8Array.from(atob(parts[2].replace(/-/g, "+").replace(/_/g, "/")), (c) =>
      c.charCodeAt(0)
    );

    const valid = await crypto.subtle.verify("HMAC", key, sig, data);
    if (!valid) return false;

    const payload = JSON.parse(atob(parts[1].replace(/-/g, "+").replace(/_/g, "/")));
    return !payload.exp || payload.exp > Math.floor(Date.now() / 1000);
  } catch {
    return false;
  }
}

// ─── Helpers ─────────────────────────────────────────────────────
function jsonResponse(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
      "x-blackroad-proxy": "1",
    },
  });
}

function corsResponse(): Response {
  return new Response(null, {
    status: 204,
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type, Authorization, x-blackroad-api-key, x-api-key",
    },
  });
}
