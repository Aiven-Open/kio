from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.controlled_shutdown.v3.request import ControlledShutdownRequest
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(ControlledShutdownRequest))
@settings(max_examples=1)
def test_controlled_shutdown_request_roundtrip(
    instance: ControlledShutdownRequest,
) -> None:
    writer = entity_writer(ControlledShutdownRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(ControlledShutdownRequest))
    assert instance == result
