from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.decommission_controller.v0.request import DecommissionControllerRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import setup_buffer

read_decommission_controller_request: Final = entity_reader(
    DecommissionControllerRequest
)


@pytest.mark.roundtrip
@given(from_type(DecommissionControllerRequest))
def test_decommission_controller_request_roundtrip(
    instance: DecommissionControllerRequest,
) -> None:
    writer = entity_writer(DecommissionControllerRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_decommission_controller_request(
            buffer.getvalue(),
            0,
        )

    assert instance == result
