import asyncio
import io
import secrets
import uuid
from asyncio import StreamReader
from asyncio import StreamWriter
from contextlib import closing
from typing import Any
from typing import Final
from typing import TypeVar
from unittest import mock

import pytest

import kio.schema.request_header.v0.header
import kio.schema.request_header.v1.header
import kio.schema.request_header.v2.header
import kio.schema.response_header.v0.header
import kio.schema.response_header.v1.header
from kio.schema.create_topics.v7.request import CreatableTopic
from kio.schema.primitive import i16
from kio.schema.primitive import i32
from kio.schema.protocol import Entity
from kio.schema.protocol import Payload
from kio.schema.types import BrokerId
from kio.schema.types import TopicName
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_async
from kio.serial.decoders import decode_int32
from kio.serial.encoders import Writable
from kio.serial.encoders import write_int32

uuid_zero: Final = uuid.UUID(int=0)


def write_request_header(
    buffer: Writable,
    payload: Payload,
    correlation_id: i32,
    client_id: str | None,
) -> None:
    header_schema = payload.__header_schema__
    header: Entity

    if issubclass(header_schema, kio.schema.request_header.v0.header.RequestHeader):
        header = header_schema(
            request_api_key=payload.__api_key__,
            request_api_version=payload.__version__,
            correlation_id=correlation_id,
        )
    elif issubclass(
        header_schema,
        (
            kio.schema.request_header.v1.header.RequestHeader,
            kio.schema.request_header.v2.header.RequestHeader,
        ),
    ):
        header = header_schema(
            request_api_key=payload.__api_key__,
            request_api_version=payload.__version__,
            correlation_id=correlation_id,
            client_id=client_id,
        )
    else:
        raise NotImplementedError(f"Unknown request header schema: {header_schema}")

    print(f"request {header=}")
    print(f"request {header.__version__=}")
    print(f"request {header.__flexible__=}")

    entity_writer(header_schema)(buffer, header)  # type: ignore[type-var]


async def send(
    stream: StreamWriter,
    payload: Payload,
    correlation_id: i32,
) -> None:
    write_request = entity_writer(type(payload))

    # Write header and payload to a temporary in-memory buffer, this is necessary
    # because we need to be able to determine the byte size of the full message.
    buffer = io.BytesIO()
    write_request_header(
        buffer=buffer,
        payload=payload,
        correlation_id=correlation_id,
        client_id="test-integration",
    )
    write_request(buffer, payload)

    # Write message size.
    message_size = i32(buffer.getbuffer().nbytes)
    write_int32(stream, message_size)

    # Write message.
    buffer.seek(0)
    while chunk := buffer.read(1024):
        stream.write(chunk)

    # Draining the stream to make sure full message is sent.
    await stream.drain()


class CorrelationIdMismatch(RuntimeError):
    ...


R = TypeVar("R", bound=Payload)


async def receive(
    stream: StreamReader,
    response_type: type[R],
    correlation_id: i32,
) -> R:
    # I don't think it makes sense to use this value to read the exact length from the
    # buffer directly. I think it makes sense to keep reading from the buffer ad-hoc.
    # However, we could use this to introduce some wrapper around the buffer, so that it
    # raises an error once the value has been (or is about to be) exceeded.
    message_length = await read_async(stream, decode_int32)
    print(f"received {message_length=}")

    # fixme
    header_schema: Any = response_type.__header_schema__
    read_header = entity_decoder(header_schema)
    header = await read_async(stream, read_header)

    print(f"response {header=}")

    if header.correlation_id != correlation_id:
        raise CorrelationIdMismatch

    read_payload = entity_decoder(response_type)
    return await read_async(stream, read_payload)


async def make_request(
    request: Payload,
    response_type: type[R],
) -> R:
    correlation_id = i32(secrets.randbelow(i32.__high__ + 1))  # type: ignore[operator]
    stream_reader, stream_writer = await asyncio.open_connection(
        host="127.0.0.1",
        port=9092,
    )
    with closing(stream_writer):
        async with asyncio.timeout(1):
            await send(stream_writer, request, correlation_id)
            return await receive(stream_reader, response_type, correlation_id)


async def test_roundtrip_metadata():
    from kio.schema.metadata.v12.request import MetadataRequest
    from kio.schema.metadata.v12.request import MetadataRequestTopic
    from kio.schema.metadata.v12.response import MetadataResponse
    from kio.schema.metadata.v12.response import MetadataResponseBroker

    response = await make_request(
        request=MetadataRequest(
            topics=(
                MetadataRequestTopic(
                    topic_id=uuid_zero,
                    name=TopicName("le-topic"),
                ),
            ),
            allow_auto_topic_creation=True,
            include_topic_authorized_operations=False,
        ),
        response_type=MetadataResponse,
    )
    print(f"{response=}")

    assert response == MetadataResponse(
        throttle_time_ms=i32(0),
        brokers=(
            MetadataResponseBroker(
                node_id=BrokerId(1),
                host="broker",
                port=i32(9092),
            ),
        ),
        cluster_id=mock.ANY,
        controller_id=BrokerId(1),
        # Should maybe reset cluster between tests to enable checking this.
        topics=mock.ANY,
    )


async def test_roundtrip_v5_metadata():
    from kio.schema.metadata.v5.request import MetadataRequest
    from kio.schema.metadata.v5.request import MetadataRequestTopic
    from kio.schema.metadata.v5.response import MetadataResponse
    from kio.schema.metadata.v5.response import MetadataResponseBroker

    response = await make_request(
        request=MetadataRequest(
            topics=(MetadataRequestTopic(name=TopicName("le-topic")),),
        ),
        response_type=MetadataResponse,
    )
    print(f"{response=}")

    assert response == MetadataResponse(
        throttle_time_ms=i32(0),
        brokers=(
            MetadataResponseBroker(
                node_id=BrokerId(1),
                host="broker",
                port=i32(9092),
            ),
        ),
        # le-topic might or might not exist.
        topics=mock.ANY,
        controller_id=BrokerId(1),
        cluster_id=mock.ANY,
    )


async def test_roundtrip_api_versions():
    # FIXME: Why is v3 not working?! Something else that's undocumented and
    #  special-cased?
    from kio.schema.api_versions.v2.request import ApiVersionsRequest
    from kio.schema.api_versions.v2.response import ApiVersion
    from kio.schema.api_versions.v2.response import ApiVersionsResponse

    response = await make_request(
        request=ApiVersionsRequest(
            # client_software_name="",
            # client_software_version="",
        ),
        response_type=ApiVersionsResponse,
    )
    print(f"{response=}")
    assert response == ApiVersionsResponse(
        error_code=i16(0),
        throttle_time_ms=i32(0),
        api_keys=(
            ApiVersion(api_key=i16(0), min_version=i16(0), max_version=i16(9)),
            ApiVersion(api_key=i16(1), min_version=i16(0), max_version=i16(13)),
            ApiVersion(api_key=i16(2), min_version=i16(0), max_version=i16(7)),
            ApiVersion(api_key=i16(3), min_version=i16(0), max_version=i16(12)),
            ApiVersion(api_key=i16(8), min_version=i16(0), max_version=i16(8)),
            ApiVersion(api_key=i16(9), min_version=i16(0), max_version=i16(8)),
            ApiVersion(api_key=i16(10), min_version=i16(0), max_version=i16(4)),
            ApiVersion(api_key=i16(11), min_version=i16(0), max_version=i16(9)),
            ApiVersion(api_key=i16(12), min_version=i16(0), max_version=i16(4)),
            ApiVersion(api_key=i16(13), min_version=i16(0), max_version=i16(5)),
            ApiVersion(api_key=i16(14), min_version=i16(0), max_version=i16(5)),
            ApiVersion(api_key=i16(15), min_version=i16(0), max_version=i16(5)),
            ApiVersion(api_key=i16(16), min_version=i16(0), max_version=i16(4)),
            ApiVersion(api_key=i16(17), min_version=i16(0), max_version=i16(1)),
            ApiVersion(api_key=i16(18), min_version=i16(0), max_version=i16(3)),
            ApiVersion(api_key=i16(19), min_version=i16(0), max_version=i16(7)),
            ApiVersion(api_key=i16(20), min_version=i16(0), max_version=i16(6)),
            ApiVersion(api_key=i16(21), min_version=i16(0), max_version=i16(2)),
            ApiVersion(api_key=i16(22), min_version=i16(0), max_version=i16(4)),
            ApiVersion(api_key=i16(23), min_version=i16(0), max_version=i16(4)),
            ApiVersion(api_key=i16(24), min_version=i16(0), max_version=i16(3)),
            ApiVersion(api_key=i16(25), min_version=i16(0), max_version=i16(3)),
            ApiVersion(api_key=i16(26), min_version=i16(0), max_version=i16(3)),
            ApiVersion(api_key=i16(27), min_version=i16(0), max_version=i16(1)),
            ApiVersion(api_key=i16(28), min_version=i16(0), max_version=i16(3)),
            ApiVersion(api_key=i16(29), min_version=i16(0), max_version=i16(3)),
            ApiVersion(api_key=i16(30), min_version=i16(0), max_version=i16(3)),
            ApiVersion(api_key=i16(31), min_version=i16(0), max_version=i16(3)),
            ApiVersion(api_key=i16(32), min_version=i16(0), max_version=i16(4)),
            ApiVersion(api_key=i16(33), min_version=i16(0), max_version=i16(2)),
            ApiVersion(api_key=i16(34), min_version=i16(0), max_version=i16(2)),
            ApiVersion(api_key=i16(35), min_version=i16(0), max_version=i16(4)),
            ApiVersion(api_key=i16(36), min_version=i16(0), max_version=i16(2)),
            ApiVersion(api_key=i16(37), min_version=i16(0), max_version=i16(3)),
            ApiVersion(api_key=i16(42), min_version=i16(0), max_version=i16(2)),
            ApiVersion(api_key=i16(43), min_version=i16(0), max_version=i16(2)),
            ApiVersion(api_key=i16(44), min_version=i16(0), max_version=i16(1)),
            ApiVersion(api_key=i16(45), min_version=i16(0), max_version=i16(0)),
            ApiVersion(api_key=i16(46), min_version=i16(0), max_version=i16(0)),
            ApiVersion(api_key=i16(47), min_version=i16(0), max_version=i16(0)),
            ApiVersion(api_key=i16(48), min_version=i16(0), max_version=i16(1)),
            ApiVersion(api_key=i16(49), min_version=i16(0), max_version=i16(1)),
            ApiVersion(api_key=i16(55), min_version=i16(0), max_version=i16(1)),
            ApiVersion(api_key=i16(57), min_version=i16(0), max_version=i16(1)),
            ApiVersion(api_key=i16(60), min_version=i16(0), max_version=i16(0)),
            ApiVersion(api_key=i16(61), min_version=i16(0), max_version=i16(0)),
            ApiVersion(api_key=i16(64), min_version=i16(0), max_version=i16(0)),
            ApiVersion(api_key=i16(65), min_version=i16(0), max_version=i16(0)),
            ApiVersion(api_key=i16(66), min_version=i16(0), max_version=i16(0)),
        ),
    )
    mapped = {api_version.api_key: api_version for api_version in response.api_keys}
    create_topics = mapped[i16(19)]
    print(f"{create_topics=}")


@pytest.mark.xfail
async def test_multiple_stuff():
    # Some issue with v2 request headers ..., versions v5+ don't work. Kafka expects a
    # longer header than what we are producing.
    # FIXME: Update, above solved. Now, Kafka responds with a too short response ...
    # TopicConfigErrorCode is a prime suspect, when uncommented, the response parses
    # successfully. It has a schema feature that we haven't implemented: "tag": 0.
    # ... needs more research ...

    # This is likely it! So, need to somehow split things up in a way that makes sense
    # ... maybe just xfail this test for now?

    from kio.schema.create_topics.v7.request import CreateTopicsRequest
    from kio.schema.create_topics.v7.response import CreateTopicsResponse
    from kio.schema.metadata.v12.request import MetadataRequest
    from kio.schema.metadata.v12.request import MetadataRequestTopic
    from kio.schema.metadata.v12.response import MetadataResponse
    from kio.schema.metadata.v12.response import MetadataResponseBroker

    create_topics_response = await make_request(
        request=CreateTopicsRequest(
            topics=(
                CreatableTopic(
                    name=TopicName("le-topic"),
                    num_partitions=i32(3),
                    replication_factor=i16(1),
                    assignments=(),
                    configs=(),
                ),
            ),
            timeout_ms=i16(30_000),
        ),
        response_type=CreateTopicsResponse,
    )
    print(f"{create_topics_response=}")
    assert create_topics_response == CreateTopicsResponse(
        throttle_time_ms=i32(0),
        topics=(),
    )

    response = await make_request(
        request=MetadataRequest(
            topics=(
                MetadataRequestTopic(
                    topic_id=uuid_zero,
                    name=TopicName("le-topic"),
                ),
            ),
            allow_auto_topic_creation=True,
            include_topic_authorized_operations=False,
        ),
        response_type=MetadataResponse,
    )
    print(f"{response=}")
    assert response == MetadataResponse(
        throttle_time_ms=i32(0),
        brokers=(
            MetadataResponseBroker(
                node_id=BrokerId(1),
                host="broker",
                port=i32(9092),
            ),
        ),
        cluster_id=mock.ANY,
        controller_id=BrokerId(1),
        topics=(),
    )
