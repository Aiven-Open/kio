use std::cmp::Ordering;
use std::str;
use pyo3::prelude::*;
use pyo3::types::{PyBytes, PyString};
use pyo3::{PyNativeType, Python};
use pyo3::exceptions::PyValueError;

mod parse;
mod readers;

/// A Python module implemented in Rust.
#[pymodule]
fn _kio_core(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(readers::read_boolean, m)?)?;

    m.add_function(wrap_pyfunction!(readers::read_int8, m)?)?;
    m.add_function(wrap_pyfunction!(readers::read_int16, m)?)?;
    m.add_function(wrap_pyfunction!(readers::read_int32, m)?)?;
    m.add_function(wrap_pyfunction!(readers::read_int64, m)?)?;
    m.add_function(wrap_pyfunction!(readers::read_uint8, m)?)?;
    m.add_function(wrap_pyfunction!(readers::read_uint16, m)?)?;
    m.add_function(wrap_pyfunction!(readers::read_uint32, m)?)?;
    m.add_function(wrap_pyfunction!(readers::read_uint64, m)?)?;
    m.add_function(wrap_pyfunction!(readers::read_unsigned_varint, m)?)?;

    m.add_function(wrap_pyfunction!(readers::read_float64, m)?)?;

    m.add_function(wrap_pyfunction!(readers::read_compact_string_as_bytes, m)?)?;
    m.add_function(wrap_pyfunction!(readers::read_compact_string_as_bytes_nullable, m)?)?;
    m.add_function(wrap_pyfunction!(readers::read_compact_string, m)?)?;
    m.add_function(wrap_pyfunction!(readers::read_compact_string_nullable, m)?)?;

    m.add_function(wrap_pyfunction!(readers::read_legacy_bytes, m)?)?;
    m.add_function(wrap_pyfunction!(readers::read_nullable_legacy_bytes, m)?)?;
    m.add_function(wrap_pyfunction!(readers::read_legacy_string, m)?)?;
    m.add_function(wrap_pyfunction!(readers::read_nullable_legacy_string, m)?)?;

    m.add_function(wrap_pyfunction!(readers::read_legacy_array_length, m)?)?;
    m.add_function(wrap_pyfunction!(readers::read_compact_array_length, m)?)?;

    m.add_function(wrap_pyfunction!(readers::read_uuid, m)?)?;
    m.add_function(wrap_pyfunction!(readers::read_error_code, m)?)?;
    m.add_function(wrap_pyfunction!(readers::read_timedelta_i32, m)?)?;
    m.add_function(wrap_pyfunction!(readers::read_timedelta_i64, m)?)?;
    m.add_function(wrap_pyfunction!(readers::read_datetime_i64, m)?)?;
    m.add_function(wrap_pyfunction!(readers::read_nullable_datetime_i64, m)?)?;

    Ok(())
}
