from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.update_metadata.v2.response import UpdateMetadataResponse
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(UpdateMetadataResponse))
@settings(max_examples=1)
def test_update_metadata_response_roundtrip(instance: UpdateMetadataResponse) -> None:
    writer = entity_writer(UpdateMetadataResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(UpdateMetadataResponse))
    assert instance == result
