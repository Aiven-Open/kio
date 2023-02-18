from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.find_coordinator.v1.response import FindCoordinatorResponse
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(FindCoordinatorResponse))
@settings(max_examples=1)
def test_find_coordinator_response_roundtrip(instance: FindCoordinatorResponse) -> None:
    writer = entity_writer(FindCoordinatorResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(FindCoordinatorResponse))
    assert instance == result
