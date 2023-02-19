from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.stop_replica.v1.request import StopReplicaTopicV1
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(StopReplicaTopicV1))
@settings(max_examples=1)
def test_stop_replica_topic_v1_roundtrip(instance: StopReplicaTopicV1) -> None:
    writer = entity_writer(StopReplicaTopicV1)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(StopReplicaTopicV1))
    assert instance == result


from kio.schema.stop_replica.v1.request import StopReplicaRequest


@given(from_type(StopReplicaRequest))
@settings(max_examples=1)
def test_stop_replica_request_roundtrip(instance: StopReplicaRequest) -> None:
    writer = entity_writer(StopReplicaRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(StopReplicaRequest))
    assert instance == result
