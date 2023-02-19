from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.snapshot_footer_record.v0.data import SnapshotFooterRecord
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(SnapshotFooterRecord))
@settings(max_examples=1)
def test_snapshot_footer_record_roundtrip(instance: SnapshotFooterRecord) -> None:
    writer = entity_writer(SnapshotFooterRecord)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(SnapshotFooterRecord))
    assert instance == result
