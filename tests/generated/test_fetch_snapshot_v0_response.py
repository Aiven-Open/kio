from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.fetch_snapshot.v0.response import FetchSnapshotResponse
from kio.schema.fetch_snapshot.v0.response import LeaderIdAndEpoch
from kio.schema.fetch_snapshot.v0.response import PartitionSnapshot
from kio.schema.fetch_snapshot.v0.response import SnapshotId
from kio.schema.fetch_snapshot.v0.response import TopicSnapshot
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(SnapshotId))
@settings(max_examples=1)
def test_snapshot_id_roundtrip(instance: SnapshotId) -> None:
    writer = entity_writer(SnapshotId)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(SnapshotId))
    assert instance == result


@given(from_type(LeaderIdAndEpoch))
@settings(max_examples=1)
def test_leader_id_and_epoch_roundtrip(instance: LeaderIdAndEpoch) -> None:
    writer = entity_writer(LeaderIdAndEpoch)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(LeaderIdAndEpoch))
    assert instance == result


@given(from_type(PartitionSnapshot))
@settings(max_examples=1)
def test_partition_snapshot_roundtrip(instance: PartitionSnapshot) -> None:
    writer = entity_writer(PartitionSnapshot)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(PartitionSnapshot))
    assert instance == result


@given(from_type(TopicSnapshot))
@settings(max_examples=1)
def test_topic_snapshot_roundtrip(instance: TopicSnapshot) -> None:
    writer = entity_writer(TopicSnapshot)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(TopicSnapshot))
    assert instance == result


@given(from_type(FetchSnapshotResponse))
@settings(max_examples=1)
def test_fetch_snapshot_response_roundtrip(instance: FetchSnapshotResponse) -> None:
    writer = entity_writer(FetchSnapshotResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(FetchSnapshotResponse))
    assert instance == result
