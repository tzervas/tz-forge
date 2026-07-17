# Assistant intensity profiles

tz-forge templates compose AI coding-assistant surface **by profile** — never force
`CLAUDE.md` / `AGENTS.md` / skills onto human-only OSS libraries.

Design refs:

- [P27_DEVTOOLING_TEMPLATES.md](../../plans/fractal/P27_DEVTOOLING_TEMPLATES.md) (workstation)
- [AI_ASSISTANT_COMPOSABLE.md](../../plans/evidence/P27-devtooling/AI_ASSISTANT_COMPOSABLE.md)

## Profiles

| Profile | Humans | Solo AI files | Fractal swarm | Includes |
|---------|:------:|:-------------:|:-------------:|----------|
| **`humans-only`** | ✅ | ❌ | ❌ | fleet + license + pre-commit — **no** CLAUDE / AGENTS / skills |
| **`solo-ai`** | ✅ | ✅ | ❌ | + `CLAUDE.md` lite + `AGENTS.md` lite |
| **`solo-ai-rich`** | ✅ | ✅ | ❌ | + `skills/*` pack + `.claude/kickoffs` |
| **`fractal-swarm`** | ✅ | ✅ | ✅ | + fractal `AGENTS.md`, multi-skills, kickoffs, `docs/MODEL_POLICY.md` |

## CLI

```bash
tz-new rust-lib mylib --assistant=humans-only
tz-new rust-lib mylib --assistant=solo-ai
tz-new python-mcp mysvc --assistant=solo-ai-rich
tz-new agent-swarm mywave --assistant=fractal-swarm
```

Default assistant is declared per project kind (`project-kinds/*.yaml`).

## Config-as-code

Generated projects write `.tz-forge.yaml`:

```yaml
kind: rust-lib
assistant:
  profile: fractal-swarm
  tools:
    claude: true
    agents_md: true
    skills:
      - commit-prep
      - pr-review
      - fleet-gap
      - unsafe-review
      - cargo-check
    cursor: false
    copilot_instructions: false   # file off by default; NEVER auto-review
    tero: true
    harness: true
    cabal: true
```

## Module map

| Module | humans-only | solo-ai | solo-ai-rich | fractal-swarm |
|--------|:-----------:|:-------:|:------------:|:-------------:|
| fleet, license, pre-commit | ✅ | ✅ | ✅ | ✅ |
| local-ci / cargo-deny (rust kinds) | ✅ | ✅ | ✅ | ✅ |
| claude-md-lite | | ✅ | ✅ | ✅ |
| agents-md-lite | | ✅ | ✅ | |
| agents-md-fractal | | | | ✅ |
| skills-generic | | | ✅ | ✅ |
| kickoffs | | | ✅ | ✅ |
| model-policy | | | | ✅ |

## Copilot policy

- Automatic Copilot **code review** remains **off** fleet-wide (P26).
- Optional `.github/copilot-instructions.md` is **not** installed by default.
- Model policy snippet: L0 = frontier (rare), L1 = composer (default implementer).

## Verification

```bash
# fractal: expect AGENTS + CLAUDE + skills
python cli/tz_new.py rust-lib /tmp/demo-crate --assistant=fractal-swarm
test -f /tmp/demo-crate/AGENTS.md && test -f /tmp/demo-crate/CLAUDE.md
test -d /tmp/demo-crate/skills

# humans-only: no AI context files
python cli/tz_new.py rust-lib /tmp/demo-human --assistant=humans-only
test ! -f /tmp/demo-human/AGENTS.md && test ! -f /tmp/demo-human/CLAUDE.md
```
