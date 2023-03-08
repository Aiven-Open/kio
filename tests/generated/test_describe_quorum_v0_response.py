from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.describe_quorum.v0.response import DescribeQuorumResponse
from kio.schema.describe_quorum.v0.response import PartitionData
from kio.schema.describe_quorum.v0.response import ReplicaState
from kio.schema.describe_quorum.v0.response import TopicData
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(ReplicaState))
@settings(max_examples=1)
def test_replica_state_roundtrip(instance: ReplicaState) -> None:
    writer = entity_writer(ReplicaState)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(ReplicaState))
    assert instance == result


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


@given(from_type(DescribeQuorumResponse))
@settings(max_examples=1)
def test_describe_quorum_response_roundtrip(instance: DescribeQuorumResponse) -> None:
    writer = entity_writer(DescribeQuorumResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DescribeQuorumResponse))
    assert instance == result
