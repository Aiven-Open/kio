from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.describe_configs.v3.response import DescribeConfigsSynonym
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(DescribeConfigsSynonym))
@settings(max_examples=1)
def test_describe_configs_synonym_roundtrip(instance: DescribeConfigsSynonym) -> None:
    writer = entity_writer(DescribeConfigsSynonym)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DescribeConfigsSynonym))
    assert instance == result


from kio.schema.describe_configs.v3.response import DescribeConfigsResourceResult


@given(from_type(DescribeConfigsResourceResult))
@settings(max_examples=1)
def test_describe_configs_resource_result_roundtrip(
    instance: DescribeConfigsResourceResult,
) -> None:
    writer = entity_writer(DescribeConfigsResourceResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DescribeConfigsResourceResult))
    assert instance == result


from kio.schema.describe_configs.v3.response import DescribeConfigsResult


@given(from_type(DescribeConfigsResult))
@settings(max_examples=1)
def test_describe_configs_result_roundtrip(instance: DescribeConfigsResult) -> None:
    writer = entity_writer(DescribeConfigsResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DescribeConfigsResult))
    assert instance == result


from kio.schema.describe_configs.v3.response import DescribeConfigsResponse


@given(from_type(DescribeConfigsResponse))
@settings(max_examples=1)
def test_describe_configs_response_roundtrip(instance: DescribeConfigsResponse) -> None:
    writer = entity_writer(DescribeConfigsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DescribeConfigsResponse))
    assert instance == result
