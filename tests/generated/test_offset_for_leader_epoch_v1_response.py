from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.offset_for_leader_epoch.v1.response import EpochEndOffset
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(EpochEndOffset))
@settings(max_examples=1)
def test_epoch_end_offset_roundtrip(instance: EpochEndOffset) -> None:
    writer = entity_writer(EpochEndOffset)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(EpochEndOffset))
    assert instance == result


from kio.schema.offset_for_leader_epoch.v1.response import OffsetForLeaderTopicResult


@given(from_type(OffsetForLeaderTopicResult))
@settings(max_examples=1)
def test_offset_for_leader_topic_result_roundtrip(
    instance: OffsetForLeaderTopicResult,
) -> None:
    writer = entity_writer(OffsetForLeaderTopicResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(OffsetForLeaderTopicResult))
    assert instance == result


from kio.schema.offset_for_leader_epoch.v1.response import OffsetForLeaderEpochResponse


@given(from_type(OffsetForLeaderEpochResponse))
@settings(max_examples=1)
def test_offset_for_leader_epoch_response_roundtrip(
    instance: OffsetForLeaderEpochResponse,
) -> None:
    writer = entity_writer(OffsetForLeaderEpochResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(OffsetForLeaderEpochResponse))
    assert instance == result
