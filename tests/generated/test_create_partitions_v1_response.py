from __future__ import annotations

from typing import Final

import pytest
from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.create_partitions.v1.response import CreatePartitionsResponse
from kio.schema.create_partitions.v1.response import CreatePartitionsTopicResult
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_create_partitions_topic_result: Final = entity_reader(CreatePartitionsTopicResult)


@pytest.mark.roundtrip
@given(from_type(CreatePartitionsTopicResult))
@settings(max_examples=1)
def test_create_partitions_topic_result_roundtrip(
    instance: CreatePartitionsTopicResult,
) -> None:
    writer = entity_writer(CreatePartitionsTopicResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_create_partitions_topic_result(buffer)
    assert instance == result


read_create_partitions_response: Final = entity_reader(CreatePartitionsResponse)


@pytest.mark.roundtrip
@given(from_type(CreatePartitionsResponse))
@settings(max_examples=1)
def test_create_partitions_response_roundtrip(
    instance: CreatePartitionsResponse,
) -> None:
    writer = entity_writer(CreatePartitionsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_create_partitions_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(CreatePartitionsResponse))
def test_create_partitions_response_java(
    instance: CreatePartitionsResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
