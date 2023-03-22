from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.delete_records.v2.response import DeleteRecordsPartitionResult
from kio.schema.delete_records.v2.response import DeleteRecordsResponse
from kio.schema.delete_records.v2.response import DeleteRecordsTopicResult
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import setup_buffer

read_delete_records_partition_result: Final = entity_reader(
    DeleteRecordsPartitionResult
)


@given(from_type(DeleteRecordsPartitionResult))
@settings(max_examples=1)
def test_delete_records_partition_result_roundtrip(
    instance: DeleteRecordsPartitionResult,
) -> None:
    writer = entity_writer(DeleteRecordsPartitionResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_delete_records_partition_result(buffer)
    assert instance == result


read_delete_records_topic_result: Final = entity_reader(DeleteRecordsTopicResult)


@given(from_type(DeleteRecordsTopicResult))
@settings(max_examples=1)
def test_delete_records_topic_result_roundtrip(
    instance: DeleteRecordsTopicResult,
) -> None:
    writer = entity_writer(DeleteRecordsTopicResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_delete_records_topic_result(buffer)
    assert instance == result


read_delete_records_response: Final = entity_reader(DeleteRecordsResponse)


@given(from_type(DeleteRecordsResponse))
@settings(max_examples=1)
def test_delete_records_response_roundtrip(instance: DeleteRecordsResponse) -> None:
    writer = entity_writer(DeleteRecordsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_delete_records_response(buffer)
    assert instance == result
