import asyncio
import io
import secrets
from asyncio import StreamReader
from asyncio import StreamWriter
from contextlib import closing
from typing import Any
from typing import TypeVar
from unittest import mock

import kio.schema.request_header.v0.header
import kio.schema.request_header.v1.header
import kio.schema.request_header.v2.header
import kio.schema.response_header.v0.header
import kio.schema.response_header.v1.header
from kio.schema.api_versions.v2 import request as api_versions_v2_request
from kio.schema.api_versions.v2 import response as api_versions_v2_response
from kio.schema.api_versions.v3 import request as api_versions_v3_request
from kio.schema.api_versions.v3 import response as api_versions_v3_response
from kio.schema.create_topics.v7 import CreateTopicsRequest
from kio.schema.create_topics.v7 import CreateTopicsResponse
from kio.schema.create_topics.v7.request import CreatableTopic
from kio.schema.create_topics.v7.response import CreatableTopicResult
from kio.schema.delete_topics.v6 import DeleteTopicsRequest
from kio.schema.delete_topics.v6 import DeleteTopicsResponse
from kio.schema.delete_topics.v6.request import DeleteTopicState
from kio.schema.delete_topics.v6.response import DeletableTopicResult
from kio.schema.metadata.v5 import request as metadata_v5_request
from kio.schema.metadata.v5 import response as metadata_v5_response
from kio.schema.metadata.v12 import request as metadata_v12_request
from kio.schema.metadata.v12 import response as metadata_v12_response
from kio.schema.types import BrokerId
from kio.schema.types import TopicName
from kio.serial import entity_reader
from kio.serial import entity_writer
from kio.serial.readers import read_int32
from kio.serial.writers import Writable
from kio.serial.writers import write_int32
from kio.static.constants import ErrorCode
from kio.static.constants import uuid_zero
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.protocol import Entity
from kio.static.protocol import Payload


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
            kio.schema.request_header.v1.header.RequestHeader
            | kio.schema.request_header.v2.header.RequestHeader
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
    write_int32(stream, i32(buffer.tell()))

    # Write message to connection stream.
    buffer.seek(0)
    stream.write(buffer.getvalue())

    # Draining the stream to make sure full message is sent.
    await stream.drain()


class CorrelationIdMismatch(RuntimeError):
    ...


async def read_response_bytes(stream: StreamReader) -> io.BytesIO:
    response_length_bytes = await stream.read(4)
    response_length = read_int32(io.BytesIO(response_length_bytes))
    return io.BytesIO(await stream.read(response_length))


R = TypeVar("R", bound=Payload)


def parse_response(
    buffer: io.BytesIO,
    response_type: type[R],
    correlation_id: i32,
) -> R:
    header_schema: Any = response_type.__header_schema__
    read_header = entity_reader(header_schema)
    header = read_header(buffer)

    if header.correlation_id != correlation_id:
        raise CorrelationIdMismatch

    read_payload = entity_reader(response_type)
    return read_payload(buffer)


async def make_request(
    request: Payload,
    response_type: type[R],
) -> R:
    correlation_id = i32(secrets.randbelow(i32.__high__ + 1))  # type: ignore[operator]
    stream_reader, stream_writer = await asyncio.open_connection(
        host="127.0.0.1",
        port=9092,
    )

    # We use asynchronous facilities to send the request and read the raw response into
    # a BytesIO buffer.
    with closing(stream_writer):
        async with asyncio.timeout(1):
            await send(stream_writer, request, correlation_id)
            response = await read_response_bytes(stream_reader)

    # After this point, the connection is closed, and we're making synchronously reading
    # the response from the in-memory buffer.
    with response as open_message_buffer:
        return parse_response(open_message_buffer, response_type, correlation_id)


async def test_roundtrip_api_versions_v3() -> None:
    response = await make_request(
        request=api_versions_v3_request.ApiVersionsRequest(
            client_software_name="foo123",
            client_software_version="foo123",
        ),
        response_type=api_versions_v3_response.ApiVersionsResponse,
    )
    ApiVersion = api_versions_v3_response.ApiVersion
    assert response == api_versions_v3_response.ApiVersionsResponse(
        error_code=ErrorCode.none,
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
        error_code=ErrorCode.none,
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
            topics=(DeleteTopicState(name=topic_name, topic_id=uuid_zero),),
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
        ),
    )

    # The previous deletion call should guarantee this call succeeds.
    create_topics_response = await create_topic(topic_name)
    assert create_topics_response == CreateTopicsResponse(
        throttle_time_ms=i32(0),
        topics=(
            CreatableTopicResult(
                name=topic_name,
                topic_id=mock.ANY,
                error_code=ErrorCode.none,
                error_message=None,
                num_partitions=i32(3),
                replication_factor=i16(1),
                configs=mock.ANY,
            ),
        ),
    )
    (created_topic,) = create_topics_response.topics

    # The previous creation call should guarantee this call contains the topic.
    response_v12 = await metadata_v12()
    assert response_v12 == metadata_v12_response.MetadataResponse(
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
                error_code=ErrorCode.none,
                name=created_topic.name,
                topic_id=created_topic.topic_id,
                partitions=mock.ANY,
            ),
        ),
    )

    # Test also with a legacy format API version, i.e. non-flexible.
    response_v5 = await metadata_v5()
    assert response_v5 == metadata_v5_response.MetadataResponse(
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
                error_code=ErrorCode.none,
                name=created_topic.name,
                partitions=mock.ANY,
            ),
        ),
        controller_id=BrokerId(1),
        cluster_id=mock.ANY,
    )
