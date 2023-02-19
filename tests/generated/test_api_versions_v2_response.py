from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.api_versions.v2.response import ApiVersion
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(ApiVersion))
@settings(max_examples=1)
def test_api_version_roundtrip(instance: ApiVersion) -> None:
    writer = entity_writer(ApiVersion)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(ApiVersion))
    assert instance == result


from kio.schema.api_versions.v2.response import ApiVersionsResponse


@given(from_type(ApiVersionsResponse))
@settings(max_examples=1)
def test_api_versions_response_roundtrip(instance: ApiVersionsResponse) -> None:
    writer = entity_writer(ApiVersionsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(ApiVersionsResponse))
    assert instance == result
