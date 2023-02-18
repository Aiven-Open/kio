from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.offset_for_leader_epoch.v2.request import OffsetForLeaderPartition
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(OffsetForLeaderPartition))
@settings(max_examples=1)
def test_offset_for_leader_partition_roundtrip(
    instance: OffsetForLeaderPartition,
) -> None:
    writer = entity_writer(OffsetForLeaderPartition)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(OffsetForLeaderPartition))
    assert instance == result


from kio.schema.offset_for_leader_epoch.v2.request import OffsetForLeaderTopic


@given(from_type(OffsetForLeaderTopic))
@settings(max_examples=1)
def test_offset_for_leader_topic_roundtrip(instance: OffsetForLeaderTopic) -> None:
    writer = entity_writer(OffsetForLeaderTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(OffsetForLeaderTopic))
    assert instance == result


from kio.schema.offset_for_leader_epoch.v2.request import OffsetForLeaderEpochRequest


@given(from_type(OffsetForLeaderEpochRequest))
@settings(max_examples=1)
def test_offset_for_leader_epoch_request_roundtrip(
    instance: OffsetForLeaderEpochRequest,
) -> None:
    writer = entity_writer(OffsetForLeaderEpochRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(OffsetForLeaderEpochRequest))
    assert instance == result
