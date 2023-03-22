from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.offset_fetch.v8.request import OffsetFetchRequest
from kio.schema.offset_fetch.v8.request import OffsetFetchRequestGroup
from kio.schema.offset_fetch.v8.request import OffsetFetchRequestTopics
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import setup_buffer

read_offset_fetch_request_topics: Final = entity_reader(OffsetFetchRequestTopics)


@given(from_type(OffsetFetchRequestTopics))
@settings(max_examples=1)
def test_offset_fetch_request_topics_roundtrip(
    instance: OffsetFetchRequestTopics,
) -> None:
    writer = entity_writer(OffsetFetchRequestTopics)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_offset_fetch_request_topics(buffer)
    assert instance == result


read_offset_fetch_request_group: Final = entity_reader(OffsetFetchRequestGroup)


@given(from_type(OffsetFetchRequestGroup))
@settings(max_examples=1)
def test_offset_fetch_request_group_roundtrip(
    instance: OffsetFetchRequestGroup,
) -> None:
    writer = entity_writer(OffsetFetchRequestGroup)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_offset_fetch_request_group(buffer)
    assert instance == result


read_offset_fetch_request: Final = entity_reader(OffsetFetchRequest)


@given(from_type(OffsetFetchRequest))
@settings(max_examples=1)
def test_offset_fetch_request_roundtrip(instance: OffsetFetchRequest) -> None:
    writer = entity_writer(OffsetFetchRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_offset_fetch_request(buffer)
    assert instance == result
