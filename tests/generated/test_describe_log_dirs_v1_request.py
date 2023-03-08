from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.describe_log_dirs.v1.request import DescribableLogDirTopic
from kio.schema.describe_log_dirs.v1.request import DescribeLogDirsRequest
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(DescribableLogDirTopic))
@settings(max_examples=1)
def test_describable_log_dir_topic_roundtrip(instance: DescribableLogDirTopic) -> None:
    writer = entity_writer(DescribableLogDirTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DescribableLogDirTopic))
    assert instance == result


@given(from_type(DescribeLogDirsRequest))
@settings(max_examples=1)
def test_describe_log_dirs_request_roundtrip(instance: DescribeLogDirsRequest) -> None:
    writer = entity_writer(DescribeLogDirsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DescribeLogDirsRequest))
    assert instance == result
