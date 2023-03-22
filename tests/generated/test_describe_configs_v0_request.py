from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.describe_configs.v0.request import DescribeConfigsRequest
from kio.schema.describe_configs.v0.request import DescribeConfigsResource
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import setup_buffer

read_describe_configs_resource: Final = entity_reader(DescribeConfigsResource)


@given(from_type(DescribeConfigsResource))
@settings(max_examples=1)
def test_describe_configs_resource_roundtrip(instance: DescribeConfigsResource) -> None:
    writer = entity_writer(DescribeConfigsResource)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_describe_configs_resource(buffer)
    assert instance == result


read_describe_configs_request: Final = entity_reader(DescribeConfigsRequest)


@given(from_type(DescribeConfigsRequest))
@settings(max_examples=1)
def test_describe_configs_request_roundtrip(instance: DescribeConfigsRequest) -> None:
    writer = entity_writer(DescribeConfigsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_describe_configs_request(buffer)
    assert instance == result
