from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.describe_acls.v0.response import AclDescription
from kio.schema.describe_acls.v0.response import DescribeAclsResource
from kio.schema.describe_acls.v0.response import DescribeAclsResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import setup_buffer

read_acl_description: Final = entity_reader(AclDescription)


@given(from_type(AclDescription))
@settings(max_examples=1)
def test_acl_description_roundtrip(instance: AclDescription) -> None:
    writer = entity_writer(AclDescription)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_acl_description(buffer)
    assert instance == result


read_describe_acls_resource: Final = entity_reader(DescribeAclsResource)


@given(from_type(DescribeAclsResource))
@settings(max_examples=1)
def test_describe_acls_resource_roundtrip(instance: DescribeAclsResource) -> None:
    writer = entity_writer(DescribeAclsResource)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_describe_acls_resource(buffer)
    assert instance == result


read_describe_acls_response: Final = entity_reader(DescribeAclsResponse)


@given(from_type(DescribeAclsResponse))
@settings(max_examples=1)
def test_describe_acls_response_roundtrip(instance: DescribeAclsResponse) -> None:
    writer = entity_writer(DescribeAclsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_describe_acls_response(buffer)
    assert instance == result
