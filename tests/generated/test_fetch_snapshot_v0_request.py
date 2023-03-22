from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.fetch_snapshot.v0.request import FetchSnapshotRequest
from kio.schema.fetch_snapshot.v0.request import PartitionSnapshot
from kio.schema.fetch_snapshot.v0.request import SnapshotId
from kio.schema.fetch_snapshot.v0.request import TopicSnapshot
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import setup_buffer

read_snapshot_id: Final = entity_reader(SnapshotId)


@given(from_type(SnapshotId))
@settings(max_examples=1)
def test_snapshot_id_roundtrip(instance: SnapshotId) -> None:
    writer = entity_writer(SnapshotId)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_snapshot_id(buffer)
    assert instance == result


read_partition_snapshot: Final = entity_reader(PartitionSnapshot)


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


@given(from_type(TopicSnapshot))
@settings(max_examples=1)
def test_topic_snapshot_roundtrip(instance: TopicSnapshot) -> None:
    writer = entity_writer(TopicSnapshot)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_topic_snapshot(buffer)
    assert instance == result


read_fetch_snapshot_request: Final = entity_reader(FetchSnapshotRequest)


@given(from_type(FetchSnapshotRequest))
@settings(max_examples=1)
def test_fetch_snapshot_request_roundtrip(instance: FetchSnapshotRequest) -> None:
    writer = entity_writer(FetchSnapshotRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_fetch_snapshot_request(buffer)
    assert instance == result
