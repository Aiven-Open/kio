import datetime
import io
import uuid

from dataclasses import dataclass
from dataclasses import field
from dataclasses import fields
from typing import ClassVar

import pytest

from kio.schema.metadata.v12 import MetadataResponse
from kio.schema.metadata.v12.response import MetadataResponseBroker
from kio.schema.metadata.v12.response import MetadataResponsePartition
from kio.schema.metadata.v12.response import MetadataResponseTopic
from kio.schema.types import BrokerId
from kio.schema.types import TopicName
from kio.serial import entity_writer
from kio.serial import writers
from kio.serial._serialize import get_field_writer
from kio.serial._serialize import get_writer
from kio.serial._shared import NullableEntityMarker
from kio.serial.readers import read_boolean
from kio.serial.readers import read_compact_array_length
from kio.serial.readers import read_compact_string
from kio.serial.readers import read_compact_string_nullable
from kio.serial.readers import read_int8
from kio.serial.readers import read_int16
from kio.serial.readers import read_int32
from kio.serial.readers import read_unsigned_varint
from kio.serial.readers import read_uuid
from kio.static.constants import EntityType
from kio.static.constants import ErrorCode
from kio.static.primitive import i8
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i32Timedelta


class TestGetWriter:
    @pytest.mark.parametrize(
        "kafka_type, flexible, optional, expected",
        (
            ("int8", True, False, writers.write_int8),
            ("int8", False, False, writers.write_int8),
            ("int16", True, False, writers.write_int16),
            ("int16", False, False, writers.write_int16),
            ("int32", True, False, writers.write_int32),
            ("int32", False, False, writers.write_int32),
            ("int64", True, False, writers.write_int64),
            ("int64", False, False, writers.write_int64),
            ("uint8", True, False, writers.write_uint8),
            ("uint8", False, False, writers.write_uint8),
            ("uint16", True, False, writers.write_uint16),
            ("uint16", False, False, writers.write_uint16),
            ("uint32", True, False, writers.write_uint32),
            ("uint32", False, False, writers.write_uint32),
            ("uint64", True, False, writers.write_uint64),
            ("uint64", False, False, writers.write_uint64),
            ("float64", True, False, writers.write_float64),
            ("float64", False, False, writers.write_float64),
            ("string", True, False, writers.write_compact_string),
            ("string", True, True, writers.write_nullable_compact_string),
            ("string", False, False, writers.write_legacy_string),
            ("string", False, True, writers.write_nullable_legacy_string),
            ("bytes", True, True, writers.write_nullable_compact_string),
            ("bytes", False, True, writers.write_nullable_legacy_bytes),
            ("bytes", True, False, writers.write_compact_string),
            ("bytes", False, False, writers.write_legacy_bytes),
            ("records", True, True, writers.write_nullable_compact_string),
            ("records", False, True, writers.write_nullable_legacy_bytes),
            ("records", True, False, writers.write_compact_string),
            ("records", False, False, writers.write_legacy_bytes),
            ("uuid", False, False, writers.write_uuid),
            ("uuid", True, False, writers.write_uuid),
            ("uuid", False, True, writers.write_uuid),
            ("uuid", True, True, writers.write_uuid),
            ("bool", False, False, writers.write_boolean),
            ("bool", True, False, writers.write_boolean),
            ("error_code", True, False, writers.write_error_code),
            ("error_code", False, False, writers.write_error_code),
            ("timedelta_i32", True, False, writers.write_timedelta_i32),
            ("timedelta_i32", False, False, writers.write_timedelta_i32),
            ("timedelta_i64", True, False, writers.write_timedelta_i64),
            ("timedelta_i64", False, False, writers.write_timedelta_i64),
            ("datetime_i64", True, False, writers.write_datetime_i64),
            ("datetime_i64", False, False, writers.write_datetime_i64),
            ("datetime_i64", True, True, writers.write_nullable_datetime_i64),
            ("datetime_i64", False, True, writers.write_nullable_datetime_i64),
        ),
    )
    def test_can_match_kafka_type_with_writer(
        self,
        kafka_type: str,
        flexible: bool,
        optional: bool,
        expected: writers.Writer,
    ) -> None:
        assert get_writer(kafka_type, flexible, optional) == expected

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
            ("bool", False, True),
            ("bool", True, True),
            ("error_code", True, True),
            ("error_code", False, True),
            ("timedelta_i32", True, True),
            ("timedelta_i32", False, True),
            ("timedelta_i64", True, True),
            ("timedelta_i64", False, True),
        ),
    )
    def test_raises_not_implemented_error_for_invalid_combination(
        self,
        kafka_type: str,
        flexible: bool,
        optional: bool,
    ) -> None:
        with pytest.raises(NotImplementedError):
            get_writer(kafka_type, flexible, optional)


class TestGetFieldWriter:
    def test_special_cases_request_header_client_id(self) -> None:
        @dataclass
        class E:
            client_id: int

        [field] = fields(E)
        writer = get_field_writer(
            field=field, flexible=True, is_request_header=True, is_tag=False
        )
        assert writer == writers.write_nullable_legacy_string

    def test_returns_plain_writer_for_primitive_field(self) -> None:
        @dataclass
        class E:
            a: i8 = field(metadata={"kafka_type": "int8"})

        [extracted_field] = fields(E)
        writer = get_field_writer(
            field=extracted_field, flexible=True, is_request_header=True, is_tag=False
        )
        assert writer == writers.write_int8

    def test_returns_array_writer_for_primitive_tuple_field(
        self,
        buffer: io.BytesIO,
    ) -> None:
        @dataclass
        class E:
            a: tuple[i8, ...] = field(metadata={"kafka_type": "int8"})

        [extracted_field] = fields(E)
        writer = get_field_writer(
            field=extracted_field, flexible=True, is_request_header=True, is_tag=False
        )

        # We test that the returned object is an int8 array writer, by making
        # sure it behaves like one.
        writer(buffer, [1, 2, 3])
        buffer.seek(0)
        assert read_compact_array_length(buffer) == 3
        assert read_int8(buffer) == 1
        assert read_int8(buffer) == 2
        assert read_int8(buffer) == 3

    def test_returns_entity_writer_for_entity_field(
        self,
        buffer: io.BytesIO,
    ) -> None:
        @dataclass
        class A:
            __flexible__: ClassVar = True
            f: i8 = field(metadata={"kafka_type": "int8"})

        @dataclass
        class B:
            a: A

        [extracted_field] = fields(B)
        writer = get_field_writer(
            field=extracted_field, flexible=True, is_request_header=True, is_tag=False
        )

        writer(buffer, A(f=i8(23)))
        buffer.seek(0)
        assert read_int8(buffer) == 23
        assert read_unsigned_varint(buffer) == 0  # tags

    def test_returns_entity_writer_for_nullable_entity_field(
        self,
        buffer: io.BytesIO,
    ) -> None:
        @dataclass
        class A:
            __flexible__: ClassVar = True
            f: i8 = field(metadata={"kafka_type": "int8"})

        @dataclass
        class B:
            a: A | None

        [extracted_field] = fields(B)
        writer = get_field_writer(
            field=extracted_field, flexible=True, is_request_header=True, is_tag=False
        )

        writer(buffer, A(f=i8(23)))
        writer(buffer, None)
        buffer.seek(0)
        assert NullableEntityMarker(read_int8(buffer)) is NullableEntityMarker.not_null
        assert read_int8(buffer) == 23
        assert read_unsigned_varint(buffer) == 0  # tags
        assert NullableEntityMarker(read_int8(buffer)) is NullableEntityMarker.null

    def test_returns_entity_tuple_writer_for_entity_tuple_field(
        self,
        buffer: io.BytesIO,
    ) -> None:
        @dataclass
        class A:
            __flexible__: ClassVar = True
            f: i8 = field(metadata={"kafka_type": "int8"})

        @dataclass
        class B:
            a: tuple[A, ...]

        [extracted_field] = fields(B)
        writer = get_field_writer(
            field=extracted_field, flexible=True, is_request_header=True, is_tag=False
        )

        writer(buffer, [A(f=i8(23)), A(f=i8(17))])
        buffer.seek(0)
        assert read_compact_array_length(buffer) == 2
        assert read_int8(buffer) == 23
        assert read_unsigned_varint(buffer) == 0  # tags
        assert read_int8(buffer) == 17
        assert read_unsigned_varint(buffer) == 0  # tags


@dataclass(frozen=True, slots=True, kw_only=True)
class LegacyWithTag:
    __type__: ClassVar = EntityType.header
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    value: str = field(metadata={"kafka_type": "string", "tag": 0})


class TestEntityWriter:
    def test_raises_value_error_for_tagged_field_on_legacy_model(self) -> None:
        with pytest.raises(
            ValueError,
            match=r"^Found tagged fields on a non-flexible model$",
        ):
            entity_writer(LegacyWithTag)


def test_serialize_complex_entity(buffer: io.BytesIO) -> None:
    write_metadata_response = entity_writer(MetadataResponse)

    topic_id = uuid.uuid4()
    instance = MetadataResponse(
        throttle_time=i32Timedelta.parse(datetime.timedelta(milliseconds=123)),
        brokers=(
            MetadataResponseBroker(
                node_id=BrokerId(1),
                host="foo.bar",
                port=i32(1234),
                rack=None,
            ),
            MetadataResponseBroker(
                node_id=BrokerId(2),
                host="foo.bar",
                port=i32(1234),
                rack=None,
            ),
        ),
        cluster_id="556",
        controller_id=BrokerId(3),
        topics=(
            MetadataResponseTopic(
                error_code=ErrorCode.kafka_storage_error,
                name=TopicName("topic 1"),
                topic_id=topic_id,
                is_internal=False,
                partitions=(
                    MetadataResponsePartition(
                        error_code=ErrorCode.delegation_token_expired,
                        partition_index=i32(5679),
                        leader_id=BrokerId(2345),
                        leader_epoch=i32(6445678),
                        replica_nodes=(BrokerId(12345), BrokerId(7651)),
                        isr_nodes=(),
                        offline_replicas=(),
                    ),
                ),
                topic_authorized_operations=i32(765443),
            ),
        ),
    )
    write_metadata_response(buffer, instance)
    buffer.seek(0)

    # throttle time
    assert read_int32(buffer) == 123

    # brokers
    assert read_compact_array_length(buffer) == 2
    for i in range(1, 3):
        # node_id
        assert i == read_int32(buffer)
        # host
        assert read_compact_string(buffer) == "foo.bar"
        # port
        assert read_int32(buffer) == 1234
        # rack
        assert read_compact_string_nullable(buffer) is None
        # tagged fields
        assert read_unsigned_varint(buffer) == 0

    # cluster_id
    assert read_compact_string_nullable(buffer) == "556"

    # controller id
    assert read_int32(buffer) == 3

    # topics
    assert read_compact_array_length(buffer) == 1
    for _ in range(1):
        # error code
        assert read_int16(buffer) == ErrorCode.kafka_storage_error.value
        # name
        assert read_compact_string_nullable(buffer) == "topic 1"
        # topic id
        assert topic_id == read_uuid(buffer)
        # is internal
        assert read_boolean(buffer) is False
        # partitions
        assert read_compact_array_length(buffer) == 1
        for __ in range(1):
            # error code
            assert read_int16(buffer) == ErrorCode.delegation_token_expired.value
            # partition index
            assert read_int32(buffer) == 5679
            # leader id
            assert read_int32(buffer) == 2345
            # leader epoch
            assert read_int32(buffer) == 6445678
            # replica nodes
            assert read_compact_array_length(buffer) == 2
            assert read_int32(buffer) == 12345
            assert read_int32(buffer) == 7651
            # isr nodes
            assert read_compact_array_length(buffer) == 0
            # offline replicas
            assert read_compact_array_length(buffer) == 0
            # partition tagged fields
            assert read_unsigned_varint(buffer) == 0
        # topic authorized operations
        assert read_int32(buffer) == 765443
        # topic tagged fields
        assert read_unsigned_varint(buffer) == 0

    # main entity tagged fields
    assert read_unsigned_varint(buffer) == 0


@dataclass(frozen=True, slots=True, kw_only=True)
class Child:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(-1)
    name: str = field(metadata={"kafka_type": "string"})


@dataclass(frozen=True, slots=True, kw_only=True)
class NestedNullable:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(-1)
    child: Child | None = field(default=None)
    name: str = field(metadata={"kafka_type": "string"})


def test_can_write_populated_nested_nullable_entity(buffer: io.BytesIO) -> None:
    write_nested_nullable = entity_writer(NestedNullable)
    instance = NestedNullable(
        child=Child(name="child name"),
        name="parent name",
    )
    write_nested_nullable(buffer, instance)
    buffer.seek(0)

    assert read_int8(buffer) == NullableEntityMarker.not_null.value
    assert read_compact_string(buffer) == "child name"
    assert read_unsigned_varint(buffer) == 0  # tagged fields
    assert read_compact_string(buffer) == "parent name"
    assert read_unsigned_varint(buffer) == 0  # tagged fields


def test_can_write_empty_nested_nullable_entity(buffer: io.BytesIO) -> None:
    write_nested_nullable = entity_writer(NestedNullable)
    instance = NestedNullable(
        child=None,
        name="parent name",
    )
    write_nested_nullable(buffer, instance)
    buffer.seek(0)

    assert read_int8(buffer) == NullableEntityMarker.null.value
    assert read_compact_string(buffer) == "parent name"
    assert read_unsigned_varint(buffer) == 0  # tagged fields
