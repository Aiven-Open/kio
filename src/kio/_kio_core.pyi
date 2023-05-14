import datetime
from uuid import UUID

from phantom.datetime import TZAware

from kio.static.constants import ErrorCode
from kio.static.primitive import i8, i16, i32, i64, u8, u16, u32, u64, f64
from typing import TypeVar, TypeAlias

T = TypeVar("T")
_Result: TypeAlias = tuple[T, int]

def read_boolean(
    bytes: bytes,
    offset: int,
) -> _Result[bool]:
    ...

def read_int8(
    bytes: bytes,
    offset: int,
) -> _Result[i8]:
    ...

def read_int16(
    bytes: bytes,
    offset: int,
) -> _Result[i16]:
    ...

def read_int32(
    bytes: bytes,
    offset: int,
) -> _Result[i32]:
    ...
def read_int64(
    bytes: bytes,
    offset: int,
) -> _Result[i64]:
    ...
def read_uint8(
    bytes: bytes,
    offset: int,
) -> _Result[u8]:
    ...
def read_uint16(
    bytes: bytes,
    offset: int,
) -> _Result[u16]:
    ...
def read_uint32(
    bytes: bytes,
    offset: int,
) -> _Result[u32]:
    ...
def read_uint64(
    bytes: bytes,
    offset: int,
) -> _Result[u64]:
    ...
def read_unsigned_varint(
    bytes: bytes,
    offset: int,
) -> _Result[int]:
    ...

def read_float64(
    bytes: bytes,
    offset: int,
) -> _Result[f64]:
    ...

def read_compact_string_as_bytes(
    bytes: bytes,
    offset: int,
) -> _Result[bytes]:
    ...

def read_compact_string_as_bytes_nullable(
    bytes: bytes,
    offset: int,
) -> _Result[bytes | None]:
    ...

def read_compact_string(
    bytes: bytes,
    offset: int,
) -> _Result[str]:
    ...
def read_compact_string_nullable(
    bytes: bytes,
    offset: int,
) -> _Result[str | None]:
    ...



def read_legacy_bytes(
    bytes: bytes,
    offset: int,
) -> _Result[bytes]:
    ...
def read_nullable_legacy_bytes(
    bytes: bytes,
    offset: int,
) -> _Result[bytes | None]:
    ...
def read_legacy_string(
    bytes: bytes,
    offset: int,
) -> _Result[str]:
    ...
def read_nullable_legacy_string(
    bytes: bytes,
    offset: int,
) -> _Result[str | None]:
    ...


def read_legacy_array_length(
    bytes: bytes,
    offset: int,
) -> _Result[i32]:
    ...
def read_compact_array_length(
    bytes: bytes,
    offset: int,
) -> _Result[int]:  # todo: type as uvarint
    ...

def read_uuid(
    bytes: bytes,
    offset: int,
) -> _Result[UUID]:
    ...
def read_error_code(
    bytes: bytes,
    offset: int,
) -> _Result[ErrorCode]:
    ...
def read_timedelta_i32(
    bytes: bytes,
    offset: int,
) -> _Result[datetime.timedelta]:
    ...
def read_timedelta_i64(
    bytes: bytes,
    offset: int,
) -> _Result[datetime.timedelta]:
    ...
def read_datetime_i64(
    bytes: bytes,
    offset: int,
) -> _Result[TZAware]:
    ...
def read_nullable_datetime_i64(
    bytes: bytes,
    offset: int,
) -> _Result[TZAware|None]:
    ...
