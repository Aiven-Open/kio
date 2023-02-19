from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.leave_group.v2.response import LeaveGroupResponse
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(LeaveGroupResponse))
@settings(max_examples=1)
def test_leave_group_response_roundtrip(instance: LeaveGroupResponse) -> None:
    writer = entity_writer(LeaveGroupResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(LeaveGroupResponse))
    assert instance == result
