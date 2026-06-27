use pyo3::prelude::*;
use pyo3::sync::PyOnceLock;

use super::import_attr;

static UUID_LOCK: PyOnceLock<Py<PyAny>> = PyOnceLock::new();

pub(crate) fn UUID(py: Python<'_>) -> PyResult<Py<PyAny>> {
    Ok(UUID_LOCK
        .get_or_try_init(py, || import_attr(py, "uuid", "UUID"))?
        .clone_ref(py))
}
