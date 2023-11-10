from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.describe_client_quotas.v1.request import ComponentData
from kio.schema.describe_client_quotas.v1.request import DescribeClientQuotasRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_component_data: Final = entity_reader(ComponentData)


@given(from_type(ComponentData))
@settings(max_examples=1)
def test_component_data_roundtrip(instance: ComponentData) -> None:
    writer = entity_writer(ComponentData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_component_data(buffer)
    assert instance == result


read_describe_client_quotas_request: Final = entity_reader(DescribeClientQuotasRequest)


@given(from_type(DescribeClientQuotasRequest))
@settings(max_examples=1)
def test_describe_client_quotas_request_roundtrip(
    instance: DescribeClientQuotasRequest,
) -> None:
    writer = entity_writer(DescribeClientQuotasRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_describe_client_quotas_request(buffer)
    assert instance == result


@given(instance=from_type(DescribeClientQuotasRequest))
def test_describe_client_quotas_request_java(
    instance: DescribeClientQuotasRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
