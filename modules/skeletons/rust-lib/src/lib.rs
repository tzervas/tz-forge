//! {{project}} — library crate scaffolded by tz-forge.

/// Return a greeting for smoke tests.
pub fn hello() -> &'static str {
    "ok"
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn hello_ok() {
        assert_eq!(hello(), "ok");
    }
}
