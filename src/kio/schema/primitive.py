# Note! This file is auto-generated from a template, make changes in
# codegen/template/primitive.py.
from __future__ import annotations

import math
from typing import TYPE_CHECKING

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

        return floats(allow_nan=False)
