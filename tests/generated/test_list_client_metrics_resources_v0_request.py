from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.list_client_metrics_resources.v0.request import (
    ListClientMetricsResourcesRequest,
)
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_list_client_metrics_resources_request: Final = entity_reader(
    ListClientMetricsResourcesRequest
)


@pytest.mark.roundtrip
@given(from_type(ListClientMetricsResourcesRequest))
def test_list_client_metrics_resources_request_roundtrip(
    instance: ListClientMetricsResourcesRequest,
) -> None:
    writer = entity_writer(ListClientMetricsResourcesRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_list_client_metrics_resources_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(ListClientMetricsResourcesRequest))
def test_list_client_metrics_resources_request_java(
    instance: ListClientMetricsResourcesRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
