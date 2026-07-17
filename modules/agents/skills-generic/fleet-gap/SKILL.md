---
name: fleet-gap
description: Detect drift from tzervas fleet standards (workflows, badges, issue tiers, Copilot off). Use when auditing a repo or filing fleet-gap issues.
metadata:
  author: tz-forge
  version: "1.0"
allowed-tools: Bash(git:*) Bash(gh:*) Bash(rg:*)
---

# Fleet gap audit

Compare a consumer repo against the P26 fleet pack (also shipped as
`modules/fleet` in tz-forge).

## When to use

- Onboarding a repo to fleet standards
- Periodic hygiene after workflow edits
- Filing `.github/ISSUE_TEMPLATE/fleet-gap.yml` issues

## Expected artifacts

| Path | Role |
|------|------|
| `.github/workflows/fleet-ci.yml` | Push/PR CI (self-hosted labels) |
| `.github/workflows/fleet-security.yml` | Security + weekly |
| `.github/workflows/close-issues-on-main.yml` | Close issues on main merge |
| `.github/workflows/reopen-issues-closed-off-main.yml` | Reopen if Closes used off-main |
| `scripts/close-linked-issues.sh` | Helper for close workflow |
| `.github/ISSUE_TEMPLATE/fleet-gap.yml` | Gap intake |
| `.github/PULL_REQUEST_TEMPLATE.md` | Refs vs Closes checklist |
| README badges | Live Actions SVG for trunk branch |

## Audit steps

1. **Workflows present?**

```bash
ls .github/workflows/
```

2. **Byte drift vs pack** (from a tz-forge checkout):

```bash
diff -u path/to/tz-forge/modules/fleet/.github/workflows/fleet-ci.yml \
        .github/workflows/fleet-ci.yml
```

3. **Badges live?** README should use GitHub Actions badge URLs for the real
   trunk branch — not static green images.

4. **Issue policy documented?** PR template mentions Refs on dev / Closes on main.

5. **Copilot auto-review off?** No workflow or settings that request automatic
   Copilot reviews.

6. **Permissions** — workflows use minimum `permissions:` blocks.

## Report

```markdown
## Fleet gap — <repo>

| Check | Status | Notes |
|-------|--------|-------|
| fleet-ci.yml | ok/missing/drift | |
| fleet-security.yml | | |
| close/reopen workflows | | |
| close-linked-issues.sh | | |
| issue + PR templates | | |
| live badges | | |
| Copilot auto-review | off/ON(BAD) | |

### Recommended actions
1. …
```

Open a **fleet-gap** issue when remediation is non-trivial; fix trivial drift
in a chore PR with `Refs #n`.
