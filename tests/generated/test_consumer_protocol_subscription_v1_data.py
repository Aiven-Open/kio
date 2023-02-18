from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.consumer_protocol_subscription.v1.data import TopicPartition
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(TopicPartition))
@settings(max_examples=1)
def test_topic_partition_roundtrip(instance: TopicPartition) -> None:
    writer = entity_writer(TopicPartition)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(TopicPartition))
    assert instance == result


from kio.schema.consumer_protocol_subscription.v1.data import (
    ConsumerProtocolSubscription,
)


@given(from_type(ConsumerProtocolSubscription))
@settings(max_examples=1)
def test_consumer_protocol_subscription_roundtrip(
    instance: ConsumerProtocolSubscription,
) -> None:
    writer = entity_writer(ConsumerProtocolSubscription)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(ConsumerProtocolSubscription))
    assert instance == result
