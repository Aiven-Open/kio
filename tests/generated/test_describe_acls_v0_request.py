from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.describe_acls.v0.request import DescribeAclsRequest
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(DescribeAclsRequest))
@settings(max_examples=1)
def test_describe_acls_request_roundtrip(instance: DescribeAclsRequest) -> None:
    writer = entity_writer(DescribeAclsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DescribeAclsRequest))
    assert instance == result
