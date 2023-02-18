from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.delete_acls.v0.response import DeleteAclsMatchingAcl
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(DeleteAclsMatchingAcl))
@settings(max_examples=1)
def test_delete_acls_matching_acl_roundtrip(instance: DeleteAclsMatchingAcl) -> None:
    writer = entity_writer(DeleteAclsMatchingAcl)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DeleteAclsMatchingAcl))
    assert instance == result


from kio.schema.delete_acls.v0.response import DeleteAclsFilterResult


@given(from_type(DeleteAclsFilterResult))
@settings(max_examples=1)
def test_delete_acls_filter_result_roundtrip(instance: DeleteAclsFilterResult) -> None:
    writer = entity_writer(DeleteAclsFilterResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DeleteAclsFilterResult))
    assert instance == result


from kio.schema.delete_acls.v0.response import DeleteAclsResponse


@given(from_type(DeleteAclsResponse))
@settings(max_examples=1)
def test_delete_acls_response_roundtrip(instance: DeleteAclsResponse) -> None:
    writer = entity_writer(DeleteAclsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DeleteAclsResponse))
    assert instance == result
