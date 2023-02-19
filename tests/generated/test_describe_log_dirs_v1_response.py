from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.describe_log_dirs.v1.response import DescribeLogDirsPartition
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(DescribeLogDirsPartition))
@settings(max_examples=1)
def test_describe_log_dirs_partition_roundtrip(
    instance: DescribeLogDirsPartition,
) -> None:
    writer = entity_writer(DescribeLogDirsPartition)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DescribeLogDirsPartition))
    assert instance == result


from kio.schema.describe_log_dirs.v1.response import DescribeLogDirsTopic


@given(from_type(DescribeLogDirsTopic))
@settings(max_examples=1)
def test_describe_log_dirs_topic_roundtrip(instance: DescribeLogDirsTopic) -> None:
    writer = entity_writer(DescribeLogDirsTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DescribeLogDirsTopic))
    assert instance == result


from kio.schema.describe_log_dirs.v1.response import DescribeLogDirsResult


@given(from_type(DescribeLogDirsResult))
@settings(max_examples=1)
def test_describe_log_dirs_result_roundtrip(instance: DescribeLogDirsResult) -> None:
    writer = entity_writer(DescribeLogDirsResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DescribeLogDirsResult))
    assert instance == result


from kio.schema.describe_log_dirs.v1.response import DescribeLogDirsResponse


@given(from_type(DescribeLogDirsResponse))
@settings(max_examples=1)
def test_describe_log_dirs_response_roundtrip(
    instance: DescribeLogDirsResponse,
) -> None:
    writer = entity_writer(DescribeLogDirsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DescribeLogDirsResponse))
    assert instance == result
