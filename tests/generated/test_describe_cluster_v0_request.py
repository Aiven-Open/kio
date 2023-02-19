from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.describe_cluster.v0.request import DescribeClusterRequest
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(DescribeClusterRequest))
@settings(max_examples=1)
def test_describe_cluster_request_roundtrip(instance: DescribeClusterRequest) -> None:
    writer = entity_writer(DescribeClusterRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DescribeClusterRequest))
    assert instance == result
