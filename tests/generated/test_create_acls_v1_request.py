from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.create_acls.v1.request import AclCreation
from kio.schema.create_acls.v1.request import CreateAclsRequest
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(AclCreation))
@settings(max_examples=1)
def test_acl_creation_roundtrip(instance: AclCreation) -> None:
    writer = entity_writer(AclCreation)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(AclCreation))
    assert instance == result


@given(from_type(CreateAclsRequest))
@settings(max_examples=1)
def test_create_acls_request_roundtrip(instance: CreateAclsRequest) -> None:
    writer = entity_writer(CreateAclsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(CreateAclsRequest))
    assert instance == result
