use std::collections::HashMap;
use pyo3::exceptions::PyNotImplementedError;
use pyo3::{IntoPy, Py, PyAny, PyResult};
use pyo3::types::PyBytes;
use crate::readers;
use crate::readers::read_unsigned_varint;

mod kio_errors {
    pyo3::import_exception!(kio.serial.errors, SerialError);
}

type Reader<T> = fn(&PyBytes, usize) -> PyResult<(T, usize)>;

pub fn get_reader<T: IntoPy<Py<PyAny>>>(
    kafka_type: &str,
    flexible: bool,
    optional: bool,
) -> PyResult<Reader<T>> {
    match (kafka_type, flexible, optional) {
        ("int8", _, false) => Ok(readers::read_int8),
        ("int16", _, false) => Ok(readers::read_int16),
        ("int32", _, false) => Ok(readers::read_int32),
        ("int64", _, false) => Ok(readers::read_int64),
        ("uint8", _, false) => Ok(readers::read_uint8),
        ("uint16", _, false) => Ok(readers::read_uint16),
        ("uint32", _, false) => Ok(readers::read_uint32),
        ("uint64", _, false) => Ok(readers::read_uint64),
        ("float64", _, false) => Ok(readers::read_float64),
        ("string", true, false) => Ok(readers::read_compact_string),
        ("string", true, true) => Ok(readers::read_compact_string_nullable),
        ("string", false, false) => Ok(readers::read_legacy_string),
        ("string", false, true) => Ok(readers::read_nullable_legacy_string),
        ("bytes", true, false) => Ok(readers::read_compact_string_as_bytes),
        ("bytes", true, true) => Ok(readers::read_compact_string_as_bytes_nullable),
        ("bytes", false, false) => Ok(readers::read_legacy_bytes),
        ("bytes", false, true) => Ok(readers::read_nullable_legacy_bytes),
        ("records", _, true) => Ok(readers::read_nullable_legacy_bytes),
        ("uuid", _, true) => Ok(readers::read_uuid),
        ("bool", _, false) => Ok(readers::read_boolean),
        ("error_code", _, false) => Ok(readers::read_error_code),
        ("timedelta_i32", _, false) => Ok(readers::read_timedelta_i32),
        ("timedelta_i64", _, false) => Ok(readers::read_timedelta_i64),
        ("datetime_i64", _, false) => Ok(readers::read_datetime_i64),
        ("datetime_i64", _, true) => Ok(readers::read_nullable_datetime_i64),
        _ => Err(
            PyNotImplementedError::new_err(
                format!(
                    "Failed identifying reader for {} field flexible={} optional={}",
                    kafka_type,
                    flexible,
                    optional,
                )
            )
        )
    }
}


fn get_tag_reader<T>(
    tagged_field_readers: HashMap<usize, T>,
    tag: &usize,
) -> PyResult<T> {
    match tagged_field_readers.get(tag).copied() {
        Some(tag_reader) => Ok(tag_reader),
        None => Err(
            kio_errors::SerialError:new_err(format!("Missing tag reader for tag {}", tag))
        ),
    }
}

struct EntityReader {
    field_readers: [(&str, Reader<&PyAny>)],
    tag_readers: HashMap<usize, (&str, Reader<&PyAny>)>,
}

fn entity_reader(
    model: &PyAny,
) -> PyResult<EntityReader> {
    // ...
}

type EntityData = HashMap<str, PyAny>;

// TODO: Note! Don't involve instantiation here. Just take bytes and readers,
//       return a dict ready to be passed as **kwargs.
pub fn read_entity(
    bytes: &PyBytes,
    reader: EntityReader,
) -> PyResult<(&PyAny, usize)> {
    let mut values: Vec<(&str, &PyAny)> = Vec::new();
    let mut offset: usize = 0;

    for (field_name, reader) in reader.field_readers.iter() {
        let (value, next_offset) = reader(bytes, offset)?;
        values.push((field_name, value));
        offset = next_offset;
    }

    // TODO: Handle non-flexible models. Same func or not!?

    let (num_tagged_fields, mut offset) = readers::read_unsigned_varint(bytes, offset)?;

    for _ in 0..num_tagged_fields {
        let (tag, local_offset) = readers::read_unsigned_varint(bytes, offset)?;
        let field_name, tag_reader = get_tag_reader(reader.tagged_field_readers, tag)?;
        let (field_length, local_offset) = readers::read_unsigned_varint(bytes, local_offset);
        let sliced = &bytes[local_offset..local_offset + field_length];
        let (value, field_read_offset) = tag_reader(sliced, 0);
        assert!(field_read_offset == field_length);
        values.push((field_name, value));
        offset = local_offset + field_length;
    }

    Ok()
}
