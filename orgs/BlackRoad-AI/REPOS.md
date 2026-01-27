# BlackRoad-AI Repositories

> Repo specs for the AI org

---

## Repository List

### `router` (P0 - Build First)

**Purpose:** The brain that routes requests to the right model/tool

**Structure:**
```
router/
├── src/
│   ├── main.py           ← FastAPI entry
│   ├── router.py         ← Core routing logic
│   ├── intent.py         ← Intent classification
│   ├── providers/
│   │   ├── claude.py     ← Anthropic API wrapper
│   │   ├── openai.py     ← OpenAI API wrapper
│   │   ├── hailo.py      ← Local Hailo-8 inference
│   │   ├── numpy_tools.py← Math/science tools
│   │   └── database.py   ← Database lookups
│   └── middleware/
│       ├── auth.py       ← Authentication
│       ├── rate_limit.py ← Rate limiting
│       └── logging.py    ← Request logging
├── tests/
├── configs/
│   └── models.yaml       ← Model configs
├── Dockerfile
└── README.md
```

**Key Endpoints:**
```
POST /route          ← Main routing endpoint
POST /chat           ← Conversational interface
GET  /models         ← List available models
GET  /health         ← Health check
```

---

### `prompts` (P0 - Build First)

**Purpose:** Prompt library and Cece's personality

**Structure:**
```
prompts/
├── cece/
│   ├── system.md         ← Core system prompt
│   ├── style.md          ← Communication style guide
│   ├── memory.md         ← Persistent memory template
│   └── capabilities.md   ← What Cece can do
├── templates/
│   ├── code_review.md    ← Code review prompt
│   ├── summarize.md      ← Summarization prompt
│   ├── analyze.md        ← Analysis prompt
│   └── ...
├── tools/
│   ├── function_call.md  ← Tool use prompts
│   └── ...
└── README.md
```

---

### `agents` (P1)

**Purpose:** Autonomous agent definitions

**Structure:**
```
agents/
├── definitions/
│   ├── researcher.yaml   ← Research agent
│   ├── coder.yaml        ← Coding agent
│   ├── reviewer.yaml     ← Review agent
│   └── ...
├── orchestration/
│   ├── runner.py         ← Agent runner
│   ├── memory.py         ← Agent memory
│   └── tools.py          ← Agent tools
├── examples/
└── README.md
```

---

### `hailo` (P1)

**Purpose:** Hailo-8 inference code for octavia

**Structure:**
```
hailo/
├── src/
│   ├── inference.py      ← Core inference
│   ├── models/           ← Model definitions
│   └── utils/
├── models/               ← Compiled Hailo models (.hef)
├── benchmarks/
├── deploy/
│   └── octavia.sh        ← Deploy to octavia node
└── README.md
```

---

### `models` (P1)

**Purpose:** Model configurations and API wrappers

**Structure:**
```
models/
├── configs/
│   ├── claude.yaml       ← Claude models config
│   ├── openai.yaml       ← OpenAI models config
│   ├── local.yaml        ← Local models config
│   └── ...
├── wrappers/
│   ├── base.py           ← Base model wrapper
│   ├── anthropic.py      ← Anthropic wrapper
│   ├── openai.py         ← OpenAI wrapper
│   └── ...
├── rate_limits/
└── README.md
```

---

### `eval` (P2)

**Purpose:** Evaluation and benchmarking

**Structure:**
```
eval/
├── benchmarks/
│   ├── routing_accuracy.py
│   ├── latency.py
│   └── cost.py
├── datasets/
├── reports/
└── README.md
```

---

## Repo Creation Order

```
1. router     ← Core functionality
2. prompts    ← Cece's personality
3. agents     ← Autonomous agents
4. hailo      ← Edge AI
5. models     ← Model management
6. eval       ← Testing/benchmarking
```

---

## Signals on Creation

When each repo is created:
```
✔️ AI → OS : router created
✔️ AI → OS : prompts created
...
✔️ AI → OS : All repos initialized
```

---

*Each repo is a piece of the routing layer.*
