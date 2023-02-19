from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.leader_and_isr.v5.request import LeaderAndIsrPartitionState
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(LeaderAndIsrPartitionState))
@settings(max_examples=1)
def test_leader_and_isr_partition_state_roundtrip(
    instance: LeaderAndIsrPartitionState,
) -> None:
    writer = entity_writer(LeaderAndIsrPartitionState)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(LeaderAndIsrPartitionState))
    assert instance == result


from kio.schema.leader_and_isr.v5.request import LeaderAndIsrTopicState


@given(from_type(LeaderAndIsrTopicState))
@settings(max_examples=1)
def test_leader_and_isr_topic_state_roundtrip(instance: LeaderAndIsrTopicState) -> None:
    writer = entity_writer(LeaderAndIsrTopicState)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(LeaderAndIsrTopicState))
    assert instance == result


from kio.schema.leader_and_isr.v5.request import LeaderAndIsrLiveLeader


@given(from_type(LeaderAndIsrLiveLeader))
@settings(max_examples=1)
def test_leader_and_isr_live_leader_roundtrip(instance: LeaderAndIsrLiveLeader) -> None:
    writer = entity_writer(LeaderAndIsrLiveLeader)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(LeaderAndIsrLiveLeader))
    assert instance == result


from kio.schema.leader_and_isr.v5.request import LeaderAndIsrRequest


@given(from_type(LeaderAndIsrRequest))
@settings(max_examples=1)
def test_leader_and_isr_request_roundtrip(instance: LeaderAndIsrRequest) -> None:
    writer = entity_writer(LeaderAndIsrRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(LeaderAndIsrRequest))
    assert instance == result
