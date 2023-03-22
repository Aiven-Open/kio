from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.describe_configs.v1.response import DescribeConfigsResourceResult
from kio.schema.describe_configs.v1.response import DescribeConfigsResponse
from kio.schema.describe_configs.v1.response import DescribeConfigsResult
from kio.schema.describe_configs.v1.response import DescribeConfigsSynonym
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import setup_buffer

read_describe_configs_synonym: Final = entity_reader(DescribeConfigsSynonym)


@given(from_type(DescribeConfigsSynonym))
@settings(max_examples=1)
def test_describe_configs_synonym_roundtrip(instance: DescribeConfigsSynonym) -> None:
    writer = entity_writer(DescribeConfigsSynonym)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_describe_configs_synonym(buffer)
    assert instance == result


read_describe_configs_resource_result: Final = entity_reader(
    DescribeConfigsResourceResult
)


@given(from_type(DescribeConfigsResourceResult))
@settings(max_examples=1)
def test_describe_configs_resource_result_roundtrip(
    instance: DescribeConfigsResourceResult,
) -> None:
    writer = entity_writer(DescribeConfigsResourceResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_describe_configs_resource_result(buffer)
    assert instance == result


read_describe_configs_result: Final = entity_reader(DescribeConfigsResult)


@given(from_type(DescribeConfigsResult))
@settings(max_examples=1)
def test_describe_configs_result_roundtrip(instance: DescribeConfigsResult) -> None:
    writer = entity_writer(DescribeConfigsResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_describe_configs_result(buffer)
    assert instance == result


read_describe_configs_response: Final = entity_reader(DescribeConfigsResponse)


@given(from_type(DescribeConfigsResponse))
@settings(max_examples=1)
def test_describe_configs_response_roundtrip(instance: DescribeConfigsResponse) -> None:
    writer = entity_writer(DescribeConfigsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_describe_configs_response(buffer)
    assert instance == result
