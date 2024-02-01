from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.api_versions.v0.response import ApiVersion
from kio.schema.api_versions.v0.response import ApiVersionsResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_api_version: Final = entity_reader(ApiVersion)


@pytest.mark.roundtrip
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


@pytest.mark.roundtrip
@given(from_type(ApiVersionsResponse))
@settings(max_examples=1)
def test_api_versions_response_roundtrip(instance: ApiVersionsResponse) -> None:
    writer = entity_writer(ApiVersionsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_api_versions_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(ApiVersionsResponse))
def test_api_versions_response_java(
    instance: ApiVersionsResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
