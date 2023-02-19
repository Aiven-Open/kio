from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.delete_records.v1.response import DeleteRecordsPartitionResult
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(DeleteRecordsPartitionResult))
@settings(max_examples=1)
def test_delete_records_partition_result_roundtrip(
    instance: DeleteRecordsPartitionResult,
) -> None:
    writer = entity_writer(DeleteRecordsPartitionResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DeleteRecordsPartitionResult))
    assert instance == result


from kio.schema.delete_records.v1.response import DeleteRecordsTopicResult


@given(from_type(DeleteRecordsTopicResult))
@settings(max_examples=1)
def test_delete_records_topic_result_roundtrip(
    instance: DeleteRecordsTopicResult,
) -> None:
    writer = entity_writer(DeleteRecordsTopicResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DeleteRecordsTopicResult))
    assert instance == result


from kio.schema.delete_records.v1.response import DeleteRecordsResponse


@given(from_type(DeleteRecordsResponse))
@settings(max_examples=1)
def test_delete_records_response_roundtrip(instance: DeleteRecordsResponse) -> None:
    writer = entity_writer(DeleteRecordsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DeleteRecordsResponse))
    assert instance == result
