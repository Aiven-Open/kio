from __future__ import annotations

import asyncio
import struct
from collections.abc import Callable
from collections.abc import Generator
from typing import IO
from typing import Any
from typing import TypeAlias
from typing import TypeVar

from typing_extensions import assert_never

from kio.serial.errors import UnexpectedNull

T = TypeVar("T")
Cursor: TypeAlias = Generator["int | Decoder[object]", Any, T]
Decoder: TypeAlias = Callable[[], Cursor[T]]


def decode_boolean() -> Cursor[bool]:
    byte_value: bytes = yield 1
    (value,) = struct.unpack(">?", byte_value)
    return value  # type: ignore[no-any-return]


def decode_int8() -> Cursor[int]:
    byte_value: bytes = yield 1
    (value,) = struct.unpack(">b", byte_value)
    return value  # type: ignore[no-any-return]


def decode_int16() -> Cursor[int]:
    byte_value: bytes = yield 2
    (value,) = struct.unpack(">h", byte_value)
    return value  # type: ignore[no-any-return]


def decode_int32() -> Cursor[int]:
    byte_value: bytes = yield 4
    (value,) = struct.unpack(">i", byte_value)
    return value  # type: ignore[no-any-return]


def decode_int64() -> Cursor[int]:
    byte_value: bytes = yield 8
    (value,) = struct.unpack(">q", byte_value)
    return value  # type: ignore[no-any-return]


def decode_uint8() -> Cursor[int]:
    byte_value: bytes = yield 1
    (value,) = struct.unpack(">B", byte_value)
    return value  # type: ignore[no-any-return]


def decode_uint16() -> Cursor[int]:
    byte_value: bytes = yield 2
    (value,) = struct.unpack(">H", byte_value)
    return value  # type: ignore[no-any-return]


def decode_uint32() -> Cursor[int]:
    byte_value: bytes = yield 4
    (value,) = struct.unpack(">I", byte_value)
    return value  # type: ignore[no-any-return]


def decode_uint64() -> Cursor[int]:
    byte_value: bytes = yield 8
    (value,) = struct.unpack(">Q", byte_value)
    return value  # type: ignore[no-any-return]


def decode_unsigned_varint() -> Cursor[int]:
    """Deserialize an integer stored into variable number of bytes (1-5).

    See description and Kafka implementation:
    - https://developers.google.com/protocol-buffers/docs/encoding?csw=1#varints
    - https://github.com/apache/kafka/blob/ef96ac07f565a73e35c5b0f4c56c8e87cfbaaf59/clients/src/main/java/org/apache/kafka/common/utils/ByteUtils.java#L262
    """
    result = 0
    # Increase shift by 7 on each iteration, looping at most 5 times.
    for shift in range(0, 4 * 7 + 1, 7):
        # Read value by a byte at a time.
        (byte,) = yield 1
        # Add 7 least significant bits to the result.
        seven_bit_chunk = byte & 0b01111111
        result |= seven_bit_chunk << shift
        # If the most significant bit is 1, continue. Otherwise, stop.
        if byte & 0b10000000 == 0:
            return result
    raise ValueError(
        "Varint is too long, the most significant bit in the 5th byte is set"
    )


def decode_compact_string_as_bytes() -> Cursor[bytes]:
    raw_length: int = yield decode_unsigned_varint
    # Kafka uses the string length plus 1.
    length = raw_length - 1
    if length == -1:
        raise UnexpectedNull(
            "Unexpectedly read null where compact string/bytes was expected"
        )
    byte_value: bytes = yield length
    return byte_value


def decode_compact_string_as_bytes_nullable() -> Cursor[bytes | None]:
    raw_length: int = yield decode_unsigned_varint
    # Kafka uses the string length plus 1.
    length = raw_length - 1
    if length == -1:
        return None
    byte_value: bytes = yield length
    return byte_value


def decode_compact_string() -> Cursor[str]:
    bytes_value: bytes = yield decode_compact_string_as_bytes
    return bytes_value.decode()


def decode_compact_string_nullable() -> Cursor[str | None]:
    bytes_value: bytes | None = yield decode_compact_string_as_bytes_nullable
    if bytes_value is None:
        return None
    return bytes_value.decode()


def decode_raw_bytes() -> Cursor[bytes | None]:
    length: int = yield decode_int32
    if length == 0:
        return None
    byte_value: bytes | None = yield length - 1
    return byte_value


def decode_string() -> Cursor[str]:
    length: int = yield decode_int16
    if length == -1:
        raise UnexpectedNull("Unexpectedly read null where string/bytes was expected")
    bytes_value: bytes = yield length
    return bytes_value.decode()


def decode_string_nullable() -> Cursor[str | None]:
    length: int = yield decode_int16
    if length == -1:
        return None
    bytes_value: bytes = yield length
    return bytes_value.decode()


decode_array_length = decode_int32


def decode_compact_array_length() -> Generator[Decoder[int], int, int]:
    decoded_value: int = yield decode_unsigned_varint
    # Kafka uses the array size plus 1.
    return decoded_value - 1


async def read_async(
    reader: asyncio.StreamReader,
    decoder: Decoder[T],
) -> T:
    cursor = decoder()
    instruction = next(cursor)
    step_value: Any
    while True:
        if isinstance(instruction, int):
            step_value = await reader.readexactly(instruction)
        elif callable(instruction):
            step_value = await read_async(reader, instruction)
        else:
            assert_never(instruction)

        try:
            instruction = cursor.send(step_value)
        except StopIteration as exc:
            return exc.value  # type: ignore[no-any-return]


def read_sync(
    buffer: IO[bytes],
    decoder: Decoder[T],
) -> T:
    cursor = decoder()
    instruction = next(cursor)
    step_value: Any
    while True:
        if isinstance(instruction, int):
            step_value = buffer.read(instruction)
        elif callable(instruction):
            step_value = read_sync(buffer, instruction)
        else:
            assert_never(instruction)

        try:
            instruction = cursor.send(step_value)
        except StopIteration as exc:
            return exc.value  # type: ignore[no-any-return]
