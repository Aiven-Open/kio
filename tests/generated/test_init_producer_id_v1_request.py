from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.init_producer_id.v1.request import InitProducerIdRequest
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(InitProducerIdRequest))
@settings(max_examples=1)
def test_init_producer_id_request_roundtrip(instance: InitProducerIdRequest) -> None:
    writer = entity_writer(InitProducerIdRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(InitProducerIdRequest))
    assert instance == result
