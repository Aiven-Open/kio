from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.create_acls.v0.response import AclCreationResult
from kio.schema.create_acls.v0.response import CreateAclsResponse
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(AclCreationResult))
@settings(max_examples=1)
def test_acl_creation_result_roundtrip(instance: AclCreationResult) -> None:
    writer = entity_writer(AclCreationResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(AclCreationResult))
    assert instance == result


@given(from_type(CreateAclsResponse))
@settings(max_examples=1)
def test_create_acls_response_roundtrip(instance: CreateAclsResponse) -> None:
    writer = entity_writer(CreateAclsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(CreateAclsResponse))
    assert instance == result
