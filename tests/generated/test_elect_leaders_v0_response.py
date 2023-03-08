from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.elect_leaders.v0.response import ElectLeadersResponse
from kio.schema.elect_leaders.v0.response import PartitionResult
from kio.schema.elect_leaders.v0.response import ReplicaElectionResult
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(PartitionResult))
@settings(max_examples=1)
def test_partition_result_roundtrip(instance: PartitionResult) -> None:
    writer = entity_writer(PartitionResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(PartitionResult))
    assert instance == result


@given(from_type(ReplicaElectionResult))
@settings(max_examples=1)
def test_replica_election_result_roundtrip(instance: ReplicaElectionResult) -> None:
    writer = entity_writer(ReplicaElectionResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(ReplicaElectionResult))
    assert instance == result


@given(from_type(ElectLeadersResponse))
@settings(max_examples=1)
def test_elect_leaders_response_roundtrip(instance: ElectLeadersResponse) -> None:
    writer = entity_writer(ElectLeadersResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(ElectLeadersResponse))
    assert instance == result
