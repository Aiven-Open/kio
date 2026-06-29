import datetime

from dataclasses import Field
from typing import Any
from typing import TypeVar
from uuid import UUID

from typing_extensions import Buffer

from kio.schema.errors import ErrorCode
from kio.serial.readers import Reader
from kio.serial.readers import SizedResult
from kio.static.primitive import TZAware
from kio.static.primitive import f64
from kio.static.primitive import i8
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i64
from kio.static.primitive import u8
from kio.static.primitive import u16
from kio.static.primitive import u32
from kio.static.primitive import u64
from kio.static.primitive import uvarint
from kio.static.primitive import uvarlong
from kio.static.protocol import Entity

T = TypeVar("T")

def read_boolean(
    buffered: Buffer,
    offset: int,
    /,
) -> SizedResult[bool]: ...
def read_int8(
    buffered: Buffer,
    offset: int,
    /,
) -> SizedResult[i8]: ...
def read_int16(
    buffered: Buffer,
    offset: int,
    /,
) -> SizedResult[i16]: ...
def read_int32(
    buffered: Buffer,
    offset: int,
    /,
) -> SizedResult[i32]: ...
def read_int64(
    buffered: Buffer,
    offset: int,
    /,
) -> SizedResult[i64]: ...
def read_uint8(
    buffered: Buffer,
    offset: int,
    /,
) -> SizedResult[u8]: ...
def read_uint16(
    buffered: Buffer,
    offset: int,
    /,
) -> SizedResult[u16]: ...
def read_uint32(
    buffered: Buffer,
    offset: int,
    /,
) -> SizedResult[u32]: ...
def read_uint64(
    buffered: Buffer,
    offset: int,
    /,
) -> SizedResult[u64]: ...
def read_unsigned_varint(
    buffered: Buffer,
    offset: int,
    /,
) -> SizedResult[uvarint]: ...
def read_unsigned_varlong(
    buffered: Buffer,
    offset: int,
    /,
) -> SizedResult[uvarlong]: ...
def read_float64(
    buffered: Buffer,
    offset: int,
    /,
) -> SizedResult[f64]: ...
def read_compact_string_as_bytes(
    buffered: Buffer,
    offset: int,
    /,
) -> SizedResult[bytes]: ...
def read_compact_string_as_bytes_nullable(
    buffered: Buffer,
    offset: int,
    /,
) -> SizedResult[bytes | None]: ...
def read_compact_string(
    buffered: Buffer,
    offset: int,
    /,
) -> SizedResult[str]: ...
def read_compact_string_nullable(
    buffered: Buffer,
    offset: int,
    /,
) -> SizedResult[str | None]: ...
def read_legacy_bytes(
    buffered: Buffer,
    offset: int,
    /,
) -> SizedResult[bytes]: ...
def read_nullable_legacy_bytes(
    buffered: Buffer,
    offset: int,
    /,
) -> SizedResult[bytes | None]: ...
def read_legacy_string(
    buffered: Buffer,
    offset: int,
    /,
) -> SizedResult[str]: ...
def read_nullable_legacy_string(
    buffered: Buffer,
    offset: int,
    /,
) -> SizedResult[str | None]: ...
def read_legacy_array_length(
    buffered: Buffer,
    offset: int,
    /,
) -> SizedResult[i32]: ...
def read_compact_array_length(
    buffered: Buffer,
    offset: int,
    /,
) -> SizedResult[int | None]: ...
def read_uuid(
    buffered: Buffer,
    offset: int,
    /,
) -> SizedResult[UUID | None]: ...
def read_error_code(
    buffered: Buffer,
    offset: int,
    /,
) -> SizedResult[ErrorCode]: ...
def read_timedelta_i32(
    buffered: Buffer,
    offset: int,
    /,
) -> SizedResult[datetime.timedelta]: ...
def read_timedelta_i64(
    buffered: Buffer,
    offset: int,
    /,
) -> SizedResult[datetime.timedelta]: ...
def read_datetime_i64(
    buffered: Buffer,
    offset: int,
    /,
) -> SizedResult[TZAware]: ...
def read_nullable_datetime_i64(
    buffered: Buffer,
    offset: int,
    /,
) -> SizedResult[TZAware | None]: ...
def read_signed_varint(
    buffered: Buffer,
    offset: int,
    /,
) -> SizedResult[int]: ...
def read_signed_varlong(
    buffered: Buffer,
    offset: int,
    /,
) -> SizedResult[int]: ...
def tz_aware_from_i64(timestamp_ms: i64) -> TZAware: ...
def compact_array_reader(item_reader: Reader[T]) -> Reader[tuple[T, ...] | None]: ...
def legacy_array_reader(item_reader: Reader[T]) -> Reader[tuple[T, ...] | None]: ...
def entity_reader(entity_type: type[Entity], nullable: bool = False) -> Reader[Any]: ...
def get_field_reader(
    entity_type: type[Entity],
    field: Field[Any],
    is_request_header: bool,
    is_tagged_field: bool,
) -> Reader[Any]: ...
def get_reader(
    kafka_type: str,
    flexible: bool,
    optional: bool,
) -> Reader: ...
