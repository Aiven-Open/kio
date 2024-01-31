from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.write_txn_markers.v1.request import WritableTxnMarker
from kio.schema.write_txn_markers.v1.request import WritableTxnMarkerTopic
from kio.schema.write_txn_markers.v1.request import WriteTxnMarkersRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_writable_txn_marker_topic: Final = entity_reader(WritableTxnMarkerTopic)


@pytest.mark.roundtrip
@given(from_type(WritableTxnMarkerTopic))
@settings(max_examples=1)
def test_writable_txn_marker_topic_roundtrip(instance: WritableTxnMarkerTopic) -> None:
    writer = entity_writer(WritableTxnMarkerTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_writable_txn_marker_topic(buffer)
    assert instance == result


read_writable_txn_marker: Final = entity_reader(WritableTxnMarker)


@pytest.mark.roundtrip
@given(from_type(WritableTxnMarker))
@settings(max_examples=1)
def test_writable_txn_marker_roundtrip(instance: WritableTxnMarker) -> None:
    writer = entity_writer(WritableTxnMarker)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_writable_txn_marker(buffer)
    assert instance == result


read_write_txn_markers_request: Final = entity_reader(WriteTxnMarkersRequest)


@pytest.mark.roundtrip
@given(from_type(WriteTxnMarkersRequest))
@settings(max_examples=1)
def test_write_txn_markers_request_roundtrip(instance: WriteTxnMarkersRequest) -> None:
    writer = entity_writer(WriteTxnMarkersRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_write_txn_markers_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(WriteTxnMarkersRequest))
def test_write_txn_markers_request_java(
    instance: WriteTxnMarkersRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
