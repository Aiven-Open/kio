from __future__ import annotations

from typing import Final

import pytest
from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.api_versions.v3.request import ApiVersionsRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_api_versions_request: Final = entity_reader(ApiVersionsRequest)


@pytest.mark.roundtrip
@given(from_type(ApiVersionsRequest))
@settings(max_examples=1)
def test_api_versions_request_roundtrip(instance: ApiVersionsRequest) -> None:
    writer = entity_writer(ApiVersionsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_api_versions_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(ApiVersionsRequest))
def test_api_versions_request_java(
    instance: ApiVersionsRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
