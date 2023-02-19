from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.write_txn_markers.v0.response import WritableTxnMarkerPartitionResult
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(WritableTxnMarkerPartitionResult))
@settings(max_examples=1)
def test_writable_txn_marker_partition_result_roundtrip(
    instance: WritableTxnMarkerPartitionResult,
) -> None:
    writer = entity_writer(WritableTxnMarkerPartitionResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(WritableTxnMarkerPartitionResult))
    assert instance == result


from kio.schema.write_txn_markers.v0.response import WritableTxnMarkerTopicResult


@given(from_type(WritableTxnMarkerTopicResult))
@settings(max_examples=1)
def test_writable_txn_marker_topic_result_roundtrip(
    instance: WritableTxnMarkerTopicResult,
) -> None:
    writer = entity_writer(WritableTxnMarkerTopicResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(WritableTxnMarkerTopicResult))
    assert instance == result


from kio.schema.write_txn_markers.v0.response import WritableTxnMarkerResult


@given(from_type(WritableTxnMarkerResult))
@settings(max_examples=1)
def test_writable_txn_marker_result_roundtrip(
    instance: WritableTxnMarkerResult,
) -> None:
    writer = entity_writer(WritableTxnMarkerResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(WritableTxnMarkerResult))
    assert instance == result


from kio.schema.write_txn_markers.v0.response import WriteTxnMarkersResponse


@given(from_type(WriteTxnMarkersResponse))
@settings(max_examples=1)
def test_write_txn_markers_response_roundtrip(
    instance: WriteTxnMarkersResponse,
) -> None:
    writer = entity_writer(WriteTxnMarkersResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(WriteTxnMarkersResponse))
    assert instance == result
