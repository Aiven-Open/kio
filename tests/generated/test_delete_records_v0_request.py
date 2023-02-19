from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.delete_records.v0.request import DeleteRecordsPartition
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(DeleteRecordsPartition))
@settings(max_examples=1)
def test_delete_records_partition_roundtrip(instance: DeleteRecordsPartition) -> None:
    writer = entity_writer(DeleteRecordsPartition)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DeleteRecordsPartition))
    assert instance == result


from kio.schema.delete_records.v0.request import DeleteRecordsTopic


@given(from_type(DeleteRecordsTopic))
@settings(max_examples=1)
def test_delete_records_topic_roundtrip(instance: DeleteRecordsTopic) -> None:
    writer = entity_writer(DeleteRecordsTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DeleteRecordsTopic))
    assert instance == result


from kio.schema.delete_records.v0.request import DeleteRecordsRequest


@given(from_type(DeleteRecordsRequest))
@settings(max_examples=1)
def test_delete_records_request_roundtrip(instance: DeleteRecordsRequest) -> None:
    writer = entity_writer(DeleteRecordsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DeleteRecordsRequest))
    assert instance == result
