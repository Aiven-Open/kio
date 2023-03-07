import io
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar
from typing import cast

import pytest

from kio.schema.primitive import i32
from kio.schema.primitive import u8
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from kio.serial.decoders import decode_legacy_array_length
from kio.serial.decoders import decode_legacy_string
from kio.serial.decoders import decode_uint8
from kio.serial.encoders import write_legacy_array_length
from kio.serial.encoders import write_legacy_string
from kio.serial.encoders import write_uint8
from kio.serial.errors import OutOfBoundValue


@dataclass(frozen=True, slots=True, kw_only=True)
class Child:
    __flexible__: ClassVar[bool] = False
    name: str = field(metadata={"kafka_type": "string"})


@dataclass(frozen=True, slots=True, kw_only=True)
class Parent:
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

    instance = read_sync(buffer, entity_decoder(Parent))

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

    assert read_sync(buffer, decode_legacy_string) == "Parent Name"
    assert read_sync(buffer, decode_legacy_array_length) == 2
    assert read_sync(buffer, decode_legacy_string) == "Child 1"
    assert read_sync(buffer, decode_legacy_string) == "Child 2"


@dataclass(frozen=True, slots=True, kw_only=True)
class Flat:
    __flexible__: ClassVar[bool] = False
    values: tuple[u8, ...] = field(metadata={"kafka_type": "uint8"})


def test_can_parse_legacy_primitive_array(buffer: io.BytesIO) -> None:
    write_legacy_array_length(buffer, i32(3))
    write_uint8(buffer, u8(123))
    write_uint8(buffer, u8(0))
    write_uint8(buffer, u8(255))
    buffer.seek(0)

    instance = read_sync(buffer, entity_decoder(Flat))

    assert instance == Flat(values=(u8(123), u8(0), u8(255)))


def test_can_serialize_legacy_primitive_array(buffer: io.BytesIO) -> None:
    write_flat = entity_writer(Flat)
    instance = Flat(values=(u8(123), u8(0), u8(255)))
    write_flat(buffer, instance)
    buffer.seek(0)

    assert read_sync(buffer, decode_legacy_array_length) == 3
    assert read_sync(buffer, decode_uint8) == 123
    assert read_sync(buffer, decode_uint8) == 0
    assert read_sync(buffer, decode_uint8) == 255


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
