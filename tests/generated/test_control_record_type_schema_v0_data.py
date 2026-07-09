from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.control_record_type_schema.v0.data import ControlRecordTypeSchema
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_control_record_type_schema: Final = entity_reader(ControlRecordTypeSchema)


@pytest.mark.roundtrip
@given(from_type(ControlRecordTypeSchema))
def test_control_record_type_schema_roundtrip(
    instance: ControlRecordTypeSchema,
) -> None:
    writer = entity_writer(ControlRecordTypeSchema)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_control_record_type_schema(
            buffer.getvalue(),
            0,
        )

    assert instance == result


@pytest.mark.java
@given(instance=from_type(ControlRecordTypeSchema))
def test_control_record_type_schema_java(
    instance: ControlRecordTypeSchema, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
