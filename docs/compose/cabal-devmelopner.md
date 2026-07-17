# cabal-profile — compose cabal-devmelopner by reference

**Module:** `modules/agents/cabal-profile`  
**Profiles:** `fractal-swarm`  
**Does not vendor** the cabal CLI — document profile + real repo.

## Real repo

| Field | Value |
|-------|-------|
| GitHub | https://github.com/tzervas/cabal-devmelopner |
| Role | Long-running dev agent (CLI/TUI), tero-first AGENTS |
| Default branch | often **`dev`** (check remote) |
| Local clone | `/root/work/cabal-devmelopner` (if present) |

## 5-minute consumer path

```bash
git clone https://github.com/tzervas/cabal-devmelopner.git ../cabal-devmelopner
cd ../cabal-devmelopner
./setup.sh          # or: uv sync
# CLI entry depends on package; prefer README in that repo
```

Optional siblings (do not auto-install):

- https://github.com/tzervas/tero-mcp — memory / knowledge MCP
- https://github.com/tzervas/agent-harness — swarm dry-run

## Profile defaults for fractal work

| Setting | Value |
|---------|-------|
| AGENTS style | tero-first, subagent excavation (see `agents-md-fractal`) |
| Model policy | L0 frontier / L1 composer — `docs/MODEL_POLICY.md` |
| Issue keywords | `Refs` on feature; `Closes` on main |
| Copilot reviews | **off** |

## Wire into tz-forge

```bash
tz-new agent-swarm my-cabal-wave --assistant=fractal-swarm
# installs agents-md-fractal + model-policy + kickoffs + this COMPOSE.md
```

## Non-goals

- Embedding cabal binary in templates
- Automating mycelium paths
