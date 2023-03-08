from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.fetch.v1.request import FetchPartition
from kio.schema.fetch.v1.request import FetchRequest
from kio.schema.fetch.v1.request import FetchTopic
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(FetchPartition))
@settings(max_examples=1)
def test_fetch_partition_roundtrip(instance: FetchPartition) -> None:
    writer = entity_writer(FetchPartition)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(FetchPartition))
    assert instance == result


@given(from_type(FetchTopic))
@settings(max_examples=1)
def test_fetch_topic_roundtrip(instance: FetchTopic) -> None:
    writer = entity_writer(FetchTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(FetchTopic))
    assert instance == result


@given(from_type(FetchRequest))
@settings(max_examples=1)
def test_fetch_request_roundtrip(instance: FetchRequest) -> None:
    writer = entity_writer(FetchRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(FetchRequest))
    assert instance == result
