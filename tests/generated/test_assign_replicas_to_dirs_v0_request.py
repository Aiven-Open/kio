from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.assign_replicas_to_dirs.v0.request import AssignReplicasToDirsRequest
from kio.schema.assign_replicas_to_dirs.v0.request import DirectoryData
from kio.schema.assign_replicas_to_dirs.v0.request import PartitionData
from kio.schema.assign_replicas_to_dirs.v0.request import TopicData
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_partition_data: Final = entity_reader(PartitionData)


@pytest.mark.roundtrip
@given(from_type(PartitionData))
def test_partition_data_roundtrip(instance: PartitionData) -> None:
    writer = entity_writer(PartitionData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_partition_data(buffer)
    assert instance == result


read_topic_data: Final = entity_reader(TopicData)


@pytest.mark.roundtrip
@given(from_type(TopicData))
def test_topic_data_roundtrip(instance: TopicData) -> None:
    writer = entity_writer(TopicData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_topic_data(buffer)
    assert instance == result


read_directory_data: Final = entity_reader(DirectoryData)


@pytest.mark.roundtrip
@given(from_type(DirectoryData))
def test_directory_data_roundtrip(instance: DirectoryData) -> None:
    writer = entity_writer(DirectoryData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_directory_data(buffer)
    assert instance == result


read_assign_replicas_to_dirs_request: Final = entity_reader(AssignReplicasToDirsRequest)


@pytest.mark.roundtrip
@given(from_type(AssignReplicasToDirsRequest))
def test_assign_replicas_to_dirs_request_roundtrip(
    instance: AssignReplicasToDirsRequest,
) -> None:
    writer = entity_writer(AssignReplicasToDirsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_assign_replicas_to_dirs_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(AssignReplicasToDirsRequest))
def test_assign_replicas_to_dirs_request_java(
    instance: AssignReplicasToDirsRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
