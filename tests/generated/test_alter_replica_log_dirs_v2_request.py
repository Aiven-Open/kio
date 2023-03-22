from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.alter_replica_log_dirs.v2.request import AlterReplicaLogDir
from kio.schema.alter_replica_log_dirs.v2.request import AlterReplicaLogDirsRequest
from kio.schema.alter_replica_log_dirs.v2.request import AlterReplicaLogDirTopic
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import setup_buffer

read_alter_replica_log_dir_topic: Final = entity_reader(AlterReplicaLogDirTopic)


@given(from_type(AlterReplicaLogDirTopic))
@settings(max_examples=1)
def test_alter_replica_log_dir_topic_roundtrip(
    instance: AlterReplicaLogDirTopic,
) -> None:
    writer = entity_writer(AlterReplicaLogDirTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_alter_replica_log_dir_topic(buffer)
    assert instance == result


read_alter_replica_log_dir: Final = entity_reader(AlterReplicaLogDir)


@given(from_type(AlterReplicaLogDir))
@settings(max_examples=1)
def test_alter_replica_log_dir_roundtrip(instance: AlterReplicaLogDir) -> None:
    writer = entity_writer(AlterReplicaLogDir)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_alter_replica_log_dir(buffer)
    assert instance == result


read_alter_replica_log_dirs_request: Final = entity_reader(AlterReplicaLogDirsRequest)


@given(from_type(AlterReplicaLogDirsRequest))
@settings(max_examples=1)
def test_alter_replica_log_dirs_request_roundtrip(
    instance: AlterReplicaLogDirsRequest,
) -> None:
    writer = entity_writer(AlterReplicaLogDirsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_alter_replica_log_dirs_request(buffer)
    assert instance == result
