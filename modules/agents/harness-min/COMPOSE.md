# harness-min — compose agent-harness by reference

**Module:** `modules/agents/harness-min`  
**Profiles:** `fractal-swarm` (agent-swarm / ML operator kinds)  
**Does not vendor** the harness binary — pin docs + invoke real repo.

## Real repo

| Field | Value |
|-------|-------|
| GitHub | https://github.com/tzervas/agent-harness |
| Role | Universal multi-agent harness (offline dry-run / orchestrator) |
| Default branch | `main` |
| Local clone (workstation) | `/root/work/agent-harness` (if present) |

## 5-minute consumer path

```bash
# sibling clone preferred over submodules
git clone https://github.com/tzervas/agent-harness.git ../agent-harness
cd ../agent-harness
uv sync
uv run agent-harness version   # or: python -m agent_harness
uv run agent-harness doctor    # offline checks
./scripts/local-ci.sh 2>/dev/null || ./scripts/check.sh 2>/dev/null || true
```

## Wire into a tz-forge project

1. Scaffold with fractal profile:
   ```bash
   tz-new agent-swarm my-wave --assistant=fractal-swarm
   ```
2. Keep swarm product code in `my-wave`; call harness as a **sibling tool**.
3. Document the path in project `docs/compose/agent-harness.md` (this file is the module source).
4. Kickoffs under `.claude/kickoffs/` describe L0/L1 waves; harness runs dry-run first.

## Fleet notes

- agent-harness already carries P26 fleet workflows.
- Prefer `Refs #n` on feature branches; `Closes #n` only on main delivery.
- **Never** enable Copilot auto-review from this module.

## Non-goals

- Shipping harness wheels inside every consumer
- Touching mycelium
