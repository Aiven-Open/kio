from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.join_group.v3.response import JoinGroupResponse
from kio.schema.join_group.v3.response import JoinGroupResponseMember
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_join_group_response_member: Final = entity_reader(JoinGroupResponseMember)


@pytest.mark.roundtrip
@given(from_type(JoinGroupResponseMember))
def test_join_group_response_member_roundtrip(
    instance: JoinGroupResponseMember,
) -> None:
    writer = entity_writer(JoinGroupResponseMember)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_join_group_response_member(buffer)
    assert instance == result


read_join_group_response: Final = entity_reader(JoinGroupResponse)


@pytest.mark.roundtrip
@given(from_type(JoinGroupResponse))
def test_join_group_response_roundtrip(instance: JoinGroupResponse) -> None:
    writer = entity_writer(JoinGroupResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_join_group_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(JoinGroupResponse))
def test_join_group_response_java(
    instance: JoinGroupResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
