from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.write_txn_markers.v1.request import WritableTxnMarkerTopic
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(WritableTxnMarkerTopic))
@settings(max_examples=1)
def test_writable_txn_marker_topic_roundtrip(instance: WritableTxnMarkerTopic) -> None:
    writer = entity_writer(WritableTxnMarkerTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(WritableTxnMarkerTopic))
    assert instance == result


from kio.schema.write_txn_markers.v1.request import WritableTxnMarker


@given(from_type(WritableTxnMarker))
@settings(max_examples=1)
def test_writable_txn_marker_roundtrip(instance: WritableTxnMarker) -> None:
    writer = entity_writer(WritableTxnMarker)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(WritableTxnMarker))
    assert instance == result


from kio.schema.write_txn_markers.v1.request import WriteTxnMarkersRequest


@given(from_type(WriteTxnMarkersRequest))
@settings(max_examples=1)
def test_write_txn_markers_request_roundtrip(instance: WriteTxnMarkersRequest) -> None:
    writer = entity_writer(WriteTxnMarkersRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(WriteTxnMarkersRequest))
    assert instance == result
