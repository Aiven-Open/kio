use pyo3::exceptions::PyNotImplementedError;
use pyo3::prelude::*;
use pyo3::types::PyModule;

#[pyfunction]
pub fn get_reader(
    py: Python<'_>,
    kafka_type: &str,
    flexible: bool,
    optional: bool,
) -> PyResult<Py<PyAny>> {
    get_reader_inner(py, kafka_type, flexible, optional)
}

fn get_reader_inner(
    py: Python<'_>,
    kafka_type: &str,
    flexible: bool,
    optional: bool,
) -> PyResult<Py<PyAny>> {
    let reader_name = match (kafka_type, flexible, optional) {
        ("int8", _, false) => "read_int8",
        ("int16", _, false) => "read_int16",
        ("int32", _, false) => "read_int32",
        ("int64", _, false) => "read_int64",
        ("uint8", _, false) => "read_uint8",
        ("uint16", _, false) => "read_uint16",
        ("uint32", _, false) => "read_uint32",
        ("uint64", _, false) => "read_uint64",
        ("float64", _, false) => "read_float64",
        ("string", true, false) => "read_compact_string",
        ("string", true, true) => "read_compact_string_nullable",
        ("string", false, false) => "read_legacy_string",
        ("string", false, true) => "read_nullable_legacy_string",
        ("bytes" | "records", true, false) => "read_compact_string_as_bytes",
        ("bytes" | "records", true, true) => "read_compact_string_as_bytes_nullable",
        ("bytes" | "records", false, false) => "read_legacy_bytes",
        ("bytes" | "records", false, true) => "read_nullable_legacy_bytes",
        ("uuid", _, _) => "read_uuid",
        ("bool", _, false) => "read_boolean",
        ("error_code", _, false) => "read_error_code",
        ("timedelta_i32", _, false) => "read_timedelta_i32",
        ("timedelta_i64", _, false) => "read_timedelta_i64",
        ("datetime_i64", _, false) => "read_datetime_i64",
        ("datetime_i64", _, true) => "read_nullable_datetime_i64",
        _ => {
            return Err(PyNotImplementedError::new_err(format!(
                "Failed identifying reader for {} field flexible={} optional={}",
                kafka_type, flexible, optional,
            )));
        }
    };
    Ok(PyModule::import(py, "kio._kio_native")?
        .getattr(reader_name)?
        .into())
}
