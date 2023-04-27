from __future__ import annotations

import datetime
import math
from typing import TYPE_CHECKING
from typing import Final

from phantom import Phantom
from phantom.interval import Inclusive

if TYPE_CHECKING:
    from hypothesis.strategies import SearchStrategy


class i64(int, Inclusive, low=-(2**63), high=2**63 - 1):
    ...


class i32(i64, Inclusive, low=-(2**31), high=2**31 - 1):
    ...


class i16(i32, Inclusive, low=-(2**15), high=2**15 - 1):
    ...


class i8(i16, Inclusive, low=-128, high=127):
    ...


class u64(int, Inclusive, low=0, high=2**64 - 1):
    ...


class u32(u64, Inclusive, low=0, high=2**32 - 1):
    ...


class u16(u32, Inclusive, low=0, high=2**16 - 1):
    ...


class u8(u16, Inclusive, low=0, high=2**8 - 1):
    ...


class f64(float, Phantom, predicate=math.isfinite):
    @classmethod
    def __register_strategy__(cls) -> SearchStrategy:
        from hypothesis.strategies import floats

        return floats(allow_nan=False, allow_infinity=False)


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


class i32Timedelta(datetime.timedelta, Phantom, predicate=is_i32_timedelta):
    @classmethod
    def __register_strategy__(cls) -> SearchStrategy:
        from hypothesis.strategies import composite

        @composite
        def timedeltas(  # type: ignore[no-untyped-def]
            draw,
            elements=i32.__register_strategy__(),
        ) -> datetime.timedelta:
            return datetime.timedelta(milliseconds=draw(elements))

        return timedeltas()


i64_timedelta_min: Final = datetime.timedelta.min
i64_timedelta_max: Final = datetime.timedelta.max


def is_i64_timedelta(value: datetime.timedelta) -> bool:
    return (
        i64_timedelta_min <= value <= i64_timedelta_max
        and has_millisecond_precision(value)
    )


class i64Timedelta(datetime.timedelta, Phantom, predicate=is_i64_timedelta):
    @classmethod
    def __register_strategy__(cls) -> SearchStrategy:
        from hypothesis.strategies import composite

        @composite
        def timedeltas(  # type: ignore[no-untyped-def]
            draw,
            elements=i64.__register_strategy__(),
        ) -> datetime.timedelta:
            return datetime.timedelta(milliseconds=draw(elements))

        return timedeltas()
