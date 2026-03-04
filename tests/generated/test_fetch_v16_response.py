from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.fetch.v16.response import AbortedTransaction
from kio.schema.fetch.v16.response import EpochEndOffset
from kio.schema.fetch.v16.response import FetchableTopicResponse
from kio.schema.fetch.v16.response import FetchResponse
from kio.schema.fetch.v16.response import LeaderIdAndEpoch
from kio.schema.fetch.v16.response import NodeEndpoint
from kio.schema.fetch.v16.response import PartitionData
from kio.schema.fetch.v16.response import SnapshotId
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_epoch_end_offset: Final = entity_reader(EpochEndOffset)


@pytest.mark.roundtrip
@given(from_type(EpochEndOffset))
def test_epoch_end_offset_roundtrip(instance: EpochEndOffset) -> None:
    writer = entity_writer(EpochEndOffset)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_epoch_end_offset(
            buffer.getvalue(),
            0,
        )

    assert instance == result


read_leader_id_and_epoch: Final = entity_reader(LeaderIdAndEpoch)


@pytest.mark.roundtrip
@given(from_type(LeaderIdAndEpoch))
def test_leader_id_and_epoch_roundtrip(instance: LeaderIdAndEpoch) -> None:
    writer = entity_writer(LeaderIdAndEpoch)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_leader_id_and_epoch(
            buffer.getvalue(),
            0,
        )

    assert instance == result


read_snapshot_id: Final = entity_reader(SnapshotId)


@pytest.mark.roundtrip
@given(from_type(SnapshotId))
def test_snapshot_id_roundtrip(instance: SnapshotId) -> None:
    writer = entity_writer(SnapshotId)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_snapshot_id(
            buffer.getvalue(),
            0,
        )

    assert instance == result


read_aborted_transaction: Final = entity_reader(AbortedTransaction)


@pytest.mark.roundtrip
@given(from_type(AbortedTransaction))
def test_aborted_transaction_roundtrip(instance: AbortedTransaction) -> None:
    writer = entity_writer(AbortedTransaction)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_aborted_transaction(
            buffer.getvalue(),
            0,
        )

    assert instance == result


read_partition_data: Final = entity_reader(PartitionData)


@pytest.mark.roundtrip
@given(from_type(PartitionData))
def test_partition_data_roundtrip(instance: PartitionData) -> None:
    writer = entity_writer(PartitionData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_partition_data(
            buffer.getvalue(),
            0,
        )

    assert instance == result


read_fetchable_topic_response: Final = entity_reader(FetchableTopicResponse)


@pytest.mark.roundtrip
@given(from_type(FetchableTopicResponse))
def test_fetchable_topic_response_roundtrip(instance: FetchableTopicResponse) -> None:
    writer = entity_writer(FetchableTopicResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_fetchable_topic_response(
            buffer.getvalue(),
            0,
        )

    assert instance == result


read_node_endpoint: Final = entity_reader(NodeEndpoint)


@pytest.mark.roundtrip
@given(from_type(NodeEndpoint))
def test_node_endpoint_roundtrip(instance: NodeEndpoint) -> None:
    writer = entity_writer(NodeEndpoint)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_node_endpoint(
            buffer.getvalue(),
            0,
        )

    assert instance == result


read_fetch_response: Final = entity_reader(FetchResponse)


@pytest.mark.roundtrip
@given(from_type(FetchResponse))
def test_fetch_response_roundtrip(instance: FetchResponse) -> None:
    writer = entity_writer(FetchResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_fetch_response(
            buffer.getvalue(),
            0,
        )

    assert instance == result


@pytest.mark.java
@given(instance=from_type(FetchResponse))
def test_fetch_response_java(instance: FetchResponse, java_tester: JavaTester) -> None:
    java_tester.test(instance)
