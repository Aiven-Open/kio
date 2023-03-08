from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.produce.v7.response import PartitionProduceResponse
from kio.schema.produce.v7.response import ProduceResponse
from kio.schema.produce.v7.response import TopicProduceResponse
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(PartitionProduceResponse))
@settings(max_examples=1)
def test_partition_produce_response_roundtrip(
    instance: PartitionProduceResponse,
) -> None:
    writer = entity_writer(PartitionProduceResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(PartitionProduceResponse))
    assert instance == result


@given(from_type(TopicProduceResponse))
@settings(max_examples=1)
def test_topic_produce_response_roundtrip(instance: TopicProduceResponse) -> None:
    writer = entity_writer(TopicProduceResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(TopicProduceResponse))
    assert instance == result


@given(from_type(ProduceResponse))
@settings(max_examples=1)
def test_produce_response_roundtrip(instance: ProduceResponse) -> None:
    writer = entity_writer(ProduceResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(ProduceResponse))
    assert instance == result
