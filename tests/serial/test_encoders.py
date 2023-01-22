import io
import struct
from collections.abc import Callable
from contextlib import closing

import pytest

from kio.serial.encoders import Writable
from kio.serial.encoders import write_compact_string
from kio.serial.encoders import write_empty_tagged_fields
from kio.serial.encoders import write_int8
from kio.serial.encoders import write_int16
from kio.serial.encoders import write_int32
from kio.serial.encoders import write_int64
from kio.serial.encoders import write_legacy_string
from kio.serial.encoders import write_nullable_compact_string
from kio.serial.encoders import write_uint8
from kio.serial.encoders import write_uint16
from kio.serial.encoders import write_uint32
from kio.serial.encoders import write_uint64
from kio.serial.encoders import write_unsigned_varint


class IntWriterContract:
    write_function: Callable[[Writable, int], None]
    lower_limit: int
    lower_limit_as_bytes: bytes
    upper_limit: int
    upper_limit_as_bytes: bytes
    zero_as_bytes: bytes

    @property
    def match_error_message(self) -> str:
        return rf"format requires {self.lower_limit} <= number <= {self.upper_limit}"

    @property
    def upper_limit_error_message(self) -> str:
        return self.match_error_message

    @property
    def lower_limit_error_message(self) -> str:
        return self.match_error_message

    @classmethod
    def call_function(cls, buffer: io.BytesIO, value: int) -> None:
        cls.write_function(buffer, value)

    def test_raises_struct_error_when_exceeding_lower_limit(
        self,
        buffer: io.BytesIO,
    ) -> None:
        with pytest.raises(struct.error, match=self.lower_limit_error_message):
            self.call_function(buffer, self.lower_limit - 1)

    def test_raises_struct_error_when_exceeding_upper_limit(
        self,
        buffer: io.BytesIO,
    ) -> None:
        with pytest.raises(struct.error, match=self.upper_limit_error_message):
            self.call_function(buffer, self.upper_limit + 1)

    def test_can_encode_lower_limit(self, buffer: io.BytesIO) -> None:
        self.call_function(buffer, self.lower_limit)
        buffer.seek(0)
        assert self.lower_limit_as_bytes == buffer.read(100)

    def test_can_encode_upper_limit(self, buffer: io.BytesIO) -> None:
        self.call_function(buffer, self.upper_limit)
        buffer.seek(0)
        assert self.upper_limit_as_bytes == buffer.read(100)

    def test_can_write_zero(self, buffer: io.BytesIO) -> None:
        self.call_function(buffer, 0)
        buffer.seek(0)
        assert self.zero_as_bytes == buffer.read(100)


class TestWriteInt8(IntWriterContract):
    write_function = write_int8
    lower_limit = -128
    lower_limit_as_bytes = b"\x80"
    upper_limit = 127
    upper_limit_as_bytes = b"\x7f"
    zero_as_bytes = b"\x00"


class TestWriteInt16(IntWriterContract):
    write_function = write_int16
    lower_limit = -(2**15)
    lower_limit_as_bytes = b"\x80\x00"
    upper_limit = 2**15 - 1
    upper_limit_as_bytes = b"\x7f\xff"
    zero_as_bytes = b"\x00\x00"


class TestWriteInt32(IntWriterContract):
    write_function = write_int32
    lower_limit = -(2**31)
    lower_limit_as_bytes = b"\x80\x00\x00\x00"
    upper_limit = 2**31 - 1
    upper_limit_as_bytes = b"\x7f\xff\xff\xff"
    zero_as_bytes = b"\x00\x00\x00\x00"


class TestWriteInt64(IntWriterContract):
    write_function = write_int64
    lower_limit = -(2**63)
    lower_limit_as_bytes = b"\x80\x00\x00\x00\x00\x00\x00\x00"
    upper_limit = 2**63 - 1
    upper_limit_as_bytes = b"\x7f\xff\xff\xff\xff\xff\xff\xff"
    zero_as_bytes = b"\x00\x00\x00\x00\x00\x00\x00\x00"
    match_error_message = "int too large to convert"


class TestWriteUint8(IntWriterContract):
    write_function = write_uint8
    lower_limit = 0
    lower_limit_as_bytes = zero_as_bytes = b"\x00"
    upper_limit = 2**8 - 1
    upper_limit_as_bytes = b"\xff"


class TestWriteUint16(IntWriterContract):
    write_function = write_uint16
    lower_limit = 0
    lower_limit_as_bytes = zero_as_bytes = b"\x00\x00"
    upper_limit = 2**16 - 1
    upper_limit_as_bytes = b"\xff\xff"
    lower_limit_error_message = "argument out of range"


class TestWriteUint32(IntWriterContract):
    write_function = write_uint32
    lower_limit = 0
    lower_limit_as_bytes = zero_as_bytes = b"\x00\x00\x00\x00"
    upper_limit = 2**32 - 1
    upper_limit_as_bytes = b"\xff\xff\xff\xff"
    lower_limit_error_message = "argument out of range"


class TestWriteUint64(IntWriterContract):
    write_function = write_uint64
    lower_limit = 0
    lower_limit_as_bytes = zero_as_bytes = b"\x00\x00\x00\x00\x00\x00\x00\x00"
    upper_limit = 2**64 - 1
    upper_limit_as_bytes = b"\xff\xff\xff\xff\xff\xff\xff\xff"
    match_error_message = r"int too large to convert"


class TestWriteUnsignedVarint:
    def test_raises_value_error_for_negative_value(self, buffer: io.BytesIO) -> None:
        with (pytest.raises(ValueError, match=r"^Value must be positive$")):
            write_unsigned_varint(buffer, -1)

    def test_raises_value_error_when_upper_limit_exceeded(
        self,
        buffer: io.BytesIO,
    ) -> None:
        with pytest.raises(ValueError, match=r"^Value cannot exceed 2147483647$"):
            write_unsigned_varint(buffer, 2**31)

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            (0, b"\x00"),
            (10, b"\n"),
            (256, b"\x80\x02"),
            (1073741823, b"\xff\xff\xff\xff\x03"),
            (2**31 - 1, b"\xff\xff\xff\xff\x07"),
        ],
    )
    def test_can_write_valid_value(
        self,
        buffer: io.BytesIO,
        value: int,
        expected: bytes,
    ) -> None:
        write_unsigned_varint(buffer, value)
        buffer.seek(0)
        assert buffer.read(1000) == expected


class TestWriteEmptyTaggedFields:
    def test_writes_unsigned_varint_zero(
        self,
        buffer: io.BytesIO,
    ) -> None:
        write_empty_tagged_fields(buffer)
        buffer.seek(0)
        assert buffer.read(1) == b"\x00"


class TestWriteNullableCompactString:
    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            (None, b"\x00"),
            ("lazy fox 🍩", b"\x0elazy fox \xf0\x9f\x8d\xa9"),
            (b"jumps over", b"\x0bjumps over"),
        ],
    )
    def test_can_write_valid_value(self, value: bytes | None, expected: bytes) -> None:
        with closing(io.BytesIO()) as buffer:
            write_nullable_compact_string(buffer, value)
            buffer.seek(0)
            assert buffer.read(1000) == expected


class TestWriteCompactString:
    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("lazy fox 🍩", b"\x0elazy fox \xf0\x9f\x8d\xa9"),
            (b"jumps over", b"\x0bjumps over"),
        ],
    )
    def test_can_write_valid_value(self, value: bytes, expected: bytes) -> None:
        with closing(io.BytesIO()) as buffer:
            write_compact_string(buffer, value)
            buffer.seek(0)
            assert buffer.read(1000) == expected

    def test_raises_type_error_for_none(self) -> None:
        with (
            pytest.raises(TypeError, match=r"^Unexpectedly received None value"),
            closing(io.BytesIO()) as buffer,
        ):
            write_compact_string(buffer, None)  # type: ignore[arg-type]


class TestWriteLegacyString:
    def test_can_write_valid_value(self, buffer: io.BytesIO) -> None:
        value = "The quick brown 🦊 jumps over the lazy dog 🧖"
        byte_value = value.encode()
        byte_length = len(byte_value)
        write_legacy_string(buffer, value)
        buffer.seek(0)
        (read_length,) = struct.unpack(">h", buffer.read(2))
        assert read_length == byte_length
        assert buffer.read(1000) == byte_value

    def test_raises_type_error_for_none(self, buffer: io.BytesIO) -> None:
        with pytest.raises(TypeError, match=r"^Unexpectedly received None value"):
            write_legacy_string(buffer, None)  # type: ignore[arg-type]
