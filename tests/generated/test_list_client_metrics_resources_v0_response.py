from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.list_client_metrics_resources.v0.response import ClientMetricsResource
from kio.schema.list_client_metrics_resources.v0.response import (
    ListClientMetricsResourcesResponse,
)
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_client_metrics_resource: Final = entity_reader(ClientMetricsResource)


@pytest.mark.roundtrip
@given(from_type(ClientMetricsResource))
def test_client_metrics_resource_roundtrip(instance: ClientMetricsResource) -> None:
    writer = entity_writer(ClientMetricsResource)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_client_metrics_resource(buffer)
    assert instance == result


read_list_client_metrics_resources_response: Final = entity_reader(
    ListClientMetricsResourcesResponse
)


@pytest.mark.roundtrip
@given(from_type(ListClientMetricsResourcesResponse))
def test_list_client_metrics_resources_response_roundtrip(
    instance: ListClientMetricsResourcesResponse,
) -> None:
    writer = entity_writer(ListClientMetricsResourcesResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_list_client_metrics_resources_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(ListClientMetricsResourcesResponse))
def test_list_client_metrics_resources_response_java(
    instance: ListClientMetricsResourcesResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
