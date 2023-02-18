from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.find_coordinator.v4.request import FindCoordinatorRequest
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(FindCoordinatorRequest))
@settings(max_examples=1)
def test_find_coordinator_request_roundtrip(instance: FindCoordinatorRequest) -> None:
    writer = entity_writer(FindCoordinatorRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(FindCoordinatorRequest))
    assert instance == result
