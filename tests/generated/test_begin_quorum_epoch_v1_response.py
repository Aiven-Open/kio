from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.begin_quorum_epoch.v1.response import BeginQuorumEpochResponse
from kio.schema.begin_quorum_epoch.v1.response import NodeEndpoint
from kio.schema.begin_quorum_epoch.v1.response import PartitionData
from kio.schema.begin_quorum_epoch.v1.response import TopicData
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

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


read_topic_data: Final = entity_reader(TopicData)


@pytest.mark.roundtrip
@given(from_type(TopicData))
def test_topic_data_roundtrip(instance: TopicData) -> None:
    writer = entity_writer(TopicData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_topic_data(buffer)
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


read_begin_quorum_epoch_response: Final = entity_reader(BeginQuorumEpochResponse)


@pytest.mark.roundtrip
@given(from_type(BeginQuorumEpochResponse))
def test_begin_quorum_epoch_response_roundtrip(
    instance: BeginQuorumEpochResponse,
) -> None:
    writer = entity_writer(BeginQuorumEpochResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_begin_quorum_epoch_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(BeginQuorumEpochResponse))
def test_begin_quorum_epoch_response_java(
    instance: BeginQuorumEpochResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
