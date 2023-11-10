from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.offset_for_leader_epoch.v1.request import OffsetForLeaderEpochRequest
from kio.schema.offset_for_leader_epoch.v1.request import OffsetForLeaderPartition
from kio.schema.offset_for_leader_epoch.v1.request import OffsetForLeaderTopic
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_offset_for_leader_partition: Final = entity_reader(OffsetForLeaderPartition)


@given(from_type(OffsetForLeaderPartition))
@settings(max_examples=1)
def test_offset_for_leader_partition_roundtrip(
    instance: OffsetForLeaderPartition,
) -> None:
    writer = entity_writer(OffsetForLeaderPartition)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_offset_for_leader_partition(buffer)
    assert instance == result


read_offset_for_leader_topic: Final = entity_reader(OffsetForLeaderTopic)


@given(from_type(OffsetForLeaderTopic))
@settings(max_examples=1)
def test_offset_for_leader_topic_roundtrip(instance: OffsetForLeaderTopic) -> None:
    writer = entity_writer(OffsetForLeaderTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_offset_for_leader_topic(buffer)
    assert instance == result


read_offset_for_leader_epoch_request: Final = entity_reader(OffsetForLeaderEpochRequest)


@given(from_type(OffsetForLeaderEpochRequest))
@settings(max_examples=1)
def test_offset_for_leader_epoch_request_roundtrip(
    instance: OffsetForLeaderEpochRequest,
) -> None:
    writer = entity_writer(OffsetForLeaderEpochRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_offset_for_leader_epoch_request(buffer)
    assert instance == result


@given(instance=from_type(OffsetForLeaderEpochRequest))
def test_offset_for_leader_epoch_request_java(
    instance: OffsetForLeaderEpochRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
