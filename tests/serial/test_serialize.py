import asyncio

from kio.schema.entity import BrokerId
from kio.schema.metadata.response.v12 import MetadataResponse
from kio.schema.metadata.response.v12 import MetadataResponseBroker
from kio.serial.decoders import decode_compact_array_length
from kio.serial.decoders import decode_compact_string
from kio.serial.decoders import decode_compact_string_nullable
from kio.serial.decoders import decode_int32
from kio.serial.decoders import read_async
from kio.serial.decoders import skip_tagged_fields
from kio.serial.serialize import entity_writer


async def test_serialize_complex_entity_async(
    stream_reader: asyncio.StreamReader,
    stream_writer: asyncio.StreamWriter,
) -> None:
    write_metadata_response = entity_writer(MetadataResponse)

    instance = MetadataResponse(
        throttle_time_ms=123,
        brokers=(
            MetadataResponseBroker(
                node_id=BrokerId(1),
                host="foo.bar",
                port=1234,
                rack=None,
            ),
            MetadataResponseBroker(
                node_id=BrokerId(2),
                host="foo.bar",
                port=1234,
                rack=None,
            ),
        ),
        cluster_id="556",
        controller_id=BrokerId(3),
        topics=(),
    )
    write_metadata_response(stream_writer, instance)
    await stream_writer.drain()

    # throttle time
    assert 123 == await read_async(stream_reader, decode_int32)

    # brokers
    length = await read_async(stream_reader, decode_compact_array_length)
    assert length == 2
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
    assert 0 == await read_async(stream_reader, decode_compact_array_length)

    # main entity tagged fields
    await read_async(stream_reader, skip_tagged_fields)
