use pyo3::prelude::*;
use pyo3::sync::PyOnceLock;

use super::import_attr;

static TIMEDELTA_LOCK: PyOnceLock<Py<PyAny>> = PyOnceLock::new();
static DATETIME_LOCK: PyOnceLock<Py<PyAny>> = PyOnceLock::new();
static UTC_LOCK: PyOnceLock<Py<PyAny>> = PyOnceLock::new();

pub(crate) fn timedelta(py: Python<'_>) -> PyResult<Py<PyAny>> {
    Ok(TIMEDELTA_LOCK
        .get_or_try_init(py, || import_attr(py, "datetime", "timedelta"))?
        .clone_ref(py))
}

pub(crate) fn datetime(py: Python<'_>) -> PyResult<Py<PyAny>> {
    Ok(DATETIME_LOCK
        .get_or_try_init(py, || import_attr(py, "datetime", "datetime"))?
        .clone_ref(py))
}

pub(crate) fn UTC(py: Python<'_>) -> PyResult<Py<PyAny>> {
    Ok(UTC_LOCK
        .get_or_try_init(py, || import_attr(py, "datetime", "UTC"))?
        .clone_ref(py))
}
