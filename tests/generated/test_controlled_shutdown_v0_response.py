from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.controlled_shutdown.v0.response import RemainingPartition
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(RemainingPartition))
@settings(max_examples=1)
def test_remaining_partition_roundtrip(instance: RemainingPartition) -> None:
    writer = entity_writer(RemainingPartition)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(RemainingPartition))
    assert instance == result


from kio.schema.controlled_shutdown.v0.response import ControlledShutdownResponse


@given(from_type(ControlledShutdownResponse))
@settings(max_examples=1)
def test_controlled_shutdown_response_roundtrip(
    instance: ControlledShutdownResponse,
) -> None:
    writer = entity_writer(ControlledShutdownResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(ControlledShutdownResponse))
    assert instance == result
