---
name: cargo-check
description: Run the standard Rust local gate (fmt, clippy -D warnings, build, test). Use before commits/PRs on Rust crates.
metadata:
  author: tz-forge
  version: "1.0"
allowed-tools: Bash(cargo:*) Bash(rustup:*) Bash(./scripts/check.sh:*)
---

# Cargo check (local gate)

Canonical Rust quality gate used across the fleet.

## When to use

- Before commit or PR on a Rust crate / workspace
- After dependency or edition changes
- When CI is remote-manual and local parity matters

## Preferred entrypoint

```bash
./scripts/check.sh          # full gate
./scripts/check.sh --fix    # rustfmt write
./scripts/check.sh --quick  # skip build if script supports it
```

`modules/local-ci/rust/check.sh` is the tz-forge template for this script.

## Manual equivalent

```bash
export CARGO_TERM_COLOR=always
export RUST_BACKTRACE=1
TOOLCHAIN="${RUSTUP_TOOLCHAIN:-stable}"

rustup component add rustfmt clippy --toolchain "$TOOLCHAIN" || true

cargo +"$TOOLCHAIN" fmt --check
cargo +"$TOOLCHAIN" clippy --all-targets --all-features -- -D warnings
cargo +"$TOOLCHAIN" build --all-features
cargo +"$TOOLCHAIN" test --all-features --verbose
```

### Optional license / advisory

```bash
cargo deny check    # when deny.toml is present (modules/rust/cargo-deny)
```

## Failure playbook

| Step | Failure | Action |
|------|---------|--------|
| fmt | diff | `cargo fmt` or `./scripts/check.sh --fix` |
| clippy | `-D warnings` | Fix or justify with scoped `#[allow]` + comment |
| build | compile err | Fix API / features |
| test | assert / panic | Fix code or update tests intentionally |
| deny | license/advisory | Adjust allowlist only with review |

## Output

```
Cargo check
===========
fmt:     ✅/❌
clippy:  ✅/❌
build:   ✅/❌
test:    ✅/❌
deny:    ✅/❌/skipped
```

Do not claim "green" unless the commands actually ran successfully in this environment.
