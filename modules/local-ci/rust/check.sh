#!/usr/bin/env bash
# Local CI parity for Rust crates (tz-forge modules/local-ci/rust).
# Usage:
#   ./scripts/check.sh          # fmt --check, clippy -D warnings, build, test
#   ./scripts/check.sh --fix    # apply rustfmt
#   ./scripts/check.sh --quick  # skip build (fmt + clippy + test only)
set -euo pipefail
cd "$(dirname "$0")/.."
MODE="${1:-}"
export CARGO_TERM_COLOR="${CARGO_TERM_COLOR:-always}"
export RUST_BACKTRACE="${RUST_BACKTRACE:-1}"
TOOLCHAIN="${RUSTUP_TOOLCHAIN:-stable}"
CARGO=(cargo)
if command -v rustup >/dev/null 2>&1; then
  rustup component add rustfmt clippy --toolchain "$TOOLCHAIN" >/dev/null 2>&1 || true
  CARGO=(cargo "+$TOOLCHAIN")
fi

if [[ "$MODE" == "--fix" ]]; then
  "${CARGO[@]}" fmt
else
  "${CARGO[@]}" fmt --check
fi

"${CARGO[@]}" clippy --all-targets --all-features -- -D warnings

if [[ "$MODE" != "--quick" ]]; then
  "${CARGO[@]}" build --all-features
fi

"${CARGO[@]}" test --all-features --verbose
echo "OK: checks passed ($(basename "$PWD"))"
