from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.share_acknowledge.v0.response import LeaderIdAndEpoch
from kio.schema.share_acknowledge.v0.response import NodeEndpoint
from kio.schema.share_acknowledge.v0.response import PartitionData
from kio.schema.share_acknowledge.v0.response import ShareAcknowledgeResponse
from kio.schema.share_acknowledge.v0.response import ShareAcknowledgeTopicResponse
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


read_share_acknowledge_topic_response: Final = entity_reader(
    ShareAcknowledgeTopicResponse
)


@pytest.mark.roundtrip
@given(from_type(ShareAcknowledgeTopicResponse))
def test_share_acknowledge_topic_response_roundtrip(
    instance: ShareAcknowledgeTopicResponse,
) -> None:
    writer = entity_writer(ShareAcknowledgeTopicResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_share_acknowledge_topic_response(buffer)
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


read_share_acknowledge_response: Final = entity_reader(ShareAcknowledgeResponse)


@pytest.mark.roundtrip
@given(from_type(ShareAcknowledgeResponse))
def test_share_acknowledge_response_roundtrip(
    instance: ShareAcknowledgeResponse,
) -> None:
    writer = entity_writer(ShareAcknowledgeResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_share_acknowledge_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(ShareAcknowledgeResponse))
def test_share_acknowledge_response_java(
    instance: ShareAcknowledgeResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
