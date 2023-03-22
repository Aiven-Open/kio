from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.describe_log_dirs.v1.response import DescribeLogDirsPartition
from kio.schema.describe_log_dirs.v1.response import DescribeLogDirsResponse
from kio.schema.describe_log_dirs.v1.response import DescribeLogDirsResult
from kio.schema.describe_log_dirs.v1.response import DescribeLogDirsTopic
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import setup_buffer

read_describe_log_dirs_partition: Final = entity_reader(DescribeLogDirsPartition)


@given(from_type(DescribeLogDirsPartition))
@settings(max_examples=1)
def test_describe_log_dirs_partition_roundtrip(
    instance: DescribeLogDirsPartition,
) -> None:
    writer = entity_writer(DescribeLogDirsPartition)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_describe_log_dirs_partition(buffer)
    assert instance == result


read_describe_log_dirs_topic: Final = entity_reader(DescribeLogDirsTopic)


@given(from_type(DescribeLogDirsTopic))
@settings(max_examples=1)
def test_describe_log_dirs_topic_roundtrip(instance: DescribeLogDirsTopic) -> None:
    writer = entity_writer(DescribeLogDirsTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_describe_log_dirs_topic(buffer)
    assert instance == result


read_describe_log_dirs_result: Final = entity_reader(DescribeLogDirsResult)


@given(from_type(DescribeLogDirsResult))
@settings(max_examples=1)
def test_describe_log_dirs_result_roundtrip(instance: DescribeLogDirsResult) -> None:
    writer = entity_writer(DescribeLogDirsResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_describe_log_dirs_result(buffer)
    assert instance == result


read_describe_log_dirs_response: Final = entity_reader(DescribeLogDirsResponse)


@given(from_type(DescribeLogDirsResponse))
@settings(max_examples=1)
def test_describe_log_dirs_response_roundtrip(
    instance: DescribeLogDirsResponse,
) -> None:
    writer = entity_writer(DescribeLogDirsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_describe_log_dirs_response(buffer)
    assert instance == result
