from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.delete_groups.v0.request import DeleteGroupsRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_delete_groups_request: Final = entity_reader(DeleteGroupsRequest)


@pytest.mark.roundtrip
@given(from_type(DeleteGroupsRequest))
def test_delete_groups_request_roundtrip(instance: DeleteGroupsRequest) -> None:
    writer = entity_writer(DeleteGroupsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_delete_groups_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(DeleteGroupsRequest))
def test_delete_groups_request_java(
    instance: DeleteGroupsRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
