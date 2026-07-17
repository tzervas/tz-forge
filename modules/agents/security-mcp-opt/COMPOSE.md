# security-mcp-opt — optional security screening MCP

**Module:** `modules/agents/security-mcp-opt`  
**Profiles:** opt-in (fractal-swarm+security / explicit `--skills` / kind modules)  
**Does not force** runtime on every project.

## Real repo

| Field | Value |
|-------|-------|
| GitHub | https://github.com/tzervas/security-mcp |
| Role | Content screening MCP (Rust); alpha detectors |
| Entry | `security-mcp --stdio` |
| Local clone | `/root/work/security-mcp` (if present) |

## 5-minute path

```bash
git clone https://github.com/tzervas/security-mcp.git ../security-mcp
cd ../security-mcp
cargo build --release
# or: cargo install --path .
security-mcp --stdio   # MCP client wires stdio
cargo test
```

## Optional `.mcp.json` fragment (consumer)

```json
{
  "mcpServers": {
    "security-mcp": {
      "command": "security-mcp",
      "args": ["--stdio"]
    }
  }
}
```

Only add when the project opts into security screening. Alpha rules — not a compliance certificate.

## When to include

- Agent / MCP product kinds that handle untrusted content
- Operator request for security gate before publish
- Pair with gitleaks pre-commit (already in fleet pre-commit module)

## Non-goals

- Mandatory install on humans-only / plain rust-lib
- Claiming production-grade detection accuracy
