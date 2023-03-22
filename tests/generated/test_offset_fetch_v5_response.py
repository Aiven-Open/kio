from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.offset_fetch.v5.response import OffsetFetchResponse
from kio.schema.offset_fetch.v5.response import OffsetFetchResponsePartition
from kio.schema.offset_fetch.v5.response import OffsetFetchResponseTopic
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import setup_buffer

read_offset_fetch_response_partition: Final = entity_reader(
    OffsetFetchResponsePartition
)


@given(from_type(OffsetFetchResponsePartition))
@settings(max_examples=1)
def test_offset_fetch_response_partition_roundtrip(
    instance: OffsetFetchResponsePartition,
) -> None:
    writer = entity_writer(OffsetFetchResponsePartition)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_offset_fetch_response_partition(buffer)
    assert instance == result


read_offset_fetch_response_topic: Final = entity_reader(OffsetFetchResponseTopic)


@given(from_type(OffsetFetchResponseTopic))
@settings(max_examples=1)
def test_offset_fetch_response_topic_roundtrip(
    instance: OffsetFetchResponseTopic,
) -> None:
    writer = entity_writer(OffsetFetchResponseTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_offset_fetch_response_topic(buffer)
    assert instance == result


read_offset_fetch_response: Final = entity_reader(OffsetFetchResponse)


@given(from_type(OffsetFetchResponse))
@settings(max_examples=1)
def test_offset_fetch_response_roundtrip(instance: OffsetFetchResponse) -> None:
    writer = entity_writer(OffsetFetchResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_offset_fetch_response(buffer)
    assert instance == result
