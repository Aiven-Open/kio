from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.share_acknowledge.v0.request import AcknowledgementBatch
from kio.schema.share_acknowledge.v0.request import AcknowledgePartition
from kio.schema.share_acknowledge.v0.request import AcknowledgeTopic
from kio.schema.share_acknowledge.v0.request import ShareAcknowledgeRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_acknowledgement_batch: Final = entity_reader(AcknowledgementBatch)


@pytest.mark.roundtrip
@given(from_type(AcknowledgementBatch))
def test_acknowledgement_batch_roundtrip(instance: AcknowledgementBatch) -> None:
    writer = entity_writer(AcknowledgementBatch)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_acknowledgement_batch(buffer)
    assert instance == result


read_acknowledge_partition: Final = entity_reader(AcknowledgePartition)


@pytest.mark.roundtrip
@given(from_type(AcknowledgePartition))
def test_acknowledge_partition_roundtrip(instance: AcknowledgePartition) -> None:
    writer = entity_writer(AcknowledgePartition)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_acknowledge_partition(buffer)
    assert instance == result


read_acknowledge_topic: Final = entity_reader(AcknowledgeTopic)


@pytest.mark.roundtrip
@given(from_type(AcknowledgeTopic))
def test_acknowledge_topic_roundtrip(instance: AcknowledgeTopic) -> None:
    writer = entity_writer(AcknowledgeTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_acknowledge_topic(buffer)
    assert instance == result


read_share_acknowledge_request: Final = entity_reader(ShareAcknowledgeRequest)


@pytest.mark.roundtrip
@given(from_type(ShareAcknowledgeRequest))
def test_share_acknowledge_request_roundtrip(instance: ShareAcknowledgeRequest) -> None:
    writer = entity_writer(ShareAcknowledgeRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_share_acknowledge_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(ShareAcknowledgeRequest))
def test_share_acknowledge_request_java(
    instance: ShareAcknowledgeRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
