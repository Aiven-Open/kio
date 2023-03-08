from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.list_groups.v0.response import ListedGroup
from kio.schema.list_groups.v0.response import ListGroupsResponse
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(ListedGroup))
@settings(max_examples=1)
def test_listed_group_roundtrip(instance: ListedGroup) -> None:
    writer = entity_writer(ListedGroup)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(ListedGroup))
    assert instance == result


@given(from_type(ListGroupsResponse))
@settings(max_examples=1)
def test_list_groups_response_roundtrip(instance: ListGroupsResponse) -> None:
    writer = entity_writer(ListGroupsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(ListGroupsResponse))
    assert instance == result
