//! {{project}} — Rust MCP server skeleton (tz-forge).
//! Donor pattern: security-mcp (`--stdio` entry).

fn main() {
    let mode = std::env::args().nth(1).unwrap_or_else(|| "--help".into());
    match mode.as_str() {
        "--stdio" => {
            // TODO: attach MCP stdio transport + tools
            eprintln!("{{project}}: stdio MCP stub — implement tools");
        }
        "--version" => println!("{{project}} 0.1.0"),
        _ => {
            eprintln!("Usage: {{project}} --stdio | --version");
            std::process::exit(2);
        }
    }
}

#[cfg(test)]
mod tests {
    #[test]
    fn smoke() {
        assert!(true);
    }
}
