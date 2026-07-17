# Compose docs (harness / cabal / security)

These docs also ship as installable modules under `modules/agents/`:

| Module | Install destination | Real repo |
|--------|---------------------|-----------|
| `harness-min` | `docs/compose/agent-harness.md` | [agent-harness](https://github.com/tzervas/agent-harness) |
| `cabal-profile` | `docs/compose/cabal-devmelopner.md` | [cabal-devmelopner](https://github.com/tzervas/cabal-devmelopner) |
| `security-mcp-opt` | `docs/compose/security-mcp.md` | [security-mcp](https://github.com/tzervas/security-mcp) |

Sources of truth for module content:

- `modules/agents/harness-min/COMPOSE.md`
- `modules/agents/cabal-profile/COMPOSE.md`
- `modules/agents/security-mcp-opt/COMPOSE.md`

Copy for local reading:

```bash
cp modules/agents/harness-min/COMPOSE.md docs/compose/agent-harness.md
cp modules/agents/cabal-profile/COMPOSE.md docs/compose/cabal-devmelopner.md
cp modules/agents/security-mcp-opt/COMPOSE.md docs/compose/security-mcp.md
```
