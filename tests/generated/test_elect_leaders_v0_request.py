from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.elect_leaders.v0.request import TopicPartitions
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(TopicPartitions))
@settings(max_examples=1)
def test_topic_partitions_roundtrip(instance: TopicPartitions) -> None:
    writer = entity_writer(TopicPartitions)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(TopicPartitions))
    assert instance == result


from kio.schema.elect_leaders.v0.request import ElectLeadersRequest


@given(from_type(ElectLeadersRequest))
@settings(max_examples=1)
def test_elect_leaders_request_roundtrip(instance: ElectLeadersRequest) -> None:
    writer = entity_writer(ElectLeadersRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(ElectLeadersRequest))
    assert instance == result
