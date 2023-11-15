from __future__ import annotations

from typing import Final

import pytest
from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.init_producer_id.v4.response import InitProducerIdResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_init_producer_id_response: Final = entity_reader(InitProducerIdResponse)


@pytest.mark.roundtrip
@given(from_type(InitProducerIdResponse))
@settings(max_examples=1)
def test_init_producer_id_response_roundtrip(instance: InitProducerIdResponse) -> None:
    writer = entity_writer(InitProducerIdResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_init_producer_id_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(InitProducerIdResponse))
def test_init_producer_id_response_java(
    instance: InitProducerIdResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
