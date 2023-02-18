from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.offset_fetch.v6.request import OffsetFetchRequestTopic
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(OffsetFetchRequestTopic))
@settings(max_examples=1)
def test_offset_fetch_request_topic_roundtrip(
    instance: OffsetFetchRequestTopic,
) -> None:
    writer = entity_writer(OffsetFetchRequestTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(OffsetFetchRequestTopic))
    assert instance == result


from kio.schema.offset_fetch.v6.request import OffsetFetchRequest


@given(from_type(OffsetFetchRequest))
@settings(max_examples=1)
def test_offset_fetch_request_roundtrip(instance: OffsetFetchRequest) -> None:
    writer = entity_writer(OffsetFetchRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(OffsetFetchRequest))
    assert instance == result
