from __future__ import annotations

import datetime
import struct
from collections.abc import Callable
from typing import IO
from typing import Final
from typing import TypeAlias
from typing import TypeVar
from uuid import UUID

from kio.static.constants import ErrorCode
from kio.static.constants import uuid_zero
from kio.static.primitive import TZAware
from kio.static.primitive import i8
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i32Timedelta
from kio.static.primitive import i64
from kio.static.primitive import i64Timedelta
from kio.static.primitive import u8
from kio.static.primitive import u16
from kio.static.primitive import u32
from kio.static.primitive import u64

from .errors import UnexpectedNull

T = TypeVar("T")
Reader: TypeAlias = Callable[[IO[bytes]], T]


def read_boolean(buffer: IO[bytes]) -> bool:
    return struct.unpack(">?", buffer.read(1))[0]  # type: ignore[no-any-return]


def read_int8(buffer: IO[bytes]) -> i8:
    return struct.unpack(">b", buffer.read(1))[0]  # type: ignore[no-any-return]


def read_int16(buffer: IO[bytes]) -> i16:
    return struct.unpack(">h", buffer.read(2))[0]  # type: ignore[no-any-return]


def read_int32(buffer: IO[bytes]) -> i32:
    return struct.unpack(">i", buffer.read(4))[0]  # type: ignore[no-any-return]


def read_int64(buffer: IO[bytes]) -> i64:
    return struct.unpack(">q", buffer.read(8))[0]  # type: ignore[no-any-return]


def read_uint8(buffer: IO[bytes]) -> u8:
    return struct.unpack(">B", buffer.read(1))[0]  # type: ignore[no-any-return]


def read_uint16(buffer: IO[bytes]) -> u16:
    return struct.unpack(">H", buffer.read(2))[0]  # type: ignore[no-any-return]


def read_uint32(buffer: IO[bytes]) -> u32:
    return struct.unpack(">I", buffer.read(4))[0]  # type: ignore[no-any-return]


def read_uint64(buffer: IO[bytes]) -> u64:
    return struct.unpack(">Q", buffer.read(8))[0]  # type: ignore[no-any-return]


# See description and upstream implementation.
# https://developers.google.com/protocol-buffers/docs/encoding?csw=1#varints
# https://github.com/apache/kafka/blob/ef96ac07f565a73e35c5b0f4c56c8e87cfbaaf59/clients/src/main/java/org/apache/kafka/common/utils/ByteUtils.java#L262
def read_unsigned_varint(buffer: IO[bytes]) -> int:
    """Deserialize an integer stored into variable number of bytes (1-5)."""
    result = 0
    # Increase shift by 7 on each iteration, looping at most 5 times.
    for shift in range(0, 4 * 7 + 1, 7):
        # Read value by a byte at a time.
        (byte,) = buffer.read(1)
        # Add 7 least significant bits to the result.
        seven_bit_chunk = byte & 0b01111111
        result |= seven_bit_chunk << shift
        # If the most significant bit is 1, continue. Otherwise, stop.
        if byte & 0b10000000 == 0:
            return result
    raise ValueError(
        "Varint is too long, the most significant bit in the 5th byte is set"
    )


def read_float64(buffer: IO[bytes]) -> float:
    return struct.unpack(">d", buffer.read(8))[0]  # type: ignore[no-any-return]


def read_compact_string_as_bytes(buffer: IO[bytes]) -> bytes:
    # Apache Kafka® uses the string length plus 1.
    length = read_unsigned_varint(buffer) - 1
    if length == -1:
        raise UnexpectedNull(
            "Unexpectedly read null where compact string/bytes was expected"
        )
    return buffer.read(length)


def read_compact_string_as_bytes_nullable(buffer: IO[bytes]) -> bytes | None:
    # Apache Kafka® uses the string length plus 1.
    length = read_unsigned_varint(buffer) - 1
    if length == -1:
        return None
    return buffer.read(length)


def read_compact_string(buffer: IO[bytes]) -> str:
    return read_compact_string_as_bytes(buffer).decode()


def read_compact_string_nullable(buffer: IO[bytes]) -> str | None:
    bytes_value: bytes | None = read_compact_string_as_bytes_nullable(buffer)
    if bytes_value is None:
        return None
    return bytes_value.decode()


def read_raw_bytes(buffer: IO[bytes]) -> bytes | None:
    length = read_int32(buffer)
    if length == 0:
        return None
    return buffer.read(length - 1)


def read_legacy_bytes(buffer: IO[bytes]) -> bytes:
    length = read_int16(buffer)
    if length == -1:
        raise UnexpectedNull("Unexpectedly read null where bytes was expected")
    return buffer.read(length)


def read_nullable_legacy_bytes(buffer: IO[bytes]) -> bytes | None:
    length = read_int16(buffer)
    if length == -1:
        return None
    return buffer.read(length)


def read_legacy_string(buffer: IO[bytes]) -> str:
    length = read_int16(buffer)
    if length == -1:
        raise UnexpectedNull("Unexpectedly read null where string/bytes was expected")
    return buffer.read(length).decode()


def read_nullable_legacy_string(buffer: IO[bytes]) -> str | None:
    length = read_int16(buffer)
    if length == -1:
        return None
    return buffer.read(length).decode()


read_legacy_array_length: Final = read_int32


def read_compact_array_length(buffer: IO[bytes]) -> int:
    # Apache Kafka® uses the array size plus 1.
    return read_unsigned_varint(buffer) - 1


def read_uuid(buffer: IO[bytes]) -> UUID | None:
    byte_value: bytes = buffer.read(16)
    if byte_value == uuid_zero.bytes:
        return None
    return UUID(bytes=byte_value)


def compact_array_reader(item_reader: Reader[T]) -> Reader[tuple[T, ...]]:
    def read_compact_array(buffer: IO[bytes]) -> tuple[T, ...]:
        return tuple(
            item_reader(buffer) for _ in range(read_compact_array_length(buffer))
        )

    return read_compact_array


def legacy_array_reader(item_reader: Reader[T]) -> Reader[tuple[T, ...]]:
    def read_compact_array(buffer: IO[bytes]) -> tuple[T, ...]:
        return tuple(
            item_reader(buffer) for _ in range(read_legacy_array_length(buffer))
        )

    return read_compact_array


def read_error_code(buffer: IO[bytes]) -> ErrorCode:
    return ErrorCode(read_int16(buffer))


def read_timedelta_i32(buffer: IO[bytes]) -> i32Timedelta:
    return datetime.timedelta(milliseconds=read_int32(buffer))  # type: ignore[return-value]


def read_timedelta_i64(buffer: IO[bytes]) -> i64Timedelta:
    return datetime.timedelta(milliseconds=read_int64(buffer))  # type: ignore[return-value]


def read_datetime_i64(buffer: IO[bytes]) -> TZAware:
    return datetime.datetime.fromtimestamp(  # type: ignore[return-value]
        read_int64(buffer) / 1000,
        datetime.UTC,
    )


def read_nullable_datetime_i64(buffer: IO[bytes]) -> TZAware | None:
    timestamp = read_int64(buffer)
    if timestamp == -1:
        return None
    return TZAware.fromtimestamp(timestamp / 1000)
