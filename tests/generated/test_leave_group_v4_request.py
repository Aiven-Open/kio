from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.leave_group.v4.request import MemberIdentity
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(MemberIdentity))
@settings(max_examples=1)
def test_member_identity_roundtrip(instance: MemberIdentity) -> None:
    writer = entity_writer(MemberIdentity)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(MemberIdentity))
    assert instance == result


from kio.schema.leave_group.v4.request import LeaveGroupRequest


@given(from_type(LeaveGroupRequest))
@settings(max_examples=1)
def test_leave_group_request_roundtrip(instance: LeaveGroupRequest) -> None:
    writer = entity_writer(LeaveGroupRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(LeaveGroupRequest))
    assert instance == result
