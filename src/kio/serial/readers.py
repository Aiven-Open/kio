from __future__ import annotations

import datetime
from collections.abc import Callable
from typing import IO
from typing import TypeAlias
from typing import TypeVar

from phantom.datetime import TZAware

from kio.static.constants import ErrorCode
from kio.static.primitive import i32Timedelta
from kio.static.primitive import i64Timedelta

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
