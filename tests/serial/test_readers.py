import datetime
import io
import struct
import sys
import uuid

from dataclasses import dataclass
from dataclasses import field
from typing import IO
from typing import ClassVar
from typing import final

import pytest

from kio.serial import entity_reader
from kio.serial.errors import BufferUnderflow
from kio.serial.errors import OutOfBoundValue
from kio.serial.errors import UnexpectedNull
from kio.serial.readers import Reader
from kio.serial.readers import compact_array_reader
from kio.serial.readers import legacy_array_reader
from kio.serial.readers import read_compact_string
from kio.serial.readers import read_compact_string_as_bytes
from kio.serial.readers import read_compact_string_as_bytes_nullable
from kio.serial.readers import read_compact_string_nullable
from kio.serial.readers import read_datetime_i64
from kio.serial.readers import read_error_code
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
from kio.serial.readers import read_timedelta_i32
from kio.serial.readers import read_uint8
from kio.serial.readers import read_uint16
from kio.serial.readers import read_uint32
from kio.serial.readers import read_uint64
from kio.serial.readers import read_unsigned_varint
from kio.serial.readers import read_uuid
from kio.static.constants import EntityType
from kio.static.constants import ErrorCode
from kio.static.constants import uuid_zero
from kio.static.primitive import TZAware
from kio.static.primitive import i8
from kio.static.primitive import i16


class BufferUnderflowContract:
    reader: Reader[object]
    valid_serialization: bytes

    @classmethod
    def read(cls, buffer: IO[bytes]) -> object:
        return cls.reader(buffer)

    @final
    def test_raises_buffer_underflow_when_not_enough_bytes_for_value(
        self,
        buffer: IO[bytes],
    ) -> None:
        buffer.write(self.valid_serialization[:-1])
        buffer.seek(0)

        with pytest.raises(BufferUnderflow):
            self.read(buffer)


class LengthBufferUnderflowContract(BufferUnderflowContract):
    length_num_bytes: int

    @final
    def test_raises_buffer_underflow_when_not_enough_bytes_for_length(
        self,
        buffer: IO[bytes],
    ) -> None:
        buffer.write(self.valid_serialization[: self.length_num_bytes - 1])
        buffer.seek(0)

        with pytest.raises(BufferUnderflow):
            self.read(buffer)


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

    @final
    def test_can_read_lower_limit_sync(self, buffer: io.BytesIO) -> None:
        buffer.write(self.lower_limit_as_bytes)
        buffer.seek(0)
        assert self.lower_limit == self.read(buffer)

    @final
    def test_can_read_upper_limit_sync(self, buffer: io.BytesIO) -> None:
        buffer.write(self.upper_limit_as_bytes)
        buffer.seek(0)
        assert self.upper_limit == self.read(buffer)

    @final
    def test_can_read_zero_sync(self, buffer: io.BytesIO) -> None:
        buffer.write(self.zero_as_bytes)
        buffer.seek(0)
        assert self.read(buffer) == 0


class TestReadInt8(IntReaderContract, BufferUnderflowContract):
    reader = read_int8
    lower_limit = -128
    lower_limit_as_bytes = b"\x80"
    upper_limit = 127
    upper_limit_as_bytes = b"\x7f"
    zero_as_bytes = b"\x00"
    valid_serialization = zero_as_bytes


class TestReadInt16(IntReaderContract, BufferUnderflowContract):
    reader = read_int16
    lower_limit = -(2**15)
    lower_limit_as_bytes = b"\x80\x00"
    upper_limit = 2**15 - 1
    upper_limit_as_bytes = b"\x7f\xff"
    zero_as_bytes = b"\x00\x00"
    valid_serialization = zero_as_bytes


class TestReadInt32(IntReaderContract, BufferUnderflowContract):
    reader = read_int32
    lower_limit = -(2**31)
    lower_limit_as_bytes = b"\x80\x00\x00\x00"
    upper_limit = 2**31 - 1
    upper_limit_as_bytes = b"\x7f\xff\xff\xff"
    zero_as_bytes = b"\x00\x00\x00\x00"
    valid_serialization = zero_as_bytes


class TestReadInt64(IntReaderContract, BufferUnderflowContract):
    reader = read_int64
    lower_limit = -(2**63)
    lower_limit_as_bytes = b"\x80\x00\x00\x00\x00\x00\x00\x00"
    upper_limit = 2**63 - 1
    upper_limit_as_bytes = b"\x7f\xff\xff\xff\xff\xff\xff\xff"
    zero_as_bytes = b"\x00\x00\x00\x00\x00\x00\x00\x00"
    valid_serialization = zero_as_bytes


class TestReadUint8(IntReaderContract, BufferUnderflowContract):
    reader = read_uint8
    lower_limit = 0
    lower_limit_as_bytes = zero_as_bytes = b"\x00"
    upper_limit = 2**8 - 1
    upper_limit_as_bytes = b"\xff"
    valid_serialization = zero_as_bytes


class TestReadUint16(IntReaderContract, BufferUnderflowContract):
    reader = read_uint16
    lower_limit = 0
    lower_limit_as_bytes = zero_as_bytes = b"\x00\x00"
    upper_limit = 2**16 - 1
    upper_limit_as_bytes = b"\xff\xff"
    lower_limit_error_message = "argument out of range"
    valid_serialization = zero_as_bytes


class TestReadUint32(IntReaderContract, BufferUnderflowContract):
    reader = read_uint32
    lower_limit = 0
    lower_limit_as_bytes = zero_as_bytes = b"\x00\x00\x00\x00"
    upper_limit = 2**32 - 1
    upper_limit_as_bytes = b"\xff\xff\xff\xff"
    lower_limit_error_message = "argument out of range"
    valid_serialization = zero_as_bytes


class TestReadUint64(IntReaderContract, BufferUnderflowContract):
    reader = read_uint64
    lower_limit = 0
    lower_limit_as_bytes = zero_as_bytes = b"\x00\x00\x00\x00\x00\x00\x00\x00"
    upper_limit = 2**64 - 1
    upper_limit_as_bytes = b"\xff\xff\xff\xff\xff\xff\xff\xff"
    match_error_message = r"int too large to convert"
    valid_serialization = zero_as_bytes


class TestReadUnsignedVarint(IntReaderContract, BufferUnderflowContract):
    reader = read_unsigned_varint
    lower_limit = 0
    lower_limit_as_bytes = zero_as_bytes = b"\x00"
    upper_limit = 2**31 - 1
    upper_limit_as_bytes = b"\xff\xff\xff\xff\x07"
    valid_serialization = zero_as_bytes

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


class TestReadFloat64(BufferUnderflowContract):
    reader = read_float64
    valid_serialization = struct.pack(">d", 0)

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
        assert self.read(buffer) == value


class TestReadCompactStringAsBytes(LengthBufferUnderflowContract):
    reader = read_compact_string_as_bytes
    length_num_bytes = 1
    valid_serialization = b"\x06hello"

    def test_raises_unexpected_null_for_negative_length_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        buffer.write(0b00000000.to_bytes(1, "little"))
        buffer.seek(0)
        with pytest.raises(UnexpectedNull):
            self.read(buffer)

    def test_can_read_bytes_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        value = b"k\x9bC\x94\xbe\x1fV\xd6"
        byte_length = len(value) + 1  # string length is offset by one
        buffer.write(byte_length.to_bytes(1, "little"))
        buffer.write(value)
        buffer.seek(0)
        assert value == self.read(buffer)


class TestReadCompactStringAsBytesNullable(LengthBufferUnderflowContract):
    reader = read_compact_string_as_bytes_nullable
    length_num_bytes = 1
    valid_serialization = b"\x06hello"

    def test_returns_null_for_negative_length_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        buffer.write(0b00000000.to_bytes(1, "little"))
        buffer.seek(0)
        assert self.read(buffer) is None

    def test_can_read_bytes_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        value = b"k\x9bC\x94\xbe\x1fV\xd6"
        byte_length = len(value) + 1  # string length is offset by one
        buffer.write(byte_length.to_bytes(1, "little"))
        buffer.write(value)
        buffer.seek(0)
        assert value == self.read(buffer)


class TestReadCompactString(LengthBufferUnderflowContract):
    reader = read_compact_string
    length_num_bytes = 1
    valid_serialization = b"\x06hello"

    def test_raises_unexpected_null_for_negative_length_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        buffer.write((0).to_bytes(1, "little"))
        buffer.seek(0)
        with pytest.raises(UnexpectedNull):
            self.read(buffer)

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
        assert value == self.read(buffer)


class TestReadCompactStringNullable(LengthBufferUnderflowContract):
    reader = read_compact_string_nullable
    length_num_bytes = 1
    valid_serialization = b"\x06hello"

    def test_returns_null_for_negative_length_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        buffer.write((0).to_bytes(1, "little"))
        buffer.seek(0)
        assert self.read(buffer) is None

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
        assert value == self.read(buffer)


class TestReadNullableLegacyBytes(LengthBufferUnderflowContract):
    reader = read_nullable_legacy_bytes
    length_num_bytes = 4
    valid_serialization = b"\x00\x00\x00\x05hello"

    def test_returns_none_for_negative_length_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        buffer.write(struct.pack(">i", -1))
        buffer.seek(0)
        assert self.read(buffer) is None

    def test_can_read_bytes_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        value = b"k\x9bC\x94\xbe\x1fV\xd6"
        byte_length = len(value)
        buffer.write(struct.pack(">i", byte_length))
        buffer.write(value)
        buffer.seek(0)
        assert value == self.read(buffer)


class TestReadLegacyString(LengthBufferUnderflowContract):
    reader = read_legacy_string
    length_num_bytes = 2
    valid_serialization = b"\x00\x05hello"

    def test_raises_unexpected_null_for_negative_length_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        buffer.write(struct.pack(">h", -1))
        buffer.seek(0)
        with pytest.raises(UnexpectedNull):
            self.read(buffer)

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
        assert value == self.read(buffer)


class TestReadNullableLegacyString(LengthBufferUnderflowContract):
    reader = read_nullable_legacy_string
    length_num_bytes = 2
    valid_serialization = b"\x00\x05hello"

    def test_returns_null_for_negative_length_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        buffer.write(struct.pack(">h", -1))
        buffer.seek(0)
        assert self.read(buffer) is None

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
        assert value == self.read(buffer)


class TestReadLegacyBytes(LengthBufferUnderflowContract):
    reader = read_legacy_bytes
    length_num_bytes = 4
    valid_serialization = b"\x00\x00\x00\x05hello"

    def test_raises_unexpected_null_for_negative_length_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        buffer.write(struct.pack(">i", -1))
        buffer.seek(0)
        with pytest.raises(UnexpectedNull):
            self.read(buffer)

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
        assert byte_value == self.read(buffer)


class TestReadUUID(BufferUnderflowContract):
    reader = read_uuid
    valid_serialization = uuid_zero.bytes

    def test_reads_zero_as_none(self, buffer: io.BytesIO) -> None:
        buffer.write(uuid_zero.bytes)
        buffer.seek(0)
        assert self.read(buffer) is None

    def test_can_read_uuid4(self, buffer: io.BytesIO) -> None:
        value = uuid.uuid4()
        buffer.write(value.bytes)
        buffer.seek(0)
        assert self.read(buffer) == value


class TestCompactArrayReader:
    def test_can_read_none(self, buffer: io.BytesIO) -> None:
        reader = compact_array_reader(read_int8)
        buffer.write(b"\x00")
        buffer.seek(0)
        assert reader(buffer) is None

    def test_can_read_empty_array(self, buffer: io.BytesIO) -> None:
        reader = compact_array_reader(read_int8)
        buffer.write(b"\x01")
        buffer.seek(0)
        assert reader(buffer) == ()

    def test_can_read_primitive_array(self, buffer: io.BytesIO) -> None:
        reader = compact_array_reader(read_int8)
        buffer.write(b"\x02\x20")
        buffer.seek(0)
        assert reader(buffer) == (32,)

    def test_can_read_entity_array(self, buffer: io.BytesIO) -> None:
        @dataclass
        class A:
            __type__: ClassVar = EntityType.nested
            __version__: ClassVar = i16(0)
            __flexible__: ClassVar = True
            p: i8 = field(metadata={"kafka_type": "int8"})
            q: str = field(metadata={"kafka_type": "string"})

        reader = compact_array_reader(entity_reader(A))
        buffer.write(
            b"\x02"  # array length
            b"\x17"  # A.p
            b"\x08foo bar"  # A.q
            b"\00"  # no tagged fields
        )
        buffer.seek(0)

        result = reader(buffer)
        assert result is not None
        [entity] = result
        assert isinstance(entity, A)
        assert entity.p == 23
        assert entity.q == "foo bar"


class TestLegacyArrayReader:
    def test_can_read_none(self, buffer: io.BytesIO) -> None:
        reader = legacy_array_reader(read_int8)
        buffer.write(b"\xff\xff\xff\xff")
        buffer.seek(0)
        assert reader(buffer) is None

    def test_can_read_empty_array(self, buffer: io.BytesIO) -> None:
        reader = legacy_array_reader(read_int8)
        buffer.write(b"\x00\x00\x00\x00")
        buffer.seek(0)
        assert reader(buffer) == ()

    def test_can_read_primitive_array(self, buffer: io.BytesIO) -> None:
        reader = legacy_array_reader(read_int8)
        buffer.write(b"\x00\x00\x00\x01\x20")
        buffer.seek(0)
        assert reader(buffer) == (32,)

    def test_can_read_entity_array(self, buffer: io.BytesIO) -> None:
        @dataclass
        class A:
            __type__: ClassVar = EntityType.nested
            __version__: ClassVar = i16(0)
            __flexible__: ClassVar = False
            p: i8 = field(metadata={"kafka_type": "int8"})
            q: str = field(metadata={"kafka_type": "string"})

        reader = legacy_array_reader(entity_reader(A))
        buffer.write(
            b"\x00\x00\x00\x01"  # array length
            b"\x17"  # A.p
            b"\x00\x07foo bar"  # A.q
        )
        buffer.seek(0)

        result = reader(buffer)
        assert result is not None
        [entity] = result
        assert isinstance(entity, A)
        assert entity.p == 23
        assert entity.q == "foo bar"


class TestReadErrorCode:
    def test_raises_buffer_underflow(self, buffer: io.BytesIO) -> None:
        buffer.write(b"\x00")
        buffer.seek(0)
        with pytest.raises(BufferUnderflow):
            read_error_code(buffer)

    def test_raises_value_error_for_unknown_error_code(
        self,
        buffer: io.BytesIO,
    ) -> None:
        buffer.write(b"\xff\xfe")
        buffer.seek(0)
        with pytest.raises(ValueError, match=r"^-2 is not a valid ErrorCode$"):
            read_error_code(buffer)

    @pytest.mark.parametrize(
        ("buffer_bytes", "expected_code"),
        (
            (b"\x00\x00", ErrorCode.none),
            (b"\x00\x01", ErrorCode.offset_out_of_range),
            (b"\xff\xff", ErrorCode.unknown_server_error),
        ),
    )
    def test_can_read_valid_error_code(
        self,
        buffer: io.BytesIO,
        buffer_bytes: bytes,
        expected_code: ErrorCode,
    ) -> None:
        buffer.write(buffer_bytes)
        buffer.seek(0)
        assert read_error_code(buffer) is expected_code


class TestReadTimedeltaI32:
    def test_raises_buffer_underflow(self, buffer: io.BytesIO) -> None:
        buffer.write(b"\x00")
        buffer.seek(0)
        with pytest.raises(BufferUnderflow):
            assert read_timedelta_i32(buffer)

    @pytest.mark.parametrize(
        ("buffer_bytes", "expected"),
        (
            (b"\x00\x00\x00\x00", datetime.timedelta()),
            (b"\x00\x00\x00\x01", datetime.timedelta(milliseconds=1)),
        ),
    )
    def test_can_read_valid_timedelta(
        self,
        buffer: io.BytesIO,
        buffer_bytes: bytes,
        expected: datetime.timedelta,
    ) -> None:
        buffer.write(buffer_bytes)
        buffer.seek(0)
        assert read_timedelta_i32(buffer) == expected


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
