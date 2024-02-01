from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.init_producer_id.v2.request import InitProducerIdRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_init_producer_id_request: Final = entity_reader(InitProducerIdRequest)


@pytest.mark.roundtrip
@given(from_type(InitProducerIdRequest))
@settings(max_examples=1)
def test_init_producer_id_request_roundtrip(instance: InitProducerIdRequest) -> None:
    writer = entity_writer(InitProducerIdRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_init_producer_id_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(InitProducerIdRequest))
def test_init_producer_id_request_java(
    instance: InitProducerIdRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
