# Templates — GitHub `isTemplate` flow

tz-forge supports **two** ways to start a repo:

1. **`tz-new` (preferred)** — config-as-code, assistant profiles, module composition  
2. **GitHub “Use this template”** — when this repo (or thin child templates) has **`isTemplate=true`**

## Marking a repo as a template

On GitHub:

- UI: **Settings → General → Template repository** (check)  
- API:

```bash
# requires admin on the repo
gh api -X PATCH repos/tzervas/tz-forge \
  -f is_template=true

# verify
gh api repos/tzervas/tz-forge --jq '.is_template'
```

After `is_template=true`, the green **Use this template** button appears on the repo home page.

### What “Use this template” gives you

- Full tree of **tz-forge itself** (modules + CLI), not a single product kind  
- You still run `tz-new` locally (or copy a `project-kinds` selection) to produce a product repo  

For a **product-shaped** template, either:

```bash
# A) Preferred: generate then push as its own template
python cli/tz_new.py rust-lib my-lib --assistant=humans-only --create-github
gh api -X PATCH repos/tzervas/my-lib -f is_template=true
```

or keep thin stubs under future `templates/<kind>/` that only document the 5-minute path and point at `tz-new`.

## 5-minute paths (golden kinds)

### 1. `rust-lib`

```bash
git clone https://github.com/tzervas/tz-forge.git && cd tz-forge
python cli/tz_new.py rust-lib /tmp/my-lib --assistant=solo-ai
cd /tmp/my-lib
# optional: cargo init already done via skeleton
./scripts/check.sh          # fmt + clippy -D warnings + build + test
# humans-only (no AI files):
# python cli/tz_new.py rust-lib /tmp/my-lib-human --assistant=humans-only
```

### 2. `python-mcp`

```bash
python cli/tz_new.py python-mcp /tmp/my-mcp --assistant=solo-ai
cd /tmp/my-mcp
# uv sync && uv run pytest -q   # when deps installed
./scripts/check.sh
# entry: src/<name>/server.py
```

### 3. `ml-rust-crate`

```bash
python cli/tz_new.py ml-rust-crate /tmp/my-ml-rs --assistant=fractal-swarm
cd /tmp/my-ml-rs
./scripts/check.sh --quick
# skills: skills/train-smoke, skills/hf-model-card (+ generic pack)
# compose: docs/compose/agent-harness.md
```

### 4. `agent-swarm`

```bash
python cli/tz_new.py agent-swarm /tmp/my-wave --assistant=fractal-swarm
cd /tmp/my-wave
# fractal AGENTS + kickoffs + harness/cabal/security compose docs
ls docs/compose/
# sibling tools (by reference — do not vendor):
#   https://github.com/tzervas/agent-harness
#   https://github.com/tzervas/cabal-devmelopner
#   https://github.com/tzervas/security-mcp
```

## Assistant profiles (reminder)

| Profile | AI surface |
|---------|------------|
| `humans-only` | none |
| `solo-ai` | CLAUDE + AGENTS lite |
| `solo-ai-rich` | + skills + kickoffs |
| `fractal-swarm` | + fractal AGENTS, model policy, multi-skill, harness docs |

```bash
python cli/tz_new.py --list
python cli/tz_new.py rust-lib foo --assistant=humans-only
python cli/tz_new.py agent-swarm bar --assistant=fractal-swarm --skills=commit-prep,pr-review
```

## Non-goals

- Auto-enabling Copilot code reviews  
- Vendoring full agent-harness / cabal / mycelium into every template  
- Forcing AI files on `humans-only` projects  
