import datetime
import io
import struct
import sys
import uuid

from contextlib import closing
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar
from typing import Generic
from typing import TypeVar

import pytest

from kio.schema.errors import ErrorCode
from kio.serial import entity_writer
from kio.serial.errors import OutOfBoundValue
from kio.serial.writers import Writer
from kio.serial.writers import compact_array_writer
from kio.serial.writers import legacy_array_writer
from kio.serial.writers import write_compact_string
from kio.serial.writers import write_datetime_i64
from kio.serial.writers import write_empty_tagged_fields
from kio.serial.writers import write_error_code
from kio.serial.writers import write_float64
from kio.serial.writers import write_int8
from kio.serial.writers import write_int16
from kio.serial.writers import write_int32
from kio.serial.writers import write_int64
from kio.serial.writers import write_legacy_bytes
from kio.serial.writers import write_legacy_string
from kio.serial.writers import write_nullable_compact_string
from kio.serial.writers import write_nullable_datetime_i64
from kio.serial.writers import write_nullable_legacy_bytes
from kio.serial.writers import write_nullable_legacy_string
from kio.serial.writers import write_timedelta_i32
from kio.serial.writers import write_timedelta_i64
from kio.serial.writers import write_uint8
from kio.serial.writers import write_uint16
from kio.serial.writers import write_uint32
from kio.serial.writers import write_uint64
from kio.serial.writers import write_unsigned_varint
from kio.serial.writers import write_unsigned_varlong
from kio.serial.writers import write_uuid
from kio.static.constants import EntityType
from kio.static.constants import uuid_zero
from kio.static.primitive import i8
from kio.static.primitive import i16
from kio.static.primitive import i32Timedelta
from kio.static.primitive import i64Timedelta
from kio.static.primitive import uvarint

_I = TypeVar("_I", bound=int, contravariant=True)


class IntWriterContract(Generic[_I]):
    write_function: Writer[_I]
    lower_limit: int
    lower_limit_as_bytes: bytes
    upper_limit: int
    upper_limit_as_bytes: bytes
    zero_as_bytes: bytes

    @property
    def match_error_message(self) -> str:
        return rf"format requires {self.lower_limit} <= number <= {self.upper_limit}$"

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

    @property
    def match_error_message(self) -> str:
        return (
            rf"^'q' format requires {self.lower_limit} <= number <= {self.upper_limit}$"
            if sys.version_info >= (3, 12)
            else r"^int too large to convert$"
        )


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

    @property
    def lower_limit_error_message(self) -> str:
        return (
            rf"^'H' format requires {self.lower_limit} <= number <= {self.upper_limit}$"
            if sys.version_info >= (3, 12)
            else r"^argument out of range$"
        )


class TestWriteUint32(IntWriterContract):
    write_function = write_uint32
    lower_limit = 0
    lower_limit_as_bytes = zero_as_bytes = b"\x00\x00\x00\x00"
    upper_limit = 2**32 - 1
    upper_limit_as_bytes = b"\xff\xff\xff\xff"

    @property
    def lower_limit_error_message(self) -> str:
        return (
            rf"^'I' format requires {self.lower_limit} <= number <= {self.upper_limit}$"
            if sys.version_info >= (3, 12)
            else r"^argument out of range$"
        )


class TestWriteUint64(IntWriterContract):
    write_function = write_uint64
    lower_limit = 0
    lower_limit_as_bytes = zero_as_bytes = b"\x00\x00\x00\x00\x00\x00\x00\x00"
    upper_limit = 2**64 - 1
    upper_limit_as_bytes = b"\xff\xff\xff\xff\xff\xff\xff\xff"

    @property
    def lower_limit_error_message(self) -> str:
        return (
            rf"^'Q' format requires {self.lower_limit} <= number <= {self.upper_limit}$"
            if sys.version_info >= (3, 12)
            # Note: this error message is clearly incorrect prior to 3.12.
            else "^int too large to convert$"
        )

    @property
    def upper_limit_error_message(self) -> str:
        return (
            rf"^'Q' format requires {self.lower_limit} <= number <= {self.upper_limit}$"
            if sys.version_info >= (3, 12)
            else r"^int too large to convert$"
        )


class TestWriteUnsignedVarint:
    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            (0, b"\x00"),
            (10, b"\n"),
            (256, b"\x80\x02"),
            (1073741823, b"\xff\xff\xff\xff\x03"),
            (2**31 - 1, b"\xff\xff\xff\xff\x07"),
            (1, b"\x01"),
            (12345, b"\xb9`"),
            (54321, b"\xb1\xa8\x03"),
            (2147483647, b"\xff\xff\xff\xff\x07"),
            (2**35 - 1, b"\xff\xff\xff\xff\x7f"),
        ],
    )
    def test_can_write_valid_value(
        self,
        buffer: io.BytesIO,
        value: uvarint,
        expected: bytes,
    ) -> None:
        write_unsigned_varint(buffer, value)
        buffer.seek(0)
        assert buffer.read(1000) == expected


class TestWriteUnsignedVarlong:
    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            (0, b"\x00"),
            (10, b"\n"),
            (256, b"\x80\x02"),
            (1073741823, b"\xff\xff\xff\xff\x03"),
            (2**31 - 1, b"\xff\xff\xff\xff\x07"),
            (1, b"\x01"),
            (12345, b"\xb9`"),
            (54321, b"\xb1\xa8\x03"),
            (2147483647, b"\xff\xff\xff\xff\x07"),
            (2**70 - 1, b"\xff\xff\xff\xff\xff\xff\xff\xff\xff\x7f"),
        ],
    )
    def test_can_write_valid_value(
        self,
        buffer: io.BytesIO,
        value: uvarint,
        expected: bytes,
    ) -> None:
        write_unsigned_varlong(buffer, value)
        buffer.seek(0)
        assert buffer.read(1000) == expected


class TestWriteFloat64:
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
        write_float64(buffer, value)
        buffer.seek(0)
        (unpacked,) = struct.unpack(">d", buffer.read(8))
        assert unpacked == value


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


class TestWriteLegacyBytes:
    def test_can_write_valid_value(self, buffer: io.BytesIO) -> None:
        value = "The quick brown 🦊 jumps over the lazy dog 🧖".encode()
        write_legacy_bytes(buffer, value)
        buffer.seek(0)
        (read_length,) = struct.unpack(">i", buffer.read(4))
        assert read_length == len(value)
        assert buffer.read(read_length) == value

    def test_raises_type_error_for_none(self, buffer: io.BytesIO) -> None:
        with pytest.raises(TypeError, match=r"^Unexpectedly received None value"):
            write_legacy_bytes(buffer, None)  # type: ignore[arg-type]


class TestWriteNullableLegacyString:
    def test_can_write_valid_value(self, buffer: io.BytesIO) -> None:
        value = "The quick brown 🦊 jumps over the lazy dog 🧖"
        byte_value = value.encode()
        byte_length = len(byte_value)
        write_nullable_legacy_string(buffer, value)
        buffer.seek(0)
        (read_length,) = struct.unpack(">h", buffer.read(2))
        assert read_length == byte_length
        assert buffer.read(1000) == byte_value

    def test_can_write_none(self, buffer: io.BytesIO) -> None:
        write_nullable_legacy_string(buffer, None)
        buffer.seek(0)
        (read_length,) = struct.unpack(">h", buffer.read(2))
        assert read_length == -1

    def test_raises_out_of_bound_value_for_too_large_string(
        self,
        buffer: io.BytesIO,
    ) -> None:
        with pytest.raises(OutOfBoundValue):
            write_nullable_legacy_string(buffer, 2**15 * "a")


class TestWriteNullableLegacyBytes:
    def test_can_write_valid_value(self, buffer: io.BytesIO) -> None:
        value = "The quick brown 🦊 jumps over the lazy dog 🧖".encode()
        write_nullable_legacy_bytes(buffer, value)
        buffer.seek(0)
        (read_length,) = struct.unpack(">i", buffer.read(4))
        assert read_length == len(value)
        assert buffer.read(read_length) == value

    def test_can_write_none(self, buffer: io.BytesIO) -> None:
        write_nullable_legacy_bytes(buffer, None)
        buffer.seek(0)
        (read_length,) = struct.unpack(">i", buffer.read(4))
        assert read_length == -1

    def test_raises_out_of_bound_value_for_too_large_string(
        self,
        buffer: io.BytesIO,
    ) -> None:
        with pytest.raises(OutOfBoundValue):
            write_nullable_legacy_bytes(buffer, 2**31 * b"a")


class TestWriteUUID:
    def test_writes_none_as_uuid_zero(self, buffer: io.BytesIO) -> None:
        write_uuid(buffer, None)
        buffer.seek(0)
        assert buffer.read(16) == uuid_zero.bytes

    def test_can_write_uuid4(self, buffer: io.BytesIO) -> None:
        value = uuid.uuid4()
        write_uuid(buffer, value)
        buffer.seek(0)
        assert buffer.read(16) == value.bytes


class TestCompactArrayWriter:
    def test_can_write_primitive_values(self, buffer: io.BytesIO) -> None:
        writer = compact_array_writer(write_int8)
        writer(buffer, (i8(1), i8(2), i8(3)))
        buffer.seek(0)
        assert buffer.read(4) == b"\x04\x01\x02\x03"

    def test_can_write_entity_values(self, buffer: io.BytesIO) -> None:
        @dataclass
        class A:
            __type__: ClassVar = EntityType.nested
            __version__: ClassVar = i16(0)
            __flexible__: ClassVar = True
            p: i8 = field(metadata={"kafka_type": "int8"})
            q: str = field(metadata={"kafka_type": "string"})

        writer = compact_array_writer(entity_writer(A))
        writer(buffer, (A(p=i8(23), q="foo bar"),))
        buffer.seek(0)
        assert buffer.read(11) == b"\x02\x17\x08foo bar\x00"

    def test_can_write_none(self, buffer: io.BytesIO) -> None:
        writer = compact_array_writer(write_int8)
        writer(buffer, None)
        buffer.seek(0)
        assert buffer.read(4) == b"\x00"


class TestLegacyArrayWriter:
    def test_can_write_primitive_values(self, buffer: io.BytesIO) -> None:
        writer = legacy_array_writer(write_int8)
        writer(buffer, (i8(1), i8(2), i8(3)))
        buffer.seek(0)
        assert buffer.read(7) == b"\x00\x00\x00\x03\x01\x02\x03"

    def test_can_write_entity_values(self, buffer: io.BytesIO) -> None:
        @dataclass
        class A:
            __type__: ClassVar = EntityType.nested
            __version__: ClassVar = i16(0)
            __flexible__: ClassVar = False
            p: i8 = field(metadata={"kafka_type": "int8"})
            q: str = field(metadata={"kafka_type": "string"})

        writer = legacy_array_writer(entity_writer(A))
        writer(buffer, (A(p=i8(23), q="foo bar"),))
        buffer.seek(0)
        assert buffer.read(14) == b"\x00\x00\x00\x01\x17\x00\x07foo bar"

    def test_can_write_none(self, buffer: io.BytesIO) -> None:
        writer = legacy_array_writer(write_int8)
        writer(buffer, None)
        buffer.seek(0)
        assert buffer.read(4) == b"\xff\xff\xff\xff"


class TestWriteErrorCode:
    @pytest.mark.parametrize(
        ("error_code", "expected_bytes"),
        (
            (ErrorCode.unknown_server_error, b"\xff\xff"),
            (ErrorCode.none, b"\x00\x00"),
            (ErrorCode.offset_out_of_range, b"\x00\x01"),
        ),
    )
    def test_can_write_error_code(
        self,
        buffer: io.BytesIO,
        error_code: ErrorCode,
        expected_bytes: bytes,
    ) -> None:
        write_error_code(buffer, error_code)
        buffer.seek(0)
        assert buffer.read(2) == expected_bytes


class TestWriteTimedeltaI32:
    @pytest.mark.parametrize(
        ("value", "expected_bytes"),
        (
            (datetime.timedelta(), b"\x00\x00\x00\x00"),
            (datetime.timedelta(milliseconds=1), b"\x00\x00\x00\x01"),
        ),
    )
    def test_can_write_timedelta(
        self,
        buffer: io.BytesIO,
        value: i32Timedelta,
        expected_bytes: bytes,
    ) -> None:
        write_timedelta_i32(buffer, value)
        buffer.seek(0)
        assert buffer.read(4) == expected_bytes


class TestWriteTimedeltaI64:
    @pytest.mark.parametrize(
        ("value", "expected_bytes"),
        (
            (datetime.timedelta(), b"\x00\x00\x00\x00\x00\x00\x00\x00"),
            (datetime.timedelta(milliseconds=1), b"\x00\x00\x00\x00\x00\x00\x00\x01"),
        ),
    )
    def test_can_write_timedelta(
        self,
        buffer: io.BytesIO,
        value: i64Timedelta,
        expected_bytes: bytes,
    ) -> None:
        write_timedelta_i64(buffer, value)
        buffer.seek(0)
        assert buffer.read(8) == expected_bytes


class TestWriteDatetimeI64:
    @pytest.mark.parametrize(
        ("value", "expected_bytes"),
        (
            (
                datetime.datetime(2024, 5, 28, 12, 31, tzinfo=datetime.UTC),
                b"\x00\x00\x01\x8f\xbf.\xb3\xa0",
            ),
            (
                datetime.datetime(1970, 1, 1, tzinfo=datetime.UTC),
                b"\x00\x00\x00\x00\x00\x00\x00\x00",
            ),
        ),
    )
    def test_can_write_datetime(
        self,
        buffer: io.BytesIO,
        value: datetime.datetime,
        expected_bytes: bytes,
    ) -> None:
        write_datetime_i64(buffer, value)
        buffer.seek(0)
        assert buffer.read(8) == expected_bytes


class TestWriteNullableDatetimeI64:
    @pytest.mark.parametrize(
        ("value", "expected_bytes"),
        (
            (None, b"\xff\xff\xff\xff\xff\xff\xff\xff"),
            (
                datetime.datetime(2024, 5, 28, 12, 31, tzinfo=datetime.UTC),
                b"\x00\x00\x01\x8f\xbf.\xb3\xa0",
            ),
            (
                datetime.datetime(1970, 1, 1, tzinfo=datetime.UTC),
                b"\x00\x00\x00\x00\x00\x00\x00\x00",
            ),
        ),
    )
    def test_can_write_datetime(
        self,
        buffer: io.BytesIO,
        value: datetime.datetime | None,
        expected_bytes: bytes,
    ) -> None:
        write_nullable_datetime_i64(buffer, value)
        buffer.seek(0)
        assert buffer.read(8) == expected_bytes
