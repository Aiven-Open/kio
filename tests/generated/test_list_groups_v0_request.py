from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.list_groups.v0.request import ListGroupsRequest
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(ListGroupsRequest))
@settings(max_examples=1)
def test_list_groups_request_roundtrip(instance: ListGroupsRequest) -> None:
    writer = entity_writer(ListGroupsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(ListGroupsRequest))
    assert instance == result
