from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.offset_fetch.v4.response import OffsetFetchResponse
from kio.schema.offset_fetch.v4.response import OffsetFetchResponsePartition
from kio.schema.offset_fetch.v4.response import OffsetFetchResponseTopic
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_offset_fetch_response_partition: Final = entity_reader(
    OffsetFetchResponsePartition
)


@pytest.mark.roundtrip
@given(from_type(OffsetFetchResponsePartition))
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


@pytest.mark.roundtrip
@given(from_type(OffsetFetchResponseTopic))
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
