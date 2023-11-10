from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.write_txn_markers.v1.response import WritableTxnMarkerPartitionResult
from kio.schema.write_txn_markers.v1.response import WritableTxnMarkerResult
from kio.schema.write_txn_markers.v1.response import WritableTxnMarkerTopicResult
from kio.schema.write_txn_markers.v1.response import WriteTxnMarkersResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_writable_txn_marker_partition_result: Final = entity_reader(
    WritableTxnMarkerPartitionResult
)


@given(from_type(WritableTxnMarkerPartitionResult))
@settings(max_examples=1)
def test_writable_txn_marker_partition_result_roundtrip(
    instance: WritableTxnMarkerPartitionResult,
) -> None:
    writer = entity_writer(WritableTxnMarkerPartitionResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_writable_txn_marker_partition_result(buffer)
    assert instance == result


read_writable_txn_marker_topic_result: Final = entity_reader(
    WritableTxnMarkerTopicResult
)


@given(from_type(WritableTxnMarkerTopicResult))
@settings(max_examples=1)
def test_writable_txn_marker_topic_result_roundtrip(
    instance: WritableTxnMarkerTopicResult,
) -> None:
    writer = entity_writer(WritableTxnMarkerTopicResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_writable_txn_marker_topic_result(buffer)
    assert instance == result


read_writable_txn_marker_result: Final = entity_reader(WritableTxnMarkerResult)


@given(from_type(WritableTxnMarkerResult))
@settings(max_examples=1)
def test_writable_txn_marker_result_roundtrip(
    instance: WritableTxnMarkerResult,
) -> None:
    writer = entity_writer(WritableTxnMarkerResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_writable_txn_marker_result(buffer)
    assert instance == result


read_write_txn_markers_response: Final = entity_reader(WriteTxnMarkersResponse)


@given(from_type(WriteTxnMarkersResponse))
@settings(max_examples=1)
def test_write_txn_markers_response_roundtrip(
    instance: WriteTxnMarkersResponse,
) -> None:
    writer = entity_writer(WriteTxnMarkersResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_write_txn_markers_response(buffer)
    assert instance == result


@given(instance=from_type(WriteTxnMarkersResponse))
def test_write_txn_markers_response_java(
    instance: WriteTxnMarkersResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
