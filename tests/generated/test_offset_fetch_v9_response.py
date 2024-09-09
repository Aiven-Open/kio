from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.offset_fetch.v9.response import OffsetFetchResponse
from kio.schema.offset_fetch.v9.response import OffsetFetchResponseGroup
from kio.schema.offset_fetch.v9.response import OffsetFetchResponsePartitions
from kio.schema.offset_fetch.v9.response import OffsetFetchResponseTopics
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_offset_fetch_response_partitions: Final = entity_reader(
    OffsetFetchResponsePartitions
)


@pytest.mark.roundtrip
@given(from_type(OffsetFetchResponsePartitions))
def test_offset_fetch_response_partitions_roundtrip(
    instance: OffsetFetchResponsePartitions,
) -> None:
    writer = entity_writer(OffsetFetchResponsePartitions)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_offset_fetch_response_partitions(buffer)
    assert instance == result


read_offset_fetch_response_topics: Final = entity_reader(OffsetFetchResponseTopics)


@pytest.mark.roundtrip
@given(from_type(OffsetFetchResponseTopics))
def test_offset_fetch_response_topics_roundtrip(
    instance: OffsetFetchResponseTopics,
) -> None:
    writer = entity_writer(OffsetFetchResponseTopics)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_offset_fetch_response_topics(buffer)
    assert instance == result


read_offset_fetch_response_group: Final = entity_reader(OffsetFetchResponseGroup)


@pytest.mark.roundtrip
@given(from_type(OffsetFetchResponseGroup))
def test_offset_fetch_response_group_roundtrip(
    instance: OffsetFetchResponseGroup,
) -> None:
    writer = entity_writer(OffsetFetchResponseGroup)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_offset_fetch_response_group(buffer)
    assert instance == result


read_offset_fetch_response: Final = entity_reader(OffsetFetchResponse)


@pytest.mark.roundtrip
@given(from_type(OffsetFetchResponse))
def test_offset_fetch_response_roundtrip(instance: OffsetFetchResponse) -> None:
    writer = entity_writer(OffsetFetchResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_offset_fetch_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(OffsetFetchResponse))
def test_offset_fetch_response_java(
    instance: OffsetFetchResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
