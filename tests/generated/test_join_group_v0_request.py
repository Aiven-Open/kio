from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.join_group.v0.request import JoinGroupRequest
from kio.schema.join_group.v0.request import JoinGroupRequestProtocol
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import setup_buffer

read_join_group_request_protocol: Final = entity_reader(JoinGroupRequestProtocol)


@given(from_type(JoinGroupRequestProtocol))
@settings(max_examples=1)
def test_join_group_request_protocol_roundtrip(
    instance: JoinGroupRequestProtocol,
) -> None:
    writer = entity_writer(JoinGroupRequestProtocol)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_join_group_request_protocol(buffer)
    assert instance == result


read_join_group_request: Final = entity_reader(JoinGroupRequest)


@given(from_type(JoinGroupRequest))
@settings(max_examples=1)
def test_join_group_request_roundtrip(instance: JoinGroupRequest) -> None:
    writer = entity_writer(JoinGroupRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_join_group_request(buffer)
    assert instance == result
