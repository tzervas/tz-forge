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

| Piece | Role |
|-------|------|
| **Modules** | Copyable fragments under `modules/` (fleet pack, local-ci, deny, agents, skills, …) |
| **`tz-new`** | CLI stub (`cli/tz_new.py`) — `tz-new <kind> <name> --assistant=…` |
| **Catalog** | `catalog.yaml` — module ids, project kinds, profile matrix |
| **Project kinds** | `project-kinds/*.yaml` — rust-lib, python-mcp, agent-swarm |
| **Assistant profiles** | humans-only → solo-ai → solo-ai-rich → fractal-swarm |

Design (P27):

- Workstation plan: `plans/fractal/P27_DEVTOOLING_TEMPLATES.md`
- AI composable surface: `plans/evidence/P27-devtooling/AI_ASSISTANT_COMPOSABLE.md`
- Extract inventory: `plans/evidence/P27-devtooling/EXTRACT_CANDIDATES.md` (top modules: fleet pack, pre-commit, local-ci rust, cargo-deny, agents/CLAUDE)

## Quick start

```bash
git clone https://github.com/tzervas/tz-forge.git
cd tz-forge

# Scaffold a Rust library ready for fractal agent waves
python cli/tz_new.py rust-lib /tmp/demo-crate --assistant=fractal-swarm

# Human OSS library — no CLAUDE.md / AGENTS.md / skills
python cli/tz_new.py rust-lib /tmp/demo-human --assistant=humans-only
```

Optional install:

```bash
pip install -e .    # exposes `tz-new` entry point (requires PyYAML)
tz-new rust-lib my-crate --assistant=solo-ai
```

## Assistant profiles

| Profile | AI files | Typical use |
|---------|----------|-------------|
| `humans-only` | none | Public OSS, human maintainers only |
| `solo-ai` | CLAUDE + AGENTS lite | Solo dev + Claude/Cursor |
| `solo-ai-rich` | + skills + kickoffs | Rich solo agent surface |
| `fractal-swarm` | + fractal AGENTS, model policy, multi-skill | Operator / L0–L1 waves |

Full matrix: [docs/ASSISTANT_PROFILES.md](docs/ASSISTANT_PROFILES.md).

```bash
tz-new rust-lib my-crate --assistant=humans-only
tz-new rust-lib my-crate --assistant=solo-ai
tz-new python-mcp my-server --assistant=solo-ai-rich
tz-new agent-swarm my-wave --assistant=fractal-swarm
```

Output always includes fleet modules for the kind; AI files **only** for the selected profile.
Generated projects write `.tz-forge.yaml` (config-as-code).

## Layout

```text
tz-forge/
  catalog.yaml              # modules + kinds + profiles
  cli/tz_new.py             # scaffolder
  project-kinds/            # rust-lib, python-mcp, agent-swarm
  modules/
    fleet/                  # P26 pack (workflows, issue close, templates, docs)
    local-ci/rust/          # check.sh
    rust/cargo-deny/        # deny.toml template
    pre-commit/             # gitleaks + trailing whitespace
    license/mit/            # LICENSE + REUSE.toml
    agents/
      claude-md-lite/       # CLAUDE.md.tmpl
      agents-md-lite/       # AGENTS.md.tmpl (short)
      agents-md-fractal/    # tero-first, subagents, Refs vs Closes
      skills-generic/       # commit-prep, pr-review, fleet-gap, unsafe-review, cargo-check
      kickoffs/             # .claude/kickoffs README
      model-policy.md       # L0 frontier / L1 composer; no Copilot auto-review
  docs/
    ASSISTANT_PROFILES.md
    FLEET_STANDARDS.md
  .github/workflows/        # fleet pack applied to this repo
```

## Modules (shipped in P27b)

| Module | Source / notes |
|--------|----------------|
| `modules/fleet` | Copied from `plans/fleet-standards/pack/` (P26) |
| `modules/local-ci/rust` | Generic `check.sh` (fmt / clippy `-D warnings` / build / test) |
| `modules/rust/cargo-deny` | MIT, Apache-2.0, BSD, ISC, Zlib, Unicode-3.0 allow set |
| `modules/pre-commit` | gitleaks + trailing whitespace; language hooks commented |
| `modules/license/mit` | MIT Copyright 2026 Tyler Zervas + REUSE fragment |
| `modules/agents/*` | Composable AI surface (profile-gated) |

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
