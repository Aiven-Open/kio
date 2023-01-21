import asyncio
import struct
from collections.abc import Callable
from typing import IO
from typing import Final
from typing import TypeAlias
from typing import TypeVar

Writable: TypeAlias = asyncio.StreamWriter | IO[bytes]
T = TypeVar("T")
Writer: TypeAlias = Callable[[Writable, T], None]


def write_boolean(buffer: Writable, value: bool) -> None:
    buffer.write(struct.pack(">?", value))


def write_int8(buffer: Writable, value: int) -> None:
    buffer.write(struct.pack(">b", value))


def write_int16(buffer: Writable, value: int) -> None:
    buffer.write(struct.pack(">h", value))


def write_int32(buffer: Writable, value: int) -> None:
    buffer.write(struct.pack(">i", value))


def write_int64(buffer: Writable, value: int) -> None:
    buffer.write(struct.pack(">q", value))


def write_uint8(buffer: Writable, value: int) -> None:
    buffer.write(struct.pack(">B", value))


def write_uint16(buffer: Writable, value: int) -> None:
    buffer.write(struct.pack(">H", value))


def write_uint32(buffer: Writable, value: int) -> None:
    buffer.write(struct.pack(">I", value))


def write_uint64(buffer: Writable, value: int) -> None:
    buffer.write(struct.pack(">Q", value))


unsigned_varint_upper_limit: Final = 2**31 - 1


def write_unsigned_varint(buffer: Writable, value: int) -> None:
    """
    Serialize an integer value between 0 and 2^31 - 1 to bytearray using 1-5
    bytes depending on value size.

    See description and Kafka implementation:
    - https://developers.google.com/protocol-buffers/docs/encoding?csw=1#varints
    - https://github.com/apache/kafka/blob/ef96ac07f565a73e35c5b0f4c56c8e87cfbaaf59/clients/src/main/java/org/apache/kafka/common/utils/ByteUtils.java#L262
    """
    if value < 0:
        raise ValueError("Value must be positive")
    if value > unsigned_varint_upper_limit:
        raise ValueError(f"Value cannot exceed {unsigned_varint_upper_limit}")

    # Read value by 7-bit chunks, shift.
    seven_bit_chunk = value & 0b01111111
    value >>= 7

    while value:
        # Add 1 as the most significant bit - the indicator that more bits
        # remain.
        buffer.write((0b10000000 | seven_bit_chunk).to_bytes(1, "little"))
        seven_bit_chunk = value & 0b01111111
        value >>= 7

    # Add (implicitly) 0 as the most significant bit - the indicator of the last
    # 7-bit chunk.
    buffer.write(seven_bit_chunk.to_bytes(1, "little"))


def write_nullable_compact_string(buffer: Writable, value: str | bytes | None) -> None:
    """Write a nullable string with compact length encoding."""
    if value is None:
        write_unsigned_varint(buffer, 0)
        return
    if isinstance(value, str):
        value = value.encode()
    # The compact string format uses the string length plus 1, so that null can be
    # encoded as an unsigned integer 0.
    write_unsigned_varint(buffer, len(value) + 1)
    buffer.write(value)


def write_compact_string(buffer: Writable, value: str | bytes) -> None:
    """Write a non-nullable string with compact length encoding."""
    if value is None:
        raise TypeError("Unexpectedly received None value")
    write_nullable_compact_string(buffer, value)


def write_nullable_legacy_string(buffer: Writable, value: str | bytes | None) -> None:
    """Write a nullable string with legacy int16 length encoding."""
    if value is None:
        write_int16(buffer, -1)
        return
    if isinstance(value, str):
        value = value.encode()
    write_int16(buffer, len(value))
    buffer.write(value)


def write_legacy_string(buffer: Writable, value: str | bytes | None) -> None:
    """Write a non-nullable string with legacy int16 length encoding."""
    if value is None:
        raise TypeError("Unexpectedly received None value")
    return write_nullable_legacy_string(buffer, value)


def write_empty_tagged_fields(buffer: Writable) -> None:
    write_unsigned_varint(buffer, 0)


def write_array_length(buffer: Writable, value: int) -> None:
    return write_int32(buffer, value)


def write_compact_array_length(buffer: Writable, value: int) -> None:
    # Kafka uses the array size plus 1 to ensure that `None` can be
    # distinguished from empty.
    return write_unsigned_varint(buffer, value + 1)
