---
name: train-smoke
description: Run a minimal train/import smoke for ML crates (Rust or Python HF). Use before claiming a training path works.
metadata:
  author: tz-forge
  version: "1.0"
  domain: ml
allowed-tools: Bash(cargo:*) Bash(uv:*) Bash(python:*) Bash(pytest:*)
---

# Train smoke

## When to use

- After scaffolding `ml-rust-crate` or `ml-python-hf`
- Before long GPU runs — validate imports and unit tests first
- CI local gate extension for ML kinds

## Rust path

```bash
./scripts/check.sh --quick   # or cargo test --all-features
cargo test --all-features
```

## Python HF path

```bash
uv sync --all-groups 2>/dev/null || uv sync
uv run python -m {{project_snake}}.train_smoke
uv run pytest -q
```

## Rules

1. Prefer CPU / no-download smoke unless user explicitly requests a model pull.
2. Do not commit `wandb/`, `checkpoints/`, `*.safetensors`, large `.bin`/`.pt`.
3. Record command + pass/fail in the PR or kickoff note.

## Output

```
Train smoke
===========
kind: ml-rust-crate | ml-python-hf
imports: ✅/❌
tests: ✅/❌
notes: ...
```
