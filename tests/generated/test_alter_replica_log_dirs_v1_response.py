from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.alter_replica_log_dirs.v1.response import (
    AlterReplicaLogDirPartitionResult,
)
from kio.schema.alter_replica_log_dirs.v1.response import AlterReplicaLogDirsResponse
from kio.schema.alter_replica_log_dirs.v1.response import AlterReplicaLogDirTopicResult
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_alter_replica_log_dir_partition_result: Final = entity_reader(
    AlterReplicaLogDirPartitionResult
)


@pytest.mark.roundtrip
@given(from_type(AlterReplicaLogDirPartitionResult))
@settings(max_examples=1)
def test_alter_replica_log_dir_partition_result_roundtrip(
    instance: AlterReplicaLogDirPartitionResult,
) -> None:
    writer = entity_writer(AlterReplicaLogDirPartitionResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_alter_replica_log_dir_partition_result(buffer)
    assert instance == result


read_alter_replica_log_dir_topic_result: Final = entity_reader(
    AlterReplicaLogDirTopicResult
)


@pytest.mark.roundtrip
@given(from_type(AlterReplicaLogDirTopicResult))
@settings(max_examples=1)
def test_alter_replica_log_dir_topic_result_roundtrip(
    instance: AlterReplicaLogDirTopicResult,
) -> None:
    writer = entity_writer(AlterReplicaLogDirTopicResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_alter_replica_log_dir_topic_result(buffer)
    assert instance == result


read_alter_replica_log_dirs_response: Final = entity_reader(AlterReplicaLogDirsResponse)


@pytest.mark.roundtrip
@given(from_type(AlterReplicaLogDirsResponse))
@settings(max_examples=1)
def test_alter_replica_log_dirs_response_roundtrip(
    instance: AlterReplicaLogDirsResponse,
) -> None:
    writer = entity_writer(AlterReplicaLogDirsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_alter_replica_log_dirs_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(AlterReplicaLogDirsResponse))
def test_alter_replica_log_dirs_response_java(
    instance: AlterReplicaLogDirsResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
