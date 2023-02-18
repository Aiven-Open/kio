from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.leader_and_isr.v0.response import LeaderAndIsrPartitionError
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(LeaderAndIsrPartitionError))
@settings(max_examples=1)
def test_leader_and_isr_partition_error_roundtrip(
    instance: LeaderAndIsrPartitionError,
) -> None:
    writer = entity_writer(LeaderAndIsrPartitionError)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(LeaderAndIsrPartitionError))
    assert instance == result


from kio.schema.leader_and_isr.v0.response import LeaderAndIsrResponse


@given(from_type(LeaderAndIsrResponse))
@settings(max_examples=1)
def test_leader_and_isr_response_roundtrip(instance: LeaderAndIsrResponse) -> None:
    writer = entity_writer(LeaderAndIsrResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(LeaderAndIsrResponse))
    assert instance == result
