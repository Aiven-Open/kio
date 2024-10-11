from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.share_fetch.v0.response import AcquiredRecords
from kio.schema.share_fetch.v0.response import LeaderIdAndEpoch
from kio.schema.share_fetch.v0.response import NodeEndpoint
from kio.schema.share_fetch.v0.response import PartitionData
from kio.schema.share_fetch.v0.response import ShareFetchableTopicResponse
from kio.schema.share_fetch.v0.response import ShareFetchResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_leader_id_and_epoch: Final = entity_reader(LeaderIdAndEpoch)


@pytest.mark.roundtrip
@given(from_type(LeaderIdAndEpoch))
def test_leader_id_and_epoch_roundtrip(instance: LeaderIdAndEpoch) -> None:
    writer = entity_writer(LeaderIdAndEpoch)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_leader_id_and_epoch(buffer)
    assert instance == result


read_acquired_records: Final = entity_reader(AcquiredRecords)


@pytest.mark.roundtrip
@given(from_type(AcquiredRecords))
def test_acquired_records_roundtrip(instance: AcquiredRecords) -> None:
    writer = entity_writer(AcquiredRecords)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_acquired_records(buffer)
    assert instance == result


read_partition_data: Final = entity_reader(PartitionData)


@pytest.mark.roundtrip
@given(from_type(PartitionData))
def test_partition_data_roundtrip(instance: PartitionData) -> None:
    writer = entity_writer(PartitionData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_partition_data(buffer)
    assert instance == result


read_share_fetchable_topic_response: Final = entity_reader(ShareFetchableTopicResponse)


@pytest.mark.roundtrip
@given(from_type(ShareFetchableTopicResponse))
def test_share_fetchable_topic_response_roundtrip(
    instance: ShareFetchableTopicResponse,
) -> None:
    writer = entity_writer(ShareFetchableTopicResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_share_fetchable_topic_response(buffer)
    assert instance == result


read_node_endpoint: Final = entity_reader(NodeEndpoint)


@pytest.mark.roundtrip
@given(from_type(NodeEndpoint))
def test_node_endpoint_roundtrip(instance: NodeEndpoint) -> None:
    writer = entity_writer(NodeEndpoint)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_node_endpoint(buffer)
    assert instance == result


read_share_fetch_response: Final = entity_reader(ShareFetchResponse)


@pytest.mark.roundtrip
@given(from_type(ShareFetchResponse))
def test_share_fetch_response_roundtrip(instance: ShareFetchResponse) -> None:
    writer = entity_writer(ShareFetchResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_share_fetch_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(ShareFetchResponse))
def test_share_fetch_response_java(
    instance: ShareFetchResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
