from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.create_acls.v1.request import AclCreation
from kio.schema.create_acls.v1.request import CreateAclsRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import setup_buffer

read_acl_creation: Final = entity_reader(AclCreation)


@given(from_type(AclCreation))
@settings(max_examples=1)
def test_acl_creation_roundtrip(instance: AclCreation) -> None:
    writer = entity_writer(AclCreation)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_acl_creation(buffer)
    assert instance == result


read_create_acls_request: Final = entity_reader(CreateAclsRequest)


@given(from_type(CreateAclsRequest))
@settings(max_examples=1)
def test_create_acls_request_roundtrip(instance: CreateAclsRequest) -> None:
    writer = entity_writer(CreateAclsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_create_acls_request(buffer)
    assert instance == result
