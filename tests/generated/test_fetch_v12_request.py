from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.fetch.v12.request import FetchPartition
from kio.schema.fetch.v12.request import FetchRequest
from kio.schema.fetch.v12.request import FetchTopic
from kio.schema.fetch.v12.request import ForgottenTopic
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import setup_buffer

read_fetch_partition: Final = entity_reader(FetchPartition)


@given(from_type(FetchPartition))
@settings(max_examples=1)
def test_fetch_partition_roundtrip(instance: FetchPartition) -> None:
    writer = entity_writer(FetchPartition)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_fetch_partition(buffer)
    assert instance == result


read_fetch_topic: Final = entity_reader(FetchTopic)


@given(from_type(FetchTopic))
@settings(max_examples=1)
def test_fetch_topic_roundtrip(instance: FetchTopic) -> None:
    writer = entity_writer(FetchTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_fetch_topic(buffer)
    assert instance == result


read_forgotten_topic: Final = entity_reader(ForgottenTopic)


@given(from_type(ForgottenTopic))
@settings(max_examples=1)
def test_forgotten_topic_roundtrip(instance: ForgottenTopic) -> None:
    writer = entity_writer(ForgottenTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_forgotten_topic(buffer)
    assert instance == result


read_fetch_request: Final = entity_reader(FetchRequest)


@given(from_type(FetchRequest))
@settings(max_examples=1)
def test_fetch_request_roundtrip(instance: FetchRequest) -> None:
    writer = entity_writer(FetchRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_fetch_request(buffer)
    assert instance == result
