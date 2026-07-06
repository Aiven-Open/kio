use pyo3::prelude::*;
use pyo3::sync::PyOnceLock;
use pyo3::types::PyModule;

static MODULE_CACHE: PyOnceLock<Py<PyAny>> = PyOnceLock::new();

pub(crate) fn module(py: Python<'_>) -> PyResult<Py<PyAny>> {
    Ok(MODULE_CACHE
        .get_or_try_init(py, || {
            PyModule::import(py, "kio._kio_native").map(|module| module.into())
        })?
        .clone_ref(py))
}
