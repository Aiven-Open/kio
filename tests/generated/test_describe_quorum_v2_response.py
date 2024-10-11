from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.describe_quorum.v2.response import DescribeQuorumResponse
from kio.schema.describe_quorum.v2.response import Listener
from kio.schema.describe_quorum.v2.response import Node
from kio.schema.describe_quorum.v2.response import PartitionData
from kio.schema.describe_quorum.v2.response import ReplicaState
from kio.schema.describe_quorum.v2.response import TopicData
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_replica_state: Final = entity_reader(ReplicaState)


@pytest.mark.roundtrip
@given(from_type(ReplicaState))
def test_replica_state_roundtrip(instance: ReplicaState) -> None:
    writer = entity_writer(ReplicaState)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_replica_state(buffer)
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


read_listener: Final = entity_reader(Listener)


@pytest.mark.roundtrip
@given(from_type(Listener))
def test_listener_roundtrip(instance: Listener) -> None:
    writer = entity_writer(Listener)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_listener(buffer)
    assert instance == result


read_node: Final = entity_reader(Node)


@pytest.mark.roundtrip
@given(from_type(Node))
def test_node_roundtrip(instance: Node) -> None:
    writer = entity_writer(Node)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_node(buffer)
    assert instance == result


read_describe_quorum_response: Final = entity_reader(DescribeQuorumResponse)


@pytest.mark.roundtrip
@given(from_type(DescribeQuorumResponse))
def test_describe_quorum_response_roundtrip(instance: DescribeQuorumResponse) -> None:
    writer = entity_writer(DescribeQuorumResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_describe_quorum_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(DescribeQuorumResponse))
def test_describe_quorum_response_java(
    instance: DescribeQuorumResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
