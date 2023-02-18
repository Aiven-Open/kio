from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.offset_fetch.v8.request import OffsetFetchRequestTopics
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(OffsetFetchRequestTopics))
@settings(max_examples=1)
def test_offset_fetch_request_topics_roundtrip(
    instance: OffsetFetchRequestTopics,
) -> None:
    writer = entity_writer(OffsetFetchRequestTopics)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(OffsetFetchRequestTopics))
    assert instance == result


from kio.schema.offset_fetch.v8.request import OffsetFetchRequestGroup


@given(from_type(OffsetFetchRequestGroup))
@settings(max_examples=1)
def test_offset_fetch_request_group_roundtrip(
    instance: OffsetFetchRequestGroup,
) -> None:
    writer = entity_writer(OffsetFetchRequestGroup)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(OffsetFetchRequestGroup))
    assert instance == result


from kio.schema.offset_fetch.v8.request import OffsetFetchRequest


@given(from_type(OffsetFetchRequest))
@settings(max_examples=1)
def test_offset_fetch_request_roundtrip(instance: OffsetFetchRequest) -> None:
    writer = entity_writer(OffsetFetchRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(OffsetFetchRequest))
    assert instance == result
