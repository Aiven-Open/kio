use pyo3::prelude::*;

mod entity;
mod parse;
mod readers;
mod schema;

#[pymodule]
mod _kio_native {
    #[pymodule_export]
    use crate::entity::compact_array_reader;
    #[pymodule_export]
    use crate::entity::entity_reader;
    #[pymodule_export]
    use crate::entity::get_field_reader;
    #[pymodule_export]
    use crate::entity::legacy_array_reader;
    #[pymodule_export]
    use crate::parse::get_reader;
    #[pymodule_export]
    use crate::readers::read_boolean;
    #[pymodule_export]
    use crate::readers::read_compact_array_length;
    #[pymodule_export]
    use crate::readers::read_compact_string;
    #[pymodule_export]
    use crate::readers::read_compact_string_as_bytes;
    #[pymodule_export]
    use crate::readers::read_compact_string_as_bytes_nullable;
    #[pymodule_export]
    use crate::readers::read_compact_string_nullable;
    #[pymodule_export]
    use crate::readers::read_datetime_i64;
    #[pymodule_export]
    use crate::readers::read_error_code;
    #[pymodule_export]
    use crate::readers::read_float64;
    #[pymodule_export]
    use crate::readers::read_int8;
    #[pymodule_export]
    use crate::readers::read_int16;
    #[pymodule_export]
    use crate::readers::read_int32;
    #[pymodule_export]
    use crate::readers::read_int64;
    #[pymodule_export]
    use crate::readers::read_legacy_array_length;
    #[pymodule_export]
    use crate::readers::read_legacy_bytes;
    #[pymodule_export]
    use crate::readers::read_legacy_string;
    #[pymodule_export]
    use crate::readers::read_nullable_datetime_i64;
    #[pymodule_export]
    use crate::readers::read_nullable_legacy_bytes;
    #[pymodule_export]
    use crate::readers::read_nullable_legacy_string;
    #[pymodule_export]
    use crate::readers::read_signed_varint;
    #[pymodule_export]
    use crate::readers::read_signed_varlong;
    #[pymodule_export]
    use crate::readers::read_timedelta_i32;
    #[pymodule_export]
    use crate::readers::read_timedelta_i64;
    #[pymodule_export]
    use crate::readers::read_uint8;
    #[pymodule_export]
    use crate::readers::read_uint16;
    #[pymodule_export]
    use crate::readers::read_uint32;
    #[pymodule_export]
    use crate::readers::read_uint64;
    #[pymodule_export]
    use crate::readers::read_unsigned_varint;
    #[pymodule_export]
    use crate::readers::read_unsigned_varlong;
    #[pymodule_export]
    use crate::readers::read_uuid;
    #[pymodule_export]
    use crate::readers::tz_aware_from_i64;
}
