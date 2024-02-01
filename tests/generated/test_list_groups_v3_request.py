from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.list_groups.v3.request import ListGroupsRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_list_groups_request: Final = entity_reader(ListGroupsRequest)


@pytest.mark.roundtrip
@given(from_type(ListGroupsRequest))
def test_list_groups_request_roundtrip(instance: ListGroupsRequest) -> None:
    writer = entity_writer(ListGroupsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_list_groups_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(ListGroupsRequest))
def test_list_groups_request_java(
    instance: ListGroupsRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
