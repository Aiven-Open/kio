from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.leave_group.v0.request import LeaveGroupRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_leave_group_request: Final = entity_reader(LeaveGroupRequest)


@pytest.mark.roundtrip
@given(from_type(LeaveGroupRequest))
def test_leave_group_request_roundtrip(instance: LeaveGroupRequest) -> None:
    writer = entity_writer(LeaveGroupRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_leave_group_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(LeaveGroupRequest))
def test_leave_group_request_java(
    instance: LeaveGroupRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
