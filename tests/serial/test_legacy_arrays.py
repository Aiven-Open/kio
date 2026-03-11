import io

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar
from typing import cast

import pytest

from kio.serial import entity_reader
from kio.serial import entity_writer
from kio.serial.errors import OutOfBoundValue
from kio.serial.readers import read_int32
from kio.serial.readers import read_legacy_array_length
from kio.serial.readers import read_legacy_string
from kio.serial.readers import read_uint8
from kio.serial.writers import write_int32
from kio.serial.writers import write_legacy_array_length
from kio.serial.writers import write_legacy_string
from kio.serial.writers import write_uint8
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import u8
from tests.read import exhaust
from tests.read import read


@dataclass(frozen=True, slots=True, kw_only=True)
class Child:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    name: str = field(metadata={"kafka_type": "string"})


@dataclass(frozen=True, slots=True, kw_only=True)
class Parent:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    name: str = field(metadata={"kafka_type": "string"})
    children: tuple[Child, ...]


def test_can_parse_legacy_entity_array(buffer: io.BytesIO) -> None:
    write_legacy_string(buffer, "Parent Name")
    write_legacy_array_length(buffer, i32(2))
    # First child
    write_legacy_string(buffer, "Child 1")
    # Second child
    write_legacy_string(buffer, "Child 2")

    instance = exhaust(entity_reader(Parent), buffer.getvalue())

    assert instance == Parent(
        name="Parent Name",
        children=(
            Child(name="Child 1"),
            Child(name="Child 2"),
        ),
    )


def test_can_serialize_legacy_entity_array(buffer: io.BytesIO) -> None:
    write_parent = entity_writer(Parent)
    instance = Parent(
        name="Parent Name",
        children=(
            Child(name="Child 1"),
            Child(name="Child 2"),
        ),
    )
    write_parent(buffer, instance)

    parent_name, remaining = read(read_legacy_string, buffer.getvalue())
    assert parent_name == "Parent Name"
    array_length, remaining = read(read_legacy_array_length, remaining)
    assert array_length == 2
    value, remaining = read(read_legacy_string, remaining)
    assert value == "Child 1"
    value = exhaust(read_legacy_string, remaining)
    assert value == "Child 2"


@dataclass(frozen=True, slots=True, kw_only=True)
class Flat:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    values: tuple[u8, ...] = field(metadata={"kafka_type": "uint8"})


def test_can_parse_legacy_primitive_array(buffer: io.BytesIO) -> None:
    write_legacy_array_length(buffer, i32(3))
    write_uint8(buffer, u8(123))
    write_uint8(buffer, u8(0))
    write_uint8(buffer, u8(255))

    instance = exhaust(entity_reader(Flat), buffer.getvalue())

    assert instance == Flat(values=(u8(123), u8(0), u8(255)))


def test_can_serialize_legacy_primitive_array(buffer: io.BytesIO) -> None:
    write_flat = entity_writer(Flat)
    instance = Flat(values=(u8(123), u8(0), u8(255)))
    write_flat(buffer, instance)

    array_length, remaining = read(read_legacy_array_length, buffer.getvalue())
    assert array_length == 3
    value, remaining = read(read_uint8, remaining)
    assert value == 123
    value, remaining = read(read_uint8, remaining)
    assert value == 0
    value = exhaust(read_uint8, remaining)
    assert value == 255


def test_serializing_raises_out_of_bound_error_for_too_large_array(
    buffer: io.BytesIO,
) -> None:
    class LargeCollection:
        def __len__(self) -> int:
            return i32.__high__ + 1

    instance = Flat(values=cast(tuple[u8, ...], LargeCollection()))
    writer = entity_writer(Flat)

    with pytest.raises(OutOfBoundValue, match=r"too long for legacy array format"):
        writer(buffer, instance)


@dataclass(frozen=True, slots=True, kw_only=True)
class NullablePrimitiveArray:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    values: tuple[i32, ...] | None = field(
        metadata={"kafka_type": "int32"},
        default=None,
    )


def test_can_serialize_nullable_primitive_array_with_values(buffer: io.BytesIO) -> None:
    entity_writer(NullablePrimitiveArray)(
        buffer,
        NullablePrimitiveArray(values=(i32(1), i32(2), i32(3))),
    )

    length, remaining = read(read_legacy_array_length, buffer.getvalue())
    assert length == 3
    value, remaining = read(read_int32, remaining)
    assert value == 1
    value, remaining = read(read_int32, remaining)
    assert value == 2
    value = exhaust(read_int32, remaining)
    assert value == 3


def test_can_serialize_nullable_primitive_array_with_null(buffer: io.BytesIO) -> None:
    entity_writer(NullablePrimitiveArray)(
        buffer,
        NullablePrimitiveArray(values=None),
    )

    length = exhaust(read_legacy_array_length, buffer.getvalue())
    assert length == -1


def test_can_parse_nullable_primitive_array_with_values(buffer: io.BytesIO) -> None:
    write_legacy_array_length(buffer, i32(2))
    write_int32(buffer, i32(42))
    write_int32(buffer, i32(99))

    instance = exhaust(entity_reader(NullablePrimitiveArray), buffer.getvalue())

    assert instance.values == (i32(42), i32(99))


def test_can_parse_nullable_primitive_array_with_null(buffer: io.BytesIO) -> None:
    write_legacy_array_length(buffer, i32(-1))

    instance = exhaust(entity_reader(NullablePrimitiveArray), buffer.getvalue())

    assert instance.values is None


def test_can_roundtrip_nullable_primitive_array_with_values(buffer: io.BytesIO) -> None:
    original = NullablePrimitiveArray(values=(i32(10), i32(20)))

    entity_writer(NullablePrimitiveArray)(buffer, original)
    result = exhaust(entity_reader(NullablePrimitiveArray), buffer.getvalue())

    assert result == original


def test_can_roundtrip_nullable_primitive_array_with_null(buffer: io.BytesIO) -> None:
    original = NullablePrimitiveArray(values=None)

    entity_writer(NullablePrimitiveArray)(buffer, original)
    result = exhaust(entity_reader(NullablePrimitiveArray), buffer.getvalue())

    assert result == original
    assert result.values is None
