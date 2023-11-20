from __future__ import annotations

from typing import Final

import pytest
from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.snapshot_footer_record.v0.data import SnapshotFooterRecord
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_snapshot_footer_record: Final = entity_reader(SnapshotFooterRecord)


@pytest.mark.roundtrip
@given(from_type(SnapshotFooterRecord))
@settings(max_examples=1)
def test_snapshot_footer_record_roundtrip(instance: SnapshotFooterRecord) -> None:
    writer = entity_writer(SnapshotFooterRecord)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_snapshot_footer_record(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(SnapshotFooterRecord))
def test_snapshot_footer_record_java(
    instance: SnapshotFooterRecord, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
