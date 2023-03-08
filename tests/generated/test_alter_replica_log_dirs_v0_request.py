from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.alter_replica_log_dirs.v0.request import AlterReplicaLogDir
from kio.schema.alter_replica_log_dirs.v0.request import AlterReplicaLogDirsRequest
from kio.schema.alter_replica_log_dirs.v0.request import AlterReplicaLogDirTopic
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(AlterReplicaLogDirTopic))
@settings(max_examples=1)
def test_alter_replica_log_dir_topic_roundtrip(
    instance: AlterReplicaLogDirTopic,
) -> None:
    writer = entity_writer(AlterReplicaLogDirTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(AlterReplicaLogDirTopic))
    assert instance == result


@given(from_type(AlterReplicaLogDir))
@settings(max_examples=1)
def test_alter_replica_log_dir_roundtrip(instance: AlterReplicaLogDir) -> None:
    writer = entity_writer(AlterReplicaLogDir)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(AlterReplicaLogDir))
    assert instance == result


@given(from_type(AlterReplicaLogDirsRequest))
@settings(max_examples=1)
def test_alter_replica_log_dirs_request_roundtrip(
    instance: AlterReplicaLogDirsRequest,
) -> None:
    writer = entity_writer(AlterReplicaLogDirsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(AlterReplicaLogDirsRequest))
    assert instance == result
