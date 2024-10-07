from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.share_fetch.v0.request import AcknowledgementBatch
from kio.schema.share_fetch.v0.request import FetchPartition
from kio.schema.share_fetch.v0.request import FetchTopic
from kio.schema.share_fetch.v0.request import ForgottenTopic
from kio.schema.share_fetch.v0.request import ShareFetchRequest
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


read_fetch_partition: Final = entity_reader(FetchPartition)


@pytest.mark.roundtrip
@given(from_type(FetchPartition))
def test_fetch_partition_roundtrip(instance: FetchPartition) -> None:
    writer = entity_writer(FetchPartition)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_fetch_partition(buffer)
    assert instance == result


read_fetch_topic: Final = entity_reader(FetchTopic)


@pytest.mark.roundtrip
@given(from_type(FetchTopic))
def test_fetch_topic_roundtrip(instance: FetchTopic) -> None:
    writer = entity_writer(FetchTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_fetch_topic(buffer)
    assert instance == result


read_forgotten_topic: Final = entity_reader(ForgottenTopic)


@pytest.mark.roundtrip
@given(from_type(ForgottenTopic))
def test_forgotten_topic_roundtrip(instance: ForgottenTopic) -> None:
    writer = entity_writer(ForgottenTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_forgotten_topic(buffer)
    assert instance == result


read_share_fetch_request: Final = entity_reader(ShareFetchRequest)


@pytest.mark.roundtrip
@given(from_type(ShareFetchRequest))
def test_share_fetch_request_roundtrip(instance: ShareFetchRequest) -> None:
    writer = entity_writer(ShareFetchRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_share_fetch_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(ShareFetchRequest))
def test_share_fetch_request_java(
    instance: ShareFetchRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
