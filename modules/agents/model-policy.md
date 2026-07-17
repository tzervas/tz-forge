# Model policy (snippet)

Install as `docs/MODEL_POLICY.md` in consumer repos (fractal-swarm profile).

## Roles

| Role | Class | Default | Use for |
|------|-------|---------|---------|
| **L0** | Frontier | Named only when architecture is hard | Design forks, irreversible naming, cross-repo program design |
| **L1** | Composer / fast implementer | **Default for all implementation** | Code, tests, docs, extraction, PR hygiene, module edits |

## Rules

1. **L1 by default.** Do not escalate to L0 unless the task explicitly names hard architecture.
2. **No silent Copilot review.** Fleet standard: automatic GitHub Copilot code reviews are **disabled**. Do not request Copilot on PRs.
3. **Copilot instructions file** (`.github/copilot-instructions.md`) is opt-in only; never enable auto-review as a side effect.
4. **Honest routing.** If a frontier (L0) call is needed, say so in the PR/wave notes; do not hide model switches.
5. **Skills over re-prompting.** Prefer repo `skills/*/SKILL.md` workflows for commit-prep, PR review, cargo-check, etc.

## Wave shape (fractal)

```text
L0 (optional)  →  design / accept criteria
L1 composer(s) →  implement leaves in parallel
L1 reviewer    →  pr-review skill / checklist
merge          →  Refs on dev, Closes on main
```
