from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.fetch_snapshot.v0.request import FetchSnapshotRequest
from kio.schema.fetch_snapshot.v0.request import PartitionSnapshot
from kio.schema.fetch_snapshot.v0.request import SnapshotId
from kio.schema.fetch_snapshot.v0.request import TopicSnapshot
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_snapshot_id: Final = entity_reader(SnapshotId)


@pytest.mark.roundtrip
@given(from_type(SnapshotId))
def test_snapshot_id_roundtrip(instance: SnapshotId) -> None:
    writer = entity_writer(SnapshotId)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_snapshot_id(buffer)
    assert instance == result


read_partition_snapshot: Final = entity_reader(PartitionSnapshot)


@pytest.mark.roundtrip
@given(from_type(PartitionSnapshot))
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
def test_topic_snapshot_roundtrip(instance: TopicSnapshot) -> None:
    writer = entity_writer(TopicSnapshot)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_topic_snapshot(buffer)
    assert instance == result


read_fetch_snapshot_request: Final = entity_reader(FetchSnapshotRequest)


@pytest.mark.roundtrip
@given(from_type(FetchSnapshotRequest))
def test_fetch_snapshot_request_roundtrip(instance: FetchSnapshotRequest) -> None:
    writer = entity_writer(FetchSnapshotRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_fetch_snapshot_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(FetchSnapshotRequest))
def test_fetch_snapshot_request_java(
    instance: FetchSnapshotRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
