from __future__ import annotations

import datetime
import math
from collections.abc import Callable
from typing import Final

from ._phantom import Phantom
from ._phantom import Predicate


def inclusive_interval(low: int, high: int) -> Predicate[int]:
    def check(value: int) -> bool:
        return low <= value <= high

    return check


class Interval(int, Phantom, bound=int, predicate=lambda _: True):
    __low__: int
    __high__: int

    def __init_subclass__(
        cls,
        low: int | None = None,
        high: int | None = None,
        **kwargs: object,
    ) -> None:
        if low is None:
            if getattr(cls, "__low__", ...) is ...:
                raise TypeError("Interval definition must set lower bound.")
        else:
            cls.__low__ = low
        if high is None:
            if getattr(cls, "__high__", ...) is ...:
                raise TypeError("Interval definition must set upper bound.")
        else:
            cls.__high__ = high
        super().__init_subclass__(
            bound=int,
            predicate=inclusive_interval(cls.__low__, cls.__high__),
        )

    @classmethod
    def __hypothesis_hook__(cls) -> None:
        from hypothesis.strategies import integers
        from hypothesis.strategies import register_type_strategy

        register_type_strategy(
            cls,
            integers(  # type: ignore[arg-type]
                min_value=getattr(cls, "__low__", None),
                max_value=getattr(cls, "__high__", None),
            ),
        )


class i64(Interval, low=-(2**63), high=2**63 - 1):
    ...


class i32(i64, low=-(2**31), high=2**31 - 1):
    ...


class i16(i32, low=-(2**15), high=2**15 - 1):
    ...


class i8(i16, low=-128, high=127):
    ...


class u64(Interval, low=0, high=2**64 - 1):
    ...


class u32(u64, high=2**32 - 1):
    ...


class u16(u32, high=2**16 - 1):
    ...


class u8(u16, high=2**8 - 1):
    ...


class f64(float, Phantom, bound=float, predicate=math.isfinite):
    @classmethod
    def __hypothesis_hook__(cls) -> None:
        from hypothesis.strategies import floats
        from hypothesis.strategies import register_type_strategy

        register_type_strategy(cls, floats(allow_nan=False, allow_infinity=False))  # type: ignore[arg-type]


def has_millisecond_precision(value: datetime.timedelta) -> bool:
    milliseconds = value.total_seconds() * 1000
    return int(milliseconds) == milliseconds


i32_timedelta_min: Final = datetime.timedelta(milliseconds=-(2**31))
i32_timedelta_max: Final = datetime.timedelta(milliseconds=2**31 - 1)


def is_i32_timedelta(value: datetime.timedelta) -> bool:
    return (
        i32_timedelta_min <= value <= i32_timedelta_max
        and has_millisecond_precision(value)
    )


class i32Timedelta(
    datetime.timedelta,
    Phantom,
    bound=datetime.timedelta,
    predicate=is_i32_timedelta,
):
    @classmethod
    def __hypothesis_hook__(cls) -> None:
        from hypothesis.strategies import SearchStrategy
        from hypothesis.strategies import composite
        from hypothesis.strategies import integers
        from hypothesis.strategies import register_type_strategy

        @composite
        def i32_timedeltas(
            draw: Callable,
            elements: SearchStrategy[int] = integers(-(2**31), 2**31 - 1),
        ) -> i32Timedelta:
            return datetime.timedelta(  # type: ignore[return-value]
                milliseconds=draw(elements)
            )

        register_type_strategy(cls, i32_timedeltas())


i64_timedelta_min: Final = datetime.timedelta.min
i64_timedelta_max: Final = datetime.timedelta.max


def is_i64_timedelta(value: datetime.timedelta) -> bool:
    return (
        i64_timedelta_min <= value <= i64_timedelta_max
        and has_millisecond_precision(value)
    )


class i64Timedelta(
    datetime.timedelta,
    Phantom,
    bound=datetime.timedelta,
    predicate=is_i64_timedelta,
):
    @classmethod
    def __hypothesis_hook__(cls) -> None:
        from hypothesis.strategies import SearchStrategy
        from hypothesis.strategies import composite
        from hypothesis.strategies import integers
        from hypothesis.strategies import register_type_strategy

        @composite
        def i64_timedeltas(
            draw: Callable,
            elements: SearchStrategy[int] = integers(-(2**63), 2**63 - 1),
        ) -> i64Timedelta:
            return datetime.timedelta(  # type: ignore[return-value]
                milliseconds=draw(elements),
            )

        register_type_strategy(cls, i64_timedeltas())


def is_tz_aware(dt: datetime.datetime) -> bool:
    return dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None


class TZAware(
    datetime.datetime,
    Phantom,
    bound=datetime.datetime,
    predicate=is_tz_aware,
):
    tzinfo: datetime.tzinfo

    @classmethod
    def __hypothesis_hook__(cls) -> None:
        from hypothesis.strategies import datetimes
        from hypothesis.strategies import register_type_strategy
        from hypothesis.strategies import timezones

        register_type_strategy(
            cls,
            datetimes(timezones=timezones()),  # type: ignore[arg-type]
        )
