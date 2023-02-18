from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.delete_groups.v1.request import DeleteGroupsRequest
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(DeleteGroupsRequest))
@settings(max_examples=1)
def test_delete_groups_request_roundtrip(instance: DeleteGroupsRequest) -> None:
    writer = entity_writer(DeleteGroupsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DeleteGroupsRequest))
    assert instance == result
