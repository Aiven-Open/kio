from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.delete_records.v0.request import DeleteRecordsPartition
from kio.schema.delete_records.v0.request import DeleteRecordsRequest
from kio.schema.delete_records.v0.request import DeleteRecordsTopic
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_delete_records_partition: Final = entity_reader(DeleteRecordsPartition)


@pytest.mark.roundtrip
@given(from_type(DeleteRecordsPartition))
@settings(max_examples=1)
def test_delete_records_partition_roundtrip(instance: DeleteRecordsPartition) -> None:
    writer = entity_writer(DeleteRecordsPartition)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_delete_records_partition(buffer)
    assert instance == result


read_delete_records_topic: Final = entity_reader(DeleteRecordsTopic)


@pytest.mark.roundtrip
@given(from_type(DeleteRecordsTopic))
@settings(max_examples=1)
def test_delete_records_topic_roundtrip(instance: DeleteRecordsTopic) -> None:
    writer = entity_writer(DeleteRecordsTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_delete_records_topic(buffer)
    assert instance == result


read_delete_records_request: Final = entity_reader(DeleteRecordsRequest)


@pytest.mark.roundtrip
@given(from_type(DeleteRecordsRequest))
@settings(max_examples=1)
def test_delete_records_request_roundtrip(instance: DeleteRecordsRequest) -> None:
    writer = entity_writer(DeleteRecordsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_delete_records_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(DeleteRecordsRequest))
def test_delete_records_request_java(
    instance: DeleteRecordsRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
