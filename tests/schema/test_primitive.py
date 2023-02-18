from typing import cast

from hypothesis import given
from hypothesis.strategies import from_type
from hypothesis.strategies import integers

from kio.schema.primitive import i8
from kio.schema.primitive import i16
from kio.schema.primitive import i32
from kio.schema.primitive import i64
from kio.schema.primitive import u8
from kio.schema.primitive import u16
from kio.schema.primitive import u32
from kio.schema.primitive import u64


class TestU8:
    low = cast(int, u8.__low__)
    high = cast(int, u8.__high__)

    @given(from_type(u8))
    def test_is_subtype_of_i16(self, value: u8) -> None:
        assert isinstance(value, i16)

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
    low = cast(int, u16.__low__)
    high = cast(int, u16.__high__)

    @given(from_type(u16))
    def test_is_subtype_of_i32(self, value: u16) -> None:
        assert isinstance(value, i32)

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
    low = cast(int, u32.__low__)
    high = cast(int, u32.__high__)

    @given(from_type(u32))
    def test_is_subtype_of_i64(self, value: u32) -> None:
        assert isinstance(value, i64)

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
    low = cast(int, u64.__low__)
    high = cast(int, u64.__high__)

    @given(from_type(u64))
    def test_valid_value_is_instance(self, value: int) -> None:
        assert isinstance(value, u64)

    @given(integers(min_value=high + 1) | integers(max_value=low - 1))
    def test_invalid_value_is_not_instance(self, value: int) -> None:
        assert not isinstance(value, u64)


class TestI8:
    low = cast(int, i8.__low__)
    high = cast(int, i8.__high__)

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
    low = cast(int, i16.__low__)
    high = cast(int, i16.__high__)

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
    low = cast(int, i32.__low__)
    high = cast(int, i32.__high__)

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
    low = cast(int, i64.__low__)
    high = cast(int, i64.__high__)

    @given(from_type(i64))
    def test_valid_value_is_instance(self, value: int) -> None:
        assert isinstance(value, i64)

    @given(integers(min_value=high + 1) | integers(max_value=low - 1))
    def test_invalid_value_is_not_instance(self, value: int) -> None:
        assert not isinstance(value, i64)
