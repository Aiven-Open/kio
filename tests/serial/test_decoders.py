import asyncio
import io
import struct
from typing import IO

import pytest

from kio.serial.decoders import Decoder
from kio.serial.decoders import decode_compact_string
from kio.serial.decoders import decode_compact_string_as_bytes
from kio.serial.decoders import decode_compact_string_as_bytes_nullable
from kio.serial.decoders import decode_compact_string_nullable
from kio.serial.decoders import decode_int8
from kio.serial.decoders import decode_int16
from kio.serial.decoders import decode_int32
from kio.serial.decoders import decode_int64
from kio.serial.decoders import decode_legacy_bytes
from kio.serial.decoders import decode_legacy_string
from kio.serial.decoders import decode_nullable_legacy_bytes
from kio.serial.decoders import decode_nullable_legacy_string
from kio.serial.decoders import decode_raw_bytes
from kio.serial.decoders import decode_uint8
from kio.serial.decoders import decode_uint16
from kio.serial.decoders import decode_uint32
from kio.serial.decoders import decode_uint64
from kio.serial.decoders import decode_unsigned_varint
from kio.serial.decoders import read_async
from kio.serial.decoders import read_sync
from kio.serial.errors import UnexpectedNull


class IntDecoderContract:
    decoder: Decoder[int]
    lower_limit: int
    lower_limit_as_bytes: bytes
    upper_limit: int
    upper_limit_as_bytes: bytes
    zero_as_bytes: bytes

    @classmethod
    async def read_async(cls, reader: asyncio.StreamReader) -> int:
        return await read_async(reader, cls.decoder)

    @classmethod
    def read_sync(cls, reader: IO[bytes]) -> int:
        return read_sync(reader, cls.decoder)

    async def test_can_read_lower_limit_async(
        self,
        stream_reader: asyncio.StreamReader,
        stream_writer: asyncio.StreamWriter,
    ) -> None:
        stream_writer.write(self.lower_limit_as_bytes)
        await stream_writer.drain()
        assert self.lower_limit == await self.read_async(stream_reader)

    def test_can_read_lower_limit_sync(self, buffer: io.BytesIO) -> None:
        buffer.write(self.lower_limit_as_bytes)
        buffer.seek(0)
        assert self.lower_limit == self.read_sync(buffer)

    async def test_can_read_upper_limit_async(
        self,
        stream_reader: asyncio.StreamReader,
        stream_writer: asyncio.StreamWriter,
    ) -> None:
        stream_writer.write(self.upper_limit_as_bytes)
        await stream_writer.drain()
        assert self.upper_limit == await self.read_async(stream_reader)

    def test_can_read_upper_limit_sync(self, buffer: io.BytesIO) -> None:
        buffer.write(self.upper_limit_as_bytes)
        buffer.seek(0)
        assert self.upper_limit == self.read_sync(buffer)

    async def test_can_read_zero_async(
        self,
        stream_reader: asyncio.StreamReader,
        stream_writer: asyncio.StreamWriter,
    ) -> None:
        stream_writer.write(self.zero_as_bytes)
        await stream_writer.drain()
        assert 0 == await self.read_async(stream_reader)

    def test_can_read_zero_sync(self, buffer: io.BytesIO) -> None:
        buffer.write(self.zero_as_bytes)
        buffer.seek(0)
        assert 0 == self.read_sync(buffer)


class TestDecodeInt8(IntDecoderContract):
    decoder = decode_int8
    lower_limit = -128
    lower_limit_as_bytes = b"\x80"
    upper_limit = 127
    upper_limit_as_bytes = b"\x7f"
    zero_as_bytes = b"\x00"


class TestDecodeInt16(IntDecoderContract):
    decoder = decode_int16
    lower_limit = -(2**15)
    lower_limit_as_bytes = b"\x80\x00"
    upper_limit = 2**15 - 1
    upper_limit_as_bytes = b"\x7f\xff"
    zero_as_bytes = b"\x00\x00"


class TestDecodeInt32(IntDecoderContract):
    decoder = decode_int32
    lower_limit = -(2**31)
    lower_limit_as_bytes = b"\x80\x00\x00\x00"
    upper_limit = 2**31 - 1
    upper_limit_as_bytes = b"\x7f\xff\xff\xff"
    zero_as_bytes = b"\x00\x00\x00\x00"


class TestDecodeInt64(IntDecoderContract):
    decoder = decode_int64
    lower_limit = -(2**63)
    lower_limit_as_bytes = b"\x80\x00\x00\x00\x00\x00\x00\x00"
    upper_limit = 2**63 - 1
    upper_limit_as_bytes = b"\x7f\xff\xff\xff\xff\xff\xff\xff"
    zero_as_bytes = b"\x00\x00\x00\x00\x00\x00\x00\x00"


class TestDecodeUint8(IntDecoderContract):
    decoder = decode_uint8
    lower_limit = 0
    lower_limit_as_bytes = zero_as_bytes = b"\x00"
    upper_limit = 2**8 - 1
    upper_limit_as_bytes = b"\xff"


class TestDecodeUint16(IntDecoderContract):
    decoder = decode_uint16
    lower_limit = 0
    lower_limit_as_bytes = zero_as_bytes = b"\x00\x00"
    upper_limit = 2**16 - 1
    upper_limit_as_bytes = b"\xff\xff"
    lower_limit_error_message = "argument out of range"


class TestDecodeUint32(IntDecoderContract):
    decoder = decode_uint32
    lower_limit = 0
    lower_limit_as_bytes = zero_as_bytes = b"\x00\x00\x00\x00"
    upper_limit = 2**32 - 1
    upper_limit_as_bytes = b"\xff\xff\xff\xff"
    lower_limit_error_message = "argument out of range"


class TestDecodeUint64(IntDecoderContract):
    decoder = decode_uint64
    lower_limit = 0
    lower_limit_as_bytes = zero_as_bytes = b"\x00\x00\x00\x00\x00\x00\x00\x00"
    upper_limit = 2**64 - 1
    upper_limit_as_bytes = b"\xff\xff\xff\xff\xff\xff\xff\xff"
    match_error_message = r"int too large to convert"


class TestDecodeUnsignedVarint(IntDecoderContract):
    decoder = decode_unsigned_varint
    lower_limit = 0
    lower_limit_as_bytes = zero_as_bytes = b"\x00"
    upper_limit = 2**31 - 1
    upper_limit_as_bytes = b"\xff\xff\xff\xff\x07"

    async def test_raises_value_error_for_too_long_value_async(
        self,
        stream_reader: asyncio.StreamReader,
        stream_writer: asyncio.StreamWriter,
    ) -> None:
        for _ in range(5):
            stream_writer.write(0b10000001.to_bytes(1, "little"))
        await stream_writer.drain()
        with pytest.raises(ValueError, match=r"^Varint is too long"):
            await self.read_async(stream_reader)

    def test_raises_value_error_for_too_long_value_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        for _ in range(5):
            buffer.write(0b10000001.to_bytes(1, "little"))
        buffer.seek(0)
        with pytest.raises(ValueError, match=r"^Varint is too long"):
            self.read_sync(buffer)


class TestDecodeCompactStringAsBytes:
    def test_raises_unexpected_null_for_negative_length_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        buffer.write(0b00000000.to_bytes(1, "little"))
        buffer.seek(0)
        with pytest.raises(UnexpectedNull):
            read_sync(buffer, decode_compact_string_as_bytes)

    async def test_raises_unexpected_null_for_negative_length_async(
        self,
        stream_reader: asyncio.StreamReader,
        stream_writer: asyncio.StreamWriter,
    ) -> None:
        stream_writer.write(0b00000000.to_bytes(1, "little"))
        await stream_writer.drain()
        with pytest.raises(UnexpectedNull):
            await read_async(stream_reader, decode_compact_string_as_bytes)

    def test_can_decode_bytes_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        value = b"k\x9bC\x94\xbe\x1fV\xd6"
        byte_length = len(value) + 1  # string length is offset by one
        buffer.write(byte_length.to_bytes(1, "little"))
        buffer.write(value)
        buffer.seek(0)
        assert value == read_sync(buffer, decode_compact_string_as_bytes)

    async def test_can_decode_bytes_async(
        self,
        stream_reader: asyncio.StreamReader,
        stream_writer: asyncio.StreamWriter,
    ) -> None:
        value = b"k\x9bC\x94\xbe\x1fV\xd6"
        byte_length = len(value) + 1  # string length is offset by one
        stream_writer.write(byte_length.to_bytes(1, "little"))
        stream_writer.write(value)
        await stream_writer.drain()
        assert value == await read_async(stream_reader, decode_compact_string_as_bytes)


class TestDecodeCompactStringAsBytesNullable:
    def test_returns_null_for_negative_length_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        buffer.write(0b00000000.to_bytes(1, "little"))
        buffer.seek(0)
        assert read_sync(buffer, decode_compact_string_as_bytes_nullable) is None

    async def test_returns_null_for_negative_length_async(
        self,
        stream_reader: asyncio.StreamReader,
        stream_writer: asyncio.StreamWriter,
    ) -> None:
        stream_writer.write(0b00000000.to_bytes(1, "little"))
        await stream_writer.drain()
        assert (
            await read_async(stream_reader, decode_compact_string_as_bytes_nullable)
            is None
        )

    def test_can_decode_bytes_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        value = b"k\x9bC\x94\xbe\x1fV\xd6"
        byte_length = len(value) + 1  # string length is offset by one
        buffer.write(byte_length.to_bytes(1, "little"))
        buffer.write(value)
        buffer.seek(0)
        assert value == read_sync(buffer, decode_compact_string_as_bytes_nullable)

    async def test_can_decode_bytes_async(
        self,
        stream_reader: asyncio.StreamReader,
        stream_writer: asyncio.StreamWriter,
    ) -> None:
        value = b"k\x9bC\x94\xbe\x1fV\xd6"
        byte_length = len(value) + 1  # string length is offset by one
        stream_writer.write(byte_length.to_bytes(1, "little"))
        stream_writer.write(value)
        await stream_writer.drain()
        assert value == await read_async(
            stream_reader,
            decode_compact_string_as_bytes_nullable,
        )


class TestDecodeCompactString:
    def test_raises_unexpected_null_for_negative_length_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        buffer.write((0).to_bytes(1, "little"))
        buffer.seek(0)
        with pytest.raises(UnexpectedNull):
            read_sync(buffer, decode_compact_string)

    async def test_raises_unexpected_null_for_negative_length_async(
        self,
        stream_reader: asyncio.StreamReader,
        stream_writer: asyncio.StreamWriter,
    ) -> None:
        stream_writer.write((0).to_bytes(1, "little"))
        await stream_writer.drain()
        with pytest.raises(UnexpectedNull):
            await read_async(stream_reader, decode_compact_string)

    def test_can_decode_string_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        value = "The quick brown 🦊 jumps over the lazy dog 🧖"
        byte_value = value.encode()
        byte_length = len(byte_value) + 1  # string length is offset by one
        buffer.write(byte_length.to_bytes(1, "little"))
        buffer.write(byte_value)
        buffer.seek(0)
        assert value == read_sync(buffer, decode_compact_string)

    async def test_can_decode_string_async(
        self,
        stream_reader: asyncio.StreamReader,
        stream_writer: asyncio.StreamWriter,
    ) -> None:
        value = "The quick brown fox jumps over the lazy 🐶"
        byte_value = value.encode()
        byte_length = len(byte_value) + 1  # string length is offset by one
        stream_writer.write(byte_length.to_bytes(1, "little"))
        stream_writer.write(byte_value)
        await stream_writer.drain()
        assert value == await read_async(stream_reader, decode_compact_string)


class TestDecodeCompactStringNullable:
    def test_returns_null_for_negative_length_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        buffer.write((0).to_bytes(1, "little"))
        buffer.seek(0)
        assert read_sync(buffer, decode_compact_string_nullable) is None

    async def test_raises_unexpected_null_for_negative_length_async(
        self,
        stream_reader: asyncio.StreamReader,
        stream_writer: asyncio.StreamWriter,
    ) -> None:
        stream_writer.write((0).to_bytes(1, "little"))
        await stream_writer.drain()
        assert await read_async(stream_reader, decode_compact_string_nullable) is None

    def test_can_decode_string_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        value = "The quick brown 🦊 jumps over the lazy dog 🧖"
        byte_value = value.encode()
        byte_length = len(byte_value) + 1  # string length is offset by one
        buffer.write(byte_length.to_bytes(1, "little"))
        buffer.write(byte_value)
        buffer.seek(0)
        assert value == read_sync(buffer, decode_compact_string_nullable)

    async def test_can_decode_string_async(
        self,
        stream_reader: asyncio.StreamReader,
        stream_writer: asyncio.StreamWriter,
    ) -> None:
        value = "The quick brown fox jumps over the lazy 🐶"
        byte_value = value.encode()
        byte_length = len(byte_value) + 1  # string length is offset by one
        stream_writer.write(byte_length.to_bytes(1, "little"))
        stream_writer.write(byte_value)
        await stream_writer.drain()
        assert value == await read_async(stream_reader, decode_compact_string_nullable)


class TestDecodeRawBytes:
    def test_returns_null_for_negative_length_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        buffer.write((0).to_bytes(4, "big"))
        buffer.seek(0)
        assert read_sync(buffer, decode_raw_bytes) is None

    async def test_returns_null_for_negative_length_async(
        self,
        stream_reader: asyncio.StreamReader,
        stream_writer: asyncio.StreamWriter,
    ) -> None:
        stream_writer.write((0).to_bytes(4, "big"))
        await stream_writer.drain()
        assert await read_async(stream_reader, decode_raw_bytes) is None

    def test_can_decode_bytes_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        value = b"k\x9bC\x94\xbe\x1fV\xd6"
        byte_length = len(value) + 1  # string length is offset by one
        buffer.write(struct.pack(">i", byte_length))
        buffer.write(value)
        buffer.seek(0)
        assert value == read_sync(buffer, decode_raw_bytes)

    async def test_can_decode_bytes_async(
        self,
        stream_reader: asyncio.StreamReader,
        stream_writer: asyncio.StreamWriter,
    ) -> None:
        value = b"k\x9bC\x94\xbe\x1fV\xd6"
        byte_length = len(value) + 1  # string length is offset by one
        stream_writer.write(struct.pack(">i", byte_length))
        stream_writer.write(value)
        await stream_writer.drain()
        assert value == await read_async(stream_reader, decode_raw_bytes)


class TestDecodeNullableLegacyBytes:
    def test_returns_none_for_negative_length_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        buffer.write(struct.pack(">h", -1))
        buffer.seek(0)
        assert read_sync(buffer, decode_nullable_legacy_bytes) is None

    async def test_returns_none_for_negative_length_async(
        self,
        stream_reader: asyncio.StreamReader,
        stream_writer: asyncio.StreamWriter,
    ) -> None:
        stream_writer.write(struct.pack(">h", -1))
        await stream_writer.drain()
        assert await read_async(stream_reader, decode_nullable_legacy_bytes) is None

    def test_can_decode_bytes_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        value = b"k\x9bC\x94\xbe\x1fV\xd6"
        byte_length = len(value)
        buffer.write(struct.pack(">h", byte_length))
        buffer.write(value)
        buffer.seek(0)
        assert value == read_sync(buffer, decode_nullable_legacy_bytes)

    async def test_can_decode_bytes_async(
        self,
        stream_reader: asyncio.StreamReader,
        stream_writer: asyncio.StreamWriter,
    ) -> None:
        value = b"k\x9bC\x94\xbe\x1fV\xd6"
        byte_length = len(value)
        stream_writer.write(struct.pack(">h", byte_length))
        stream_writer.write(value)
        await stream_writer.drain()
        assert value == await read_async(stream_reader, decode_nullable_legacy_bytes)


class TestDecodeLegacyString:
    def test_raises_unexpected_null_for_negative_length_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        buffer.write(struct.pack(">h", -1))
        buffer.seek(0)
        with pytest.raises(UnexpectedNull):
            read_sync(buffer, decode_legacy_string)

    async def test_raises_unexpected_null_for_negative_length_async(
        self,
        stream_reader: asyncio.StreamReader,
        stream_writer: asyncio.StreamWriter,
    ) -> None:
        stream_writer.write(struct.pack(">h", -1))
        await stream_writer.drain()
        with pytest.raises(UnexpectedNull):
            await read_async(stream_reader, decode_legacy_string)

    def test_can_decode_string_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        value = "The quick brown 🦊 jumps over the lazy dog 🧖"
        byte_value = value.encode()
        byte_length = len(byte_value)
        buffer.write(struct.pack(">h", byte_length))
        buffer.write(byte_value)
        buffer.seek(0)
        assert value == read_sync(buffer, decode_legacy_string)

    async def test_can_decode_string_async(
        self,
        stream_reader: asyncio.StreamReader,
        stream_writer: asyncio.StreamWriter,
    ) -> None:
        value = "The quick brown fox jumps over the lazy 🐶"
        byte_value = value.encode()
        byte_length = len(byte_value)
        stream_writer.write(struct.pack(">h", byte_length))
        stream_writer.write(byte_value)
        await stream_writer.drain()
        assert value == await read_async(stream_reader, decode_legacy_string)


class TestDecodeNullableLegacyString:
    def test_returns_null_for_negative_length_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        buffer.write(struct.pack(">h", -1))
        buffer.seek(0)
        assert read_sync(buffer, decode_nullable_legacy_string) is None

    async def test_returns_null_for_negative_length_async(
        self,
        stream_reader: asyncio.StreamReader,
        stream_writer: asyncio.StreamWriter,
    ) -> None:
        stream_writer.write(struct.pack(">h", -1))
        await stream_writer.drain()
        assert await read_async(stream_reader, decode_nullable_legacy_string) is None

    def test_can_decode_string_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        value = "The quick brown 🦊 jumps over the lazy dog 🧖"
        byte_value = value.encode()
        byte_length = len(byte_value)
        buffer.write(struct.pack(">h", byte_length))
        buffer.write(byte_value)
        buffer.seek(0)
        assert value == read_sync(buffer, decode_nullable_legacy_string)

    async def test_can_decode_string_async(
        self,
        stream_reader: asyncio.StreamReader,
        stream_writer: asyncio.StreamWriter,
    ) -> None:
        value = "The quick brown fox jumps over the lazy 🐶"
        byte_value = value.encode()
        byte_length = len(byte_value)
        stream_writer.write(struct.pack(">h", byte_length))
        stream_writer.write(byte_value)
        await stream_writer.drain()
        assert value == await read_async(stream_reader, decode_nullable_legacy_string)


class TestDecodeLegacyBytes:
    def test_raises_unexpected_null_for_negative_length_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        buffer.write(struct.pack(">h", -1))
        buffer.seek(0)
        with pytest.raises(UnexpectedNull):
            read_sync(buffer, decode_legacy_bytes)

    async def test_raises_unexpected_null_for_negative_length_async(
        self,
        stream_reader: asyncio.StreamReader,
        stream_writer: asyncio.StreamWriter,
    ) -> None:
        stream_writer.write(struct.pack(">h", -1))
        await stream_writer.drain()
        with pytest.raises(UnexpectedNull):
            await read_async(stream_reader, decode_legacy_bytes)

    def test_can_decode_bytes_sync(
        self,
        buffer: io.BytesIO,
    ) -> None:
        value = "The quick brown 🦊 jumps over the lazy dog 🧖"
        byte_value = value.encode()
        byte_length = len(byte_value)
        buffer.write(struct.pack(">h", byte_length))
        buffer.write(byte_value)
        buffer.seek(0)
        assert byte_value == read_sync(buffer, decode_legacy_bytes)

    async def test_can_decode_bytes_async(
        self,
        stream_reader: asyncio.StreamReader,
        stream_writer: asyncio.StreamWriter,
    ) -> None:
        value = "The quick brown fox jumps over the lazy 🐶"
        byte_value = value.encode()
        byte_length = len(byte_value)
        stream_writer.write(struct.pack(">h", byte_length))
        stream_writer.write(byte_value)
        await stream_writer.drain()
        assert byte_value == await read_async(stream_reader, decode_legacy_bytes)
