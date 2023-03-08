from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.end_quorum_epoch.v0.response import EndQuorumEpochResponse
from kio.schema.end_quorum_epoch.v0.response import PartitionData
from kio.schema.end_quorum_epoch.v0.response import TopicData
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


@given(from_type(TopicData))
@settings(max_examples=1)
def test_topic_data_roundtrip(instance: TopicData) -> None:
    writer = entity_writer(TopicData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(TopicData))
    assert instance == result


@given(from_type(EndQuorumEpochResponse))
@settings(max_examples=1)
def test_end_quorum_epoch_response_roundtrip(instance: EndQuorumEpochResponse) -> None:
    writer = entity_writer(EndQuorumEpochResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(EndQuorumEpochResponse))
    assert instance == result
