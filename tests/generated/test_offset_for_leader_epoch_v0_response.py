from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.offset_for_leader_epoch.v0.response import EpochEndOffset
from kio.schema.offset_for_leader_epoch.v0.response import OffsetForLeaderEpochResponse
from kio.schema.offset_for_leader_epoch.v0.response import OffsetForLeaderTopicResult
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import setup_buffer

read_epoch_end_offset: Final = entity_reader(EpochEndOffset)


@given(from_type(EpochEndOffset))
@settings(max_examples=1)
def test_epoch_end_offset_roundtrip(instance: EpochEndOffset) -> None:
    writer = entity_writer(EpochEndOffset)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_epoch_end_offset(buffer)
    assert instance == result


read_offset_for_leader_topic_result: Final = entity_reader(OffsetForLeaderTopicResult)


@given(from_type(OffsetForLeaderTopicResult))
@settings(max_examples=1)
def test_offset_for_leader_topic_result_roundtrip(
    instance: OffsetForLeaderTopicResult,
) -> None:
    writer = entity_writer(OffsetForLeaderTopicResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_offset_for_leader_topic_result(buffer)
    assert instance == result


read_offset_for_leader_epoch_response: Final = entity_reader(
    OffsetForLeaderEpochResponse
)


@given(from_type(OffsetForLeaderEpochResponse))
@settings(max_examples=1)
def test_offset_for_leader_epoch_response_roundtrip(
    instance: OffsetForLeaderEpochResponse,
) -> None:
    writer = entity_writer(OffsetForLeaderEpochResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_offset_for_leader_epoch_response(buffer)
    assert instance == result
