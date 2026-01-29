# Test Coverage Analysis

## Executive Summary

The BlackRoad codebase contains **73 Python source files** across **6,262 lines of code**, spanning 7 prototype modules and 7 template modules. **There are currently zero test files in the entire repository.** The CI pipeline (`ci.yml`) includes test jobs that either fall through to inline smoke checks or print "No tests yet." Test dependencies in `requirements.txt` files are commented out.

Despite this, the code is well-structured for testing: it uses dataclasses, abstract base classes, dependency injection, and already includes a `MockServiceClient`. The gap between testable architecture and actual test coverage is significant.

---

## Current State

| Metric | Value |
|---|---|
| Python source files | 73 |
| Lines of code | ~6,262 |
| Test files | **0** |
| Test directories | **0** |
| Test config files (pytest.ini, etc.) | **0** |
| CI test jobs | 3 (operator, dispatcher, webhooks) |
| CI test jobs running real pytest | **0** (all fall through to inline scripts) |
| Test dependencies installed | No (commented out in requirements.txt) |

---

## Priority 1: Operator Classification (Critical)

**Files:** `prototypes/operator/routing/core/classifier.py`, `parser.py`, `router.py`

The classifier is the decision-making core that routes every request to one of 15 organizations based on regex pattern matching and keyword scoring. Misclassification sends requests to the wrong org entirely.

### What to test

- **Classifier.classify()** for each of the 14 categories (ai, crm, storage, security, infrastructure, hardware, metaverse, media, education, governance, design, commerce, enterprise, experiment). Verify correct `org_code` and `category` for unambiguous inputs.
- **Ambiguous queries** that match multiple categories (e.g., "deploy the AI model" matches both `infrastructure` and `ai`). Verify the highest-scoring category wins.
- **Empty/nonsense input** falls back to `ai`/`AI` with confidence 0.5.
- **Confidence normalization** stays in range [0, 1.0] regardless of how many patterns match.
- **Parser._detect_type()** correctly distinguishes TEXT, HTTP, WEBHOOK, SIGNAL, and CLI inputs based on content shape.
- **Parser._parse_signal()** correctly splits signal-format strings on `:`.
- **Operator.route()** end-to-end: input string -> RouteResult with correct org, signal string, and confidence.
- **Operator.route_batch()** processes lists correctly.
- **Operator history** stays bounded at 1000 entries (trim to 500 at overflow).
- **Operator.stats** computes correct totals, per-org counts, and average confidence.

### Why this matters

Every other module downstream depends on correct classification. A bug here cascades through dispatching and webhook routing.

---

## Priority 2: Dispatcher Routing (Critical)

**Files:** `prototypes/dispatcher/dispatcher/core.py`, `registry.py`, `client.py`

The dispatcher takes classified requests and routes them to actual service endpoints. It integrates the registry, the operator, and the HTTP client.

### What to test

- **Registry._load()** parses `routes/registry.yaml` correctly: all 15 orgs loaded, services populated with correct fields (name, endpoint, health, type, provider, nodes).
- **Registry.get_org()** returns the correct `Org` for valid codes and `None` for invalid codes.
- **Registry.get_service()** returns correct `Service` for valid org+service combos.
- **Registry.get_endpoint()** with explicit service name, with default service, and with fallback when no default exists.
- **Registry.match()** applies routing rules in priority order and returns `(org_code, service_name)`. Test that higher-priority rules take precedence.
- **RoutingRule.matches()** correctly applies regex patterns (case-insensitive).
- **Registry with missing/malformed YAML** handles gracefully without crashing.
- **Dispatcher.dispatch()** (async, using `MockServiceClient`):
  - Routes to correct org when operator classification succeeds.
  - Falls back to registry pattern matching when operator is unavailable.
  - Returns error result when org is unknown.
  - Returns error result when no service is found.
  - Tracks latency in result.
  - Appends to history.
- **Dispatcher.dispatch_to()** (async):
  - Routes directly to specified org/service.
  - Returns error for unknown org.
  - Returns error for unknown service.
  - Uses default service when service_name is None.
- **Dispatcher._category_to_service()** maps classification categories to service names correctly, with fallback to first service.
- **Dispatcher.list_routes()** returns all org/service combinations.
- **Dispatcher.stats** computes success_rate, by_org counts, and avg_latency correctly. Empty history returns zeroed stats.
- **DispatchResult.__post_init__** generates correct signal strings for success vs. failure cases.

---

## Priority 3: Webhook Processing (High)

**Files:** `prototypes/webhooks/webhooks/receiver.py`, `signal.py`, `handlers/*.py`

The webhook system is the external interface — it receives events from GitHub, Stripe, Salesforce, Cloudflare, Slack, Google, and Figma, then converts them to internal signals.

### What to test

- **WebhookReceiver.process()**:
  - Invalid JSON body returns error result.
  - No matching handler returns error result.
  - Signature verification failure (when secret is set) returns error result.
  - Handler parse exception returns error result.
  - Successful processing returns result with signal, handler name, and verified flag.
  - Processing time is tracked.
  - History is appended.
- **WebhookReceiver._find_handler()**:
  - `provider_hint` selects the named handler directly.
  - Without hint, `can_handle()` is called on each handler in order.
- **GitHubHandler.can_handle()** returns true when `X-GitHub-Event` header is present.
- **GitHubHandler.verify()** validates HMAC-SHA256 signatures correctly. Test with valid signature, invalid signature, and missing signature.
- **GitHubHandler.parse()** for each event type (push, pull_request, issues, workflow_run, release, ping) extracts the correct signal type and data fields.
- **GitHubHandler._determine_target()** maps repo org prefixes to correct org codes; defaults to `OS` for unknown repos.
- **StripeHandler, SalesforceHandler, CloudflareHandler, SlackHandler, GoogleHandler, FigmaHandler**: each handler's `can_handle()`, `parse()`, and `verify()` methods need basic coverage.
- **Signal dataclass**:
  - `__post_init__` generates deterministic ID from type+source+timestamp.
  - `format()` produces correct signal string with emoji.
  - `to_dict()` / `from_dict()` round-trip correctly.
  - `_get_emoji()` returns correct emoji for known types and fallback for unknown.
- **WebhookResult.to_dict()** serializes correctly with and without a signal.
- **WebhookReceiver.stats** computes correct totals, success rate, avg processing time, and per-handler/signal-type breakdowns. Empty history returns zeroed stats.

---

## Priority 4: Data Models and Serialization (Medium)

**Files:** Various dataclass definitions across all modules

### What to test

- **DispatchResult, RouteResult, WebhookResult, Classification, Request, CodeMetrics**: `to_dict()` methods produce expected key sets and value types.
- **Signal.from_dict()** reconstructs correctly from `to_dict()` output (round-trip).
- **Org.get_service()** and **Org.default_service()** edge cases: empty services dict returns `None`.
- **Service dataclass** optional fields default correctly.

---

## Priority 5: Metrics and Counter (Medium)

**Files:** `prototypes/metrics/metrics/counter.py`, `health.py`, `dashboard.py`

### What to test

- **Counter._count_files()** correctly counts files and lines, skips `.git`/`node_modules`/`__pycache__` directories, and categorizes by extension.
- **Counter._count_orgs()** counts org directories and repo definitions from `REPOS.md` files.
- **Counter._count_commits()** handles the case where `git` is not available or returns an error.
- **Counter.quick_count()** returns dict with expected keys.
- **Counter.format_summary()** returns a string (smoke test, no crashes).
- **CodeMetrics.to_dict()** returns all expected keys.

---

## Priority 6: AI Router Template (Medium)

**Files:** `templates/ai-router/ai_router/routing/router.py`, `strategy.py`, `providers/*.py`, `tracking/costs.py`

### What to test

- **Provider base class** contract: subclasses implement required abstract methods.
- **Routing strategy** selection logic: round-robin, cost-based, latency-based, or fallback.
- **Cost tracking** accumulates and reports costs correctly.
- **Router** selects the correct provider based on strategy and request parameters.

---

## Priority 7: YAML Configuration Validation (Low)

**Files:** `routes/registry.yaml`, `nodes/*.yaml`, `templates/*/config.yaml`

### What to test

- **All 7 node configs** parse without errors and contain required `node` key.
- **registry.yaml** contains `orgs` and `rules` keys; every org has at least a name and one service.
- **Template configs** parse correctly and contain expected structure.

These are partially covered by the `validate-config` CI job inline scripts, but proper pytest tests would be more maintainable and give better failure diagnostics.

---

## Recommended Test Infrastructure Setup

### 1. Create test directories

```
prototypes/operator/tests/
prototypes/dispatcher/tests/
prototypes/webhooks/tests/
prototypes/metrics/tests/
templates/ai-router/tests/
```

### 2. Add pytest configuration

Create `pyproject.toml` at the repo root:

```toml
[tool.pytest.ini_options]
testpaths = [
    "prototypes/operator/tests",
    "prototypes/dispatcher/tests",
    "prototypes/webhooks/tests",
    "prototypes/metrics/tests",
]
asyncio_mode = "auto"
```

### 3. Uncomment test dependencies

In each `requirements.txt`, enable:

```
pytest>=7.0.0
pytest-asyncio>=0.21.0
```

### 4. Update CI to run real pytest

Replace inline Python scripts in `ci.yml` with:

```yaml
- name: Run tests
  run: python -m pytest tests/ -v --tb=short
```

### 5. Suggested first test files

Listed in order of impact:

| File | Tests | Rationale |
|---|---|---|
| `prototypes/operator/tests/test_classifier.py` | ~20 tests | Core routing brain, pure logic, no dependencies |
| `prototypes/operator/tests/test_parser.py` | ~10 tests | Input normalization, pure logic |
| `prototypes/dispatcher/tests/test_registry.py` | ~15 tests | Registry loading and lookup, uses YAML fixture |
| `prototypes/webhooks/tests/test_receiver.py` | ~12 tests | Webhook processing pipeline, uses handler mocks |
| `prototypes/webhooks/tests/test_github_handler.py` | ~10 tests | Most complex handler, HMAC verification |
| `prototypes/webhooks/tests/test_signal.py` | ~8 tests | Signal model serialization round-trips |
| `prototypes/dispatcher/tests/test_dispatcher.py` | ~12 tests | Async dispatch with MockServiceClient |
| `prototypes/operator/tests/test_router.py` | ~8 tests | End-to-end operator routing |
| `prototypes/metrics/tests/test_counter.py` | ~6 tests | File counting with temp directory fixtures |

**Estimated total: ~100 tests** to achieve meaningful coverage of all critical paths.

---

## Risk Areas With No Coverage

These are specific code paths that are most likely to harbor bugs without test coverage:

1. **Classifier tie-breaking**: When two categories score identically, `max()` picks arbitrarily by dict key iteration order. This is not deterministic across Python versions.
2. **Registry fallback chain**: `get_endpoint()` has a 3-level fallback (explicit service -> default service config -> first service). Each level can return `None`.
3. **HMAC verification in GitHubHandler**: Uses `hmac.new()` which should be `hmac.new` — this code has never been exercised by tests and may contain a runtime error (`hmac.new` vs `hmac.HMAC`).
4. **Dispatcher operator lazy-loading**: The `sys.path` manipulation in `core.py:17` to import the operator module is fragile and path-dependent.
5. **WebhookReceiver with secrets**: The interaction between `secrets.get(handler.name)` and `handler.verify()` has a subtle logic branch where a missing secret skips verification entirely — this should be explicitly tested.
6. **Signal ID generation**: The hash is based on type+source+timestamp but not the actual data content, meaning two signals of the same type from the same source within the same second get the same ID.
