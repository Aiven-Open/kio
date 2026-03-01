from __future__ import annotations

import datetime

from collections.abc import Generator
from typing import Protocol
from typing import TypeAlias
from typing import TypeVar
from typing import overload

from typing_extensions import Buffer

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
from kio._kio_native import read_timedelta_i32
from kio._kio_native import read_timedelta_i64
from kio._kio_native import read_uint8
from kio._kio_native import read_uint16
from kio._kio_native import read_uint32
from kio._kio_native import read_uint64
from kio._kio_native import read_unsigned_varint
from kio._kio_native import read_unsigned_varlong
from kio._kio_native import read_uuid
from kio.static.primitive import TZAware
from kio.static.primitive import i64
from kio.static.primitive import svarint
from kio.static.primitive import svarlong
from kio.static.primitive import uvarint
from kio.static.primitive import uvarlong

from .errors import OutOfBoundValue

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


@overload
def _zigzag_decode(value: uvarint) -> svarint: ...


@overload
def _zigzag_decode(value: uvarlong) -> svarlong: ...


def _zigzag_decode(value: uvarlong | uvarint) -> int:
    return (value >> 1) ^ -(value & 1)


# https://protobuf.dev/programming-guides/encoding/#signed-ints
def read_signed_varint(buffer: Buffer, offset: int) -> SizedResult[svarint]:
    zigzag_encoded, size = read_unsigned_varint(buffer, offset)
    return _zigzag_decode(zigzag_encoded), size


def read_signed_varlong(buffer: Buffer, offset: int) -> SizedResult[svarlong]:
    zigzag_encoded, size = read_unsigned_varlong(buffer, offset)
    return _zigzag_decode(zigzag_encoded), size


P = TypeVar("P")
Q = TypeVar("Q")


def _materialize_and_return(
    generator: Generator[P, None, Q],
) -> tuple[tuple[P, ...], Q]:
    values = []
    try:
        while True:
            values.append(next(generator))
    except StopIteration as stop:
        return tuple(values), stop.value
    else:
        raise ValueError("Generator did not raise StopIteration")


def _read_length_items(
    item_reader: Reader[T],
    length: int,
    buffer: Buffer,
    offset: int,
) -> Generator[T, None, int]:
    accumulating_offset = offset
    for _ in range(length):
        item_value, item_size = item_reader(buffer, accumulating_offset)
        accumulating_offset += item_size
        yield item_value
    return accumulating_offset - offset


def compact_array_reader(item_reader: Reader[T]) -> Reader[tuple[T, ...] | None]:
    def read_compact_array(
        buffer: Buffer, offset: int, /
    ) -> SizedResult[tuple[T, ...] | None]:
        length, length_size = read_compact_array_length(buffer, offset)
        if length is None:
            return None, length_size
        items, items_size = _materialize_and_return(
            _read_length_items(item_reader, length, buffer, offset + length_size)
        )
        return items, length_size + items_size

    return read_compact_array


def legacy_array_reader(item_reader: Reader[T]) -> Reader[tuple[T, ...] | None]:
    def read_compact_array(
        buffer: Buffer, offset: int, /
    ) -> SizedResult[tuple[T, ...] | None]:
        length, length_size = read_legacy_array_length(buffer, offset)
        if length == -1:
            return None, length_size
        items, items_size = _materialize_and_return(
            _read_length_items(item_reader, length, buffer, offset + length_size)
        )
        return items, length_size + items_size

    return read_compact_array


def tz_aware_from_i64(timestamp: i64) -> TZAware:
    dt = datetime.datetime.fromtimestamp(timestamp / 1000, datetime.UTC)
    try:
        return TZAware.truncate(dt)
    except TypeError as exception:
        raise OutOfBoundValue("Read invalid value for datetime") from exception
