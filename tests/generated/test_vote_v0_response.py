from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.vote.v0.response import PartitionData
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(PartitionData))
@settings(max_examples=1)
def test_partition_data_roundtrip(instance: PartitionData) -> None:
    writer = entity_writer(PartitionData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(PartitionData))
    assert instance == result


from kio.schema.vote.v0.response import TopicData


@given(from_type(TopicData))
@settings(max_examples=1)
def test_topic_data_roundtrip(instance: TopicData) -> None:
    writer = entity_writer(TopicData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(TopicData))
    assert instance == result


from kio.schema.vote.v0.response import VoteResponse


@given(from_type(VoteResponse))
@settings(max_examples=1)
def test_vote_response_roundtrip(instance: VoteResponse) -> None:
    writer = entity_writer(VoteResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(VoteResponse))
    assert instance == result
