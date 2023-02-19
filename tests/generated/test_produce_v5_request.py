from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.produce.v5.request import PartitionProduceData
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(PartitionProduceData))
@settings(max_examples=1)
def test_partition_produce_data_roundtrip(instance: PartitionProduceData) -> None:
    writer = entity_writer(PartitionProduceData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(PartitionProduceData))
    assert instance == result


from kio.schema.produce.v5.request import TopicProduceData


@given(from_type(TopicProduceData))
@settings(max_examples=1)
def test_topic_produce_data_roundtrip(instance: TopicProduceData) -> None:
    writer = entity_writer(TopicProduceData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(TopicProduceData))
    assert instance == result


from kio.schema.produce.v5.request import ProduceRequest


@given(from_type(ProduceRequest))
@settings(max_examples=1)
def test_produce_request_roundtrip(instance: ProduceRequest) -> None:
    writer = entity_writer(ProduceRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(ProduceRequest))
    assert instance == result
