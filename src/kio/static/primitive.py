from __future__ import annotations

import datetime
import math

from collections.abc import Callable
from typing import Final
from typing import Self

from ._phantom import Phantom
from ._phantom import Predicate


class Records(bytes, Phantom, predicate=lambda _: True, bound=bytes): ...


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


class i64(Interval, low=-(2**63), high=2**63 - 1): ...


class i32(i64, low=-(2**31), high=2**31 - 1): ...


class i16(i32, low=-(2**15), high=2**15 - 1): ...


class i8(i16, low=-128, high=127): ...


class u64(Interval, low=0, high=2**64 - 1): ...


class u32(u64, high=2**32 - 1): ...


class u16(u32, high=2**16 - 1): ...


class u8(u16, high=2**8 - 1): ...


class f64(float, Phantom, bound=float, predicate=math.isfinite):
    @classmethod
    def __hypothesis_hook__(cls) -> None:
        from hypothesis.strategies import floats
        from hypothesis.strategies import register_type_strategy

        register_type_strategy(cls, floats(allow_nan=False, allow_infinity=False))  # type: ignore[arg-type]


# Note: because datetime.timedelta is float-based, there are values that do not
# round-trip to the same value when going through timedelta -> milliseconds ->
# timedelta. We'll pragmatically ignore the inconsistency for now, but we need
# to eliminate such values to have stable tests.
# Pragma no cover because this is only used in property tests, and those do not
# contribute to coverage report.
def _timedelta_survives_roundtrip(
    value: datetime.timedelta,
) -> bool:  # pragma: no cover
    return value == datetime.timedelta(milliseconds=round(value.total_seconds() * 1000))


i32_timedelta_min: Final = datetime.timedelta(milliseconds=-(2**31))
i32_timedelta_max: Final = datetime.timedelta(milliseconds=2**31 - 1)


def is_i32_timedelta(value: datetime.timedelta) -> bool:
    return i32_timedelta_min <= value <= i32_timedelta_max


class i32Timedelta(
    datetime.timedelta,
    Phantom,
    bound=datetime.timedelta,
    predicate=is_i32_timedelta,
):
    @classmethod
    def __hypothesis_hook__(cls) -> None:  # pragma: no cover
        from hypothesis import assume
        from hypothesis.strategies import SearchStrategy
        from hypothesis.strategies import composite
        from hypothesis.strategies import integers
        from hypothesis.strategies import register_type_strategy

        @composite
        def i32_timedeltas(
            draw: Callable,
            elements: SearchStrategy[int] = integers(-(2**31), 2**31 - 1),
        ) -> i32Timedelta:
            delta = datetime.timedelta(milliseconds=draw(elements))
            assume(_timedelta_survives_roundtrip(delta))
            return i32Timedelta.parse(delta)

        register_type_strategy(cls, i32_timedeltas())


i64_timedelta_min: Final = datetime.timedelta.min
# If we allow days=999999999, seconds and microseconds can sum to more than
# 24h, which in turn causes it to not round-trip.
i64_timedelta_max: Final = datetime.timedelta.max - datetime.timedelta(days=1)


def is_i64_timedelta(value: datetime.timedelta) -> bool:
    return i64_timedelta_min <= value <= i64_timedelta_max


class i64Timedelta(
    datetime.timedelta,
    Phantom,
    bound=datetime.timedelta,
    predicate=is_i64_timedelta,
):
    @classmethod
    def __hypothesis_hook__(cls) -> None:  # pragma: no cover
        from hypothesis import assume
        from hypothesis.strategies import SearchStrategy
        from hypothesis.strategies import composite
        from hypothesis.strategies import integers
        from hypothesis.strategies import register_type_strategy

        @composite
        def i64_timedeltas(
            draw: Callable,
            elements: SearchStrategy[int] = integers(
                i64_timedelta_min // datetime.timedelta(milliseconds=1),
                i64_timedelta_max // datetime.timedelta(milliseconds=1),
            ),
        ) -> i64Timedelta:
            delta = datetime.timedelta(milliseconds=draw(elements))
            assume(_timedelta_survives_roundtrip(delta))
            return i64Timedelta.parse(delta)

        register_type_strategy(cls, i64_timedeltas())


def is_tz_aware(dt: datetime.datetime) -> bool:
    return (
        dt.tzinfo is not None
        and dt.tzinfo.utcoffset(dt) is not None
        and dt.microsecond == 0
        and dt.timestamp() >= 0
    )


class TZAware(
    datetime.datetime,
    Phantom,
    bound=datetime.datetime,
    predicate=is_tz_aware,
):
    """
    Type describing all datetime.datetime instances that are timezone aware,
    have millisecond precision, and have a non-negative unix timestamp
    representation.

    - Timezone awareness means any object lacking timezone data is excluded.
    - Millisecond precision means any object with microsecond != 0 is excluded.
    - Kafka uses -1 to represent NULL, so negative unix timestamps are not
      supported.
    """

    tzinfo: datetime.tzinfo

    @classmethod
    def __hypothesis_hook__(cls) -> None:  # pragma: no cover
        from hypothesis import assume
        from hypothesis.strategies import SearchStrategy
        from hypothesis.strategies import composite
        from hypothesis.strategies import integers
        from hypothesis.strategies import register_type_strategy
        from hypothesis.strategies import timezones

        min_ts = 0
        max_ts = int(datetime.datetime.max.replace(tzinfo=datetime.UTC).timestamp()) - 1

        @composite
        def milli_second_precision_tz_aware_datetimes(
            draw: Callable,
            timestamp_strategy: SearchStrategy[int] = integers(min_ts, max_ts),
            timezone_strategy: SearchStrategy[datetime.tzinfo] = timezones(),
        ) -> TZAware:
            """
            Generate millisecond precision datetime objects that are representable both
            within the legal boundaries of UTC timestamps, and within the boundaries of
            Python datetime objects (i.e. with 0 < year 10_000.
            """
            try:
                return TZAware.parse(
                    datetime.datetime.fromtimestamp(
                        draw(timestamp_strategy),
                        tz=datetime.UTC,
                    ).astimezone(draw(timezone_strategy))
                )
            except OverflowError:
                # Both timestamps and dates have an upper limit. This means that the
                # upper boundary for timestamps cannot be represented in all timezones.
                # For timezones where the date wraps around to the year 10_000, an
                # OverflowError occurs.
                assume(False)
                raise  # make mypy aware this branch always raises

        register_type_strategy(cls, milli_second_precision_tz_aware_datetimes())

    @classmethod
    def truncate(cls, value: datetime.datetime) -> Self:
        return cls.parse(value.replace(microsecond=0))
