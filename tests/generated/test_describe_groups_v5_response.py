from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.describe_groups.v5.response import DescribedGroup
from kio.schema.describe_groups.v5.response import DescribedGroupMember
from kio.schema.describe_groups.v5.response import DescribeGroupsResponse
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(DescribedGroupMember))
@settings(max_examples=1)
def test_described_group_member_roundtrip(instance: DescribedGroupMember) -> None:
    writer = entity_writer(DescribedGroupMember)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DescribedGroupMember))
    assert instance == result


@given(from_type(DescribedGroup))
@settings(max_examples=1)
def test_described_group_roundtrip(instance: DescribedGroup) -> None:
    writer = entity_writer(DescribedGroup)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DescribedGroup))
    assert instance == result


@given(from_type(DescribeGroupsResponse))
@settings(max_examples=1)
def test_describe_groups_response_roundtrip(instance: DescribeGroupsResponse) -> None:
    writer = entity_writer(DescribeGroupsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DescribeGroupsResponse))
    assert instance == result
