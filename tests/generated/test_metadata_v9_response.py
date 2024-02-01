from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.metadata.v9.response import MetadataResponse
from kio.schema.metadata.v9.response import MetadataResponseBroker
from kio.schema.metadata.v9.response import MetadataResponsePartition
from kio.schema.metadata.v9.response import MetadataResponseTopic
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_metadata_response_broker: Final = entity_reader(MetadataResponseBroker)


@pytest.mark.roundtrip
@given(from_type(MetadataResponseBroker))
def test_metadata_response_broker_roundtrip(instance: MetadataResponseBroker) -> None:
    writer = entity_writer(MetadataResponseBroker)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_metadata_response_broker(buffer)
    assert instance == result


read_metadata_response_partition: Final = entity_reader(MetadataResponsePartition)


@pytest.mark.roundtrip
@given(from_type(MetadataResponsePartition))
def test_metadata_response_partition_roundtrip(
    instance: MetadataResponsePartition,
) -> None:
    writer = entity_writer(MetadataResponsePartition)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_metadata_response_partition(buffer)
    assert instance == result


read_metadata_response_topic: Final = entity_reader(MetadataResponseTopic)


@pytest.mark.roundtrip
@given(from_type(MetadataResponseTopic))
def test_metadata_response_topic_roundtrip(instance: MetadataResponseTopic) -> None:
    writer = entity_writer(MetadataResponseTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_metadata_response_topic(buffer)
    assert instance == result


read_metadata_response: Final = entity_reader(MetadataResponse)


@pytest.mark.roundtrip
@given(from_type(MetadataResponse))
def test_metadata_response_roundtrip(instance: MetadataResponse) -> None:
    writer = entity_writer(MetadataResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_metadata_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(MetadataResponse))
def test_metadata_response_java(
    instance: MetadataResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
