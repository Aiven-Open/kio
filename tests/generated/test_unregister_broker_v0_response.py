from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.unregister_broker.v0.response import UnregisterBrokerResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import setup_buffer

read_unregister_broker_response: Final = entity_reader(UnregisterBrokerResponse)


@given(from_type(UnregisterBrokerResponse))
@settings(max_examples=1)
def test_unregister_broker_response_roundtrip(
    instance: UnregisterBrokerResponse,
) -> None:
    writer = entity_writer(UnregisterBrokerResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_unregister_broker_response(buffer)
    assert instance == result
