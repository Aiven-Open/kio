from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.leave_group.v1.request import LeaveGroupRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import setup_buffer

read_leave_group_request: Final = entity_reader(LeaveGroupRequest)


@given(from_type(LeaveGroupRequest))
@settings(max_examples=1)
def test_leave_group_request_roundtrip(instance: LeaveGroupRequest) -> None:
    writer = entity_writer(LeaveGroupRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_leave_group_request(buffer)
    assert instance == result
