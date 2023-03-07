import asyncio
from kio.schema.create_topics.v7.request import CreateTopicsRequest
from kio.schema.create_topics.v7.response import CreateTopicsResponse
from kio.schema.create_topics.v7.response import CreatableTopicResult
from kio.schema.metadata.v12 import response as metadata_v12_response
from kio.schema.metadata.v5 import response as metadata_v5_response
from kio.schema.metadata.v12 import request as metadata_v12_request
from kio.schema.metadata.v5 import request as metadata_v5_request
from kio.schema.delete_topics.v6.request import DeleteTopicsRequest
from kio.schema.delete_topics.v6.request import DeleteTopicState
from kio.schema.delete_topics.v6.response import DeletableTopicResult
from kio.schema.delete_topics.v6.response import DeleteTopicsResponse
from kio.schema.api_versions.v3 import request as api_versions_v3_request
from kio.schema.api_versions.v3 import response as api_versions_v3_response
from kio.schema.api_versions.v2 import request as api_versions_v2_request
from kio.schema.api_versions.v2 import response as api_versions_v2_response
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
    # Note: I don't think it makes sense to use this value to read the exact length from
    # the buffer directly. I think it makes sense to keep reading from the buffer
    # ad-hoc. However, we could use this to introduce some wrapper around the buffer, so
    # that it raises an error once the value has been (or is about to be) exceeded.
    await read_async(stream, decode_int32)  # message length
    header_schema: Any = response_type.__header_schema__
    read_header = entity_decoder(header_schema)
    header = await read_async(stream, read_header)

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


async def test_roundtrip_api_versions_v3() -> None:
    import secrets
    response = await make_request(
        request=api_versions_v3_request.ApiVersionsRequest(
            client_software_name=secrets.token_hex(3),
            client_software_version=secrets.token_hex(3),
        ),
        response_type=api_versions_v3_response.ApiVersionsResponse,
    )
    ApiVersion = api_versions_v3_response.ApiVersion
    assert response == api_versions_v3_response.ApiVersionsResponse(
        error_code=i16(0),
        throttle_time_ms=i32(0),
        supported_features=(
            api_versions_v3_response.SupportedFeatureKey(
                name="metadata.version",
                min_version=i16(1),
                max_version=i16(7),
            ),
        ),
        finalized_features=(
            api_versions_v3_response.FinalizedFeatureKey(
                name="metadata.version",
                min_version_level=i16(7),
                max_version_level=i16(7),
            ),
        ),
        finalized_features_epoch=mock.ANY,
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


async def test_roundtrip_api_versions_v2() -> None:
    response = await make_request(
        request=api_versions_v2_request.ApiVersionsRequest(),
        response_type=api_versions_v2_response.ApiVersionsResponse,
    )
    ApiVersion = api_versions_v2_response.ApiVersion
    assert response == api_versions_v2_response.ApiVersionsResponse(
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


async def delete_topic(topic_name: TopicName) -> DeleteTopicsResponse:
    return await make_request(
        request=DeleteTopicsRequest(
            topics=(
                DeleteTopicState(name=topic_name, topic_id=uuid_zero),
            ),
            timeout_ms=i16(1000),
        ),
        response_type=DeleteTopicsResponse,
    )


async def create_topic(topic_name: TopicName) -> CreateTopicsResponse:
    return await make_request(
        request=CreateTopicsRequest(
            topics=(
                CreatableTopic(
                    name=topic_name,
                    num_partitions=i32(3),
                    replication_factor=i16(1),
                    assignments=(),
                    configs=(),
                ),
            ),
            timeout_ms=i16(1000),
        ),
        response_type=CreateTopicsResponse,
    )


async def metadata_v12() -> metadata_v12_response.MetadataResponse:
    return await make_request(
        request=metadata_v12_request.MetadataRequest(
            topics=(
                metadata_v12_request.MetadataRequestTopic(
                    topic_id=uuid_zero,
                    name=TopicName("le-topic"),
                ),
            ),
            allow_auto_topic_creation=True,
            include_topic_authorized_operations=False,
        ),
        response_type=metadata_v12_response.MetadataResponse,
    )


async def metadata_v5() -> metadata_v5_response.MetadataResponse:
    return await make_request(
        request=metadata_v5_request.MetadataRequest(
            topics=(
                metadata_v5_request.MetadataRequestTopic(
                    name=TopicName("le-topic"),
                ),
            ),
        ),
        response_type=metadata_v5_response.MetadataResponse,
    )


async def test_topic_and_metadata_operations() -> None:
    topic_name = TopicName("le-topic")

    # Test delete topic which might or might not exist.
    delete_topics_response = await delete_topic(topic_name)
    assert delete_topics_response == DeleteTopicsResponse(
        throttle_time_ms=i32(0),
        responses=(
            DeletableTopicResult(
                name=topic_name,
                topic_id=mock.ANY,
                error_code=mock.ANY,
                error_message=mock.ANY,
            ),
        )
    )

    # The previous deletion call should guarantee this call succeeds.
    create_topics_response = await create_topic(topic_name)
    assert create_topics_response == CreateTopicsResponse(
        throttle_time_ms=i32(0),
        topics=(
            CreatableTopicResult(
                name=topic_name,
                topic_id=mock.ANY,
                error_code=i16(0),
                error_message=None,
                num_partitions=i32(3),
                replication_factor=i16(1),
                configs=mock.ANY
            ),
        ),
    )
    created_topic, = create_topics_response.topics

    # The previous creation call should guarantee this call contains the topic.
    response = await metadata_v12()
    assert response == metadata_v12_response.MetadataResponse(
        throttle_time_ms=i32(0),
        brokers=(
            metadata_v12_response.MetadataResponseBroker(
                node_id=BrokerId(1),
                host="broker",
                port=i32(9092),
            ),
        ),
        cluster_id=mock.ANY,
        controller_id=BrokerId(1),
        topics=(
            metadata_v12_response.MetadataResponseTopic(
                error_code=i16(0),
                name=created_topic.name,
                topic_id=created_topic.topic_id,
                partitions=mock.ANY,
            ),
        ),
    )

    # Test also with a legacy format API version, i.e. non-flexible.
    response = await metadata_v5()
    assert response == metadata_v5_response.MetadataResponse(
        throttle_time_ms=i32(0),
        brokers=(
            metadata_v5_response.MetadataResponseBroker(
                node_id=BrokerId(1),
                host="broker",
                port=i32(9092),
            ),
        ),
        topics=(
            metadata_v5_response.MetadataResponseTopic(
                error_code=i16(0),
                name=created_topic.name,
                partitions=mock.ANY,
            ),
        ),
        controller_id=BrokerId(1),
        cluster_id=mock.ANY,
    )
