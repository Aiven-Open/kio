from __future__ import annotations

from typing import Final

import pytest
from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.fetch_snapshot.v0.response import FetchSnapshotResponse
from kio.schema.fetch_snapshot.v0.response import LeaderIdAndEpoch
from kio.schema.fetch_snapshot.v0.response import PartitionSnapshot
from kio.schema.fetch_snapshot.v0.response import SnapshotId
from kio.schema.fetch_snapshot.v0.response import TopicSnapshot
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import setup_buffer

read_snapshot_id: Final = entity_reader(SnapshotId)


@pytest.mark.roundtrip
@given(from_type(SnapshotId))
@settings(max_examples=1)
def test_snapshot_id_roundtrip(instance: SnapshotId) -> None:
    writer = entity_writer(SnapshotId)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_snapshot_id(buffer)
    assert instance == result


read_leader_id_and_epoch: Final = entity_reader(LeaderIdAndEpoch)


@pytest.mark.roundtrip
@given(from_type(LeaderIdAndEpoch))
@settings(max_examples=1)
def test_leader_id_and_epoch_roundtrip(instance: LeaderIdAndEpoch) -> None:
    writer = entity_writer(LeaderIdAndEpoch)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_leader_id_and_epoch(buffer)
    assert instance == result


read_partition_snapshot: Final = entity_reader(PartitionSnapshot)


@pytest.mark.roundtrip
@given(from_type(PartitionSnapshot))
@settings(max_examples=1)
def test_partition_snapshot_roundtrip(instance: PartitionSnapshot) -> None:
    writer = entity_writer(PartitionSnapshot)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_partition_snapshot(buffer)
    assert instance == result


read_topic_snapshot: Final = entity_reader(TopicSnapshot)


@pytest.mark.roundtrip
@given(from_type(TopicSnapshot))
@settings(max_examples=1)
def test_topic_snapshot_roundtrip(instance: TopicSnapshot) -> None:
    writer = entity_writer(TopicSnapshot)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_topic_snapshot(buffer)
    assert instance == result


read_fetch_snapshot_response: Final = entity_reader(FetchSnapshotResponse)


@pytest.mark.roundtrip
@given(from_type(FetchSnapshotResponse))
@settings(max_examples=1)
def test_fetch_snapshot_response_roundtrip(instance: FetchSnapshotResponse) -> None:
    writer = entity_writer(FetchSnapshotResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_fetch_snapshot_response(buffer)
    assert instance == result
