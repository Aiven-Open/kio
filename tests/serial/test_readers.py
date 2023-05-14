import datetime
import io
import struct
import sys
import uuid
from typing import Callable

import pytest

import kio._kio_core
from kio.serial.errors import UnexpectedNull, InvalidUnicode, NegativeByteLength, \
    OutOfBoundValue
from kio.static.constants import uuid_zero, ErrorCode


class IntReaderContract:
    reader: Callable[[bytes, int], tuple[int, int]]
    lower_limit: int
    lower_limit_as_bytes: bytes
    upper_limit: int
    upper_limit_as_bytes: bytes
    zero_as_bytes: bytes

    @classmethod
    def read(cls, buffer: bytes, offset: int = 0) -> tuple[int, int]:
        return cls.reader(buffer, offset)

    def test_can_read_lower_limit(self) -> None:
        value, offset = self.read(self.lower_limit_as_bytes)
        assert value == self.lower_limit
        assert offset == len(self.lower_limit_as_bytes)

    def test_can_read_upper_limit(self) -> None:
        value, offset = self.read(self.upper_limit_as_bytes)
        assert value == self.upper_limit
        assert offset == len(self.upper_limit_as_bytes)

    def test_can_read_zero(self) -> None:
        value, offset = self.read(self.zero_as_bytes)
        assert value == 0
        assert offset == len(self.zero_as_bytes)


class TestReadInt8(IntReaderContract):
    reader = kio._kio_core.read_int8
    lower_limit = -128
    lower_limit_as_bytes = b"\x80"
    upper_limit = 127
    upper_limit_as_bytes = b"\x7f"
    zero_as_bytes = b"\x00"


class TestReadInt16(IntReaderContract):
    reader = kio._kio_core.read_int16
    lower_limit = -(2**15)
    lower_limit_as_bytes = b"\x80\x00"
    upper_limit = 2**15 - 1
    upper_limit_as_bytes = b"\x7f\xff"
    zero_as_bytes = b"\x00\x00"


class TestReadInt32(IntReaderContract):
    reader = kio._kio_core.read_int32
    lower_limit = -(2**31)
    lower_limit_as_bytes = b"\x80\x00\x00\x00"
    upper_limit = 2**31 - 1
    upper_limit_as_bytes = b"\x7f\xff\xff\xff"
    zero_as_bytes = b"\x00\x00\x00\x00"


class TestReadInt64(IntReaderContract):
    reader = kio._kio_core.read_int64
    lower_limit = -(2**63)
    lower_limit_as_bytes = b"\x80\x00\x00\x00\x00\x00\x00\x00"
    upper_limit = 2**63 - 1
    upper_limit_as_bytes = b"\x7f\xff\xff\xff\xff\xff\xff\xff"
    zero_as_bytes = b"\x00\x00\x00\x00\x00\x00\x00\x00"


class TestReadUint8(IntReaderContract):
    reader = kio._kio_core.read_uint8
    lower_limit = 0
    lower_limit_as_bytes = zero_as_bytes = b"\x00"
    upper_limit = 2**8 - 1
    upper_limit_as_bytes = b"\xff"


class TestReadUint16(IntReaderContract):
    reader = kio._kio_core.read_uint16
    lower_limit = 0
    lower_limit_as_bytes = zero_as_bytes = b"\x00\x00"
    upper_limit = 2**16 - 1
    upper_limit_as_bytes = b"\xff\xff"
    lower_limit_error_message = "argument out of range"


class TestReadUint32(IntReaderContract):
    reader = kio._kio_core.read_uint32
    lower_limit = 0
    lower_limit_as_bytes = zero_as_bytes = b"\x00\x00\x00\x00"
    upper_limit = 2**32 - 1
    upper_limit_as_bytes = b"\xff\xff\xff\xff"
    lower_limit_error_message = "argument out of range"


class TestReadUint64(IntReaderContract):
    reader = kio._kio_core.read_uint64
    lower_limit = 0
    lower_limit_as_bytes = zero_as_bytes = b"\x00\x00\x00\x00\x00\x00\x00\x00"
    upper_limit = 2**64 - 1
    upper_limit_as_bytes = b"\xff\xff\xff\xff\xff\xff\xff\xff"
    match_error_message = r"int too large to convert"


class TestReadUnsignedVarint(IntReaderContract):
    reader = kio._kio_core.read_unsigned_varint
    lower_limit = 0
    lower_limit_as_bytes = zero_as_bytes = b"\x00"
    upper_limit = 2**31 - 1
    upper_limit_as_bytes = b"\xff\xff\xff\xff\x07"

    def test_raises_value_error_for_too_long_value(self, buffer: io.BytesIO) -> None:
        value = b"".join(
            0b10000001.to_bytes(1, "little")
            for _ in range(5)
        )
        with pytest.raises(ValueError, match=r"^Varint is too long"):
            self.read(value)

    @pytest.mark.parametrize(
        "byte_value, expected",
        [
            (b"\x00", 0),
            (b"\x01", 1),
            (b"\xb9`", 12345),
            (b"\xb1\xa8\x03", 54321),
            (b"\xff\xff\xff\xff\x07", 2147483647),
        ],
    )
    def test_can_read_known_value(
        self,
        byte_value: bytes,
        expected: int,
    ) -> None:
        value, offset = self.read(byte_value)
        assert value == expected
        assert offset == len(byte_value)


class TestReadFloat64:
    @pytest.mark.parametrize(
        "value",
        (
            0,
            0.0,
            1,
            1.0001,
            -2345678.234567,
            sys.float_info.min,
            sys.float_info.max,
        ),
    )
    def test_can_read_value(self, value: float) -> None:
        byte_value = struct.pack(">d", value)
        result, offset = kio._kio_core.read_float64(byte_value, 0)
        assert result == value
        assert offset == 8


class TestReadCompactStringAsBytes:
    def test_raises_unexpected_null_for_negative_length(
        self
    ) -> None:
        length_encoded = 0b00000000.to_bytes(1, "little")
        with pytest.raises(UnexpectedNull):
            kio._kio_core.read_compact_string_as_bytes(length_encoded, 0)

    def test_can_read_bytes(
        self
    ) -> None:
        value = b"k\x9bC\x94\xbe\x1fV\xd6"
        byte_length = len(value) + 1  # string length is offset by one
        length_encoded = (
            # Note! This is a special case, length should be encoded as an
            # unsigned varint.
            byte_length.to_bytes(1, "little") + value
        )

        result, offset = kio._kio_core.read_compact_string_as_bytes(length_encoded, 0)

        assert value == result
        # Size of bytes + size of length value.
        assert offset == len(value) + 1


class TestReadCompactStringAsBytesNullable:
    def test_returns_null_for_negative_length(
        self
    ) -> None:
        length_encoded = 0b00000000.to_bytes(1, "little")
        value, offset = kio._kio_core.read_compact_string_as_bytes_nullable(length_encoded, 0)
        assert value is None
        assert offset is len(length_encoded)
        assert offset == 1

    def test_can_read_bytes(
        self
    ) -> None:
        byte_value = b"k\x9bC\x94\xbe\x1fV\xd6"
        byte_length = len(byte_value) + 1  # string length is offset by one
        length_encoded = (
            # Note! This is a special case, length should be encoded as an
            # unsigned varint.
            byte_length.to_bytes(1, "little")
            + byte_value
        )
        result, offset = kio._kio_core.read_compact_string_as_bytes_nullable(length_encoded, 0)
        assert result == byte_value
        # Size of bytes + size of length value.
        assert offset == len(byte_value) + 1


class TestReadCompactString:
    def test_raises_unexpected_null_for_negative_length(
        self
    ) -> None:
        length_encoded = (0).to_bytes(1, "little")
        with pytest.raises(UnexpectedNull):
            kio._kio_core.read_compact_string(length_encoded, 0)

    def test_raises_invalid_unicode_for_invalid_bytes(self) -> None:
        invalid_byte_value = b"\xc3\x28"
        byte_length = len(invalid_byte_value) + 1  # string length is offset by one
        length_encoded = (
            byte_length.to_bytes(1, "little")
            + invalid_byte_value
        )
        with pytest.raises(InvalidUnicode, match=r"^Failed interpreting bytes as UTF-8$",):
            kio._kio_core.read_compact_string(length_encoded, 0)

    def test_can_read_string(
        self
    ) -> None:
        value = "The quick brown 🦊 jumps over the lazy dog 🧖"
        byte_value = value.encode()
        byte_length = len(byte_value) + 1  # string length is offset by one
        length_encoded = (
            byte_length.to_bytes(1, "little")
            + byte_value
        )
        decoded, offset = kio._kio_core.read_compact_string(length_encoded, 0)
        assert decoded == value
        assert offset == len(byte_value) + 1  # length takes 1 byte


class TestReadCompactStringNullable:
    def test_returns_none_for_negative_length(
        self
    ) -> None:
        length_encoded = (0).to_bytes(1, "little")
        decoded, offset = kio._kio_core.read_compact_string_nullable(length_encoded, 0)
        assert decoded is None
        assert offset == 1

    def test_raises_invalid_unicode_for_invalid_bytes(self) -> None:
        invalid_byte_value = b"\xc3\x28"
        byte_length = len(invalid_byte_value) + 1  # string length is offset by one
        length_encoded = (
            byte_length.to_bytes(1, "little")
            + invalid_byte_value
        )
        with pytest.raises(InvalidUnicode, match=r"^Failed interpreting bytes as UTF-8$",):
            kio._kio_core.read_compact_string_nullable(length_encoded, 0)

    def test_can_read_string(
        self
    ) -> None:
        value = "The quick brown 🦊 jumps over the lazy dog 🧖"
        byte_value = value.encode()
        byte_length = len(byte_value) + 1  # string length is offset by one
        length_encoded = (byte_length.to_bytes(1, "little") + byte_value)
        decoded, offset = kio._kio_core.read_compact_string_nullable(length_encoded, 0)
        assert decoded == value
        assert offset == len(byte_value) + 1  # length takes 1 byte


class TestReadLegacyBytes:
    def test_raises_unexpected_null_for_null_length(
        self
    ) -> None:
        length_encoded = struct.pack(">h", -1)
        with pytest.raises(UnexpectedNull):
            kio._kio_core.read_legacy_bytes(length_encoded, 0)

    def test_raises_negative_byte_length_for_negative_length(
        self
    ) -> None:
        length_encoded = struct.pack(">h", -2)
        with pytest.raises(NegativeByteLength):
            kio._kio_core.read_legacy_bytes(length_encoded, 0)

    def test_can_read_bytes(
        self
    ) -> None:
        value = "The quick brown 🦊 jumps over the lazy dog 🧖"
        byte_value = value.encode()
        byte_length = len(byte_value)
        length_encoded = (
            struct.pack(">h", byte_length)
            + byte_value
        )
        decoded, offset = kio._kio_core.read_legacy_bytes(length_encoded, 0)
        assert decoded == byte_value
        assert offset == len(length_encoded)


class TestReadNullableLegacyBytes:
    def test_returns_none_for_negative_length(
        self
    ) -> None:
        length_encoded = struct.pack(">h", -1)
        decoded, offset = kio._kio_core.read_nullable_legacy_bytes(length_encoded, 0)
        assert decoded is None
        assert offset == len(length_encoded)
        assert offset == 2

    def test_raises_negative_byte_length_for_negative_length(
        self
    ) -> None:
        length_encoded = struct.pack(">h", -2)
        with pytest.raises(NegativeByteLength):
            kio._kio_core.read_nullable_legacy_bytes(length_encoded, 0)

    def test_can_read_bytes(
        self,
        buffer: io.BytesIO,
    ) -> None:
        value = b"k\x9bC\x94\xbe\x1fV\xd6"
        byte_length = len(value)
        length_encoded = (
            struct.pack(">h", byte_length)
            + value
        )
        decoded, offset = kio._kio_core.read_nullable_legacy_bytes(length_encoded, 0)
        assert decoded == value
        assert offset == len(length_encoded)


class TestReadLegacyString:
    def test_raises_unexpected_null_for_negative_length(
        self
    ) -> None:
        length_encoded = struct.pack(">h", -1)
        with pytest.raises(UnexpectedNull):
            kio._kio_core.read_legacy_string(length_encoded, 0)

    def test_raises_negative_byte_length_for_negative_length(
        self
    ) -> None:
        length_encoded = struct.pack(">h", -2)
        with pytest.raises(NegativeByteLength):
            kio._kio_core.read_legacy_string(length_encoded, 0)

    def test_can_read_string(
        self
    ) -> None:
        value = "The quick brown 🦊 jumps over the lazy dog 🧖"
        byte_value = value.encode()
        byte_length = len(byte_value)
        length_encoded = (
            struct.pack(">h", byte_length)
            + byte_value
        )
        decoded, offset = kio._kio_core.read_legacy_string(length_encoded, 0)
        assert decoded == value
        assert offset == len(length_encoded)


class TestReadNullableLegacyString:
    def test_returns_null_for_negative_length(
        self
    ) -> None:
        length_encoded = struct.pack(">h", -1)
        decoded, offset = kio._kio_core.read_nullable_legacy_string(length_encoded, 0)
        assert decoded is None
        assert offset == len(length_encoded)

    def test_raises_negative_byte_length_for_negative_length(
        self
    ) -> None:
        length_encoded = struct.pack(">h", -2)
        with pytest.raises(NegativeByteLength):
            kio._kio_core.read_nullable_legacy_string(length_encoded, 0)

    def test_can_read_string(
        self
    ) -> None:
        value = "The quick brown 🦊 jumps over the lazy dog 🧖"
        byte_value = value.encode()
        byte_length = len(byte_value)
        length_encoded = (
            struct.pack(">h", byte_length)
            + byte_value
        )
        decoded, offset = kio._kio_core.read_nullable_legacy_string(length_encoded, 0)
        assert decoded == value
        assert offset == len(length_encoded)


class TestReadUUID:
    def test_reads_zero_as_none(self) -> None:
        decoded, offset = kio._kio_core.read_uuid(uuid_zero.bytes, 0)
        assert decoded is None
        assert offset == 16

    def test_can_read_uuid4(self) -> None:
        value = uuid.uuid4()
        decoded, offset = kio._kio_core.read_uuid(value.bytes, 0)
        assert decoded == value
        assert offset == len(value.bytes)
        assert offset == 16


class TestReadErrorCode:
    def test_can_read_valid_error_code(self) -> None:
        value = ErrorCode.unknown_server_error
        encoded = struct.pack(">h", value.value)
        decoded, offset = kio._kio_core.read_error_code(encoded, 0)
        assert decoded is value
        assert offset == len(encoded)

    def test_raises_value_error_for_invalid_code(self) -> None:
        encoded = struct.pack(">h", -2)
        with pytest.raises(ValueError, match=r"^-2 is not a valid ErrorCode$"):
            kio._kio_core.read_error_code(encoded, 0)


class TestReadTimedeltaI32:
    def test_can_read_timedelta(self) -> None:
        value = datetime.timedelta(milliseconds=12345)
        encoded = struct.pack(">i", round(value.total_seconds() * 1000))
        decoded, offset = kio._kio_core.read_timedelta_i32(encoded, 0)
        assert decoded == value
        assert offset == len(encoded)


class TestReadTimedeltaI64:
    def test_can_read_timedelta(self) -> None:
        value = datetime.timedelta(milliseconds=12345)
        encoded = struct.pack(">q", round(value.total_seconds() * 1000))
        decoded, offset = kio._kio_core.read_timedelta_i64(encoded, 0)
        assert decoded == value
        assert offset == len(encoded)


class TestReadDatetimeI64:
    def test_can_read_datetime(self) -> None:
        value = datetime.datetime.now(tz=datetime.UTC).replace(microsecond=0)
        encoded = struct.pack(">q", round(value.timestamp() * 1000))
        decoded, offset = kio._kio_core.read_datetime_i64(encoded, 0)
        assert decoded == value
        assert offset == len(encoded)

    def test_raises_out_of_bound_value_for_negative_timestamp(self) -> None:
        encoded = struct.pack(">q", -1)
        with pytest.raises(OutOfBoundValue, match=r"^Cannot parse negative timestamp$"):
            kio._kio_core.read_datetime_i64(encoded, 0)


class TestReadNullableDatetimeI64:
    def test_can_read_datetime(self) -> None:
        value = datetime.datetime.now(tz=datetime.UTC).replace(microsecond=0)
        encoded = struct.pack(">q", round(value.timestamp() * 1000))
        decoded, offset = kio._kio_core.read_nullable_datetime_i64(encoded, 0)
        assert decoded == value
        assert offset == len(encoded)

    def test_can_read_none(self) -> None:
        encoded = struct.pack(">q", -1)
        decoded, offset = kio._kio_core.read_nullable_datetime_i64(encoded, 0)
        assert decoded is None
        assert offset == len(encoded)

    def test_raises_out_of_bound_value_for_negative_timestamp(self) -> None:
        encoded = struct.pack(">q", -2)
        with pytest.raises(OutOfBoundValue, match=r"^Cannot parse negative timestamp$"):
            kio._kio_core.read_nullable_datetime_i64(encoded, 0)
