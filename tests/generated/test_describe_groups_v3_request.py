from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.describe_groups.v3.request import DescribeGroupsRequest
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(DescribeGroupsRequest))
@settings(max_examples=1)
def test_describe_groups_request_roundtrip(instance: DescribeGroupsRequest) -> None:
    writer = entity_writer(DescribeGroupsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DescribeGroupsRequest))
    assert instance == result
