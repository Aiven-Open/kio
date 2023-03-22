from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.snapshot_header_record.v0.data import SnapshotHeaderRecord
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import setup_buffer

read_snapshot_header_record: Final = entity_reader(SnapshotHeaderRecord)


@given(from_type(SnapshotHeaderRecord))
@settings(max_examples=1)
def test_snapshot_header_record_roundtrip(instance: SnapshotHeaderRecord) -> None:
    writer = entity_writer(SnapshotHeaderRecord)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_snapshot_header_record(buffer)
    assert instance == result
