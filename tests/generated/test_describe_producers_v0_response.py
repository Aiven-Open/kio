from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.describe_producers.v0.response import DescribeProducersResponse
from kio.schema.describe_producers.v0.response import PartitionResponse
from kio.schema.describe_producers.v0.response import ProducerState
from kio.schema.describe_producers.v0.response import TopicResponse
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(ProducerState))
@settings(max_examples=1)
def test_producer_state_roundtrip(instance: ProducerState) -> None:
    writer = entity_writer(ProducerState)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(ProducerState))
    assert instance == result


@given(from_type(PartitionResponse))
@settings(max_examples=1)
def test_partition_response_roundtrip(instance: PartitionResponse) -> None:
    writer = entity_writer(PartitionResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(PartitionResponse))
    assert instance == result


@given(from_type(TopicResponse))
@settings(max_examples=1)
def test_topic_response_roundtrip(instance: TopicResponse) -> None:
    writer = entity_writer(TopicResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(TopicResponse))
    assert instance == result


@given(from_type(DescribeProducersResponse))
@settings(max_examples=1)
def test_describe_producers_response_roundtrip(
    instance: DescribeProducersResponse,
) -> None:
    writer = entity_writer(DescribeProducersResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DescribeProducersResponse))
    assert instance == result
