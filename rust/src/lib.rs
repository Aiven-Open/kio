use std::cmp::Ordering;
use std::str;
use pyo3::prelude::*;
use pyo3::types::{PyBytes, PyString};
use pyo3::{PyNativeType, Python};
use pyo3::exceptions::PyValueError;

mod kio_errors {
    pyo3::import_exception!(kio.serial.errors, UnexpectedNull);
    pyo3::import_exception!(kio.serial.errors, InvalidUnicode);
    pyo3::import_exception!(kio.serial.errors, NegativeByteLength);
}

fn _load_none(py: Python) -> PyResult<&PyAny> {
    let builtins = PyModule::import(py, "builtins")?;
    Ok(builtins.getattr("None")?)
}

#[pyfunction]
fn read_boolean(bytes: &PyBytes, offset: usize) -> PyResult<(bool, usize)> {
    match &(bytes.as_bytes())[offset..] {
        [0, ..] => Ok((false, offset + 1)),
        [1, ..] => Ok((true, offset + 1)),
        [] => Err(PyValueError::new_err("Buffer is exhausted")),
        _ => Err(PyValueError::new_err("Invalid boolean value")),
    }
}

#[pyfunction]
fn read_int8(bytes: &PyBytes, offset: usize) -> PyResult<(i8, usize)> {
    let end_offset = offset + 1;

    if let [a, ..] = &(bytes.as_bytes())[offset..] {
        return Ok((i8::from_be_bytes([*a]), end_offset))
    }

    Err(PyValueError::new_err("Buffer is exhausted"))
}

#[pyfunction]
fn read_int16(bytes: &PyBytes, offset: usize) -> PyResult<(i16, usize)> {
    let end_offset = offset + 2;

    if let [fst, snd, ..] = &(bytes.as_bytes())[offset..] {
        return Ok((i16::from_be_bytes([*fst, *snd]), end_offset))
    }

    Err(PyValueError::new_err("Buffer is exhausted"))
}

#[pyfunction]
fn read_int32(bytes: &PyBytes, offset: usize) -> PyResult<(i32, usize)> {
    let end_offset = offset + 4;

    if let [a, b, c, d, ..] = &(bytes.as_bytes())[offset..] {
        return Ok((i32::from_be_bytes([*a, *b, *c, *d]), end_offset))
    }

    Err(PyValueError::new_err("Buffer is exhausted"))
}

#[pyfunction]
fn read_int64(bytes: &PyBytes, offset: usize) -> PyResult<(i64, usize)> {
    let end_offset = offset + 8;

    if let [a, b, c, d, e, f, g, h, ..] = &(bytes.as_bytes())[offset..] {
        return Ok((i64::from_be_bytes([*a, *b, *c, *d, *e, *f, *g, *h]), end_offset))
    }

    Err(PyValueError::new_err("Buffer is exhausted"))
}

#[pyfunction]
fn read_uint8(bytes: &PyBytes, offset: usize) -> PyResult<(u8, usize)> {
    let end_offset = offset + 1;

    if let [a, ..] = &(bytes.as_bytes())[offset..] {
        return Ok((u8::from_be_bytes([*a]), end_offset))
    }

    Err(PyValueError::new_err("Buffer is exhausted"))
}

#[pyfunction]
fn read_uint16(bytes: &PyBytes, offset: usize) -> PyResult<(u16, usize)> {
    let end_offset = offset + 2;

    if let [a, b, ..] = &(bytes.as_bytes())[offset..] {
        return Ok((u16::from_be_bytes([*a, *b]), end_offset))
    }

    Err(PyValueError::new_err("Buffer is exhausted"))
}

#[pyfunction]
fn read_uint32(bytes: &PyBytes, offset: usize) -> PyResult<(u32, usize)> {
    let end_offset = offset + 4;

    if let [a, b, c, d, ..] = &(bytes.as_bytes())[offset..] {
        return Ok((u32::from_be_bytes([*a, *b, *c, *d]), end_offset))
    }

    Err(PyValueError::new_err("Buffer is exhausted"))
}

#[pyfunction]
fn read_uint64(bytes: &PyBytes, offset: usize) -> PyResult<(u64, usize)> {
    let end_offset = offset + 8;

    if let [a, b, c, d, e, f, g, h, ..] = &(bytes.as_bytes())[offset..] {
        return Ok((u64::from_be_bytes([*a, *b, *c, *d, *e, *f, *g, *h]), end_offset))
    }

    Err(PyValueError::new_err("Buffer is exhausted"))
}

// See description and Kafka implementation.
// https://developers.google.com/protocol-buffers/docs/encoding?csw=1#varints
// https://github.com/apache/kafka/blob/ef96ac07f565a73e35c5b0f4c56c8e87cfbaaf59/clients/src/main/java/org/apache/kafka/common/utils/ByteUtils.java#L262
#[pyfunction]
fn read_unsigned_varint(bytes: &PyBytes, offset: usize) -> PyResult<(usize, usize)> {
    let mut result: usize = 0;
    let real_bytes = &(bytes.as_bytes());
    let mut byte_count = 0;
    let mut shift: u8 = 0;

    loop {
        if byte_count == 5 {
            return Err(PyValueError::new_err(
                "Varint is too long, the most significant bit in the 5th byte is set"
            ))
        }
        // Read value by a byte at a time.
        if let Some(byte) = real_bytes.get(offset + byte_count) {
            byte_count += 1;
            // Add 7 least significant bits to the result.
            let seven_bit_chunk = byte & 0b01111111;
            result |= usize::from(seven_bit_chunk) << shift;
            // Increase shift by 7 on each iteration.
            shift += 7;
            // If the most significant bit is 1, continue. Otherwise, stop.
            if byte & 0b10000000 == 0 {
                break
            }
        } else {
            return Err(PyValueError::new_err("Buffer is exhauseted"))
        }
    }

    Ok((result, offset + byte_count))
}

#[pyfunction]
fn read_float64(bytes: &PyBytes, offset: usize) -> PyResult<(f64, usize)> {
    let end_offset = offset + 8;

    if let [a, b, c, d, e, f, g, h, ..] = &(bytes.as_bytes())[offset..] {
        return Ok((
            f64::from_be_bytes([*a, *b, *c, *d, *e, *f, *g, *h]),
            end_offset,
        ))
    }

    Err(PyValueError::new_err("Buffer is exhausted"))
}

#[pyfunction]
fn read_compact_string_as_bytes(bytes: &PyBytes, offset: usize) -> PyResult<(&PyBytes, usize)> {
    match read_unsigned_varint(bytes, offset) {
        Err(error) => Err(error),
        Ok((0, _)) => Err(
            kio_errors::UnexpectedNull::new_err(
                "Unexpectedly read null where compact string/bytes was expected"
            )
        ),
        Ok((length, byte_offset)) => {
            // String length is encoded with an offset of 1, to allow encoding
            // null as 0.
            let byte_end = byte_offset + length - 1;
            let sliced = &bytes[byte_offset..byte_end];
            let py_bytes = PyBytes::new(bytes.py(), sliced);
            Ok((py_bytes, byte_end))
        },
    }
}

#[pyfunction]
fn read_compact_string_as_bytes_nullable(bytes: &PyBytes, offset: usize) -> PyResult<(&PyAny, usize)> {
    match read_unsigned_varint(bytes, offset) {
        Err(error) => Err(error),
        Ok((0, offset)) => {
            let builtins = PyModule::import(bytes.py(), "builtins")?;
            let none = builtins.getattr("None")?;
            Ok((none, offset))
        },
        Ok((length, byte_offset)) => {
            // String length is encoded with an offset of 1, to allow encoding
            // null as 0.
            let byte_end = byte_offset + length - 1;
            let sliced = &bytes[byte_offset..byte_end];
            let py_bytes = PyBytes::new(bytes.py(), sliced);
            Ok((py_bytes, byte_end))
        },
    }
}

fn _decode_compact_string(bytes: &PyBytes, offset: usize, length: usize) -> PyResult<(&PyAny, usize)> {
    // String length is encoded with an offset of 1, to allow encoding
    // null as 0.
    let byte_end = offset + length - 1;
    let sliced = &bytes[offset..byte_end];

    match str::from_utf8(sliced) {
        Err(_) => Err(
            kio_errors::InvalidUnicode::new_err("Failed interpreting bytes as UTF-8")
        ),
        Ok(string) => {
            let py_string = PyString::new(bytes.py(), string);
            Ok((py_string, byte_end))
        }
    }
}

#[pyfunction]
fn read_compact_string(bytes: &PyBytes, offset: usize) -> PyResult<(&PyAny, usize)> {
    match read_unsigned_varint(bytes, offset) {
        Err(error) => Err(error),
        Ok((0, _)) => Err(
            kio_errors::UnexpectedNull::new_err(
                "Unexpectedly read null where compact string/bytes was expected"
            )
        ),
        Ok((length, byte_offset)) => _decode_compact_string(bytes, byte_offset, length)
    }
}

#[pyfunction]
fn read_compact_string_nullable(bytes: &PyBytes, offset: usize) -> PyResult<(&PyAny, usize)> {
    match read_unsigned_varint(bytes, offset) {
        Err(error) => Err(error),
        Ok((0, offset)) => {
            let builtins = PyModule::import(bytes.py(), "builtins")?;
            let none = builtins.getattr("None")?;
            Ok((none, offset))
        },
        Ok((length, byte_offset)) => _decode_compact_string(bytes, byte_offset, length)
    }
}

fn _slice_legacy_bytes(bytes: &PyBytes, offset: usize, length: usize) -> PyResult<(&PyAny, usize)> {
    let byte_end = offset + length;
    let sliced = &bytes[offset..byte_end];
    let py_bytes = PyBytes::new(bytes.py(), sliced);
    Ok((py_bytes, byte_end))
}

#[pyfunction]
fn read_legacy_bytes(bytes: &PyBytes, offset: usize) -> PyResult<(&PyAny, usize)> {
    const NULL_VALUE: i16 = -1;

    match read_int16(bytes, offset) {
        Err(error) => Err(error),
        Ok((length, offset)) => {
            match (usize::try_from(length), length) {
                (Ok(length), _) => _slice_legacy_bytes(bytes, offset, length),
                (Err(_), NULL_VALUE) => Err(
                    kio_errors::UnexpectedNull::new_err(
                        "Unexpectedly read null where compact string/bytes was expected"
                    )
                ),
                (Err(_), _) => Err(
                    kio_errors::NegativeByteLength::new_err("Found negative byte length")
                ),
            }
        },
    }
}

#[pyfunction]
fn read_nullable_legacy_bytes(bytes: &PyBytes, offset: usize) -> PyResult<(&PyAny, usize)> {
    const NULL_VALUE: i16 = -1;

    match read_int16(bytes, offset) {
        Err(error) => Err(error),
        Ok((length, offset)) => {
            match (usize::try_from(length), length) {
                (Ok(length), _) => _slice_legacy_bytes(bytes, offset, length),
                (Err(_), NULL_VALUE) => Ok((_load_none(bytes.py())?, offset)),
                (Err(_), _) => Err(
                    kio_errors::NegativeByteLength::new_err("Found negative byte length")
                ),
            }
        },
    }
}

#[pyfunction]
fn read_legacy_string(bytes: &PyBytes, offset: usize) -> PyResult<(&PyAny, usize)> {
    const NULL_VALUE: i16 = -1;

    match read_int16(bytes, offset) {
        Err(error) => Err(error),
        Ok((length, offset)) => {
            match (usize::try_from(length), length) {
                (Ok(length), _) => _decode_compact_string(bytes, offset, length + 1),
                (Err(_), NULL_VALUE) => Err(
                    kio_errors::UnexpectedNull::new_err(
                        "Unexpectedly read null where compact string/bytes was expected"
                    )
                ),
                (Err(_), _) => Err(
                    kio_errors::NegativeByteLength::new_err("Found negative byte length")
                ),
            }
        },
    }
}

#[pyfunction]
fn read_nullable_legacy_string(bytes: &PyBytes, offset: usize) -> PyResult<(&PyAny, usize)> {
    const NULL_VALUE: i16 = -1;

    match read_int16(bytes, offset) {
        Err(error) => Err(error),
        Ok((length, offset)) => {
            match (usize::try_from(length), length) {
                (Ok(length), _) => _decode_compact_string(bytes, offset, length + 1),
                (Err(_), NULL_VALUE) => Ok((_load_none(bytes.py())?, offset)),
                (Err(_), _) => Err(
                    kio_errors::NegativeByteLength::new_err("Found negative byte length")
                ),
            }
        },
    }
}

#[pyfunction]
fn read_legacy_array_length(bytes: &PyBytes, offset: usize) -> PyResult<(i32, usize)> {
    read_int32(bytes, offset)
}

#[pyfunction]
fn read_compact_array_length(bytes: &PyBytes, offset: usize) -> PyResult<(usize, usize)> {
    match read_unsigned_varint(bytes, offset) {
        Ok((0, _)) => Err(
            kio_errors::NegativeByteLength::new_err("Found negative array length")
        ),
        // Kafka uses the array size plus 1.
        Ok((value, offset)) => Ok((value - 1, offset)),
        Err(error) => Err(error),
    }
}

#[pyfunction]
fn read_uuid(bytes: &PyBytes, offset: usize) -> PyResult<(&PyAny, usize)> {
    const NULL_VALUE: u32 = 0;
    let byte_end = offset + 16;
    let sliced = &bytes[offset..byte_end];
    let byte_sum: u32 = sliced.iter().map(|&b| b as u32).sum();

    match byte_sum.cmp(&NULL_VALUE) {
        Ordering::Less | Ordering::Equal => {
            let builtins = PyModule::import(bytes.py(), "builtins")?;
            let none = builtins.getattr("None")?;
            Ok((none, byte_end))
        },
        Ordering::Greater => {
            let py = bytes.py();
            let none = _load_none(py)?;
            let py_bytes = PyBytes::new(py, sliced);
            let uuid_cls: Py<PyAny> = PyModule::import(py, "uuid")?.getattr("UUID")?.into();
            // bytes is second key-word argument. We pass hex=None to avoid having to construct
            // key-word arguments.
            let args = (none, py_bytes);
            let uuid_value = uuid_cls.call1(py, args)?.into_ref(py);
            Ok((uuid_value, byte_end))
        },
    }
}


/// A Python module implemented in Rust.
#[pymodule]
fn _kio_core(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(read_boolean, m)?)?;

    m.add_function(wrap_pyfunction!(read_int8, m)?)?;
    m.add_function(wrap_pyfunction!(read_int16, m)?)?;
    m.add_function(wrap_pyfunction!(read_int32, m)?)?;
    m.add_function(wrap_pyfunction!(read_int64, m)?)?;
    m.add_function(wrap_pyfunction!(read_uint8, m)?)?;
    m.add_function(wrap_pyfunction!(read_uint16, m)?)?;
    m.add_function(wrap_pyfunction!(read_uint32, m)?)?;
    m.add_function(wrap_pyfunction!(read_uint64, m)?)?;
    m.add_function(wrap_pyfunction!(read_unsigned_varint, m)?)?;

    m.add_function(wrap_pyfunction!(read_float64, m)?)?;

    m.add_function(wrap_pyfunction!(read_compact_string_as_bytes, m)?)?;
    m.add_function(wrap_pyfunction!(read_compact_string_as_bytes_nullable, m)?)?;
    m.add_function(wrap_pyfunction!(read_compact_string, m)?)?;
    m.add_function(wrap_pyfunction!(read_compact_string_nullable, m)?)?;

    m.add_function(wrap_pyfunction!(read_legacy_bytes, m)?)?;
    m.add_function(wrap_pyfunction!(read_nullable_legacy_bytes, m)?)?;
    m.add_function(wrap_pyfunction!(read_legacy_string, m)?)?;
    m.add_function(wrap_pyfunction!(read_nullable_legacy_string, m)?)?;

    m.add_function(wrap_pyfunction!(read_legacy_array_length, m)?)?;
    m.add_function(wrap_pyfunction!(read_compact_array_length, m)?)?;

    m.add_function(wrap_pyfunction!(read_uuid, m)?)?;

    Ok(())
}
