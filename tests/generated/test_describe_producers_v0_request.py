from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.describe_producers.v0.request import DescribeProducersRequest
from kio.schema.describe_producers.v0.request import TopicRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import setup_buffer

read_topic_request: Final = entity_reader(TopicRequest)


@given(from_type(TopicRequest))
@settings(max_examples=1)
def test_topic_request_roundtrip(instance: TopicRequest) -> None:
    writer = entity_writer(TopicRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_topic_request(buffer)
    assert instance == result


read_describe_producers_request: Final = entity_reader(DescribeProducersRequest)


@given(from_type(DescribeProducersRequest))
@settings(max_examples=1)
def test_describe_producers_request_roundtrip(
    instance: DescribeProducersRequest,
) -> None:
    writer = entity_writer(DescribeProducersRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_describe_producers_request(buffer)
    assert instance == result
