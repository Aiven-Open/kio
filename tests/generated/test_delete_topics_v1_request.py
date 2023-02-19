from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.delete_topics.v1.request import DeleteTopicsRequest
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(DeleteTopicsRequest))
@settings(max_examples=1)
def test_delete_topics_request_roundtrip(instance: DeleteTopicsRequest) -> None:
    writer = entity_writer(DeleteTopicsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DeleteTopicsRequest))
    assert instance == result
