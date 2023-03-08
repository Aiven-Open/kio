from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.alter_replica_log_dirs.v2.response import (
    AlterReplicaLogDirPartitionResult,
)
from kio.schema.alter_replica_log_dirs.v2.response import AlterReplicaLogDirsResponse
from kio.schema.alter_replica_log_dirs.v2.response import AlterReplicaLogDirTopicResult
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(AlterReplicaLogDirPartitionResult))
@settings(max_examples=1)
def test_alter_replica_log_dir_partition_result_roundtrip(
    instance: AlterReplicaLogDirPartitionResult,
) -> None:
    writer = entity_writer(AlterReplicaLogDirPartitionResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(AlterReplicaLogDirPartitionResult))
    assert instance == result


@given(from_type(AlterReplicaLogDirTopicResult))
@settings(max_examples=1)
def test_alter_replica_log_dir_topic_result_roundtrip(
    instance: AlterReplicaLogDirTopicResult,
) -> None:
    writer = entity_writer(AlterReplicaLogDirTopicResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(AlterReplicaLogDirTopicResult))
    assert instance == result


@given(from_type(AlterReplicaLogDirsResponse))
@settings(max_examples=1)
def test_alter_replica_log_dirs_response_roundtrip(
    instance: AlterReplicaLogDirsResponse,
) -> None:
    writer = entity_writer(AlterReplicaLogDirsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(AlterReplicaLogDirsResponse))
    assert instance == result
