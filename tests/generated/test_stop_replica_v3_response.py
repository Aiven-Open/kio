from __future__ import annotations

from typing import Final

import pytest
from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.stop_replica.v3.response import StopReplicaPartitionError
from kio.schema.stop_replica.v3.response import StopReplicaResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_stop_replica_partition_error: Final = entity_reader(StopReplicaPartitionError)


@pytest.mark.roundtrip
@given(from_type(StopReplicaPartitionError))
@settings(max_examples=1)
def test_stop_replica_partition_error_roundtrip(
    instance: StopReplicaPartitionError,
) -> None:
    writer = entity_writer(StopReplicaPartitionError)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_stop_replica_partition_error(buffer)
    assert instance == result


read_stop_replica_response: Final = entity_reader(StopReplicaResponse)


@pytest.mark.roundtrip
@given(from_type(StopReplicaResponse))
@settings(max_examples=1)
def test_stop_replica_response_roundtrip(instance: StopReplicaResponse) -> None:
    writer = entity_writer(StopReplicaResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_stop_replica_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(StopReplicaResponse))
def test_stop_replica_response_java(
    instance: StopReplicaResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
