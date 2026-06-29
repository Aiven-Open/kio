from __future__ import annotations

from typing import Protocol
from typing import TypeAlias
from typing import TypeVar

from typing_extensions import Buffer

from kio._kio_native import compact_array_reader
from kio._kio_native import legacy_array_reader
from kio._kio_native import read_boolean
from kio._kio_native import read_compact_array_length
from kio._kio_native import read_compact_string
from kio._kio_native import read_compact_string_as_bytes
from kio._kio_native import read_compact_string_as_bytes_nullable
from kio._kio_native import read_compact_string_nullable
from kio._kio_native import read_datetime_i64
from kio._kio_native import read_error_code
from kio._kio_native import read_float64
from kio._kio_native import read_int8
from kio._kio_native import read_int16
from kio._kio_native import read_int32
from kio._kio_native import read_int64
from kio._kio_native import read_legacy_array_length
from kio._kio_native import read_legacy_bytes
from kio._kio_native import read_legacy_string
from kio._kio_native import read_nullable_datetime_i64
from kio._kio_native import read_nullable_legacy_bytes
from kio._kio_native import read_nullable_legacy_string
from kio._kio_native import read_signed_varint
from kio._kio_native import read_signed_varlong
from kio._kio_native import read_timedelta_i32
from kio._kio_native import read_timedelta_i64
from kio._kio_native import read_uint8
from kio._kio_native import read_uint16
from kio._kio_native import read_uint32
from kio._kio_native import read_uint64
from kio._kio_native import read_unsigned_varint
from kio._kio_native import read_unsigned_varlong
from kio._kio_native import read_uuid
from kio._kio_native import tz_aware_from_i64

T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)
SizedResult: TypeAlias = tuple[T, int]


class Reader(Protocol[T_co]):
    def __call__(
        self,
        buffer: Buffer,
        offset: int,
        /,
    ) -> SizedResult[T_co]: ...


__all__ = (
    "read_boolean",
    "read_int8",
    "read_int16",
    "read_int32",
    "read_int64",
    "read_uint8",
    "read_uint16",
    "read_uint32",
    "read_uint64",
    "read_float64",
    "read_uuid",
    "read_unsigned_varint",
    "read_unsigned_varlong",
    "read_compact_string_as_bytes",
    "read_compact_string_as_bytes_nullable",
    "read_compact_string",
    "read_compact_string_nullable",
    "read_legacy_bytes",
    "read_nullable_legacy_bytes",
    "read_legacy_string",
    "read_nullable_legacy_string",
    "read_legacy_array_length",
    "read_compact_array_length",
    "read_error_code",
    "read_timedelta_i32",
    "read_timedelta_i64",
    "read_datetime_i64",
    "read_nullable_datetime_i64",
    "read_signed_varint",
    "read_signed_varlong",
    "compact_array_reader",
    "legacy_array_reader",
    "tz_aware_from_i64",
)
