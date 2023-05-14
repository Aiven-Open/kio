import io
import uuid
from typing import TypeVar, Callable

from hypothesis import given
from hypothesis.strategies import binary
from hypothesis.strategies import booleans
from hypothesis.strategies import from_type
from hypothesis.strategies import integers
from hypothesis.strategies import none
from hypothesis.strategies import text
from hypothesis.strategies import uuids

from kio.schema.metadata.v12.response import MetadataResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from kio.serial.writers import Writer
from kio.serial.writers import write_boolean
from kio.serial.writers import write_compact_array_length
from kio.serial.writers import write_compact_string
from kio.serial.writers import write_int8
from kio.serial.writers import write_int16
from kio.serial.writers import write_int32
from kio.serial.writers import write_int64
from kio.serial.writers import write_legacy_array_length
from kio.serial.writers import write_legacy_string
from kio.serial.writers import write_nullable_compact_string
from kio.serial.writers import write_nullable_legacy_string
from kio.serial.writers import write_uint8
from kio.serial.writers import write_uint16
from kio.serial.writers import write_uint32
from kio.serial.writers import write_uint64
from kio.serial.writers import write_unsigned_varint
from kio.serial.writers import write_uuid
import kio._kio_core


@given(booleans(), booleans())
def test_booleans_roundtrip(a: bool, b: bool) -> None:
    with io.BytesIO() as buffer:
        write_boolean(buffer, a)
        write_boolean(buffer, b)
        encoded = buffer.getvalue()

    offset = 0
    value, offset = kio._kio_core.read_boolean(encoded, offset)
    assert a is value
    assert offset == 1
    value, offset = kio._kio_core.read_boolean(encoded, offset)
    assert b is value
    assert offset == 2


_I = TypeVar("_I", bound=int, contravariant=True)


def create_integer_roundtrip_test(
    int_writer: Writer[_I],
    int_reader: Callable[[bytes, int], tuple[int, int]],
    min_value: int,
    max_value: int,
) -> type:
    parameterize = given(
        integers(min_value=min_value, max_value=max_value),
        integers(min_value=min_value, max_value=max_value),
    )

    class Test:
        @parameterize
        def test_roundtrip(self, a: _I, b: _I) -> None:
            buffer = io.BytesIO()
            int_writer(buffer, a)
            int_writer(buffer, b)

            encoded = buffer.getvalue()
            offset = 0
            value, offset = int_reader(encoded, offset)
            assert a == value
            value, offset = int_reader(encoded, offset)
            assert b == value
            assert len(encoded) == offset

    return Test


TestInt8Roundtrip = create_integer_roundtrip_test(
    int_writer=write_int8,
    int_reader=kio._kio_core.read_int8,
    min_value=-(2**7),
    max_value=2**7 - 1,
)
TestInt16Roundtrip = create_integer_roundtrip_test(
    int_writer=write_int16,
    int_reader=kio._kio_core.read_int16,
    min_value=-(2**15),
    max_value=2**15 - 1,
)
TestInt32Roundtrip = create_integer_roundtrip_test(
    int_writer=write_int32,
    int_reader=kio._kio_core.read_int32,
    min_value=-(2**31),
    max_value=2**31 - 1,
)
TestInt64Roundtrip = create_integer_roundtrip_test(
    int_writer=write_int64,
    int_reader=kio._kio_core.read_int64,
    min_value=-(2**63),
    max_value=2**63 - 1,
)
TestUint8Roundtrip = create_integer_roundtrip_test(
    int_writer=write_uint8,
    int_reader=kio._kio_core.read_uint8,
    min_value=0,
    max_value=2**7 - 1,
)
TestUint16Roundtrip = create_integer_roundtrip_test(
    int_writer=write_uint16,
    int_reader=kio._kio_core.read_uint16,
    min_value=0,
    max_value=2**15 - 1,
)
TestUint32Roundtrip = create_integer_roundtrip_test(
    int_writer=write_uint32,
    int_reader=kio._kio_core.read_uint32,
    min_value=0,
    max_value=2**31 - 1,
)
TestUint64Roundtrip = create_integer_roundtrip_test(
    int_writer=write_uint64,
    int_reader=kio._kio_core.read_uint64,
    min_value=0,
    max_value=2**63 - 1,
)
TestUnsignedVarintRoundtrip = create_integer_roundtrip_test(
    int_writer=write_unsigned_varint,
    int_reader=kio._kio_core.read_unsigned_varint,
    min_value=0,
    max_value=2**31 - 1,
)
TestLegacyArrayLengthRoundtrip = create_integer_roundtrip_test(
    int_writer=write_legacy_array_length,
    int_reader=kio._kio_core.read_legacy_array_length,
    min_value=-(2**31),
    max_value=2**31 - 1,
)
TestCompactArrayLengthRoundtrip = create_integer_roundtrip_test(
    int_writer=write_compact_array_length,
    int_reader=kio._kio_core.read_compact_array_length,
    min_value=0,
    max_value=2**31 - 2,
)


@given(text(), text())
def test_compact_string_roundtrip_sync(a: str, b: str) -> None:
    buffer = io.BytesIO()
    write_compact_string(buffer, a)
    write_compact_string(buffer, b)
    encoded = buffer.getvalue()
    decoded_a, offset = kio._kio_core.read_compact_string(encoded, 0)
    decoded_b, offset = kio._kio_core.read_compact_string(encoded, offset)
    assert decoded_a == a
    assert decoded_b == b
    assert offset == buffer.tell()


@given(binary(), binary())
def test_compact_bytes_roundtrip(a: bytes, b: bytes) -> None:
    buffer = io.BytesIO()
    write_compact_string(buffer, a)
    write_compact_string(buffer, b)
    encoded = buffer.getvalue()
    decoded_a, offset = kio._kio_core.read_compact_string_as_bytes(encoded, 0)
    decoded_b, offset = kio._kio_core.read_compact_string_as_bytes(encoded, offset)
    assert decoded_a == a
    assert decoded_b == b
    assert offset == buffer.tell()


def test_compact_bytes_roundtrip_none() -> None:
    with io.BytesIO() as buffer:
        write_nullable_compact_string(buffer, None)
        write_nullable_compact_string(buffer, None)
        encoded = buffer.getvalue()
    decoded_a, offset = kio._kio_core.read_compact_string_as_bytes_nullable(encoded, 0)
    decoded_b, offset = kio._kio_core.read_compact_string_as_bytes_nullable(encoded, offset)
    assert decoded_a is None
    assert decoded_b is None
    assert offset == buffer.tell()


def test_compact_string_roundtrip_none() -> None:
    with io.BytesIO() as buffer:
        write_nullable_compact_string(buffer, None)
        write_nullable_compact_string(buffer, None)
        encoded = buffer.getvalue()
    decoded_a, offset = kio._kio_core.read_compact_string_nullable(encoded, 0)
    decoded_b, offset = kio._kio_core.read_compact_string_nullable(encoded, offset)
    assert decoded_a is None
    assert decoded_b is None
    assert offset == buffer.tell()


@given(text(), text())
def test_legacy_string_roundtrip(a: str, b: str) -> None:
    with io.BytesIO() as buffer:
        write_legacy_string(buffer, a)
        write_legacy_string(buffer, b)
        encoded = buffer.getvalue()
    decoded_a, offset = kio._kio_core.read_legacy_string(encoded, 0)
    decoded_b, offset = kio._kio_core.read_legacy_string(encoded, offset)
    assert decoded_a == a
    assert decoded_b == b
    assert offset == len(encoded)


@given(text() | none(), text() | none())
def test_nullable_legacy_string_roundtrip(a: str | None, b: str | None) -> None:
    with io.BytesIO() as buffer:
        write_nullable_legacy_string(buffer, a)
        write_nullable_legacy_string(buffer, b)
        encoded = buffer.getvalue()
    decoded_a, offset = kio._kio_core.read_nullable_legacy_string(encoded, 0)
    decoded_b, offset = kio._kio_core.read_nullable_legacy_string(encoded, offset)
    assert decoded_a == a
    assert decoded_b == b
    assert offset == len(encoded)


@given(binary(), binary())
def test_legacy_bytes_roundtrip(a: bytes, b: bytes) -> None:
    with io.BytesIO() as buffer:
        write_legacy_string(buffer, a)
        write_legacy_string(buffer, b)
        encoded = buffer.getvalue()
    decoded_a, offset = kio._kio_core.read_legacy_bytes(encoded, 0)
    decoded_b, offset = kio._kio_core.read_legacy_bytes(encoded, offset)
    assert decoded_a == a
    assert decoded_b == b
    assert offset == len(encoded)


@given(uuids() | none(), uuids() | none())
def test_uuid_roundtrip(a: uuid.UUID | None, b: uuid.UUID | None) -> None:
    with io.BytesIO() as buffer:
        write_uuid(buffer, a)
        write_uuid(buffer, b)
        encoded = buffer.getvalue()
    decoded_a, offset = kio._kio_core.read_uuid(encoded, 0)
    decoded_b, offset = kio._kio_core.read_uuid(encoded, offset)
    assert decoded_a == a
    assert decoded_b == b
    assert offset == len(encoded)


@given(from_type(MetadataResponse))
async def test_flexible_entity_roundtrip(instance: MetadataResponse) -> None:
    with io.BytesIO() as buffer:
        write_metadata_response = entity_writer(MetadataResponse)
        write_metadata_response(buffer, instance)
        encoded = buffer.getvalue()

    result, offset = entity_reader(MetadataResponse)(encoded, 0)
    assert instance == result
    assert offset == len(encoded)
