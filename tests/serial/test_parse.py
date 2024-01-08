import datetime
import io
import uuid
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

import pytest

from kio.schema.metadata.v5.response import (
    MetadataResponseBroker as MetadataResponseBrokerV5,
)
from kio.schema.metadata.v12.response import MetadataResponse
from kio.schema.metadata.v12.response import (
    MetadataResponseBroker as MetadataResponseBrokerV12,
)
from kio.serial import entity_reader
from kio.serial import readers
from kio.serial._parse import get_reader
from kio.serial._shared import NullableEntityMarker
from kio.serial.writers import write_boolean
from kio.serial.writers import write_compact_array_length
from kio.serial.writers import write_compact_string
from kio.serial.writers import write_empty_tagged_fields
from kio.serial.writers import write_int8
from kio.serial.writers import write_int16
from kio.serial.writers import write_int32
from kio.serial.writers import write_legacy_string
from kio.serial.writers import write_nullable_compact_string
from kio.serial.writers import write_uuid
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i32


class TestGetReader:
    @pytest.mark.parametrize(
        "kafka_type, flexible, optional, expected",
        (
            ("int8", True, False, readers.read_int8),
            ("int8", False, False, readers.read_int8),
            ("int16", True, False, readers.read_int16),
            ("int16", False, False, readers.read_int16),
            ("int32", True, False, readers.read_int32),
            ("int32", False, False, readers.read_int32),
            ("int64", True, False, readers.read_int64),
            ("int64", False, False, readers.read_int64),
            ("uint8", True, False, readers.read_uint8),
            ("uint8", False, False, readers.read_uint8),
            ("uint16", True, False, readers.read_uint16),
            ("uint16", False, False, readers.read_uint16),
            ("uint32", True, False, readers.read_uint32),
            ("uint32", False, False, readers.read_uint32),
            ("uint64", True, False, readers.read_uint64),
            ("uint64", False, False, readers.read_uint64),
            ("float64", True, False, readers.read_float64),
            ("float64", False, False, readers.read_float64),
            ("string", True, False, readers.read_compact_string),
            ("string", True, True, readers.read_compact_string_nullable),
            ("string", False, False, readers.read_legacy_string),
            ("string", False, True, readers.read_nullable_legacy_string),
            ("bytes", True, False, readers.read_compact_string_as_bytes),
            ("bytes", True, True, readers.read_compact_string_as_bytes_nullable),
            ("bytes", False, False, readers.read_legacy_bytes),
            ("bytes", False, True, readers.read_nullable_legacy_bytes),
            ("records", True, True, readers.read_nullable_legacy_bytes),
            ("records", False, True, readers.read_nullable_legacy_bytes),
            ("uuid", False, True, readers.read_uuid),
            ("uuid", True, True, readers.read_uuid),
            ("bool", False, False, readers.read_boolean),
            ("bool", True, False, readers.read_boolean),
            ("error_code", False, False, readers.read_error_code),
            ("error_code", True, False, readers.read_error_code),
            ("timedelta_i32", False, False, readers.read_timedelta_i32),
            ("timedelta_i32", True, False, readers.read_timedelta_i32),
            ("timedelta_i64", False, False, readers.read_timedelta_i64),
            ("timedelta_i64", True, False, readers.read_timedelta_i64),
            ("datetime_i64", True, False, readers.read_datetime_i64),
            ("datetime_i64", False, False, readers.read_datetime_i64),
            ("datetime_i64", True, True, readers.read_nullable_datetime_i64),
            ("datetime_i64", False, True, readers.read_nullable_datetime_i64),
        ),
    )
    def test_can_match_kafka_type_with_reader(
        self,
        kafka_type: str,
        flexible: bool,
        optional: bool,
        expected: readers.Reader,
    ) -> None:
        assert get_reader(kafka_type, flexible, optional) == expected

    @pytest.mark.parametrize(
        "kafka_type, flexible, optional",
        (
            ("int8", True, True),
            ("int8", False, True),
            ("int16", True, True),
            ("int16", False, True),
            ("int32", True, True),
            ("int32", False, True),
            ("int64", True, True),
            ("int64", False, True),
            ("uint8", True, True),
            ("uint8", False, True),
            ("uint16", True, True),
            ("uint16", False, True),
            ("uint32", True, True),
            ("uint32", False, True),
            ("uint64", True, True),
            ("uint64", False, True),
            ("float64", True, True),
            ("float64", False, True),
            ("uuid", False, False),
            ("uuid", True, False),
            ("bool", False, True),
            ("bool", True, True),
            ("error_code", True, True),
            ("error_code", False, True),
            ("timedelta_i32", True, True),
            ("timedelta_i32", False, True),
            ("timedelta_i64", True, True),
            ("timedelta_i64", False, True),
            ("records", True, False),
            ("records", False, False),
        ),
    )
    def test_raises_not_implemented_error_for_invalid_combination(
        self,
        kafka_type: str,
        flexible: bool,
        optional: bool,
    ) -> None:
        with pytest.raises(NotImplementedError):
            get_reader(kafka_type, flexible, optional)


def test_can_parse_entity(buffer: io.BytesIO) -> None:
    assert MetadataResponseBrokerV12.__flexible__
    # node_id
    write_int32(buffer, i32(123))
    # host
    write_compact_string(buffer, "kafka.aiven.test")
    # port
    write_int32(buffer, i32(23_126))
    # rack
    write_compact_string(buffer, "da best")
    # tagged fields
    write_empty_tagged_fields(buffer)

    buffer.seek(0)
    instance = entity_reader(MetadataResponseBrokerV12)(buffer)
    assert isinstance(instance, MetadataResponseBrokerV12)

    assert instance.node_id == 123
    assert instance.host == "kafka.aiven.test"
    assert instance.port == 23_126
    assert instance.rack == "da best"


def test_can_parse_legacy_entity(buffer: io.BytesIO) -> None:
    assert not MetadataResponseBrokerV5.__flexible__
    # node_id
    write_int32(buffer, i32(123))
    # host
    write_legacy_string(buffer, "kafka.aiven.test")
    # port
    write_int32(buffer, i32(23_126))
    # rack
    write_legacy_string(buffer, "da best")

    buffer.seek(0)
    instance = entity_reader(MetadataResponseBrokerV5)(buffer)
    assert isinstance(instance, MetadataResponseBrokerV5)

    assert instance.node_id == 123
    assert instance.host == "kafka.aiven.test"
    assert instance.port == 23_126
    assert instance.rack == "da best"


def test_can_parse_complex_entity(buffer: io.BytesIO) -> None:
    assert MetadataResponse.__flexible__

    # throttle time
    write_int32(buffer, i32(123))

    # brokers
    write_compact_array_length(buffer, 2)
    for i in range(1, 3):
        # node_id
        write_int32(buffer, i32(i))
        # host
        write_compact_string(buffer, "kafka.aiven.test")
        # port
        write_int32(buffer, i**i)
        # rack
        write_compact_string(buffer, "da best")

        write_empty_tagged_fields(buffer)

    # cluster_id
    write_nullable_compact_string(buffer, None)

    # controller id
    write_int32(buffer, i32(321))

    # topics
    write_compact_array_length(buffer, 1)
    topic_id = uuid.uuid4()
    for i in range(1):
        # error code
        write_int16(buffer, i16(0))
        # name
        write_compact_string(buffer, f"great topic {i}")
        # topic_id
        write_uuid(buffer, topic_id)
        # is_internal
        write_boolean(buffer, False)

        # partitions
        write_compact_array_length(buffer, 1)
        for ii in range(1):
            # error_code
            write_int16(buffer, i16(0))
            # partition_index
            write_int32(buffer, i32(ii))
            # leader_id
            write_int32(buffer, i32(321))
            # leader_epoch
            write_int32(buffer, i32(13))
            # replica_nodes
            write_compact_array_length(buffer, 0)
            # isr_nodes
            write_compact_array_length(buffer, 0)
            # offline_replicas
            write_compact_array_length(buffer, 3)
            write_int32(buffer, i32(123))
            write_int32(buffer, i32(1090))
            write_int32(buffer, i32(3321))
            # tagged fields
            write_empty_tagged_fields(buffer)

        # topic_authorized_operations
        write_int32(buffer, i32(0))
        # tagged fields
        write_empty_tagged_fields(buffer)

    # main entity tagged fields
    write_empty_tagged_fields(buffer)

    buffer.seek(0)

    instance = entity_reader(MetadataResponse)(buffer)
    assert isinstance(instance, MetadataResponse)

    assert instance.throttle_time == datetime.timedelta(milliseconds=123)
    assert len(instance.brokers) == 2
    assert instance.cluster_id is None
    assert instance.controller_id == 321
    assert len(instance.topics) == 1
    assert instance.topics[0].error_code == 0
    assert instance.topics[0].name == "great topic 0"
    assert instance.topics[0].topic_id == topic_id
    assert instance.topics[0].is_internal is False
    assert len(instance.topics[0].partitions) == 1
    assert instance.topics[0].topic_authorized_operations == 0


@dataclass(frozen=True, slots=True, kw_only=True)
class Child:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(-1)
    name: str = field(metadata={"kafka_type": "string"})


@dataclass(frozen=True, slots=True, kw_only=True)
class UniParent:
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(-1)
    name: str = field(metadata={"kafka_type": "string"})
    child: Child


def test_can_parse_nested_non_array_entity(buffer: io.BytesIO) -> None:
    write_compact_string(buffer, "parent name")
    write_compact_string(buffer, "child name")
    write_empty_tagged_fields(buffer)  # child fields
    write_empty_tagged_fields(buffer)  # parent fields
    buffer.seek(0)

    instance = entity_reader(UniParent)(buffer)

    assert instance == UniParent(
        name="parent name",
        child=Child(name="child name"),
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class MultiParent:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(-2)
    name: str = field(metadata={"kafka_type": "string"})
    children: tuple[Child, ...]


def test_can_parse_nested_entity_array(buffer: io.BytesIO) -> None:
    write_compact_string(buffer, "parent name")
    write_compact_array_length(buffer, 2)
    write_compact_string(buffer, "first child")
    write_empty_tagged_fields(buffer)  # first child fields
    write_compact_string(buffer, "second child")
    write_empty_tagged_fields(buffer)  # second child fields
    write_empty_tagged_fields(buffer)  # parent fields
    buffer.seek(0)

    instance = entity_reader(MultiParent)(buffer)

    assert instance == MultiParent(
        name="parent name",
        children=(
            Child(name="first child"),
            Child(name="second child"),
        ),
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class EmptyFlexible:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True


@dataclass(frozen=True, slots=True, kw_only=True)
class EmptyLegacy:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False


def test_can_read_empty_flexible_entity(buffer: io.BytesIO) -> None:
    write_empty_tagged_fields(buffer)
    buffer.seek(0)
    instance = entity_reader(EmptyFlexible)(buffer)
    assert instance == EmptyFlexible()


def test_can_read_empty_legacy_entity(buffer: io.BytesIO) -> None:
    instance = entity_reader(EmptyLegacy)(buffer)
    assert instance == EmptyLegacy()


@dataclass(frozen=True, slots=True, kw_only=True)
class LegacyWithTag:
    __type__: ClassVar = EntityType.data
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    value: str = field(metadata={"kafka_type": "string", "tag": 0})


def test_raises_value_error_for_tagged_field_on_legacy_model() -> None:
    with pytest.raises(
        ValueError,
        match=r"^Found tagged fields on a non-flexible model$",
    ):
        entity_reader(LegacyWithTag)


@dataclass(frozen=True, slots=True, kw_only=True)
class NestedNullable:
    __type__: ClassVar = EntityType.header
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(-1)
    child: Child | None = field(default=None)
    name: str = field(metadata={"kafka_type": "string"})


def test_can_read_populated_nested_nullable_entity(buffer: io.BytesIO) -> None:
    write_int8(buffer, NullableEntityMarker.not_null.value)
    write_compact_string(buffer, "child name")
    write_empty_tagged_fields(buffer)  # child fields
    write_compact_string(buffer, "parent name")
    write_empty_tagged_fields(buffer)  # parent fields
    buffer.seek(0)

    instance = entity_reader(NestedNullable)(buffer)

    assert instance == NestedNullable(
        child=Child(name="child name"),
        name="parent name",
    )


def test_can_read_empty_nested_nullable_entity(buffer: io.BytesIO) -> None:
    write_int8(buffer, NullableEntityMarker.null.value)
    write_compact_string(buffer, "parent name")
    write_empty_tagged_fields(buffer)  # parent fields
    buffer.seek(0)

    instance = entity_reader(NestedNullable)(buffer)

    assert instance == NestedNullable(
        child=None,
        name="parent name",
    )
