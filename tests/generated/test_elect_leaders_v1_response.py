from __future__ import annotations

from typing import Final

import pytest
from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.elect_leaders.v1.response import ElectLeadersResponse
from kio.schema.elect_leaders.v1.response import PartitionResult
from kio.schema.elect_leaders.v1.response import ReplicaElectionResult
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_partition_result: Final = entity_reader(PartitionResult)


@pytest.mark.roundtrip
@given(from_type(PartitionResult))
@settings(max_examples=1)
def test_partition_result_roundtrip(instance: PartitionResult) -> None:
    writer = entity_writer(PartitionResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_partition_result(buffer)
    assert instance == result


read_replica_election_result: Final = entity_reader(ReplicaElectionResult)


@pytest.mark.roundtrip
@given(from_type(ReplicaElectionResult))
@settings(max_examples=1)
def test_replica_election_result_roundtrip(instance: ReplicaElectionResult) -> None:
    writer = entity_writer(ReplicaElectionResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_replica_election_result(buffer)
    assert instance == result


read_elect_leaders_response: Final = entity_reader(ElectLeadersResponse)


@pytest.mark.roundtrip
@given(from_type(ElectLeadersResponse))
@settings(max_examples=1)
def test_elect_leaders_response_roundtrip(instance: ElectLeadersResponse) -> None:
    writer = entity_writer(ElectLeadersResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_elect_leaders_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(ElectLeadersResponse))
def test_elect_leaders_response_java(
    instance: ElectLeadersResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
