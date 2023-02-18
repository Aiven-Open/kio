from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.describe_cluster.v0.response import DescribeClusterBroker
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(DescribeClusterBroker))
@settings(max_examples=1)
def test_describe_cluster_broker_roundtrip(instance: DescribeClusterBroker) -> None:
    writer = entity_writer(DescribeClusterBroker)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DescribeClusterBroker))
    assert instance == result


from kio.schema.describe_cluster.v0.response import DescribeClusterResponse


@given(from_type(DescribeClusterResponse))
@settings(max_examples=1)
def test_describe_cluster_response_roundtrip(instance: DescribeClusterResponse) -> None:
    writer = entity_writer(DescribeClusterResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DescribeClusterResponse))
    assert instance == result
