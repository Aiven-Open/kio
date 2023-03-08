from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.delete_groups.v1.response import DeletableGroupResult
from kio.schema.delete_groups.v1.response import DeleteGroupsResponse
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(DeletableGroupResult))
@settings(max_examples=1)
def test_deletable_group_result_roundtrip(instance: DeletableGroupResult) -> None:
    writer = entity_writer(DeletableGroupResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DeletableGroupResult))
    assert instance == result


@given(from_type(DeleteGroupsResponse))
@settings(max_examples=1)
def test_delete_groups_response_roundtrip(instance: DeleteGroupsResponse) -> None:
    writer = entity_writer(DeleteGroupsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DeleteGroupsResponse))
    assert instance == result
