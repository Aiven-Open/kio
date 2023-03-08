from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.offset_fetch.v8.response import OffsetFetchResponse
from kio.schema.offset_fetch.v8.response import OffsetFetchResponseGroup
from kio.schema.offset_fetch.v8.response import OffsetFetchResponsePartitions
from kio.schema.offset_fetch.v8.response import OffsetFetchResponseTopics
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(OffsetFetchResponsePartitions))
@settings(max_examples=1)
def test_offset_fetch_response_partitions_roundtrip(
    instance: OffsetFetchResponsePartitions,
) -> None:
    writer = entity_writer(OffsetFetchResponsePartitions)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(OffsetFetchResponsePartitions))
    assert instance == result


@given(from_type(OffsetFetchResponseTopics))
@settings(max_examples=1)
def test_offset_fetch_response_topics_roundtrip(
    instance: OffsetFetchResponseTopics,
) -> None:
    writer = entity_writer(OffsetFetchResponseTopics)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(OffsetFetchResponseTopics))
    assert instance == result


@given(from_type(OffsetFetchResponseGroup))
@settings(max_examples=1)
def test_offset_fetch_response_group_roundtrip(
    instance: OffsetFetchResponseGroup,
) -> None:
    writer = entity_writer(OffsetFetchResponseGroup)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(OffsetFetchResponseGroup))
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
