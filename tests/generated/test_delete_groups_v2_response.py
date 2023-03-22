from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.delete_groups.v2.response import DeletableGroupResult
from kio.schema.delete_groups.v2.response import DeleteGroupsResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import setup_buffer

read_deletable_group_result: Final = entity_reader(DeletableGroupResult)


@given(from_type(DeletableGroupResult))
@settings(max_examples=1)
def test_deletable_group_result_roundtrip(instance: DeletableGroupResult) -> None:
    writer = entity_writer(DeletableGroupResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_deletable_group_result(buffer)
    assert instance == result


read_delete_groups_response: Final = entity_reader(DeleteGroupsResponse)


@given(from_type(DeleteGroupsResponse))
@settings(max_examples=1)
def test_delete_groups_response_roundtrip(instance: DeleteGroupsResponse) -> None:
    writer = entity_writer(DeleteGroupsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_delete_groups_response(buffer)
    assert instance == result
