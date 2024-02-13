from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.stop_replica.v3.request import StopReplicaPartitionState
from kio.schema.stop_replica.v3.request import StopReplicaRequest
from kio.schema.stop_replica.v3.request import StopReplicaTopicState
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_stop_replica_partition_state: Final = entity_reader(StopReplicaPartitionState)


@pytest.mark.roundtrip
@given(from_type(StopReplicaPartitionState))
def test_stop_replica_partition_state_roundtrip(
    instance: StopReplicaPartitionState,
) -> None:
    writer = entity_writer(StopReplicaPartitionState)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_stop_replica_partition_state(buffer)
    assert instance == result


read_stop_replica_topic_state: Final = entity_reader(StopReplicaTopicState)


@pytest.mark.roundtrip
@given(from_type(StopReplicaTopicState))
def test_stop_replica_topic_state_roundtrip(instance: StopReplicaTopicState) -> None:
    writer = entity_writer(StopReplicaTopicState)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_stop_replica_topic_state(buffer)
    assert instance == result


read_stop_replica_request: Final = entity_reader(StopReplicaRequest)


@pytest.mark.roundtrip
@given(from_type(StopReplicaRequest))
def test_stop_replica_request_roundtrip(instance: StopReplicaRequest) -> None:
    writer = entity_writer(StopReplicaRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_stop_replica_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(StopReplicaRequest))
def test_stop_replica_request_java(
    instance: StopReplicaRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
