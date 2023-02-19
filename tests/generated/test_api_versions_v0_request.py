from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.api_versions.v0.request import ApiVersionsRequest
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(ApiVersionsRequest))
@settings(max_examples=1)
def test_api_versions_request_roundtrip(instance: ApiVersionsRequest) -> None:
    writer = entity_writer(ApiVersionsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(ApiVersionsRequest))
    assert instance == result
