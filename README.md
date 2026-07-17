# tz-forge

<!-- FLEET-BADGES:BEGIN -->
[![CI](https://github.com/tzervas/tz-forge/actions/workflows/fleet-ci.yml/badge.svg?branch=main)](https://github.com/tzervas/tz-forge/actions/workflows/fleet-ci.yml?query=branch%3Amain)
[![Security](https://github.com/tzervas/tz-forge/actions/workflows/fleet-security.yml/badge.svg?branch=main)](https://github.com/tzervas/tz-forge/actions/workflows/fleet-security.yml?query=branch%3Amain)
<!-- FLEET-BADGES:END -->

**Composable dev-tooling meta repository** for the tzervas fleet.

tz-forge packages repeated CI, license, pre-commit, and AI coding-assistant surface
as **modules**, maps them to **project kinds**, and scaffolds new repos with **`tz-new`**
in under five minutes — with an explicit **assistant intensity** slider from
humans-only through fractal L0/L1 swarms.

This repo is a **GitHub template** (`isTemplate=true`). Prefer `tz-new` for config-as-code
product scaffolds; see [templates/README.md](templates/README.md).

| Piece | Role |
|-------|------|
| **Modules** | Copyable fragments under `modules/` (fleet, local-ci, deny, agents, skills, …) |
| **`tz-new`** | CLI (`cli/tz_new.py`) — kinds, `--assistant=`, `--skills=`, `--create-github` |
| **Catalog** | `catalog.yaml` — module ids, project kinds, profile matrix |
| **Project kinds** | 10 kinds under `project-kinds/*.yaml` |
| **Skeletons** | Code stubs under `modules/skeletons/<kind>/` |
| **Assistant profiles** | humans-only → solo-ai → solo-ai-rich → fractal-swarm |

Design (P27):

- Workstation plan: `plans/fractal/P27_DEVTOOLING_TEMPLATES.md`
- AI composable surface: `plans/evidence/P27-devtooling/AI_ASSISTANT_COMPOSABLE.md`
- Operator profile: `plans/evidence/P27-devtooling/OPERATOR_PROFILE.md`

## Quick start

```bash
git clone https://github.com/tzervas/tz-forge.git
cd tz-forge

# List kinds
python3 cli/tz_new.py --list

# Scaffold a Rust library ready for fractal agent waves
python3 cli/tz_new.py rust-lib /tmp/demo-crate --assistant=fractal-swarm

# Human OSS library — no CLAUDE.md / AGENTS.md / skills
python3 cli/tz_new.py rust-lib /tmp/demo-human --assistant=humans-only

# Optional skill selection + GitHub create
python3 cli/tz_new.py agent-swarm my-wave \
  --assistant=fractal-swarm \
  --skills=commit-prep,pr-review \
  --create-github
```

Optional install:

```bash
pip install -e .    # exposes `tz-new` entry point (requires PyYAML)
tz-new rust-lib my-crate --assistant=solo-ai
```

## Project kinds

| Kind | Default assistant | Skeleton |
|------|-------------------|----------|
| `rust-lib` | solo-ai | Cargo lib + tests |
| `rust-cli` | solo-ai | clap binary |
| `python-lib` | solo-ai | uv/hatch library |
| `python-mcp` | solo-ai | MCP server stub |
| `agent-swarm` | fractal-swarm | compose pointers + kickoffs |
| `ml-rust-crate` | fractal-swarm | ML train/infer crate |
| `ml-python-hf` | fractal-swarm | HF train + model card |
| `mcp-rust` | solo-ai | Rust MCP (`--stdio`) |
| `hybrid-rust-python` | solo-ai | PyO3-ready dual stack |
| `infra-ops` | humans-only | bootstrap scripts + fleet |

## Assistant profiles

| Profile | AI files | Typical use |
|---------|----------|-------------|
| `humans-only` | none | Public OSS, human maintainers only |
| `solo-ai` | CLAUDE + AGENTS lite | Solo dev + Claude/Cursor |
| `solo-ai-rich` | + skills + kickoffs | Rich solo agent surface |
| `fractal-swarm` | + fractal AGENTS, model policy, multi-skill, harness docs | Operator / L0–L1 waves |

Full matrix: [docs/ASSISTANT_PROFILES.md](docs/ASSISTANT_PROFILES.md).

Output always includes fleet modules for the kind; AI files **only** for the selected profile.
Generated projects write `.tz-forge.yaml` (config-as-code).

## 5-minute golden paths

See [templates/README.md](templates/README.md) for:

- `rust-lib`, `python-mcp`, `ml-rust-crate`, `agent-swarm`
- GitHub `isTemplate` flow (`gh api -X PATCH … -f is_template=true`)

## Layout

```text
tz-forge/
  catalog.yaml
  cli/tz_new.py
  project-kinds/            # 10 kinds
  modules/
    fleet/                  # P26 pack
    local-ci/{rust,python}/
    rust/{cargo-deny,toolchain}/
    gha/{dependabot-*,gitleaks-config}/
    git/gitignore-*
    devcontainer/{rust,python-uv}/
    pre-commit/
    license/mit/
    skeletons/<kind>/
    agents/
      claude-md-lite/, agents-md-{lite,fractal}/
      skills-generic/, skills-ml/
      harness-min/, cabal-profile/, security-mcp-opt/
      kickoffs/, model-policy.md
  templates/README.md
  docs/{ASSISTANT_PROFILES,FLEET_STANDARDS,compose}/
```

## Modules (P27b + P27c)

| Module | Notes |
|--------|-------|
| `modules/fleet` | P26 workflows, issue close, badges |
| `modules/local-ci/{rust,python}` | `scripts/check.sh` |
| `modules/rust/cargo-deny` | deny.toml allow set |
| `modules/rust/toolchain` | rust-toolchain.toml |
| `modules/gha/*` | dependabot + gitleaks |
| `modules/git/*` | language gitignore fragments |
| `modules/devcontainer/*` | rust + python-uv |
| `modules/pre-commit` | gitleaks + whitespace |
| `modules/license/mit` | LICENSE + REUSE |
| `modules/skeletons/*` | 10 project skeletons |
| `modules/agents/*` | AI surface + harness compose docs |

## Compose-by-reference (P27e)

Do **not** vendor harness binaries. Fractal kinds install short docs pointing at real repos:

| Module | Real repo |
|--------|-----------|
| `harness-min` | https://github.com/tzervas/agent-harness |
| `cabal-profile` | https://github.com/tzervas/cabal-devmelopner |
| `security-mcp-opt` | https://github.com/tzervas/security-mcp |

See [docs/compose/README.md](docs/compose/README.md).

## Fleet standards

This repo applies the fleet pack to itself. Issue close policy:

- **`dev` / feature merges:** `Refs #n` only
- **`main` merges:** `Closes #n` / `Fixes #n`

Automatic **Copilot code reviews are disabled**. See [docs/FLEET_STANDARDS.md](docs/FLEET_STANDARDS.md).

## Config-as-code

```yaml
# .tz-forge.yaml (generated)
kind: rust-lib
assistant:
  profile: fractal-swarm
  tools:
    claude: true
    agents_md: true
    skills: [commit-prep, pr-review, fleet-gap, unsafe-review, cargo-check]
    copilot_instructions: false
modules:
  fleet: { version: "1" }
  rust-cargo-deny: { version: "1" }
```

## License

MIT License — Copyright (c) 2026 Tyler Zervas. See [LICENSE](LICENSE).

## Non-goals

- Extracting or templating **mycelium**
- Shipping full agent-harness / cabal binaries inside every consumer
- Enabling Copilot auto-review
