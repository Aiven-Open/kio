from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.leave_group.v3.response import LeaveGroupResponse
from kio.schema.leave_group.v3.response import MemberResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_member_response: Final = entity_reader(MemberResponse)


@pytest.mark.roundtrip
@given(from_type(MemberResponse))
def test_member_response_roundtrip(instance: MemberResponse) -> None:
    writer = entity_writer(MemberResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_member_response(buffer)
    assert instance == result


read_leave_group_response: Final = entity_reader(LeaveGroupResponse)


@pytest.mark.roundtrip
@given(from_type(LeaveGroupResponse))
def test_leave_group_response_roundtrip(instance: LeaveGroupResponse) -> None:
    writer = entity_writer(LeaveGroupResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_leave_group_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(LeaveGroupResponse))
def test_leave_group_response_java(
    instance: LeaveGroupResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
