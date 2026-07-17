---
name: commit-prep
description: Prepare code for git commit by running format checks, lints, tests, and generating a commit message. Use before committing changes.
metadata:
  author: tz-forge
  version: "1.0"
  source: adapted from SpectreOS skills/commit-prep (product-specific paths removed)
allowed-tools: Bash(cargo:*) Bash(git:*) Bash(uv:*) Bash(python:*)
---

# Commit Preparation

Prepare code changes for commit with quality checks and a clear message.

## When to use

- Ready to commit changes
- Want confidence that CI / local gates will pass
- Need a conventional commit message
- Preparing a pull request

## Workflow

### 1. Inspect changes

```bash
git status
git diff
git diff --cached
```

### 2. Run local CI

```bash
# Preferred generic gate
./scripts/check.sh

# Apply formatters when supported
./scripts/check.sh --fix

# Faster path when supported
./scripts/check.sh --quick
```

If `scripts/check.sh` is absent:

**Rust**

```bash
cargo fmt --check
cargo clippy --all-targets --all-features -- -D warnings
cargo test --all-features
```

**Python**

```bash
uv run ruff format --check .
uv run ruff check .
uv run pytest -q
```

### 3. Fix failures

- Format failures → re-run with `--fix` or `cargo fmt` / `ruff format`
- Clippy / ruff → fix findings, re-run
- Tests → fix or add coverage for new behavior

### 4. Stage intentionally

```bash
git add path/to/file.rs   # preferred
# avoid blind `git add .` when secrets or build artifacts may be present
```

### 5. Commit message

1. **Subject** (≤50 chars): imperative mood — `Add`, `Fix`, `Update`, `Refactor`
2. **Body** (wrap ~72): why, not only what
3. **Trailers**: `Refs #n` on feature/dev; `Closes #n` / `Fixes #n` only for main delivery

Type prefixes: `feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `perf:`, `chore:`

```bash
git commit -m "$(cat <<'EOF'
feat: add deny.toml allowlist for common OSS licenses

Align cargo-deny with fleet defaults so CI does not fail on
MIT/Apache transitive deps.

Refs #42
EOF
)"
```

## Checklist

- [ ] Local gate green
- [ ] No secrets or credentials in the diff
- [ ] Commit message is descriptive (not "WIP" / "update")
- [ ] Issue keyword matches branch tier (`Refs` vs `Closes`)
- [ ] No debug leftovers or unrelated files staged

## Output format

```
Commit Preparation Results
==========================
Files changed: N
Quality checks: ✅ / ❌ (list)
Suggested commit message:
-------------------------
...
Ready to commit? yes/no
```
