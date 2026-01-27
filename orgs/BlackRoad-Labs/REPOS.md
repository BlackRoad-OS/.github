# BlackRoad-Labs Repositories

> Repo specs for the Labs org

---

## Repository List

### `experiments` (Primary)

**Purpose:** Active experiments with structure

**Structure:**
```
experiments/
├── 2026-01-routing-benchmark/
│   ├── README.md
│   ├── RESULTS.md
│   ├── src/
│   │   ├── benchmark.py
│   │   └── analyze.py
│   └── data/
│       └── results.csv
├── 2026-01-hailo-latency/
│   └── ...
├── 2026-02-lora-range/
│   └── ...
└── README.md
```

**Naming:** `YYYY-MM-descriptive-name`

---

### `prototypes` (Working Demos)

**Purpose:** Experiments that proved out, now being refined

**Structure:**
```
prototypes/
├── mini-router/
│   ├── README.md
│   ├── src/
│   ├── tests/
│   └── GRADUATION.md     ← Plan for moving to prod
├── hailo-server/
│   └── ...
└── README.md
```

---

### `research` (Permanent)

**Purpose:** Research notes, papers, analysis

**Structure:**
```
research/
├── routing/
│   ├── latency-analysis.md
│   └── scaling-models.md
├── ai/
│   ├── model-comparison.md
│   └── hailo-benchmarks.md
├── mesh/
│   ├── tailscale-deep-dive.md
│   └── lora-protocols.md
└── README.md
```

---

### `sandbox` (Ephemeral)

**Purpose:** Quick throwaway tests

**Structure:**
```
sandbox/
├── test-1/               ← Delete whenever
├── trying-thing/
├── what-if/
└── README.md             ← "Everything here is temporary"
```

**Rule:** Anything in sandbox can be deleted without warning.

---

### `archive` (Historical)

**Purpose:** Graduated and failed experiments

**Structure:**
```
archive/
├── graduated/
│   ├── 2026-01-feature-x/
│   │   ├── README.md
│   │   └── GRADUATION.md  ← Where it went
│   └── ...
├── failed/
│   ├── 2026-01-idea-y/
│   │   ├── README.md
│   │   └── POST_MORTEM.md ← Why it failed
│   └── ...
└── README.md
```

---

## Experiment Template

When starting a new experiment:

```bash
# Create experiment
mkdir -p experiments/2026-01-my-experiment/{src,data}

# Create README
cat > experiments/2026-01-my-experiment/README.md << 'EOF'
# Experiment: My Experiment

## Hypothesis
[What we're testing]

## Approach
[How we're testing it]

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Timeline
Start: 2026-01-27
End: 2026-02-03 (1 week)

## Status
[x] Sandbox → [ ] Experiment → [ ] Prototype → [ ] Graduate

## Notes
[Running notes]
EOF
```

---

## Graduation Checklist

Before an experiment graduates to a production org:

- [ ] Tests passing
- [ ] Documentation complete
- [ ] Performance validated
- [ ] Security reviewed
- [ ] Target org identified
- [ ] Migration plan written
- [ ] Stakeholder sign-off (Alexa)

---

*Experiments are cheap. Knowledge is expensive.*
