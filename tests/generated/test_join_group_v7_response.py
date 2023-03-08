from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.join_group.v7.response import JoinGroupResponse
from kio.schema.join_group.v7.response import JoinGroupResponseMember
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(JoinGroupResponseMember))
@settings(max_examples=1)
def test_join_group_response_member_roundtrip(
    instance: JoinGroupResponseMember,
) -> None:
    writer = entity_writer(JoinGroupResponseMember)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(JoinGroupResponseMember))
    assert instance == result


@given(from_type(JoinGroupResponse))
@settings(max_examples=1)
def test_join_group_response_roundtrip(instance: JoinGroupResponse) -> None:
    writer = entity_writer(JoinGroupResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(JoinGroupResponse))
    assert instance == result
