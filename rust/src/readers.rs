use pyo3::Python;
use pyo3::buffer::PyBuffer;
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::PyBytes;
use std::cmp::Ordering;

mod kio_errors {
    pyo3::import_exception!(kio.serial.errors, UnexpectedNull);
    pyo3::import_exception!(kio.serial.errors, InvalidUnicode);
    pyo3::import_exception!(kio.serial.errors, NegativeByteLength);
    pyo3::import_exception!(kio.serial.errors, OutOfBoundValue);
    pyo3::import_exception!(kio.serial.errors, BufferUnderflow);
}

pub(crate) fn error_buffer_exhausted<T>() -> PyResult<T> {
    Err(kio_errors::BufferUnderflow::new_err("Buffer is exhausted"))
}

pub(crate) fn data_from_input(
    py: Python<'_>,
    buffered: Py<PyAny>,
    offset: usize,
) -> PyResult<&[u8]> {
    // https://github.com/PyO3/pyo3/issues/2824
    let buffer = PyBuffer::<u8>::get(buffered.bind(py))?;
    // Note: this requires passing read-only buffers from Python, so e.g.
    // BytesIO().getbuffer() will not work. Requiring passing a read-only buffer will
    // makes it safe to (eventually) release the GIL while parsing.
    if !buffer.readonly() {
        return Err(PyValueError::new_err(
            "Received writable byte buffer where read-only was expected",
        ));
    }
    let data_size = buffer.item_count();
    if data_size < offset {
        return error_buffer_exhausted();
    }
    let data_pointer = buffer.buf_ptr() as *const u8;
    let data = unsafe { std::slice::from_raw_parts(data_pointer, data_size) };
    Ok(&data[offset..])
}

pub(crate) type SizedResult<T> = PyResult<(T, usize)>;

pub(crate) fn internal_read_boolean(bytes: &[u8]) -> SizedResult<bool> {
    match bytes {
        [0, ..] => Ok((false, 1)),
        [1, ..] => Ok((true, 1)),
        [] => error_buffer_exhausted(),
        _ => Err(PyValueError::new_err("Invalid boolean value")),
    }
}

#[pyfunction]
pub fn read_boolean(py: Python, buffered: Py<PyAny>, offset: usize) -> SizedResult<bool> {
    internal_read_boolean(data_from_input(py, buffered, offset)?)
}

pub(crate) fn internal_read_int8(bytes: &[u8]) -> SizedResult<i8> {
    match bytes {
        [a, ..] => Ok((i8::from_be_bytes([*a]), 1)),
        _ => error_buffer_exhausted(),
    }
}

#[pyfunction]
pub fn read_int8(py: Python, buffered: Py<PyAny>, offset: usize) -> SizedResult<i8> {
    internal_read_int8(data_from_input(py, buffered, offset)?)
}

pub(crate) fn internal_read_int16(bytes: &[u8]) -> SizedResult<i16> {
    match bytes {
        [a, b, ..] => Ok((i16::from_be_bytes([*a, *b]), 2)),
        _ => error_buffer_exhausted(),
    }
}

#[pyfunction]
pub fn read_int16(py: Python, buffered: Py<PyAny>, offset: usize) -> SizedResult<i16> {
    internal_read_int16(data_from_input(py, buffered, offset)?)
}

pub(crate) fn internal_read_int32(bytes: &[u8]) -> SizedResult<i32> {
    match bytes {
        [a, b, c, d, ..] => Ok((i32::from_be_bytes([*a, *b, *c, *d]), 4)),
        _ => error_buffer_exhausted(),
    }
}

#[pyfunction]
pub fn read_int32(py: Python, buffered: Py<PyAny>, offset: usize) -> SizedResult<i32> {
    internal_read_int32(data_from_input(py, buffered, offset)?)
}

pub(crate) fn internal_read_int64(bytes: &[u8]) -> SizedResult<i64> {
    match bytes {
        [a, b, c, d, e, f, g, h, ..] => {
            Ok((i64::from_be_bytes([*a, *b, *c, *d, *e, *f, *g, *h]), 8))
        }
        _ => error_buffer_exhausted(),
    }
}

#[pyfunction]
pub fn read_int64(py: Python, buffered: Py<PyAny>, offset: usize) -> SizedResult<i64> {
    internal_read_int64(data_from_input(py, buffered, offset)?)
}

pub(crate) fn internal_read_uint8(bytes: &[u8]) -> SizedResult<u8> {
    match bytes {
        [a, ..] => Ok((u8::from_be_bytes([*a]), 1)),
        _ => error_buffer_exhausted(),
    }
}

#[pyfunction]
pub fn read_uint8(py: Python, buffered: Py<PyAny>, offset: usize) -> SizedResult<u8> {
    internal_read_uint8(data_from_input(py, buffered, offset)?)
}

pub(crate) fn internal_read_uint16(bytes: &[u8]) -> SizedResult<u16> {
    match bytes {
        [a, b, ..] => Ok((u16::from_be_bytes([*a, *b]), 2)),
        _ => error_buffer_exhausted(),
    }
}

#[pyfunction]
pub fn read_uint16(py: Python, buffered: Py<PyAny>, offset: usize) -> SizedResult<u16> {
    internal_read_uint16(data_from_input(py, buffered, offset)?)
}

pub(crate) fn internal_read_uint32(bytes: &[u8]) -> SizedResult<u32> {
    match bytes {
        [a, b, c, d, ..] => Ok((u32::from_be_bytes([*a, *b, *c, *d]), 4)),
        _ => error_buffer_exhausted(),
    }
}

#[pyfunction]
pub fn read_uint32(py: Python, buffered: Py<PyAny>, offset: usize) -> SizedResult<u32> {
    internal_read_uint32(data_from_input(py, buffered, offset)?)
}

pub(crate) fn internal_read_uint64(bytes: &[u8]) -> SizedResult<u64> {
    match bytes {
        [a, b, c, d, e, f, g, h, ..] => {
            Ok((u64::from_be_bytes([*a, *b, *c, *d, *e, *f, *g, *h]), 8))
        }
        _ => error_buffer_exhausted(),
    }
}

#[pyfunction]
pub fn read_uint64(py: Python, buffered: Py<PyAny>, offset: usize) -> SizedResult<u64> {
    internal_read_uint64(data_from_input(py, buffered, offset)?)
}

// See description and Kafka implementation.
// https://developers.google.com/protocol-buffers/docs/encoding?csw=1#varints
// https://github.com/apache/kafka/blob/ef96ac07f565a73e35c5b0f4c56c8e87cfbaaf59/clients/src/main/java/org/apache/kafka/common/utils/ByteUtils.java#L262
pub(crate) fn internal_read_unsigned_varint(bytes: &[u8]) -> SizedResult<usize> {
    let mut result: usize = 0;
    let mut byte_count = 0;
    let mut shift: u8 = 0;

    loop {
        if byte_count == 5 {
            return Err(PyValueError::new_err(
                "Varint is too long, the most significant bit in the 5th byte is set",
            ));
        }
        // Read value by a byte at a time.
        if let Some(byte) = bytes.get(byte_count) {
            byte_count += 1;
            // Add 7 least significant bits to the result.
            let seven_bit_chunk = byte & 0b01111111;
            result |= usize::from(seven_bit_chunk) << shift;
            // Increase shift by 7 on each iteration.
            shift += 7;
            // If the most significant bit is 1, continue. Otherwise, stop.
            if byte & 0b10000000 == 0 {
                break;
            }
        } else {
            return error_buffer_exhausted();
        }
    }

    Ok((result, byte_count))
}

#[pyfunction]
pub fn read_unsigned_varint(py: Python, buffered: Py<PyAny>, offset: usize) -> SizedResult<usize> {
    internal_read_unsigned_varint(data_from_input(py, buffered, offset)?)
}

// See description and Kafka implementation.
// https://developers.google.com/protocol-buffers/docs/encoding?csw=1#varints
// https://github.com/apache/kafka/blob/ef96ac07f565a73e35c5b0f4c56c8e87cfbaaf59/clients/src/main/java/org/apache/kafka/common/utils/ByteUtils.java#L262
pub(crate) fn internal_read_unsigned_varlong(bytes: &[u8]) -> SizedResult<usize> {
    let mut result: usize = 0;
    let mut byte_count = 0;
    let mut shift: u8 = 0;

    loop {
        if byte_count == 10 {
            return Err(PyValueError::new_err(
                "Varlong is too long, the most significant bit in the 10th byte is set",
            ));
        }
        // Read value by a byte at a time.
        if let Some(byte) = bytes.get(byte_count) {
            byte_count += 1;
            // Add 7 least significant bits to the result.
            let seven_bit_chunk = byte & 0b01111111;
            result |= usize::from(seven_bit_chunk) << shift;
            // Increase shift by 7 on each iteration.
            shift += 7;
            // If the most significant bit is 1, continue. Otherwise, stop.
            if byte & 0b10000000 == 0 {
                break;
            }
        } else {
            return error_buffer_exhausted();
        }
    }

    Ok((result, byte_count))
}

#[pyfunction]
pub fn read_unsigned_varlong(py: Python, buffered: Py<PyAny>, offset: usize) -> SizedResult<usize> {
    internal_read_unsigned_varlong(data_from_input(py, buffered, offset)?)
}

pub(crate) fn zigzag_decode(encoded: u64) -> i64 {
    ((encoded >> 1) as i64) ^ (-((encoded & 1) as i64))
}

#[pyfunction]
pub fn read_signed_varint(py: Python, buffered: Py<PyAny>, offset: usize) -> SizedResult<i64> {
    let (enc, size) = internal_read_unsigned_varint(data_from_input(py, buffered, offset)?)?;
    Ok((zigzag_decode(enc as u64), size))
}

#[pyfunction]
pub fn read_signed_varlong(py: Python, buffered: Py<PyAny>, offset: usize) -> SizedResult<i64> {
    let (enc, size) = internal_read_unsigned_varlong(data_from_input(py, buffered, offset)?)?;
    Ok((zigzag_decode(enc as u64), size))
}

pub(crate) fn internal_read_float64(bytes: &[u8]) -> SizedResult<f64> {
    match bytes {
        [a, b, c, d, e, f, g, h, ..] => {
            Ok((f64::from_be_bytes([*a, *b, *c, *d, *e, *f, *g, *h]), 8))
        }
        _ => error_buffer_exhausted(),
    }
}

#[pyfunction]
pub fn read_float64(py: Python, buffered: Py<PyAny>, offset: usize) -> SizedResult<f64> {
    internal_read_float64(data_from_input(py, buffered, offset)?)
}

pub(crate) fn internal_read_compact_string_as_bytes(bytes: &[u8]) -> SizedResult<&[u8]> {
    match internal_read_unsigned_varint(bytes) {
        Ok((0, _)) => Err(kio_errors::UnexpectedNull::new_err(
            "Unexpectedly read null where compact string/bytes was expected",
        )),
        Ok((length, byte_offset)) => {
            // String length is encoded with an offset of 1, to allow encoding null as 0.
            let byte_end = byte_offset + length - 1;
            if bytes.len() < byte_end {
                return error_buffer_exhausted();
            }
            let sliced = &bytes[byte_offset..byte_end];
            Ok((sliced, byte_end))
        }
        Err(error) => Err(error),
    }
}

#[pyfunction]
pub fn read_compact_string_as_bytes<'a>(
    py: Python<'a>,
    buffered: Py<PyAny>,
    offset: usize,
) -> SizedResult<&'a [u8]> {
    internal_read_compact_string_as_bytes(data_from_input(py, buffered, offset)?)
}

pub(crate) fn internal_read_compact_string_as_bytes_nullable(
    bytes: &[u8],
) -> SizedResult<Option<&[u8]>> {
    match internal_read_unsigned_varint(bytes) {
        Ok((0, offset)) => Ok((None, offset)),
        Ok((length, byte_offset)) => {
            // String length is encoded with an offset of 1, to allow encoding null as 0.
            let byte_end = byte_offset + length - 1;
            if bytes.len() < byte_end {
                return error_buffer_exhausted();
            }
            let sliced = &bytes[byte_offset..byte_end];
            Ok((Some(sliced), byte_end))
        }
        Err(error) => Err(error),
    }
}

#[pyfunction]
pub fn read_compact_string_as_bytes_nullable<'a>(
    py: Python<'a>,
    buffered: Py<PyAny>,
    offset: usize,
) -> SizedResult<Option<&'a [u8]>> {
    internal_read_compact_string_as_bytes_nullable(data_from_input(py, buffered, offset)?)
}

pub(crate) fn internal_slice_as_string(
    bytes: &[u8],
    offset: usize,
    length: usize,
) -> SizedResult<&str> {
    // String length is encoded with an offset of 1, to allow encoding null as 0.
    let byte_end = offset + length - 1;
    if bytes.len() < byte_end {
        return error_buffer_exhausted();
    }
    let sliced = &bytes[offset..byte_end];
    match std::str::from_utf8(sliced) {
        Ok(string) => Ok((string, byte_end)),
        Err(_) => Err(kio_errors::InvalidUnicode::new_err(
            "Failed interpreting bytes as UTF-8",
        )),
    }
}

pub(crate) fn internal_read_compact_string(bytes: &[u8]) -> SizedResult<&str> {
    match internal_read_unsigned_varint(bytes) {
        Ok((0, _)) => Err(kio_errors::UnexpectedNull::new_err(
            "Unexpectedly read null where compact string/bytes was expected",
        )),
        Ok((length, byte_offset)) => internal_slice_as_string(bytes, byte_offset, length),
        Err(error) => Err(error),
    }
}

#[pyfunction]
pub fn read_compact_string<'a>(
    py: Python<'a>,
    buffered: Py<PyAny>,
    offset: usize,
) -> SizedResult<&'a str> {
    internal_read_compact_string(data_from_input(py, buffered, offset)?)
}

pub(crate) fn internal_read_compact_string_nullable(bytes: &[u8]) -> SizedResult<Option<&str>> {
    match internal_read_unsigned_varint(bytes) {
        Ok((0, offset)) => Ok((None, offset)),
        Ok((length, byte_offset)) => {
            let (decoded, end_offset) = internal_slice_as_string(bytes, byte_offset, length)?;
            Ok((Some(decoded), end_offset))
        }
        Err(error) => Err(error),
    }
}

#[pyfunction]
pub fn read_compact_string_nullable<'a>(
    py: Python<'a>,
    buffered: Py<PyAny>,
    offset: usize,
) -> SizedResult<Option<&'a str>> {
    internal_read_compact_string_nullable(data_from_input(py, buffered, offset)?)
}

pub(crate) fn internal_read_int16_as_usize(bytes: &[u8]) -> SizedResult<Option<usize>> {
    const NULL_VALUE: i16 = -1;
    match internal_read_int16(bytes) {
        Ok((NULL_VALUE, offset)) => Ok((None, offset)),
        Ok((length, offset)) => match usize::try_from(length) {
            Ok(length) => Ok((Some(length), offset)),
            Err(_) => Err(kio_errors::NegativeByteLength::new_err(
                "Found negative byte length",
            )),
        },
        Err(error) => Err(error),
    }
}

pub(crate) fn internal_read_int32_as_usize(bytes: &[u8]) -> SizedResult<Option<usize>> {
    const NULL_VALUE: i32 = -1;
    match internal_read_int32(bytes) {
        Ok((NULL_VALUE, offset)) => Ok((None, offset)),
        Ok((length, offset)) => match usize::try_from(length) {
            Ok(length) => Ok((Some(length), offset)),
            Err(_) => Err(kio_errors::NegativeByteLength::new_err(
                "Found negative byte length",
            )),
        },
        Err(error) => Err(error),
    }
}

pub(crate) fn slice_legacy_bytes(bytes: &[u8], offset: usize, length: usize) -> SizedResult<&[u8]> {
    let byte_end = offset + length;
    if bytes.len() < byte_end {
        return error_buffer_exhausted();
    }
    Ok((&bytes[offset..byte_end], byte_end))
}

pub(crate) fn internal_read_legacy_bytes(bytes: &[u8]) -> SizedResult<&[u8]> {
    match internal_read_int32_as_usize(bytes) {
        Ok((Some(length), offset)) => slice_legacy_bytes(bytes, offset, length),
        Ok((None, _)) => Err(kio_errors::UnexpectedNull::new_err(
            "Unexpectedly read null where compact string/bytes was expected",
        )),
        Err(error) => Err(error),
    }
}

#[pyfunction]
pub fn read_legacy_bytes<'a>(
    py: Python<'a>,
    buffered: Py<PyAny>,
    offset: usize,
) -> SizedResult<&'a [u8]> {
    internal_read_legacy_bytes(data_from_input(py, buffered, offset)?)
}

pub(crate) fn internal_read_nullable_legacy_bytes(bytes: &[u8]) -> SizedResult<Option<&[u8]>> {
    match internal_read_int32_as_usize(bytes) {
        Ok((None, offset)) => Ok((None, offset)),
        Ok((Some(length), offset)) => {
            let (sliced_bytes, offset) = slice_legacy_bytes(bytes, offset, length)?;
            Ok((Some(sliced_bytes), offset))
        }
        Err(error) => Err(error),
    }
}

#[pyfunction]
pub fn read_nullable_legacy_bytes<'a>(
    py: Python<'a>,
    buffered: Py<PyAny>,
    offset: usize,
) -> SizedResult<Option<&'a [u8]>> {
    internal_read_nullable_legacy_bytes(data_from_input(py, buffered, offset)?)
}

pub(crate) fn internal_read_legacy_string(bytes: &[u8]) -> SizedResult<&str> {
    match internal_read_int16_as_usize(bytes) {
        Ok((Some(length), offset)) => internal_slice_as_string(bytes, offset, length + 1),
        Ok((None, _)) => Err(kio_errors::UnexpectedNull::new_err(
            "Unexpectedly read null where legacy string was expected",
        )),
        Err(error) => Err(error),
    }
}

#[pyfunction]
pub fn read_legacy_string<'a>(
    py: Python<'a>,
    buffered: Py<PyAny>,
    offset: usize,
) -> SizedResult<&'a str> {
    internal_read_legacy_string(data_from_input(py, buffered, offset)?)
}

pub(crate) fn internal_nullable_read_legacy_string(bytes: &[u8]) -> SizedResult<Option<&str>> {
    match internal_read_int16_as_usize(bytes) {
        Ok((Some(length), offset)) => {
            let (string, offset) = internal_slice_as_string(bytes, offset, length + 1)?;
            Ok((Some(string), offset))
        }
        Ok((None, offset)) => Ok((None, offset)),
        Err(error) => Err(error),
    }
}

#[pyfunction]
pub fn read_nullable_legacy_string<'a>(
    py: Python<'a>,
    buffered: Py<PyAny>,
    offset: usize,
) -> SizedResult<Option<&'a str>> {
    internal_nullable_read_legacy_string(data_from_input(py, buffered, offset)?)
}

#[pyfunction]
pub fn read_legacy_array_length(
    py: Python,
    buffered: Py<PyAny>,
    offset: usize,
) -> SizedResult<i32> {
    internal_read_int32(data_from_input(py, buffered, offset)?)
}

pub(crate) fn internal_read_compact_array_length(bytes: &[u8]) -> SizedResult<Option<usize>> {
    match internal_read_unsigned_varint(bytes) {
        Ok((0, offset)) => Ok((None, offset)),
        // Kafka uses the array size plus 1.
        Ok((value, offset)) => Ok((Some(value - 1), offset)),
        Err(error) => Err(error),
    }
}

#[pyfunction]
pub fn read_compact_array_length(
    py: Python,
    buffered: Py<PyAny>,
    offset: usize,
) -> SizedResult<Option<usize>> {
    internal_read_compact_array_length(data_from_input(py, buffered, offset)?)
}

const UUID_BYTE_SIZE: usize = 16;

pub(crate) fn internal_read_uuid(bytes: &[u8]) -> PyResult<Option<&[u8]>> {
    const NULL_VALUE: u32 = 0;
    if bytes.len() < UUID_BYTE_SIZE {
        return error_buffer_exhausted();
    }
    let sliced = &bytes[..UUID_BYTE_SIZE];
    let byte_sum: u32 = sliced.iter().map(|&b| b as u32).sum();
    match byte_sum.cmp(&NULL_VALUE) {
        Ordering::Equal | Ordering::Less => Ok(None),
        Ordering::Greater => Ok(Some(sliced)),
    }
}

pub(crate) fn instantiate_uuid<'a>(
    py: Python<'a>,
    bytes: Option<&[u8]>,
) -> SizedResult<Option<Py<PyAny>>> {
    match bytes {
        Some(bytes) => {
            let none = PyModule::import(py, "builtins")?.getattr("None")?;
            let uuid_cls: Py<PyAny> = PyModule::import(py, "uuid")?.getattr("UUID")?.into();
            let py_bytes = PyBytes::new(py, bytes);
            // bytes is second key-word argument. We pass hex=None to avoid having to construct
            // key-word arguments.
            let args = (none, py_bytes);
            let uuid_value = uuid_cls.call1(py, args)?.into();
            Ok((uuid_value, UUID_BYTE_SIZE))
        }
        None => Ok((None, UUID_BYTE_SIZE)),
    }
}

#[pyfunction]
pub fn read_uuid(py: Python, buffered: Py<PyAny>, offset: usize) -> SizedResult<Option<Py<PyAny>>> {
    instantiate_uuid(
        py,
        internal_read_uuid(data_from_input(py, buffered, offset)?)?,
    )
}

pub(crate) fn internal_read_error_code(bytes: &[u8]) -> SizedResult<i16> {
    internal_read_int16(bytes)
}

pub(crate) fn wrap_error_code_value(py: Python<'_>, int_value: i16) -> PyResult<Py<PyAny>> {
    let error_code_cls: Py<PyAny> = PyModule::import(py, "kio.schema.errors")?
        .getattr("ErrorCode")?
        .into();
    error_code_cls.call1(py, (int_value,))
}

#[pyfunction]
pub fn read_error_code(py: Python, buffered: Py<PyAny>, offset: usize) -> SizedResult<Py<PyAny>> {
    let (int_value, end_offset) = internal_read_error_code(data_from_input(py, buffered, offset)?)?;
    let error_code = wrap_error_code_value(py, int_value)?;
    Ok((error_code, end_offset))
}

pub(crate) fn instantiate_timedelta<'a, T: IntoPyObject<'a>>(
    py: Python<'a>,
    int_value: T,
) -> PyResult<Py<PyAny>> {
    let timedelta_cls: Py<PyAny> = PyModule::import(py, "datetime")?
        .getattr("timedelta")?
        .into();
    let args = (
        0,         // days
        0,         // seconds
        0,         // microseconds
        int_value, // milliseconds
    );
    timedelta_cls.call1(py, args)
}

pub(crate) fn internal_read_timedelta_i32(bytes: &[u8]) -> SizedResult<i32> {
    internal_read_int32(bytes)
}

#[pyfunction]
pub fn read_timedelta_i32(
    py: Python,
    buffered: Py<PyAny>,
    offset: usize,
) -> SizedResult<Py<PyAny>> {
    let (int_value, end_offset) =
        internal_read_timedelta_i32(data_from_input(py, buffered, offset)?)?;
    let timedelta = instantiate_timedelta(py, int_value)?;
    Ok((timedelta, end_offset))
}

pub(crate) fn internal_read_timedelta_i64(bytes: &[u8]) -> SizedResult<i64> {
    internal_read_int64(bytes)
}

#[pyfunction]
pub fn read_timedelta_i64(
    py: Python,
    buffered: Py<PyAny>,
    offset: usize,
) -> SizedResult<Py<PyAny>> {
    let (int_value, end_offset) =
        internal_read_timedelta_i64(data_from_input(py, buffered, offset)?)?;
    let timedelta = instantiate_timedelta(py, int_value)?;
    Ok((timedelta, end_offset))
}

pub(crate) fn as_datetime<'a>(py: Python<'a>, timestamp_ms: i64) -> PyResult<Py<PyAny>> {
    let module = PyModule::import(py, "datetime")?;
    let cls: Py<PyAny> = module.getattr("datetime")?.into();
    let tz: Py<PyAny> = module.getattr("UTC")?.into();
    let args = (timestamp_ms / 1000, tz);
    cls.call_method1(py, "fromtimestamp", args)
}

const DATETIME_I64_NULL: &i64 = &-1;

pub(crate) fn internal_read_datetime_i64(bytes: &[u8]) -> SizedResult<i64> {
    let (timestamp_ms, offset) = internal_read_int64(bytes)?;
    match timestamp_ms.gt(DATETIME_I64_NULL) {
        true => Ok((timestamp_ms, offset)),
        false => Err(kio_errors::OutOfBoundValue::new_err(
            "Cannot parse negative timestamp",
        )),
    }
}

#[pyfunction]
pub fn read_datetime_i64(py: Python, buffered: Py<PyAny>, offset: usize) -> SizedResult<Py<PyAny>> {
    let (timestamp_ms, end_offset) =
        internal_read_datetime_i64(data_from_input(py, buffered, offset)?)?;
    let datetime = as_datetime(py, timestamp_ms)?;
    Ok((datetime, end_offset))
}

pub(crate) fn internal_read_nullable_datetime_i64(bytes: &[u8]) -> SizedResult<Option<i64>> {
    let (timestamp_ms, offset) = internal_read_int64(bytes)?;
    match timestamp_ms.cmp(DATETIME_I64_NULL) {
        Ordering::Greater => Ok((Some(timestamp_ms), offset)),
        Ordering::Equal => Ok((None, offset)),
        Ordering::Less => Err(kio_errors::OutOfBoundValue::new_err(
            "Cannot parse negative timestamp",
        )),
    }
}

#[pyfunction]
pub fn read_nullable_datetime_i64(
    py: Python,
    buffered: Py<PyAny>,
    offset: usize,
) -> SizedResult<Option<Py<PyAny>>> {
    match internal_read_nullable_datetime_i64(data_from_input(py, buffered, offset)?)? {
        (Some(timestamp_ms), end_offset) => Ok((Some(as_datetime(py, timestamp_ms)?), end_offset)),
        (None, end_offset) => Ok((None, end_offset)),
    }
}

/// Millisecond timestamp to [`kio.static.primitive.TZAware`] via `TZAware.truncate`.
#[pyfunction]
pub fn tz_aware_from_i64(py: Python<'_>, timestamp_ms: i64) -> PyResult<Py<PyAny>> {
    let dt_mod = PyModule::import(py, "datetime")?;
    let utc = dt_mod.getattr("UTC")?;
    let dt_cls = dt_mod.getattr("datetime")?;
    let ts = (timestamp_ms as f64) / 1000.0;
    let dt = dt_cls.call_method1("fromtimestamp", (ts, &utc))?;
    let tzaware_cls = PyModule::import(py, "kio.static.primitive")?.getattr("TZAware")?;
    Ok(tzaware_cls.call_method1("truncate", (&dt,))?.unbind())
}

#[cfg(test)]
mod tests {
    use super::*;

    // ---------------------------------------------------------------------------
    // `zigzag_decode` is an internal function not exposed to Python, so it cannot
    // be tested from the Python suite.  All other reader behaviour is tested in
    // tests/serial/test_readers.py; do not add duplicate coverage here.
    // ---------------------------------------------------------------------------

    #[test]
    fn zigzag_decode_known_values() {
        // Zigzag maps non-negative integers to even encoded values and negative
        // integers to odd encoded values: 0→0, -1→1, 1→2, -2→3, 2→4.
        assert_eq!(zigzag_decode(0), 0);
        assert_eq!(zigzag_decode(1), -1);
        assert_eq!(zigzag_decode(2), 1);
        assert_eq!(zigzag_decode(3), -2);
        assert_eq!(zigzag_decode(4), 2);
        assert_eq!(zigzag_decode(u64::MAX), i64::MIN);
    }
}
