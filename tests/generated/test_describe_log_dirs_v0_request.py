from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.describe_log_dirs.v0.request import DescribableLogDirTopic
from kio.schema.describe_log_dirs.v0.request import DescribeLogDirsRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_describable_log_dir_topic: Final = entity_reader(DescribableLogDirTopic)


@given(from_type(DescribableLogDirTopic))
@settings(max_examples=1)
def test_describable_log_dir_topic_roundtrip(instance: DescribableLogDirTopic) -> None:
    writer = entity_writer(DescribableLogDirTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_describable_log_dir_topic(buffer)
    assert instance == result


read_describe_log_dirs_request: Final = entity_reader(DescribeLogDirsRequest)


@given(from_type(DescribeLogDirsRequest))
@settings(max_examples=1)
def test_describe_log_dirs_request_roundtrip(instance: DescribeLogDirsRequest) -> None:
    writer = entity_writer(DescribeLogDirsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_describe_log_dirs_request(buffer)
    assert instance == result


@given(instance=from_type(DescribeLogDirsRequest))
def test_describe_log_dirs_request_java(
    instance: DescribeLogDirsRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
