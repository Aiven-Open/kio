from __future__ import annotations

from typing import TypeVar

from typing_extensions import Buffer

from kio.serial.readers import Reader

T = TypeVar("T")


def read(
    reader: Reader[T],
    buffer: Buffer,
    offset: int = 0,
) -> tuple[T, memoryview]:
    value, size = reader(buffer, offset)
    return value, memoryview(buffer)[offset + size :]


def exhaust(
    reader: Reader[T],
    buffer: Buffer,
    offset: int = 0,
) -> T:
    value, remaining = read(reader, buffer, offset)
    assert remaining == b""
    return value
