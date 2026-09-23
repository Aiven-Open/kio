from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.decommission_controller.v0.response import (
    DecommissionControllerResponse,
)
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import setup_buffer

read_decommission_controller_response: Final = entity_reader(
    DecommissionControllerResponse
)


@pytest.mark.roundtrip
@given(from_type(DecommissionControllerResponse))
def test_decommission_controller_response_roundtrip(
    instance: DecommissionControllerResponse,
) -> None:
    writer = entity_writer(DecommissionControllerResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_decommission_controller_response(
            buffer.getvalue(),
            0,
        )

    assert instance == result
