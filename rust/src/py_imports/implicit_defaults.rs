use pyo3::prelude::*;
use pyo3::sync::PyOnceLock;

use super::import_attr;

static GET_TAGGED_FIELD_DEFAULT_CACHE: PyOnceLock<Py<PyAny>> = PyOnceLock::new();

pub(crate) fn get_tagged_field_default(py: Python<'_>) -> PyResult<Py<PyAny>> {
    Ok(GET_TAGGED_FIELD_DEFAULT_CACHE
        .get_or_try_init(py, || {
            import_attr(
                py,
                "kio.serial._implicit_defaults",
                "get_tagged_field_default",
            )
        })?
        .clone_ref(py))
}
