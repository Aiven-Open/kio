from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.join_group.v8.request import JoinGroupRequestProtocol
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(JoinGroupRequestProtocol))
@settings(max_examples=1)
def test_join_group_request_protocol_roundtrip(
    instance: JoinGroupRequestProtocol,
) -> None:
    writer = entity_writer(JoinGroupRequestProtocol)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(JoinGroupRequestProtocol))
    assert instance == result


from kio.schema.join_group.v8.request import JoinGroupRequest


@given(from_type(JoinGroupRequest))
@settings(max_examples=1)
def test_join_group_request_roundtrip(instance: JoinGroupRequest) -> None:
    writer = entity_writer(JoinGroupRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(JoinGroupRequest))
    assert instance == result
