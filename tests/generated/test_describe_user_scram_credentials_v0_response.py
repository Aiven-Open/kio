from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.describe_user_scram_credentials.v0.response import CredentialInfo
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(CredentialInfo))
@settings(max_examples=1)
def test_credential_info_roundtrip(instance: CredentialInfo) -> None:
    writer = entity_writer(CredentialInfo)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(CredentialInfo))
    assert instance == result


from kio.schema.describe_user_scram_credentials.v0.response import (
    DescribeUserScramCredentialsResult,
)


@given(from_type(DescribeUserScramCredentialsResult))
@settings(max_examples=1)
def test_describe_user_scram_credentials_result_roundtrip(
    instance: DescribeUserScramCredentialsResult,
) -> None:
    writer = entity_writer(DescribeUserScramCredentialsResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DescribeUserScramCredentialsResult))
    assert instance == result


from kio.schema.describe_user_scram_credentials.v0.response import (
    DescribeUserScramCredentialsResponse,
)


@given(from_type(DescribeUserScramCredentialsResponse))
@settings(max_examples=1)
def test_describe_user_scram_credentials_response_roundtrip(
    instance: DescribeUserScramCredentialsResponse,
) -> None:
    writer = entity_writer(DescribeUserScramCredentialsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DescribeUserScramCredentialsResponse))
    assert instance == result
