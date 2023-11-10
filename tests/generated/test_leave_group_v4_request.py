from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.leave_group.v4.request import LeaveGroupRequest
from kio.schema.leave_group.v4.request import MemberIdentity
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_member_identity: Final = entity_reader(MemberIdentity)


@given(from_type(MemberIdentity))
@settings(max_examples=1)
def test_member_identity_roundtrip(instance: MemberIdentity) -> None:
    writer = entity_writer(MemberIdentity)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_member_identity(buffer)
    assert instance == result


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


@given(instance=from_type(LeaveGroupRequest))
def test_leave_group_request_java(
    instance: LeaveGroupRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
