from __future__ import annotations

import datetime

from kio.index import load_request_schema
from kio.index import load_response_schema
from kio.schema.decommission_controller.v0.request import DecommissionControllerRequest
from kio.schema.decommission_controller.v0.response import (
    DecommissionControllerResponse,
)
from kio.schema.errors import ErrorCode
from kio.serial import entity_reader
from kio.serial import entity_writer
from kio.static.primitive import i32
from kio.static.primitive import i32Timedelta
from tests.conftest import setup_buffer


def test_decommission_controller_is_registered_as_api_94() -> None:
    assert DecommissionControllerRequest.__api_key__ == 94
    assert DecommissionControllerResponse.__api_key__ == 94
    assert DecommissionControllerRequest.__version__ == 0
    assert DecommissionControllerResponse.__version__ == 0
    assert DecommissionControllerRequest.__flexible__
    assert DecommissionControllerResponse.__flexible__
    assert load_request_schema(94, 0) is DecommissionControllerRequest
    assert load_response_schema(94, 0) is DecommissionControllerResponse


def test_controller_id_not_registered_roundtrip() -> None:
    assert ErrorCode.controller_id_not_registered.value == 136
    assert not ErrorCode.controller_id_not_registered.retriable

    instance = DecommissionControllerResponse(
        throttle_time=i32Timedelta.parse(datetime.timedelta(milliseconds=123)),
        error_code=ErrorCode.controller_id_not_registered,
        error_message="Controller 10001 is not registered.",
    )
    writer = entity_writer(DecommissionControllerResponse)
    reader = entity_reader(DecommissionControllerResponse)

    with setup_buffer() as buffer:
        writer(buffer, instance)
        serialized = buffer.getvalue()
        result, offset = reader(serialized, 0)

    assert result == instance
    assert offset == len(serialized)


def test_decommission_controller_request_roundtrip() -> None:
    instance = DecommissionControllerRequest(controller_id=i32(10001))
    writer = entity_writer(DecommissionControllerRequest)
    reader = entity_reader(DecommissionControllerRequest)

    with setup_buffer() as buffer:
        writer(buffer, instance)
        serialized = buffer.getvalue()
        result, offset = reader(serialized, 0)

    assert result == instance
    assert offset == len(serialized)
