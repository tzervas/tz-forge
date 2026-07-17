---
name: pr-review
description: Two-pass pull request review — triage by size/risk, then grounded file:line checklist. Use when reviewing PRs or before merge.
metadata:
  author: tz-forge
  version: "1.0"
allowed-tools: Bash(gh:*) Bash(git:*) Bash(cargo:*) Bash(uv:*)
---

# PR Review (two-pass)

Structured review for feature and delivery PRs. Aligns with fleet branch tiers.

## When to use

- Reviewing an open PR (`gh pr view` / `gh pr diff`)
- Self-review before requesting human merge
- Post-implement wave close-out

## Pass 1 — Triage

```bash
gh pr view <n> --json title,body,baseRefName,headRefName,files,additions,deletions
gh pr diff <n>
```

Classify risk:

| Tier | Signal | Depth |
|------|--------|-------|
| **T0** | Docs-only, typos | Skim |
| **T1** | Small, isolated | Standard checklist |
| **T2** | Multi-file, API, security, honesty surface | Full checklist + tests |
| **T3** | Cross-repo / auth / secrets / data plane | Full + explicit threat notes |

Record: base branch (`dev` vs `main`), issue keywords (`Refs` vs `Closes`), size.

## Pass 2 — Grounded checklist

For each item, cite **file:line** (or note N/A):

1. **Correctness** — Does the change match the PR intent? Edge cases?
2. **Tests** — New behavior covered? Existing tests still meaningful?
3. **Local gate** — Would `./scripts/check.sh` (or equiv) pass?
4. **Secrets** — No tokens, keys, private URLs, or credentials
5. **Branch tier**
   - Base `dev`/feature → must use **`Refs #n`**, not `Closes`/`Fixes`
   - Base `main` → `Closes`/`Fixes` appropriate for completed work
6. **Copilot** — Do **not** request automatic Copilot code review
7. **Honesty** — Failures surfaced (no silent `except: pass`); docs not overclaiming
8. **Scope** — No unrelated drive-by refactors without note

### Language extras

**Rust:** clippy clean, `unsafe` has SAFETY comments, deny.toml if deps changed  
**Python:** ruff clean, types/tests for public APIs

## Report format

```markdown
## PR review — #<n> (T<tier>)

**Base:** <branch> · **Keywords:** Refs|Closes · **Risk:** …

### Findings
- [blocker|major|nit] file:line — …

### Checklist
- Correctness: …
- Tests: …
- Secrets: …
- Branch tier: …

### Verdict
approve | request-changes | comment-only
```

Post with `gh pr comment <n> --body-file …` when appropriate.

## Non-goals

- Replacing human judgment on product design
- Enabling Copilot auto-review
- Merging without green local/CI gates when gates exist
