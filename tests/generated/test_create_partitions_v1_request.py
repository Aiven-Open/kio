from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.create_partitions.v1.request import CreatePartitionsAssignment
from kio.schema.create_partitions.v1.request import CreatePartitionsRequest
from kio.schema.create_partitions.v1.request import CreatePartitionsTopic
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_create_partitions_assignment: Final = entity_reader(CreatePartitionsAssignment)


@pytest.mark.roundtrip
@given(from_type(CreatePartitionsAssignment))
@settings(max_examples=1)
def test_create_partitions_assignment_roundtrip(
    instance: CreatePartitionsAssignment,
) -> None:
    writer = entity_writer(CreatePartitionsAssignment)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_create_partitions_assignment(buffer)
    assert instance == result


read_create_partitions_topic: Final = entity_reader(CreatePartitionsTopic)


@pytest.mark.roundtrip
@given(from_type(CreatePartitionsTopic))
@settings(max_examples=1)
def test_create_partitions_topic_roundtrip(instance: CreatePartitionsTopic) -> None:
    writer = entity_writer(CreatePartitionsTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_create_partitions_topic(buffer)
    assert instance == result


read_create_partitions_request: Final = entity_reader(CreatePartitionsRequest)


@pytest.mark.roundtrip
@given(from_type(CreatePartitionsRequest))
@settings(max_examples=1)
def test_create_partitions_request_roundtrip(instance: CreatePartitionsRequest) -> None:
    writer = entity_writer(CreatePartitionsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_create_partitions_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(CreatePartitionsRequest))
def test_create_partitions_request_java(
    instance: CreatePartitionsRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
