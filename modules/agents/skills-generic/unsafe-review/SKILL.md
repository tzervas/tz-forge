---
name: unsafe-review
description: Review Rust unsafe blocks for SAFETY comments (what/why/invariants). Use when writing or reviewing unsafe Rust.
metadata:
  author: tz-forge
  version: "1.0"
  source: adapted from SpectreOS skills/unsafe-review (genericized)
allowed-tools: Bash(rg:*) Bash(git:*)
---

# Unsafe code review

Ensure every `unsafe` block documents why it is sound.

## When to use

- Writing new `unsafe` blocks
- Reviewing PRs that touch `unsafe`
- Auditing FFI, raw pointers, or transmute usage

## Requirements

Every `unsafe` block MUST have a `SAFETY:` comment covering:

1. **What** — operation / memory / invariant being trusted
2. **Why** — validation, type invariants, API contracts, or hardware guarantees
3. **References** — standard/docs/crate API when non-obvious

### Good

```rust
// SAFETY: `ptr` came from Box::into_raw on a T allocated in this module.
// Caller guarantees exclusive access until from_raw; alignment matches T.
// See module docs §Ownership.
unsafe {
    let _ = Box::from_raw(ptr);
}
```

### Bad

```rust
// SAFETY: this is fine
unsafe {
    *p = 1;
}
```

## Review steps

1. Find blocks:

```bash
rg -n "unsafe\s*(\{|fn|impl|trait|extern)" --type rust
```

2. For each hit, check:
   - [ ] `SAFETY:` (or equivalent) immediately above
   - [ ] WHAT is clear
   - [ ] WHY soundness holds
   - [ ] No wider `unsafe` than needed
   - [ ] Safe wrappers preferred at API boundaries

3. Common patterns:
   - **Raw pointers** — non-null, aligned, initialized, provenance
   - **FFI** — ABI, lifetimes, nullability, thread-safety
   - **Transmute** — size/align equal; prefer `bytemuck` / safe casts
   - **Static mut** — exclusive access story

## Output

```
Unsafe review
=============
Blocks found: N
Missing/weak SAFETY: (file:line …)
OK: (file:line …)
Verdict: pass | needs-work
```
