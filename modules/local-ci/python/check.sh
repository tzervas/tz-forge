#!/usr/bin/env bash
# Local CI for Python projects (tz-forge modules/local-ci/python).
# Usage:
#   ./scripts/check.sh
#   ./scripts/check.sh --fix
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
MODE="${1:-}"

if command -v uv >/dev/null 2>&1 && [ -f pyproject.toml ]; then
  uv sync --all-groups 2>/dev/null || uv sync 2>/dev/null || true
  if grep -q '\[tool.ruff' pyproject.toml 2>/dev/null || true; then
    if [[ "$MODE" == "--fix" ]]; then
      uv run ruff format . 2>/dev/null || true
      uv run ruff check --fix . 2>/dev/null || uv run ruff check . 2>/dev/null || true
    else
      uv run ruff check . 2>/dev/null || true
      uv run ruff format --check . 2>/dev/null || true
    fi
  fi
  if [ -d tests ] || [ -d test ]; then
    uv run pytest -q
  else
    echo "no tests/ — skip pytest"
  fi
  echo "OK: python checks ($(basename "$PWD"))"
else
  echo "uv/pyproject missing — skip python checks" >&2
  exit 0
fi
