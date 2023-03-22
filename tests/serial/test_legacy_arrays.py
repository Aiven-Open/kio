import io
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar
from typing import cast

import pytest

from kio.schema.primitive import i16
from kio.schema.primitive import i32
from kio.schema.primitive import u8
from kio.serial import entity_reader
from kio.serial import entity_writer
from kio.serial.errors import OutOfBoundValue
from kio.serial.readers import read_legacy_array_length
from kio.serial.readers import read_legacy_string
from kio.serial.readers import read_uint8
from kio.serial.writers import write_legacy_array_length
from kio.serial.writers import write_legacy_string
from kio.serial.writers import write_uint8


@dataclass(frozen=True, slots=True, kw_only=True)
class Child:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    name: str = field(metadata={"kafka_type": "string"})


@dataclass(frozen=True, slots=True, kw_only=True)
class Parent:
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

    buffer.seek(0)

    instance = entity_reader(Parent)(buffer)

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
    buffer.seek(0)

    assert read_legacy_string(buffer) == "Parent Name"
    assert read_legacy_array_length(buffer) == 2
    assert read_legacy_string(buffer) == "Child 1"
    assert read_legacy_string(buffer) == "Child 2"


@dataclass(frozen=True, slots=True, kw_only=True)
class Flat:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    values: tuple[u8, ...] = field(metadata={"kafka_type": "uint8"})


def test_can_parse_legacy_primitive_array(buffer: io.BytesIO) -> None:
    write_legacy_array_length(buffer, i32(3))
    write_uint8(buffer, u8(123))
    write_uint8(buffer, u8(0))
    write_uint8(buffer, u8(255))
    buffer.seek(0)

    instance = entity_reader(Flat)(buffer)

    assert instance == Flat(values=(u8(123), u8(0), u8(255)))


def test_can_serialize_legacy_primitive_array(buffer: io.BytesIO) -> None:
    write_flat = entity_writer(Flat)
    instance = Flat(values=(u8(123), u8(0), u8(255)))
    write_flat(buffer, instance)
    buffer.seek(0)

    assert read_legacy_array_length(buffer) == 3
    assert read_uint8(buffer) == 123
    assert read_uint8(buffer) == 0
    assert read_uint8(buffer) == 255


def test_serializing_raises_out_of_bound_error_for_too_large_array(
    buffer: io.BytesIO,
) -> None:
    class LargeCollection:
        def __len__(self) -> int:
            return cast(int, i32.__high__) + 1

    instance = Flat(values=cast(tuple[u8, ...], LargeCollection()))
    writer = entity_writer(Flat)

    with pytest.raises(OutOfBoundValue, match=r"too long for legacy array format"):
        writer(buffer, instance)
