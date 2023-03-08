from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.describe_producers.v0.request import DescribeProducersRequest
from kio.schema.describe_producers.v0.request import TopicRequest
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(TopicRequest))
@settings(max_examples=1)
def test_topic_request_roundtrip(instance: TopicRequest) -> None:
    writer = entity_writer(TopicRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(TopicRequest))
    assert instance == result


@given(from_type(DescribeProducersRequest))
@settings(max_examples=1)
def test_describe_producers_request_roundtrip(
    instance: DescribeProducersRequest,
) -> None:
    writer = entity_writer(DescribeProducersRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DescribeProducersRequest))
    assert instance == result
