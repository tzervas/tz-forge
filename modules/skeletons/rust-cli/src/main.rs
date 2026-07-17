//! {{project}} — CLI scaffolded by tz-forge.

use clap::Parser;

#[derive(Parser, Debug)]
#[command(name = "{{project}}", version, about = "{{description}}")]
struct Args {
    /// Optional message to print
    #[arg(short, long, default_value = "ok")]
    message: String,
}

fn main() {
    let args = Args::parse();
    println!("{}", args.message);
}

#[cfg(test)]
mod tests {
    #[test]
    fn smoke() {
        assert_eq!(2 + 2, 4);
    }
}
