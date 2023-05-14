from __future__ import annotations

from collections.abc import Callable
from typing import IO
from typing import TypeAlias
from typing import TypeVar

T = TypeVar("T")
Reader: TypeAlias = Callable[[IO[bytes]], T]


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
