import asyncio
import io
import struct
from collections.abc import Callable
from collections.abc import Sequence
from contextlib import closing
from typing import IO
from typing import Final
from typing import TypeAlias
from typing import TypeVar
from uuid import UUID

from kio.schema.primitive import i8
from kio.schema.primitive import i16
from kio.schema.primitive import i32
from kio.schema.primitive import i64
from kio.schema.primitive import u8
from kio.schema.primitive import u16
from kio.schema.primitive import u32
from kio.schema.primitive import u64

from .errors import OutOfBoundValue

Writable: TypeAlias = asyncio.StreamWriter | IO[bytes]
T = TypeVar("T")
Writer: TypeAlias = Callable[[Writable, T], None]


def write_boolean(buffer: Writable, value: bool) -> None:
    buffer.write(struct.pack(">?", value))


def write_int8(buffer: Writable, value: i8) -> None:
    buffer.write(struct.pack(">b", value))


def write_int16(buffer: Writable, value: i16) -> None:
    buffer.write(struct.pack(">h", value))


def write_int32(buffer: Writable, value: i32) -> None:
    buffer.write(struct.pack(">i", value))


def write_int64(buffer: Writable, value: i64) -> None:
    buffer.write(struct.pack(">q", value))


def write_uint8(buffer: Writable, value: u8) -> None:
    buffer.write(struct.pack(">B", value))


def write_uint16(buffer: Writable, value: u16) -> None:
    buffer.write(struct.pack(">H", value))


def write_uint32(buffer: Writable, value: u32) -> None:
    buffer.write(struct.pack(">I", value))


def write_uint64(buffer: Writable, value: u64) -> None:
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


def write_float64(buffer: Writable, value: float) -> None:
    buffer.write(struct.pack(">d", value))


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
        write_int16(buffer, i16(-1))
        return
    if isinstance(value, str):
        value = value.encode()

    try:
        length = i16(len(value))
    except TypeError as exception:
        raise OutOfBoundValue(
            f"String is too long for legacy string format ({len(value)} > "
            f"{i16.__high__})"
        ) from exception

    write_int16(buffer, length)
    buffer.write(value)


def write_legacy_string(buffer: Writable, value: str | bytes) -> None:
    """Write a non-nullable string with legacy int16 length encoding."""
    if value is None:
        raise TypeError("Unexpectedly received None value")
    write_nullable_legacy_string(buffer, value)


def write_empty_tagged_fields(buffer: Writable) -> None:
    write_unsigned_varint(buffer, 0)


def write_array_length(buffer: Writable, value: i32) -> None:
    write_int32(buffer, value)


def write_compact_array_length(buffer: Writable, value: int) -> None:
    # Kafka uses the array size plus 1 to ensure that `None` can be
    # distinguished from empty.
    write_unsigned_varint(buffer, value + 1)


def write_uuid(buffer: Writable, value: UUID) -> None:
    buffer.write(value.bytes)


def compact_array_writer(item_writer: Writer[T]) -> Writer[Sequence[T]]:
    def write_compact_array(buffer: Writable, items: Sequence[T]) -> None:
        write_compact_array_length(buffer, len(items))
        for item in items:
            item_writer(buffer, item)

    return write_compact_array


def legacy_array_writer(item_writer: Writer[T]) -> Writer[Sequence[T]]:
    def write_legacy_array(buffer: Writable, items: Sequence[T]) -> None:
        try:
            length = i32(len(items))
        except TypeError as exception:
            raise OutOfBoundValue(
                f"Sequence is too long for legacy array format ({len(items)} > "
                f"{i32.__high__})"
            ) from exception
        write_array_length(buffer, length)
        for item in items:
            item_writer(buffer, item)

    return write_legacy_array


def write_tagged_field(
    buffer: Writable,
    tag: int,
    writer: Writer[T],
    value: T,
) -> None:
    # See KIP-482 for details.
    # https://cwiki.apache.org/confluence/display/KAFKA/KIP-482%3A+The+Kafka+Protocol+should+Support+Optional+Tagged+Fields#KIP482:TheKafkaProtocolshouldSupportOptionalTaggedFields-SpecifyingTaggedFields

    # Write encoded value to a temporary buffer.
    with closing(io.BytesIO()) as value_buffer:
        writer(value_buffer, value)
        encoded = value_buffer.getvalue()

    write_unsigned_varint(buffer, tag)  # tag
    write_unsigned_varint(buffer, len(encoded))  # length
    buffer.write(encoded)  # data
