import io

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.serial import entity_reader
from kio.serial import entity_writer
from kio.serial.readers import read_compact_array_length
from kio.serial.readers import read_compact_string
from kio.serial.readers import read_uint8
from kio.serial.readers import read_unsigned_varint
from kio.serial.writers import write_compact_array_length
from kio.serial.writers import write_compact_string
from kio.serial.writers import write_empty_tagged_fields
from kio.serial.writers import write_uint8
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import u8


@dataclass(frozen=True, slots=True, kw_only=True)
class Child:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    name: str = field(metadata={"kafka_type": "string"})


@dataclass(frozen=True, slots=True, kw_only=True)
class Parent:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    name: str = field(metadata={"kafka_type": "string"})
    children: tuple[Child, ...]


def test_can_parse_flexible_entity_array(buffer: io.BytesIO) -> None:
    write_compact_string(buffer, "Parent Name")
    write_compact_array_length(buffer, 2)
    # First child
    write_compact_string(buffer, "Child 1")
    write_empty_tagged_fields(buffer)
    # Second child
    write_compact_string(buffer, "Child 2")
    write_empty_tagged_fields(buffer)
    # Parent tagged fields
    write_empty_tagged_fields(buffer)

    instance, size = entity_reader(Parent)(buffer.getvalue(), 0)

    assert size == buffer.tell()
    assert instance == Parent(
        name="Parent Name",
        children=(
            Child(name="Child 1"),
            Child(name="Child 2"),
        ),
    )


def test_can_serialize_flexible_entity_array() -> None:
    write_parent = entity_writer(Parent)
    instance = Parent(
        name="Parent Name",
        children=(
            Child(name="Child 1"),
            Child(name="Child 2"),
        ),
    )
    with io.BytesIO() as stream:
        write_parent(stream, instance)
        buffer = stream.getvalue()

    offset = 0

    parent_name, size = read_compact_string(buffer, offset)
    offset += size
    assert parent_name == "Parent Name"

    array_length, size = read_compact_array_length(buffer, offset)
    offset += size
    assert array_length == 2

    child_name, size = read_compact_string(buffer, offset)
    offset += size
    assert child_name == "Child 1"

    tagged_fields, size = read_unsigned_varint(buffer, offset)
    offset += size
    assert tagged_fields == 0

    child_name, size = read_compact_string(buffer, offset)
    offset += size
    assert child_name == "Child 2"

    tagged_fields, size = read_unsigned_varint(buffer, offset)
    offset += size
    assert tagged_fields == 0

    tagged_fields, size = read_unsigned_varint(buffer, offset)
    offset += size
    assert tagged_fields == 0

    assert offset == len(buffer)


@dataclass(frozen=True, slots=True, kw_only=True)
class Flat:
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    values: tuple[u8, ...] = field(metadata={"kafka_type": "uint8"})


def test_can_parse_flexible_primitive_array(buffer: io.BytesIO) -> None:
    write_compact_array_length(buffer, 3)
    write_uint8(buffer, u8(123))
    write_uint8(buffer, u8(0))
    write_uint8(buffer, u8(255))
    write_empty_tagged_fields(buffer)

    instance, size = entity_reader(Flat)(buffer.getvalue(), 0)

    assert size == buffer.tell()
    assert instance == Flat(values=(u8(123), u8(0), u8(255)))


def test_can_serialize_flexible_primitive_array() -> None:
    write_flat = entity_writer(Flat)
    instance = Flat(values=(u8(123), u8(0), u8(255)))
    offset = 0

    with io.BytesIO() as stream:
        write_flat(stream, instance)
        buffer = stream.getvalue()

    array_length, size = read_compact_array_length(buffer, offset)
    offset += size
    assert array_length == 3

    value, size = read_uint8(buffer, offset)
    offset += size
    assert value == 123

    value, size = read_uint8(buffer, offset)
    offset += size
    assert value == 0

    value, size = read_uint8(buffer, offset)
    offset += size
    assert value == 255

    tagged_fields, size = read_unsigned_varint(buffer, offset)
    offset += size
    assert tagged_fields == 0

    assert offset == len(buffer)
