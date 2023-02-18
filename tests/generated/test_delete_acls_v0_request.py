from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.delete_acls.v0.request import DeleteAclsFilter
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(DeleteAclsFilter))
@settings(max_examples=1)
def test_delete_acls_filter_roundtrip(instance: DeleteAclsFilter) -> None:
    writer = entity_writer(DeleteAclsFilter)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DeleteAclsFilter))
    assert instance == result


from kio.schema.delete_acls.v0.request import DeleteAclsRequest


@given(from_type(DeleteAclsRequest))
@settings(max_examples=1)
def test_delete_acls_request_roundtrip(instance: DeleteAclsRequest) -> None:
    writer = entity_writer(DeleteAclsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DeleteAclsRequest))
    assert instance == result
