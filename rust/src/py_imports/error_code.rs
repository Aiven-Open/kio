use std::collections::HashMap;

use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::sync::PyOnceLock;
use pyo3::types::PyIterator;

use super::import_attr;

static ERROR_CODE_CLASS_CACHE: PyOnceLock<Py<PyAny>> = PyOnceLock::new();
static ERROR_CODE_VALUES_CACHE: PyOnceLock<HashMap<i16, Py<PyAny>>> = PyOnceLock::new();

fn error_code_class(py: Python<'_>) -> PyResult<Py<PyAny>> {
    Ok(ERROR_CODE_CLASS_CACHE
        .get_or_try_init(py, || import_attr(py, "kio.schema.errors", "ErrorCode"))?
        .clone_ref(py))
}

fn build_error_code_values(py: Python<'_>) -> PyResult<HashMap<i16, Py<PyAny>>> {
    let cls = error_code_class(py)?;
    let cls = cls.bind(py);
    let mut values = HashMap::new();
    for member in PyIterator::from_object(cls)? {
        let member = member?;
        let value: i16 = member.getattr("value")?.extract()?;
        values.insert(value, member.into_any().unbind());
    }
    Ok(values)
}

pub(crate) fn error_code_member(py: Python<'_>, value: i16) -> PyResult<Py<PyAny>> {
    let values = ERROR_CODE_VALUES_CACHE.get_or_try_init(py, || build_error_code_values(py))?;
    values
        .get(&value)
        .map(|member| member.clone_ref(py))
        .ok_or_else(|| PyValueError::new_err(format!("{value} is not a valid ErrorCode")))
}
