#!/usr/bin/env bash
# {{project}} bootstrap — infra/ops skeleton (tz-forge)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
echo "bootstrap {{project}} from $ROOT"
# Add host prep, package installs, runner labels, etc.
