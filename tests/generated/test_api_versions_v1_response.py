from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.api_versions.v1.response import ApiVersion
from kio.schema.api_versions.v1.response import ApiVersionsResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import setup_buffer

read_api_version: Final = entity_reader(ApiVersion)


@given(from_type(ApiVersion))
@settings(max_examples=1)
def test_api_version_roundtrip(instance: ApiVersion) -> None:
    writer = entity_writer(ApiVersion)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_api_version(buffer)
    assert instance == result


read_api_versions_response: Final = entity_reader(ApiVersionsResponse)


@given(from_type(ApiVersionsResponse))
@settings(max_examples=1)
def test_api_versions_response_roundtrip(instance: ApiVersionsResponse) -> None:
    writer = entity_writer(ApiVersionsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_api_versions_response(buffer)
    assert instance == result
