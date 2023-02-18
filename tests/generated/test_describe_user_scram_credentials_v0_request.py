from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.describe_user_scram_credentials.v0.request import UserName
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(UserName))
@settings(max_examples=1)
def test_user_name_roundtrip(instance: UserName) -> None:
    writer = entity_writer(UserName)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(UserName))
    assert instance == result


from kio.schema.describe_user_scram_credentials.v0.request import (
    DescribeUserScramCredentialsRequest,
)


@given(from_type(DescribeUserScramCredentialsRequest))
@settings(max_examples=1)
def test_describe_user_scram_credentials_request_roundtrip(
    instance: DescribeUserScramCredentialsRequest,
) -> None:
    writer = entity_writer(DescribeUserScramCredentialsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DescribeUserScramCredentialsRequest))
    assert instance == result
