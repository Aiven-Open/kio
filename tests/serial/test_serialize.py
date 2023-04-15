import io
import uuid

import pytest

from kio.schema.metadata.v12 import MetadataResponse
from kio.schema.metadata.v12.response import MetadataResponseBroker
from kio.schema.metadata.v12.response import MetadataResponsePartition
from kio.schema.metadata.v12.response import MetadataResponseTopic
from kio.schema.types import BrokerId
from kio.schema.types import TopicName
from kio.serial import entity_writer
from kio.serial import writers
from kio.serial._serialize import get_writer
from kio.serial.readers import read_boolean
from kio.serial.readers import read_compact_array_length
from kio.serial.readers import read_compact_string
from kio.serial.readers import read_compact_string_nullable
from kio.serial.readers import read_int16
from kio.serial.readers import read_int32
from kio.serial.readers import read_unsigned_varint
from kio.serial.readers import read_uuid
from kio.static.constants import ErrorCode
from kio.static.primitive import i32


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
            ("bytes", False, True, writers.write_nullable_legacy_string),
            ("bytes", True, False, writers.write_compact_string),
            ("bytes", False, False, writers.write_legacy_string),
            ("records", True, True, writers.write_nullable_legacy_string),
            ("records", False, True, writers.write_nullable_legacy_string),
            ("uuid", False, False, writers.write_uuid),
            ("uuid", True, False, writers.write_uuid),
            ("uuid", False, True, writers.write_uuid),
            ("uuid", True, True, writers.write_uuid),
            ("bool", False, False, writers.write_boolean),
            ("bool", True, False, writers.write_boolean),
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
            get_writer(kafka_type, flexible, optional)


async def test_serialize_complex_entity(buffer: io.BytesIO) -> None:
    write_metadata_response = entity_writer(MetadataResponse)

    topic_id = uuid.uuid4()
    instance = MetadataResponse(
        throttle_time_ms=i32(123),
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
