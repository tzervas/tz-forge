# {{project}}

Agent swarm workspace scaffolded by [tz-forge](https://github.com/tzervas/tz-forge).

## Compose (by reference)

Do **not** vendor full harness binaries. Point at real repos:

| Component | Repo | Role |
|-----------|------|------|
| agent-harness | https://github.com/tzervas/agent-harness | Multi-agent dry-run / orchestrator |
| cabal-devmelopner | https://github.com/tzervas/cabal-devmelopner | Long-running dev agent CLI/TUI |
| security-mcp | https://github.com/tzervas/security-mcp | Optional content screening MCP |
| tero-mcp | https://github.com/tzervas/tero-mcp | Memory / knowledge MCP (opt-in) |

See `docs/compose/` after scaffold (when fractal-swarm profile installs harness modules).

## Local gate

```bash
./scripts/check.sh   # when present
```

## Kickoffs

Wave notes live under `.claude/kickoffs/` (solo-ai-rich / fractal-swarm).
