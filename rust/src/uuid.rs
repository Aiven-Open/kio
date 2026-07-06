//! Construct `uuid.UUID` from 16-byte wire values without allocating `PyBytes`.

use pyo3::prelude::*;
use pyo3::sync::PyOnceLock;
use pyo3::types::PyModule;

static UUID_CACHE: PyOnceLock<Py<PyAny>> = PyOnceLock::new();

fn uuid_class(py: Python<'_>) -> PyResult<Py<PyAny>> {
    Ok(UUID_CACHE
        .get_or_try_init(py, || {
            PyModule::import(py, "uuid")?
                .getattr("UUID")
                .map(|bound| bound.unbind())
        })?
        .clone_ref(py))
}

pub(crate) fn uuid_from_bytes(py: Python<'_>, bytes: &[u8; 16]) -> PyResult<Py<PyAny>> {
    let int = u128::from_be_bytes(*bytes);
    uuid_class(py)?.call1(py, (py.None(), py.None(), py.None(), py.None(), int))
}

#[cfg(test)]
mod tests {
    use super::*;
    use pyo3::types::{PyBytes, PyDict};
    use std::ffi::CString;

    fn with_python<F>(f: F)
    where
        F: for<'py> FnOnce(Python<'py>),
    {
        Python::initialize();
        Python::attach(f);
    }

    fn assert_eq_uuid_from_bytes(py: Python<'_>, parsed: &Bound<'_, PyAny>, bytes: [u8; 16]) {
        let code = CString::new("import uuid; assert parsed == uuid.UUID(bytes=wire_bytes)")
            .expect("test code should not contain nul bytes");
        let locals = PyDict::new(py);
        locals.set_item("parsed", parsed).expect("locals setup");
        locals
            .set_item("wire_bytes", PyBytes::new(py, &bytes))
            .expect("locals setup");
        py.run(code.as_c_str(), None, Some(&locals))
            .expect("uuid should match Python UUID(bytes=...) constructor");
    }

    #[test]
    fn uuid_from_bytes_matches_python() {
        with_python(|py| {
            for bytes in [
                [0u8; 16],
                *b"\x12\x34\x56\x78\x12\x34\x56\x78\x12\x34\x56\x78\x12\x34\x56\x78",
                *b"\xff\xee\xdd\xcc\xbb\xaa\x99\x88\x77\x66\x55\x44\x33\x22\x11\x00",
            ] {
                let parsed = uuid_from_bytes(py, &bytes).expect("uuid construction should succeed");
                let parsed = parsed.bind(py);
                assert_eq_uuid_from_bytes(py, &parsed, bytes);
            }
        });
    }
}
