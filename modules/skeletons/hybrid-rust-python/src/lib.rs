//! {{project}} — hybrid Rust/Python (PyO3-ready) skeleton.

/// Pure-Rust smoke.
pub fn hello() -> &'static str {
    "ok"
}

// Uncomment when enabling pyo3 in Cargo.toml:
// use pyo3::prelude::*;
// #[pyfunction]
// fn hello_py() -> &'static str { hello() }
// #[pymodule]
// fn {{project_snake}}(m: &Bound<'_, PyModule>) -> PyResult<()> {
//     m.add_function(wrap_pyfunction!(hello_py, m)?)?;
//     Ok(())
// }

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn hello_ok() {
        assert_eq!(hello(), "ok");
    }
}
