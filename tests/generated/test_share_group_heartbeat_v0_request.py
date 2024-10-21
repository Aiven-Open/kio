from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.share_group_heartbeat.v0.request import ShareGroupHeartbeatRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_share_group_heartbeat_request: Final = entity_reader(ShareGroupHeartbeatRequest)


@pytest.mark.roundtrip
@given(from_type(ShareGroupHeartbeatRequest))
def test_share_group_heartbeat_request_roundtrip(
    instance: ShareGroupHeartbeatRequest,
) -> None:
    writer = entity_writer(ShareGroupHeartbeatRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_share_group_heartbeat_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(ShareGroupHeartbeatRequest))
def test_share_group_heartbeat_request_java(
    instance: ShareGroupHeartbeatRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
