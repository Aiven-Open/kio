//! Cached imports of Python modules and commonly used attributes.
//!
//! Uses process-wide `PyOnceLock` caches (not subinterpreter-safe).

#![allow(non_snake_case)] // names mirror imported Python attributes

pub(crate) mod dataclasses;
pub(crate) mod error_code;
pub(crate) mod implicit_defaults;
pub(crate) mod introspect;
pub(crate) mod kio_native;
pub(crate) mod uuid;

use pyo3::prelude::*;
use pyo3::types::PyModule;

pub(super) fn import_attr(py: Python<'_>, module: &str, attr: &str) -> PyResult<Py<PyAny>> {
    Ok(PyModule::import(py, module)?.getattr(attr)?.unbind())
}
