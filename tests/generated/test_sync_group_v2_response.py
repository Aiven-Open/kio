from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.sync_group.v2.response import SyncGroupResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_sync_group_response: Final = entity_reader(SyncGroupResponse)


@given(from_type(SyncGroupResponse))
@settings(max_examples=1)
def test_sync_group_response_roundtrip(instance: SyncGroupResponse) -> None:
    writer = entity_writer(SyncGroupResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync_group_response(buffer)
    assert instance == result


@given(instance=from_type(SyncGroupResponse))
def test_sync_group_response_java(
    instance: SyncGroupResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
