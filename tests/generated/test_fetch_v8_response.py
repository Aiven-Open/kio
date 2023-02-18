from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.fetch.v8.response import AbortedTransaction
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(AbortedTransaction))
@settings(max_examples=1)
def test_aborted_transaction_roundtrip(instance: AbortedTransaction) -> None:
    writer = entity_writer(AbortedTransaction)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(AbortedTransaction))
    assert instance == result


from kio.schema.fetch.v8.response import PartitionData


@given(from_type(PartitionData))
@settings(max_examples=1)
def test_partition_data_roundtrip(instance: PartitionData) -> None:
    writer = entity_writer(PartitionData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(PartitionData))
    assert instance == result


from kio.schema.fetch.v8.response import FetchableTopicResponse


@given(from_type(FetchableTopicResponse))
@settings(max_examples=1)
def test_fetchable_topic_response_roundtrip(instance: FetchableTopicResponse) -> None:
    writer = entity_writer(FetchableTopicResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(FetchableTopicResponse))
    assert instance == result


from kio.schema.fetch.v8.response import FetchResponse


@given(from_type(FetchResponse))
@settings(max_examples=1)
def test_fetch_response_roundtrip(instance: FetchResponse) -> None:
    writer = entity_writer(FetchResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(FetchResponse))
    assert instance == result
