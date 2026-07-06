use pyo3::prelude::*;
use pyo3::sync::PyOnceLock;

use super::import_attr;

static FIELDS_CACHE: PyOnceLock<Py<PyAny>> = PyOnceLock::new();

pub(crate) fn fields(py: Python<'_>) -> PyResult<Py<PyAny>> {
    Ok(FIELDS_CACHE
        .get_or_try_init(py, || import_attr(py, "dataclasses", "fields"))?
        .clone_ref(py))
}
