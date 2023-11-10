from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.offset_fetch.v2.request import OffsetFetchRequest
from kio.schema.offset_fetch.v2.request import OffsetFetchRequestTopic
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_offset_fetch_request_topic: Final = entity_reader(OffsetFetchRequestTopic)


@given(from_type(OffsetFetchRequestTopic))
@settings(max_examples=1)
def test_offset_fetch_request_topic_roundtrip(
    instance: OffsetFetchRequestTopic,
) -> None:
    writer = entity_writer(OffsetFetchRequestTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_offset_fetch_request_topic(buffer)
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


@given(instance=from_type(OffsetFetchRequest))
def test_offset_fetch_request_java(
    instance: OffsetFetchRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
