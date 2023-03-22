import io
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i16
from kio.schema.primitive import u8
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


@dataclass(frozen=True, slots=True, kw_only=True)
class Child:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    name: str = field(metadata={"kafka_type": "string"})


@dataclass(frozen=True, slots=True, kw_only=True)
class Parent:
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

    buffer.seek(0)

    instance = entity_reader(Parent)(buffer)

    assert instance == Parent(
        name="Parent Name",
        children=(
            Child(name="Child 1"),
            Child(name="Child 2"),
        ),
    )


def test_can_serialize_flexible_entity_array(buffer: io.BytesIO) -> None:
    write_parent = entity_writer(Parent)
    instance = Parent(
        name="Parent Name",
        children=(
            Child(name="Child 1"),
            Child(name="Child 2"),
        ),
    )
    write_parent(buffer, instance)
    buffer.seek(0)

    assert read_compact_string(buffer) == "Parent Name"
    assert read_compact_array_length(buffer) == 2
    assert read_compact_string(buffer) == "Child 1"
    assert read_unsigned_varint(buffer) == 0  # child 1 tagged fields
    assert read_compact_string(buffer) == "Child 2"
    assert read_unsigned_varint(buffer) == 0  # child 2 tagged fields
    assert read_unsigned_varint(buffer) == 0  # parent tagged fields


@dataclass(frozen=True, slots=True, kw_only=True)
class Flat:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    values: tuple[u8, ...] = field(metadata={"kafka_type": "uint8"})


def test_can_parse_flexible_primitive_array(buffer: io.BytesIO) -> None:
    write_compact_array_length(buffer, 3)
    write_uint8(buffer, u8(123))
    write_uint8(buffer, u8(0))
    write_uint8(buffer, u8(255))
    write_empty_tagged_fields(buffer)
    buffer.seek(0)

    instance = entity_reader(Flat)(buffer)

    assert instance == Flat(values=(u8(123), u8(0), u8(255)))


def test_can_serialize_flexible_primitive_array(buffer: io.BytesIO) -> None:
    write_flat = entity_writer(Flat)
    instance = Flat(values=(u8(123), u8(0), u8(255)))
    write_flat(buffer, instance)
    buffer.seek(0)

    assert read_compact_array_length(buffer) == 3
    assert read_uint8(buffer) == 123
    assert read_uint8(buffer) == 0
    assert read_uint8(buffer) == 255
    assert read_unsigned_varint(buffer) == 0  # tagged fields
