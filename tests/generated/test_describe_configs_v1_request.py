from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.describe_configs.v1.request import DescribeConfigsRequest
from kio.schema.describe_configs.v1.request import DescribeConfigsResource
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(DescribeConfigsResource))
@settings(max_examples=1)
def test_describe_configs_resource_roundtrip(instance: DescribeConfigsResource) -> None:
    writer = entity_writer(DescribeConfigsResource)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DescribeConfigsResource))
    assert instance == result


@given(from_type(DescribeConfigsRequest))
@settings(max_examples=1)
def test_describe_configs_request_roundtrip(instance: DescribeConfigsRequest) -> None:
    writer = entity_writer(DescribeConfigsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DescribeConfigsRequest))
    assert instance == result
