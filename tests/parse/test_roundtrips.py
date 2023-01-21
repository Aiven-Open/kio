import io

from hypothesis import given
from hypothesis.strategies import binary
from hypothesis.strategies import booleans
from hypothesis.strategies import integers
from hypothesis.strategies import text

from kio.serial.decoders import Decoder
from kio.serial.decoders import decode_array_length
from kio.serial.decoders import decode_boolean
from kio.serial.decoders import decode_compact_array_length
from kio.serial.decoders import decode_compact_string
from kio.serial.decoders import decode_compact_string_as_bytes
from kio.serial.decoders import decode_compact_string_as_bytes_nullable
from kio.serial.decoders import decode_compact_string_nullable
from kio.serial.decoders import decode_int8
from kio.serial.decoders import decode_int16
from kio.serial.decoders import decode_int32
from kio.serial.decoders import decode_int64
from kio.serial.decoders import decode_uint8
from kio.serial.decoders import decode_uint16
from kio.serial.decoders import decode_uint32
from kio.serial.decoders import decode_uint64
from kio.serial.decoders import decode_unsigned_varint
from kio.serial.decoders import read_async
from kio.serial.decoders import read_sync
from kio.serial.encoders import Writer
from kio.serial.encoders import write_array_length
from kio.serial.encoders import write_boolean
from kio.serial.encoders import write_compact_array_length
from kio.serial.encoders import write_compact_string
from kio.serial.encoders import write_int8
from kio.serial.encoders import write_int16
from kio.serial.encoders import write_int32
from kio.serial.encoders import write_int64
from kio.serial.encoders import write_nullable_compact_string
from kio.serial.encoders import write_uint8
from kio.serial.encoders import write_uint16
from kio.serial.encoders import write_uint32
from kio.serial.encoders import write_uint64
from kio.serial.encoders import write_unsigned_varint
from tests.conftest import setup_async_buffers


@given(booleans(), booleans())
def test_booleans_roundtrip_sync(a: bool, b: bool) -> None:
    buffer = io.BytesIO()
    write_boolean(buffer, a)
    write_boolean(buffer, b)
    buffer.seek(0)
    assert a is read_sync(buffer, decode_boolean)
    assert b is read_sync(buffer, decode_boolean)
    # Make sure buffer is exhausted.
    assert buffer.read(1) == b""


def create_integer_roundtrip_test(
    int_writer: Writer[int],
    int_decoder: Decoder[int],
    min_value: int,
    max_value: int,
) -> type:
    parameterize = given(
        integers(min_value=min_value, max_value=max_value),
        integers(min_value=min_value, max_value=max_value),
    )

    class Test:
        @parameterize
        def test_roundtrip_sync(self, a: bool, b: bool) -> None:
            buffer = io.BytesIO()
            int_writer(buffer, a)
            int_writer(buffer, b)
            buffer.seek(0)
            assert a == read_sync(buffer, int_decoder)
            assert b == read_sync(buffer, int_decoder)
            # Make sure buffer is exhausted.
            assert buffer.read(1) == b"", "buffer not exhausted"

        @parameterize
        async def test_roundtrip_async(self, a: bool, b: bool) -> None:
            async with setup_async_buffers() as (stream_reader, stream_writer):
                int_writer(stream_writer, a)
                int_writer(stream_writer, b)
                assert a == await read_async(stream_reader, int_decoder)
                assert b == await read_async(stream_reader, int_decoder)

    return Test


TestInt8Roundtrip = create_integer_roundtrip_test(
    int_writer=write_int8,
    int_decoder=decode_int8,
    min_value=-(2**7),
    max_value=2**7 - 1,
)
TestInt16Roundtrip = create_integer_roundtrip_test(
    int_writer=write_int16,
    int_decoder=decode_int16,
    min_value=-(2**15),
    max_value=2**15 - 1,
)
TestInt32Roundtrip = create_integer_roundtrip_test(
    int_writer=write_int32,
    int_decoder=decode_int32,
    min_value=-(2**31),
    max_value=2**31 - 1,
)
TestInt64Roundtrip = create_integer_roundtrip_test(
    int_writer=write_int64,
    int_decoder=decode_int64,
    min_value=-(2**63),
    max_value=2**63 - 1,
)
TestUint8Roundtrip = create_integer_roundtrip_test(
    int_writer=write_uint8,
    int_decoder=decode_uint8,
    min_value=0,
    max_value=2**7 - 1,
)
TestUint16Roundtrip = create_integer_roundtrip_test(
    int_writer=write_uint16,
    int_decoder=decode_uint16,
    min_value=0,
    max_value=2**15 - 1,
)
TestUint32Roundtrip = create_integer_roundtrip_test(
    int_writer=write_uint32,
    int_decoder=decode_uint32,
    min_value=0,
    max_value=2**31 - 1,
)
TestUint64Roundtrip = create_integer_roundtrip_test(
    int_writer=write_uint64,
    int_decoder=decode_uint64,
    min_value=0,
    max_value=2**63 - 1,
)
TestUnsignedVarintRoundtrip = create_integer_roundtrip_test(
    int_writer=write_unsigned_varint,
    int_decoder=decode_unsigned_varint,
    min_value=0,
    max_value=2**31 - 1,
)
TestArrayLengthRoundtrip = create_integer_roundtrip_test(
    int_writer=write_array_length,
    int_decoder=decode_array_length,
    min_value=-(2**31),
    max_value=2**31 - 1,
)
TestCompactArrayLengthRoundtrip = create_integer_roundtrip_test(
    int_writer=write_compact_array_length,
    int_decoder=decode_compact_array_length,
    min_value=-1,
    max_value=2**31 - 2,
)


@given(text(), text())
def test_compact_string_roundtrip_sync(a: str, b: str) -> None:
    buffer = io.BytesIO()
    write_compact_string(buffer, a)
    write_compact_string(buffer, b)
    buffer.seek(0)
    assert a == read_sync(buffer, decode_compact_string)
    assert b == read_sync(buffer, decode_compact_string)
    # Make sure buffer is exhausted.
    assert buffer.read(1) == b""


@given(binary(), binary())
def test_compact_bytes_roundtrip_sync(a: bytes, b: bytes) -> None:
    buffer = io.BytesIO()
    write_compact_string(buffer, a)
    write_compact_string(buffer, b)
    buffer.seek(0)
    assert a == read_sync(buffer, decode_compact_string_as_bytes)
    assert b == read_sync(buffer, decode_compact_string_as_bytes)
    # Make sure buffer is exhausted.
    assert buffer.read(1) == b""


def test_compact_bytes_roundtrip_none_sync() -> None:
    buffer = io.BytesIO()
    write_nullable_compact_string(buffer, None)
    write_nullable_compact_string(buffer, None)
    buffer.seek(0)
    assert read_sync(buffer, decode_compact_string_as_bytes_nullable) is None
    assert read_sync(buffer, decode_compact_string_as_bytes_nullable) is None
    # Make sure buffer is exhausted.
    assert buffer.read(1) == b""


def test_compact_string_roundtrip_none_sync() -> None:
    buffer = io.BytesIO()
    write_nullable_compact_string(buffer, None)
    write_nullable_compact_string(buffer, None)
    buffer.seek(0)
    assert read_sync(buffer, decode_compact_string_nullable) is None
    assert read_sync(buffer, decode_compact_string_nullable) is None
    # Make sure buffer is exhausted.
    assert buffer.read(1) == b""
