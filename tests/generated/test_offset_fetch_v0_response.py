from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.offset_fetch.v0.response import OffsetFetchResponse
from kio.schema.offset_fetch.v0.response import OffsetFetchResponsePartition
from kio.schema.offset_fetch.v0.response import OffsetFetchResponseTopic
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(OffsetFetchResponsePartition))
@settings(max_examples=1)
def test_offset_fetch_response_partition_roundtrip(
    instance: OffsetFetchResponsePartition,
) -> None:
    writer = entity_writer(OffsetFetchResponsePartition)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(OffsetFetchResponsePartition))
    assert instance == result


@given(from_type(OffsetFetchResponseTopic))
@settings(max_examples=1)
def test_offset_fetch_response_topic_roundtrip(
    instance: OffsetFetchResponseTopic,
) -> None:
    writer = entity_writer(OffsetFetchResponseTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(OffsetFetchResponseTopic))
    assert instance == result


@given(from_type(OffsetFetchResponse))
@settings(max_examples=1)
def test_offset_fetch_response_roundtrip(instance: OffsetFetchResponse) -> None:
    writer = entity_writer(OffsetFetchResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(OffsetFetchResponse))
    assert instance == result
