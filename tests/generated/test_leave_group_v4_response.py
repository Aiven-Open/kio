from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.leave_group.v4.response import LeaveGroupResponse
from kio.schema.leave_group.v4.response import MemberResponse
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(MemberResponse))
@settings(max_examples=1)
def test_member_response_roundtrip(instance: MemberResponse) -> None:
    writer = entity_writer(MemberResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(MemberResponse))
    assert instance == result


@given(from_type(LeaveGroupResponse))
@settings(max_examples=1)
def test_leave_group_response_roundtrip(instance: LeaveGroupResponse) -> None:
    writer = entity_writer(LeaveGroupResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(LeaveGroupResponse))
    assert instance == result
