import datetime
import io
import struct
import sys
import uuid

from typing import IO

import pytest

from kio.serial.errors import OutOfBoundValue
from kio.serial.errors import UnexpectedNull
from kio.serial.readers import Reader
from kio.serial.readers import read_compact_string
from kio.serial.readers import read_compact_string_as_bytes
from kio.serial.readers import read_compact_string_as_bytes_nullable
from kio.serial.readers import read_compact_string_nullable
from kio.serial.readers import read_datetime_i64
from kio.serial.readers import read_float64
from kio.serial.readers import read_int8
from kio.serial.readers import read_int16
from kio.serial.readers import read_int32
from kio.serial.readers import read_int64
from kio.serial.readers import read_legacy_bytes
from kio.serial.readers import read_legacy_string
from kio.serial.readers import read_nullable_datetime_i64
from kio.serial.readers import read_nullable_legacy_bytes
from kio.serial.readers import read_nullable_legacy_string
from kio.serial.readers import read_uint8
from kio.serial.readers import read_uint16
from kio.serial.readers import read_uint32
from kio.serial.readers import read_uint64
from kio.serial.readers import read_unsigned_varint
from kio.serial.readers import read_uuid
from kio.static.constants import uuid_zero
from kio.static.primitive import TZAware


class IntReaderContract:
    reader: Reader[int]
    lower_limit: int
    lower_limit_as_bytes: bytes
    upper_limit: int
    upper_limit_as_bytes: bytes
    zero_as_bytes: bytes

    @classmethod
    def read(cls, buffer: IO[bytes]) -> int:
        return cls.reader(buffer)

    def test_can_read_lower_limit_sync(self, buffer: io.BytesIO) -> None:
        buffer.write(self.lower_limit_as_bytes)
        buffer.seek(0)
        assert self.lower_limit == self.read(buffer)

    def test_can_read_upper_limit_sync(self, buffer: io.BytesIO) -> None:
        buffer.write(self.upper_limit_as_bytes)
        buffer.seek(0)
        assert self.upper_limit == self.read(buffer)

    def test_can_read_zero_sync(self, buffer: io.BytesIO) -> None:
        buffer.write(self.zero_as_bytes)
        buffer.seek(0)
        assert self.read(buffer) == 0


class TestReadInt8(IntReaderContract):
    reader = read_int8
    lower_limit = -128
    lower_limit_as_bytes = b"\x80"
    upper_limit = 127
    upper_limit_as_bytes = b"\x7f"
    zero_as_bytes = b"\x00"


class TestReadInt16(IntReaderContract):
    reader = read_int16
    lower_limit = -(2**15)
    lower_limit_as_bytes = b"\x80\x00"
    upper_limit = 2**15 - 1
    upper_limit_as_bytes = b"\x7f\xff"
    zero_as_bytes = b"\x00\x00"


class TestReadInt32(IntReaderContract):
    reader = read_int32
    lower_limit = -(2**31)
    lower_limit_as_bytes = b"\x80\x00\x00\x00"
    upper_limit = 2**31 - 1
    upper_limit_as_bytes = b"\x7f\xff\xff\xff"
    zero_as_bytes = b"\x00\x00\x00\x00"


class TestReadInt64(IntReaderContract):
    reader = read_int64
    lower_limit = -(2**63)
    lower_limit_as_bytes = b"\x80\x00\x00\x00\x00\x00\x00\x00"
    upper_limit = 2**63 - 1
    upper_limit_as_bytes = b"\x7f\xff\xff\xff\xff\xff\xff\xff"
    zero_as_bytes = b"\x00\x00\x00\x00\x00\x00\x00\x00"


class TestReadUint8(IntReaderContract):
    reader = read_uint8
    lower_limit = 0
    lower_limit_as_bytes = zero_as_bytes = b"\x00"
    upper_limit = 2**8 - 1
    upper_limit_as_bytes = b"\xff"


class TestReadUint16(IntReaderContract):
    reader = read_uint16
    lower_limit = 0
    lower_limit_as_bytes = zero_as_bytes = b"\x00\x00"
    upper_limit = 2**16 - 1
    upper_limit_as_bytes = b"\xff\xff"
    lower_limit_error_message = "argument out of range"


class TestReadUint32(IntReaderContract):
    reader = read_uint32
    lower_limit = 0
    lower_limit_as_bytes = zero_as_bytes = b"\x00\x00\x00\x00"
    upper_limit = 2**32 - 1
    upper_limit_as_bytes = b"\xff\xff\xff\xff"
    lower_limit_error_message = "argument out of range"


class TestReadUint64(IntReaderContract):
    reader = read_uint64
    lower_limit = 0
    lower_limit_as_bytes = zero_as_bytes = b"\x00\x00\x00\x00\x00\x00\x00\x00"
    upper_limit = 2**64 - 1
    upper_limit_as_bytes = b"\xff\xff\xff\xff\xff\xff\xff\xff"
    match_error_message = r"int too large to convert"


class TestReadUnsignedVarint(IntReaderContract):
    reader = read_unsigned_varint
    lower_limit = 0
    lower_limit_as_bytes = zero_as_bytes = b"\x00"
    upper_limit = 2**31 - 1
    upper_limit_as_bytes = b"\xff\xff\xff\xff\x07"

    def test_raises_value_error_for_too_long_value(self, buffer: io.BytesIO) -> None:
        for _ in range(5):
            buffer.write(0b10000001.to_bytes(1, "little"))
        buffer.seek(0)
        with pytest.raises(ValueError, match=r"^Varint is too long"):
            self.read(buffer)

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
        buffer: io.BytesIO,
        byte_value: bytes,
        expected: int,
    ) -> None:
        buffer.write(byte_value)
        buffer.seek(0)
        assert self.read(buffer) == expected


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
    def test_can_read_value(self, buffer: io.BytesIO, value: float) -> None:
        buffer.write(struct.pack(">d", value))
        buffer.seek(0)
        assert read_float64(buffer) == value


class TestReadCompactStringAsBytes:
    def test_raises_unexpected_null_for_negative_length_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        buffer.write(0b00000000.to_bytes(1, "little"))
        buffer.seek(0)
        with pytest.raises(UnexpectedNull):
            read_compact_string_as_bytes(buffer)

    def test_can_read_bytes_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        value = b"k\x9bC\x94\xbe\x1fV\xd6"
        byte_length = len(value) + 1  # string length is offset by one
        buffer.write(byte_length.to_bytes(1, "little"))
        buffer.write(value)
        buffer.seek(0)
        assert value == read_compact_string_as_bytes(buffer)


class TestReadCompactStringAsBytesNullable:
    def test_returns_null_for_negative_length_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        buffer.write(0b00000000.to_bytes(1, "little"))
        buffer.seek(0)
        assert read_compact_string_as_bytes_nullable(buffer) is None

    def test_can_read_bytes_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        value = b"k\x9bC\x94\xbe\x1fV\xd6"
        byte_length = len(value) + 1  # string length is offset by one
        buffer.write(byte_length.to_bytes(1, "little"))
        buffer.write(value)
        buffer.seek(0)
        assert value == read_compact_string_as_bytes_nullable(buffer)


class TestReadCompactString:
    def test_raises_unexpected_null_for_negative_length_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        buffer.write((0).to_bytes(1, "little"))
        buffer.seek(0)
        with pytest.raises(UnexpectedNull):
            read_compact_string(buffer)

    def test_can_read_string_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        value = "The quick brown 🦊 jumps over the lazy dog 🧖"
        byte_value = value.encode()
        byte_length = len(byte_value) + 1  # string length is offset by one
        buffer.write(byte_length.to_bytes(1, "little"))
        buffer.write(byte_value)
        buffer.seek(0)
        assert value == read_compact_string(buffer)


class TestReadCompactStringNullable:
    def test_returns_null_for_negative_length_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        buffer.write((0).to_bytes(1, "little"))
        buffer.seek(0)
        assert read_compact_string_nullable(buffer) is None

    def test_can_read_string_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        value = "The quick brown 🦊 jumps over the lazy dog 🧖"
        byte_value = value.encode()
        byte_length = len(byte_value) + 1  # string length is offset by one
        buffer.write(byte_length.to_bytes(1, "little"))
        buffer.write(byte_value)
        buffer.seek(0)
        assert value == read_compact_string_nullable(buffer)


class TestReadNullableLegacyBytes:
    def test_returns_none_for_negative_length_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        buffer.write(struct.pack(">i", -1))
        buffer.seek(0)
        assert read_nullable_legacy_bytes(buffer) is None

    def test_can_read_bytes_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        value = b"k\x9bC\x94\xbe\x1fV\xd6"
        byte_length = len(value)
        buffer.write(struct.pack(">i", byte_length))
        buffer.write(value)
        buffer.seek(0)
        assert value == read_nullable_legacy_bytes(buffer)


class TestReadLegacyString:
    def test_raises_unexpected_null_for_negative_length_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        buffer.write(struct.pack(">h", -1))
        buffer.seek(0)
        with pytest.raises(UnexpectedNull):
            read_legacy_string(buffer)

    def test_can_read_string_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        value = "The quick brown 🦊 jumps over the lazy dog 🧖"
        byte_value = value.encode()
        byte_length = len(byte_value)
        buffer.write(struct.pack(">h", byte_length))
        buffer.write(byte_value)
        buffer.seek(0)
        assert value == read_legacy_string(buffer)


class TestReadNullableLegacyString:
    def test_returns_null_for_negative_length_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        buffer.write(struct.pack(">h", -1))
        buffer.seek(0)
        assert read_nullable_legacy_string(buffer) is None

    def test_can_read_string_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        value = "The quick brown 🦊 jumps over the lazy dog 🧖"
        byte_value = value.encode()
        byte_length = len(byte_value)
        buffer.write(struct.pack(">h", byte_length))
        buffer.write(byte_value)
        buffer.seek(0)
        assert value == read_nullable_legacy_string(buffer)


class TestReadLegacyBytes:
    def test_raises_unexpected_null_for_negative_length_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        buffer.write(struct.pack(">i", -1))
        buffer.seek(0)
        with pytest.raises(UnexpectedNull):
            read_legacy_bytes(buffer)

    def test_can_read_bytes_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        value = "The quick brown 🦊 jumps over the lazy dog 🧖"
        byte_value = value.encode()
        byte_length = len(byte_value)
        buffer.write(struct.pack(">i", byte_length))
        buffer.write(byte_value)
        buffer.seek(0)
        assert byte_value == read_legacy_bytes(buffer)


class TestReadUUID:
    def test_reads_zero_as_none(self, buffer: io.BytesIO) -> None:
        buffer.write(uuid_zero.bytes)
        buffer.seek(0)
        assert read_uuid(buffer) is None

    def test_can_read_uuid4(self, buffer: io.BytesIO) -> None:
        value = uuid.uuid4()
        buffer.write(value.bytes)
        buffer.seek(0)
        assert read_uuid(buffer) == value


class TestReadDatetimeI64:
    reader = read_datetime_i64
    lower_limit = datetime.datetime.fromtimestamp(0, tz=datetime.UTC)
    lower_limit_as_bytes = struct.pack(">q", 0)
    upper_limit = datetime.datetime.fromtimestamp(253402300799, datetime.UTC)
    upper_limit_as_bytes = struct.pack(">q", int(upper_limit.timestamp() * 1000))

    @classmethod
    def read(cls, buffer: IO[bytes]) -> TZAware:
        return cls.reader(buffer)

    def test_can_read_lower_limit(self, buffer: io.BytesIO) -> None:
        buffer.write(self.lower_limit_as_bytes)
        buffer.seek(0)
        assert self.lower_limit == self.read(buffer)

    def test_can_read_upper_limit(self, buffer: io.BytesIO) -> None:
        buffer.write(self.upper_limit_as_bytes)
        buffer.seek(0)
        assert self.upper_limit == self.read(buffer)

    # As -1 is special null marker, also test with -2.
    @pytest.mark.parametrize("value", (-1, -2))
    def test_raises_out_of_bound_value_for_negative_values(
        self,
        value: int,
        buffer: io.BytesIO,
    ) -> None:
        buffer.write(struct.pack(">q", value))
        buffer.seek(0)
        with pytest.raises(OutOfBoundValue):
            self.read(buffer)


class TestReadNullableDatetimeI64:
    reader = read_nullable_datetime_i64
    null_as_bytes = struct.pack(">q", -1)
    lower_limit = datetime.datetime.fromtimestamp(0, tz=datetime.UTC)
    lower_limit_as_bytes = struct.pack(">q", 0)
    upper_limit = datetime.datetime.fromtimestamp(253402300799, datetime.UTC)
    upper_limit_as_bytes = struct.pack(">q", int(upper_limit.timestamp() * 1000))

    @classmethod
    def read(cls, buffer: IO[bytes]) -> TZAware | None:
        return cls.reader(buffer)

    def test_can_read_null(self, buffer: io.BytesIO) -> None:
        buffer.write(self.null_as_bytes)
        buffer.seek(0)
        assert self.read(buffer) is None

    def test_can_read_lower_limit(self, buffer: io.BytesIO) -> None:
        buffer.write(self.lower_limit_as_bytes)
        buffer.seek(0)
        assert self.lower_limit == self.read(buffer)

    def test_can_read_upper_limit(self, buffer: io.BytesIO) -> None:
        buffer.write(self.upper_limit_as_bytes)
        buffer.seek(0)
        assert self.upper_limit == self.read(buffer)

    def test_raises_out_of_bound_value_for_negative_values(
        self,
        buffer: io.BytesIO,
    ) -> None:
        buffer.write(struct.pack(">q", -2))
        buffer.seek(0)
        with pytest.raises(OutOfBoundValue):
            self.read(buffer)
