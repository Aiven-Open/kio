from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.stop_replica.v3.response import StopReplicaPartitionError
from kio.schema.stop_replica.v3.response import StopReplicaResponse
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(StopReplicaPartitionError))
@settings(max_examples=1)
def test_stop_replica_partition_error_roundtrip(
    instance: StopReplicaPartitionError,
) -> None:
    writer = entity_writer(StopReplicaPartitionError)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(StopReplicaPartitionError))
    assert instance == result


@given(from_type(StopReplicaResponse))
@settings(max_examples=1)
def test_stop_replica_response_roundtrip(instance: StopReplicaResponse) -> None:
    writer = entity_writer(StopReplicaResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(StopReplicaResponse))
    assert instance == result
