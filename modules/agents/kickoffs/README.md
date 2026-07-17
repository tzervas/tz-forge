# Kickoffs

Kickoff files are short, pasteable prompts that start a **wave** of agent work
(fractal-swarm profile). Place them under `.claude/kickoffs/` in the consumer
repo.

## Layout

```text
.claude/kickoffs/
  README.md          # this file
  wave.md            # sample multi-leaf wave
  hygiene.md         # optional: local gate + docs sync
```

## Conventions

1. **One kickoff = one goal** with explicit done criteria
2. Name **L0 vs L1** roles (L1 composer default; L0 only for hard design)
3. Include a **Tero excavation block** when corpus tools are available
4. Specify branch base (`dev` vs feature) and issue keyword tier (`Refs` / `Closes`)
5. Point leaves at skills (`commit-prep`, `pr-review`, `cargo-check`, …)
6. Keep product secrets out of kickoff text

## Sample wave skeleton

```markdown
# Wave: <title>

## Goal
…

## Done when
- [ ] …
- [ ] Local gate green
- [ ] PR opened with Refs #n → dev

## Leaves
| id | owner (L1) | task | skill |
|----|------------|------|-------|
| a1 | composer   | …    | cargo-check |
| a2 | composer   | …    | commit-prep |

## Tero excavation
(paste block from AGENTS.md)

## Non-goals
…
```

## tz-new

The `fractal-swarm` and `solo-ai-rich` profiles install this README into
`.claude/kickoffs/`. Add project-specific kickoffs beside it.
