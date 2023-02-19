import asyncio
import uuid

import pytest

from kio.schema.metadata.v12.response import MetadataResponse
from kio.schema.metadata.v12.response import MetadataResponseBroker
from kio.schema.metadata.v12.response import MetadataResponsePartition
from kio.schema.metadata.v12.response import MetadataResponseTopic
from kio.schema.primitive import i16
from kio.schema.primitive import i32
from kio.schema.types import BrokerId
from kio.schema.types import TopicName
from kio.serial import encoders
from kio.serial.decoders import decode_boolean
from kio.serial.decoders import decode_compact_array_length
from kio.serial.decoders import decode_compact_string
from kio.serial.decoders import decode_compact_string_nullable
from kio.serial.decoders import decode_int16
from kio.serial.decoders import decode_int32
from kio.serial.decoders import decode_uuid
from kio.serial.decoders import read_async
from kio.serial.decoders import skip_tagged_fields
from kio.serial.serialize import entity_writer
from kio.serial.serialize import get_writer


class TestGetWriter:
    @pytest.mark.parametrize(
        "kafka_type, flexible, optional, expected",
        (
            ("int8", True, False, encoders.write_int8),
            ("int8", False, False, encoders.write_int8),
            ("int16", True, False, encoders.write_int16),
            ("int16", False, False, encoders.write_int16),
            ("int32", True, False, encoders.write_int32),
            ("int32", False, False, encoders.write_int32),
            ("int64", True, False, encoders.write_int64),
            ("int64", False, False, encoders.write_int64),
            ("uint8", True, False, encoders.write_uint8),
            ("uint8", False, False, encoders.write_uint8),
            ("uint16", True, False, encoders.write_uint16),
            ("uint16", False, False, encoders.write_uint16),
            ("uint32", True, False, encoders.write_uint32),
            ("uint32", False, False, encoders.write_uint32),
            ("uint64", True, False, encoders.write_uint64),
            ("uint64", False, False, encoders.write_uint64),
            ("float64", True, False, encoders.write_float64),
            ("float64", False, False, encoders.write_float64),
            ("string", True, False, encoders.write_compact_string),
            ("string", True, True, encoders.write_nullable_compact_string),
            ("string", False, False, encoders.write_legacy_string),
            ("string", False, True, encoders.write_nullable_legacy_string),
            ("uuid", False, False, encoders.write_uuid),
            ("uuid", True, False, encoders.write_uuid),
            ("bool", False, False, encoders.write_boolean),
            ("bool", True, False, encoders.write_boolean),
        ),
    )
    def test_can_match_kafka_type_with_writer(
        self,
        kafka_type: str,
        flexible: bool,
        optional: bool,
        expected: encoders.Writer,
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
            ("uuid", False, True),
            ("uuid", True, True),
            ("bool", False, True),
            ("bool", True, True),
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


async def test_serialize_complex_entity_async(
    stream_reader: asyncio.StreamReader,
    stream_writer: asyncio.StreamWriter,
) -> None:
    write_metadata_response = entity_writer(MetadataResponse)

    topic_id = uuid.uuid4()
    instance = MetadataResponse(
        throttle_time_ms=i32(123),
        brokers=(
            MetadataResponseBroker(
                node_id=BrokerId(i32(1)),
                host="foo.bar",
                port=i32(1234),
                rack=None,
            ),
            MetadataResponseBroker(
                node_id=BrokerId(i32(2)),
                host="foo.bar",
                port=i32(1234),
                rack=None,
            ),
        ),
        cluster_id="556",
        controller_id=BrokerId(i32(3)),
        topics=(
            MetadataResponseTopic(
                error_code=i16(123),
                name=TopicName("topic 1"),
                topic_id=topic_id,
                is_internal=False,
                partitions=(
                    MetadataResponsePartition(
                        error_code=i16(8765),
                        partition_index=i32(5679),
                        leader_id=BrokerId(i32(2345)),
                        leader_epoch=i32(6445678),
                        replica_nodes=(BrokerId(i32(12345)), BrokerId(i32(7651))),
                        isr_nodes=(),
                        offline_replicas=(),
                    ),
                ),
                topic_authorized_operations=i32(765443),
            ),
        ),
    )
    write_metadata_response(stream_writer, instance)
    await stream_writer.drain()

    # throttle time
    assert 123 == await read_async(stream_reader, decode_int32)

    # brokers
    assert 2 == await read_async(stream_reader, decode_compact_array_length)
    for i in range(1, 3):
        # node_id
        assert i == await read_async(stream_reader, decode_int32)
        # host
        assert "foo.bar" == await read_async(stream_reader, decode_compact_string)
        # port
        assert 1234 == await read_async(stream_reader, decode_int32)
        # rack
        assert await read_async(stream_reader, decode_compact_string_nullable) is None
        # tagged fields
        await read_async(stream_reader, skip_tagged_fields)

    # cluster_id
    assert "556" == await read_async(stream_reader, decode_compact_string_nullable)

    # controller id
    assert 3 == await read_async(stream_reader, decode_int32)

    # topics
    assert 1 == await read_async(stream_reader, decode_compact_array_length)
    for _ in range(1):
        # error code
        assert 123 == await read_async(stream_reader, decode_int16)
        # name
        assert "topic 1" == await read_async(
            stream_reader, decode_compact_string_nullable
        )
        # topic id
        assert topic_id == await read_async(stream_reader, decode_uuid)
        # is internal
        assert await read_async(stream_reader, decode_boolean) is False
        # partitions
        assert 1 == await read_async(stream_reader, decode_compact_array_length)
        for __ in range(1):
            # error code
            assert 8765 == await read_async(stream_reader, decode_int16)
            # partition index
            assert 5679 == await read_async(stream_reader, decode_int32)
            # leader id
            assert 2345 == await read_async(stream_reader, decode_int32)
            # leader epoch
            assert 6445678 == await read_async(stream_reader, decode_int32)
            # replica nodes
            assert 2 == await read_async(stream_reader, decode_compact_array_length)
            assert 12345 == await read_async(stream_reader, decode_int32)
            assert 7651 == await read_async(stream_reader, decode_int32)
            # isr nodes
            assert 0 == await read_async(stream_reader, decode_compact_array_length)
            # offline replicas
            assert 0 == await read_async(stream_reader, decode_compact_array_length)
            # partition tagged fields
            await read_async(stream_reader, skip_tagged_fields)
        # topic authorized operations
        assert 765443 == await read_async(stream_reader, decode_int32)
        # topic tagged fields
        await read_async(stream_reader, skip_tagged_fields)

    # main entity tagged fields
    await read_async(stream_reader, skip_tagged_fields)
