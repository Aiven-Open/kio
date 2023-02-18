from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.describe_acls.v2.response import AclDescription
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(AclDescription))
@settings(max_examples=1)
def test_acl_description_roundtrip(instance: AclDescription) -> None:
    writer = entity_writer(AclDescription)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(AclDescription))
    assert instance == result


from kio.schema.describe_acls.v2.response import DescribeAclsResource


@given(from_type(DescribeAclsResource))
@settings(max_examples=1)
def test_describe_acls_resource_roundtrip(instance: DescribeAclsResource) -> None:
    writer = entity_writer(DescribeAclsResource)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DescribeAclsResource))
    assert instance == result


from kio.schema.describe_acls.v2.response import DescribeAclsResponse


@given(from_type(DescribeAclsResponse))
@settings(max_examples=1)
def test_describe_acls_response_roundtrip(instance: DescribeAclsResponse) -> None:
    writer = entity_writer(DescribeAclsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DescribeAclsResponse))
    assert instance == result
