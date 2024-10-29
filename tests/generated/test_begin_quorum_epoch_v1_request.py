from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.begin_quorum_epoch.v1.request import BeginQuorumEpochRequest
from kio.schema.begin_quorum_epoch.v1.request import LeaderEndpoint
from kio.schema.begin_quorum_epoch.v1.request import PartitionData
from kio.schema.begin_quorum_epoch.v1.request import TopicData
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


read_leader_endpoint: Final = entity_reader(LeaderEndpoint)


@pytest.mark.roundtrip
@given(from_type(LeaderEndpoint))
def test_leader_endpoint_roundtrip(instance: LeaderEndpoint) -> None:
    writer = entity_writer(LeaderEndpoint)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_leader_endpoint(buffer)
    assert instance == result


read_begin_quorum_epoch_request: Final = entity_reader(BeginQuorumEpochRequest)


@pytest.mark.roundtrip
@given(from_type(BeginQuorumEpochRequest))
def test_begin_quorum_epoch_request_roundtrip(
    instance: BeginQuorumEpochRequest,
) -> None:
    writer = entity_writer(BeginQuorumEpochRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_begin_quorum_epoch_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(BeginQuorumEpochRequest))
def test_begin_quorum_epoch_request_java(
    instance: BeginQuorumEpochRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)