from __future__ import annotations

from typing import Final

import pytest
from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.stop_replica.v0.request import StopReplicaPartitionV0
from kio.schema.stop_replica.v0.request import StopReplicaRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_stop_replica_partition_v0: Final = entity_reader(StopReplicaPartitionV0)


@pytest.mark.roundtrip
@given(from_type(StopReplicaPartitionV0))
@settings(max_examples=1)
def test_stop_replica_partition_v0_roundtrip(instance: StopReplicaPartitionV0) -> None:
    writer = entity_writer(StopReplicaPartitionV0)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_stop_replica_partition_v0(buffer)
    assert instance == result


read_stop_replica_request: Final = entity_reader(StopReplicaRequest)


@pytest.mark.roundtrip
@given(from_type(StopReplicaRequest))
@settings(max_examples=1)
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
