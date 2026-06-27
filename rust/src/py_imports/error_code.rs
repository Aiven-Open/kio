use pyo3::prelude::*;
use pyo3::sync::PyOnceLock;

use super::import_attr;

static ERROR_CODE_CACHE: PyOnceLock<Py<PyAny>> = PyOnceLock::new();

pub(crate) fn ErrorCode(py: Python<'_>) -> PyResult<Py<PyAny>> {
    Ok(ERROR_CODE_CACHE
        .get_or_try_init(py, || import_attr(py, "kio.schema.errors", "ErrorCode"))?
        .clone_ref(py))
}
