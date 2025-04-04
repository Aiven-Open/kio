import io

from collections.abc import Sequence
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar
from typing import Generic
from typing import TypeVar

import pytest

from kio.serial import entity_reader
from kio.serial import entity_writer
from kio.serial.readers import Reader
from kio.serial.readers import read_compact_string
from kio.serial.readers import read_uint8
from kio.serial.readers import read_unsigned_varint
from kio.serial.writers import Writer
from kio.serial.writers import write_compact_string
from kio.serial.writers import write_tagged_field
from kio.serial.writers import write_uint8
from kio.serial.writers import write_unsigned_varint
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import u8
from kio.static.primitive import uvarint


@dataclass(frozen=True, slots=True, kw_only=True)
class Nested:
    __type__: ClassVar = EntityType.data
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(-1)
    str_field: str = field(metadata={"kafka_type": "string"})
    int_field: u8 = field(metadata={"kafka_type": "uint8"})


@dataclass(frozen=True, slots=True, kw_only=True)
class Person:
    __type__: ClassVar = EntityType.data
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(-1)
    name: str = field(metadata={"kafka_type": "string"}, default="Almaszout")
    age: u8 = field(metadata={"kafka_type": "uint8", "tag": 0})
    # "Ignorable" tagged field shall result in None-able and default=None.
    country: str | None = field(
        metadata={"kafka_type": "string", "tag": 1},
        default=None,
    )
    tagged_struct: Nested = field(metadata={"tag": 2})


read_person = entity_reader(Person)

T = TypeVar("T")


@dataclass(frozen=True, slots=True, kw_only=True)
class WritableTag(Generic[T]):
    tag: int
    writer: Writer[T]
    value: T


@pytest.mark.parametrize(
    ("tagged_values", "expected"),
    [
        (
            [WritableTag(tag=0, writer=write_uint8, value=u8(123))],
            Person(
                age=u8(123),
                tagged_struct=Nested(str_field="", int_field=u8(0)),
            ),
        ),
        (
            [
                WritableTag(tag=0, writer=write_uint8, value=u8(12)),
                WritableTag(tag=1, writer=write_compact_string, value="Borduria"),
            ],
            Person(
                age=u8(12),
                country="Borduria",
                tagged_struct=Nested(str_field="", int_field=u8(0)),
            ),
        ),
        (
            [WritableTag(tag=1, writer=write_compact_string, value="Borduria")],
            Person(
                age=u8(0),
                country="Borduria",
                tagged_struct=Nested(str_field="", int_field=u8(0)),
            ),
        ),
        (
            [
                WritableTag(
                    tag=2,
                    writer=entity_writer(Nested),
                    value=Nested(str_field="hello", int_field=u8(123)),
                ),
            ],
            Person(
                age=u8(0),
                tagged_struct=Nested(str_field="hello", int_field=u8(123)),
            ),
        ),
    ],
)
def test_can_parse_tagged_fields(
    buffer: io.BytesIO,
    tagged_values: Sequence[WritableTag],
    expected: Person,
) -> None:
    write_compact_string(buffer, "Almaszout")  # name

    write_unsigned_varint(buffer, uvarint(len(tagged_values)))  # num tagged fields
    for tagged_value in tagged_values:
        write_tagged_field(
            buffer,
            uvarint(tagged_value.tag),
            tagged_value.writer,
            tagged_value.value,
        )

    buffer.seek(0)

    assert read_person(buffer) == expected


@dataclass(frozen=True, slots=True, kw_only=True)
class ReadableTag(Generic[T]):
    tag: int
    reader: Reader[T]
    value: T


@pytest.mark.parametrize(
    ("instance", "expected_tags"),
    [
        (
            Person(
                age=u8(123),
                tagged_struct=Nested(str_field="", int_field=u8(0)),
            ),
            [ReadableTag(tag=0, reader=read_uint8, value=u8(123))],
        ),
        (
            Person(
                age=u8(12),
                country="Borduria",
                tagged_struct=Nested(str_field="", int_field=u8(0)),
            ),
            [
                ReadableTag(tag=0, reader=read_uint8, value=u8(12)),
                ReadableTag(tag=1, reader=read_compact_string, value="Borduria"),
            ],
        ),
        (
            Person(
                age=u8(1),
                country=None,
                tagged_struct=Nested(str_field="", int_field=u8(0)),
            ),
            [ReadableTag(tag=0, reader=read_uint8, value=u8(1))],
        ),
        (
            Person(age=u8(0), tagged_struct=Nested(str_field="", int_field=u8(0))),
            [],
        ),
        (
            Person(age=u8(0), tagged_struct=Nested(str_field="hello", int_field=u8(0))),
            [
                ReadableTag(
                    tag=2,
                    reader=entity_reader(Nested),
                    value=Nested(str_field="hello", int_field=u8(0)),
                )
            ],
        ),
        (
            Person(age=u8(0), tagged_struct=Nested(str_field="", int_field=u8(1))),
            [
                ReadableTag(
                    tag=2,
                    reader=entity_reader(Nested),
                    value=Nested(str_field="", int_field=u8(1)),
                )
            ],
        ),
    ],
)
def test_can_serialize_tagged_fields(
    buffer: io.BytesIO,
    instance: Person,
    expected_tags: Sequence[ReadableTag],
) -> None:
    entity_writer(Person)(buffer, instance)

    buffer.seek(0)

    assert read_compact_string(buffer) == "Almaszout"  # name

    num_tagged_values = read_unsigned_varint(buffer)
    assert num_tagged_values == len(expected_tags)
    for tag in expected_tags:
        assert read_unsigned_varint(buffer) == tag.tag
        read_unsigned_varint(buffer)  # length
        assert tag.reader(buffer) == tag.value
