from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.allocate_producer_ids.v0.request import AllocateProducerIdsRequest
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(AllocateProducerIdsRequest))
@settings(max_examples=1)
def test_allocate_producer_ids_request_roundtrip(
    instance: AllocateProducerIdsRequest,
) -> None:
    writer = entity_writer(AllocateProducerIdsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(AllocateProducerIdsRequest))
    assert instance == result
