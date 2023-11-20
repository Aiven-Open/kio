from __future__ import annotations

from typing import Final

import pytest
from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.metadata.v0.request import MetadataRequest
from kio.schema.metadata.v0.request import MetadataRequestTopic
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_metadata_request_topic: Final = entity_reader(MetadataRequestTopic)


@pytest.mark.roundtrip
@given(from_type(MetadataRequestTopic))
@settings(max_examples=1)
def test_metadata_request_topic_roundtrip(instance: MetadataRequestTopic) -> None:
    writer = entity_writer(MetadataRequestTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_metadata_request_topic(buffer)
    assert instance == result


read_metadata_request: Final = entity_reader(MetadataRequest)


@pytest.mark.roundtrip
@given(from_type(MetadataRequest))
@settings(max_examples=1)
def test_metadata_request_roundtrip(instance: MetadataRequest) -> None:
    writer = entity_writer(MetadataRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_metadata_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(MetadataRequest))
def test_metadata_request_java(
    instance: MetadataRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
