import datetime

import pytest

from hypothesis import given
from hypothesis.strategies import from_type
from hypothesis.strategies import integers

from kio.static.primitive import Interval
from kio.static.primitive import TZAware
from kio.static.primitive import i8
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i32_timedelta_max
from kio.static.primitive import i32_timedelta_min
from kio.static.primitive import i32Timedelta
from kio.static.primitive import i64
from kio.static.primitive import i64_timedelta_max
from kio.static.primitive import i64_timedelta_min
from kio.static.primitive import i64Timedelta
from kio.static.primitive import u8
from kio.static.primitive import u16
from kio.static.primitive import u32
from kio.static.primitive import u64


class TestInterval:
    def test_cannot_subclass_without_lower_bound(self) -> None:
        with pytest.raises(TypeError, match=r"must set lower bound"):

            class T(Interval, high=1): ...

    def test_cannot_subclass_without_upper_bound(self) -> None:
        with pytest.raises(TypeError, match=r"must set upper bound"):

            class T(Interval, low=1): ...


class TestU8:
    low = u8.__low__
    high = u8.__high__

    @given(from_type(u8))
    def test_is_subtype_of_u16(self, value: u8) -> None:
        assert isinstance(value, u16)

    @given(from_type(u8))
    def test_valid_value_is_instance(self, value: int) -> None:
        assert isinstance(value, u8)

    @given(integers(min_value=high + 1) | integers(max_value=low - 1))
    def test_invalid_value_is_not_instance(self, value: int) -> None:
        assert not isinstance(value, u8)


class TestU16:
    low = u16.__low__
    high = u16.__high__

    @given(from_type(u16))
    def test_is_subtype_of_u32(self, value: u16) -> None:
        assert isinstance(value, u32)

    @given(from_type(u16))
    def test_valid_value_is_instance(self, value: int) -> None:
        assert isinstance(value, u16)

    @given(integers(min_value=high + 1) | integers(max_value=low - 1))
    def test_invalid_value_is_not_instance(self, value: int) -> None:
        assert not isinstance(value, u16)


class TestU32:
    low = u32.__low__
    high = u32.__high__

    @given(from_type(u32))
    def test_is_subtype_of_u64(self, value: u32) -> None:
        assert isinstance(value, u64)

    @given(from_type(u32))
    def test_valid_value_is_instance(self, value: int) -> None:
        assert isinstance(value, u32)

    @given(integers(min_value=high + 1) | integers(max_value=low - 1))
    def test_invalid_value_is_not_instance(self, value: int) -> None:
        assert not isinstance(value, u32)


class TestU64:
    low = u64.__low__
    high = u64.__high__

    @given(from_type(u64))
    def test_valid_value_is_instance(self, value: int) -> None:
        assert isinstance(value, u64)

    @given(integers(min_value=high + 1) | integers(max_value=low - 1))
    def test_invalid_value_is_not_instance(self, value: int) -> None:
        assert not isinstance(value, u64)


class TestI8:
    low = i8.__low__
    high = i8.__high__

    @given(from_type(i8))
    def test_is_subtype_of_i16(self, value: i8) -> None:
        assert isinstance(value, i16)

    @given(from_type(i8))
    def test_valid_value_is_instance(self, value: int) -> None:
        assert isinstance(value, i8)

    @given(integers(min_value=high + 1) | integers(max_value=low - 1))
    def test_invalid_value_is_not_instance(self, value: int) -> None:
        assert not isinstance(value, i8)


class TestI16:
    low = i16.__low__
    high = i16.__high__

    @given(from_type(i16))
    def test_is_subtype_of_i32(self, value: i16) -> None:
        assert isinstance(value, i32)

    @given(from_type(i16))
    def test_valid_value_is_instance(self, value: int) -> None:
        assert isinstance(value, i16)

    @given(integers(min_value=high + 1) | integers(max_value=low - 1))
    def test_invalid_value_is_not_instance(self, value: int) -> None:
        assert not isinstance(value, i16)


class TestI32:
    low = i32.__low__
    high = i32.__high__

    @given(from_type(i32))
    def test_is_subtype_of_i64(self, value: i32) -> None:
        assert isinstance(value, i64)

    @given(from_type(i32))
    def test_valid_value_is_instance(self, value: int) -> None:
        assert isinstance(value, i32)

    @given(integers(min_value=high + 1) | integers(max_value=low - 1))
    def test_invalid_value_is_not_instance(self, value: int) -> None:
        assert not isinstance(value, i32)


class TestI64:
    low = i64.__low__
    high = i64.__high__

    @given(from_type(i64))
    def test_valid_value_is_instance(self, value: int) -> None:
        assert isinstance(value, i64)

    @given(integers(min_value=high + 1) | integers(max_value=low - 1))
    def test_invalid_value_is_not_instance(self, value: int) -> None:
        assert not isinstance(value, i64)


class TestI32Timedelta:
    @pytest.mark.parametrize(
        "value",
        (
            datetime.timedelta(milliseconds=1),
            datetime.timedelta(microseconds=1),
            datetime.timedelta(microseconds=-1),
            datetime.timedelta(milliseconds=1, microseconds=1),
            datetime.timedelta(milliseconds=1, microseconds=-1),
            # Testing upper bound.
            i32_timedelta_max,
            # Testing lower bound.
            i32_timedelta_min,
        ),
    )
    def test_valid_value_is_instance(self, value: datetime.timedelta) -> None:
        assert isinstance(value, i32Timedelta)

    @pytest.mark.parametrize(
        "value",
        (
            object(),
            1,
            # Testing lower bound.
            i32_timedelta_min - datetime.timedelta(milliseconds=1),
            # Testing both lower bound and sub precision.
            i32_timedelta_min - datetime.timedelta(microseconds=1),
            # Testing upper bound.
            i32_timedelta_max + datetime.timedelta(milliseconds=1),
            # Testing both upper bound and sub precision.
            i32_timedelta_max + datetime.timedelta(microseconds=1),
        ),
    )
    def test_invalid_value_is_not_instance(self, value: object) -> None:
        assert not isinstance(value, i32Timedelta)


class TestI64Timedelta:
    @pytest.mark.parametrize(
        "value",
        (
            datetime.timedelta(milliseconds=1),
            datetime.timedelta(microseconds=1),
            datetime.timedelta(microseconds=-1),
            datetime.timedelta(milliseconds=1, microseconds=1),
            datetime.timedelta(milliseconds=1, microseconds=-1),
            # Testing upper bound.
            i64_timedelta_max,
            # Testing lower bound.
            i64_timedelta_min,
        ),
    )
    def test_valid_value_is_instance(self, value: datetime.timedelta) -> None:
        assert isinstance(value, i64Timedelta)

    @pytest.mark.parametrize(
        "value",
        (
            object(),
            1,
            # Testing upper bound.
            i64_timedelta_max + datetime.timedelta(microseconds=1),
        ),
    )
    def test_invalid_value_is_not_instance(self, value: object) -> None:
        assert not isinstance(value, i64Timedelta)

    def test_cannot_represent_values_outside_lower_bound(self) -> None:
        with pytest.raises(OverflowError):
            i64_timedelta_min - datetime.timedelta(microseconds=1)

        with pytest.raises(OverflowError):
            i64_timedelta_min - datetime.timedelta(milliseconds=1)


class TestTZAware:
    @pytest.mark.parametrize(
        "value",
        (
            datetime.datetime(2024, 1, 1, tzinfo=datetime.UTC),
            # Testing lower bound.
            datetime.datetime.fromtimestamp(0, tz=datetime.UTC),
            # Testing upper bound.
            datetime.datetime.max.replace(tzinfo=datetime.UTC, microsecond=0),
        ),
    )
    def test_valid_value_is_instance(self, value: datetime.datetime) -> None:
        assert isinstance(value, TZAware)

    @pytest.mark.parametrize(
        "value",
        (
            # This has sub millisecond precision.
            datetime.datetime.max.replace(tzinfo=datetime.UTC),
            datetime.datetime(2024, 1, 1, microsecond=1, tzinfo=datetime.UTC),
            (
                datetime.datetime(2024, 1, 1, tzinfo=datetime.UTC)
                - datetime.timedelta(microseconds=1)
            ),
            # Testing lower bound.
            datetime.datetime.fromtimestamp(-1, tz=datetime.UTC),
            # No timezone.
            datetime.datetime(2024, 1, 1),
        ),
    )
    def test_invalid_value_is_not_instance(self, value: object) -> None:
        assert not isinstance(value, TZAware)

    def test_cannot_represent_value_over_upper_bound(self) -> None:
        with pytest.raises(OverflowError):
            (
                datetime.datetime.max.replace(tzinfo=datetime.UTC)
                + datetime.timedelta(milliseconds=1)
            )
