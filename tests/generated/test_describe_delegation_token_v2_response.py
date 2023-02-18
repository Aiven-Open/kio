from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.describe_delegation_token.v2.response import (
    DescribedDelegationTokenRenewer,
)
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(DescribedDelegationTokenRenewer))
@settings(max_examples=1)
def test_described_delegation_token_renewer_roundtrip(
    instance: DescribedDelegationTokenRenewer,
) -> None:
    writer = entity_writer(DescribedDelegationTokenRenewer)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DescribedDelegationTokenRenewer))
    assert instance == result


from kio.schema.describe_delegation_token.v2.response import DescribedDelegationToken


@given(from_type(DescribedDelegationToken))
@settings(max_examples=1)
def test_described_delegation_token_roundtrip(
    instance: DescribedDelegationToken,
) -> None:
    writer = entity_writer(DescribedDelegationToken)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DescribedDelegationToken))
    assert instance == result


from kio.schema.describe_delegation_token.v2.response import (
    DescribeDelegationTokenResponse,
)


@given(from_type(DescribeDelegationTokenResponse))
@settings(max_examples=1)
def test_describe_delegation_token_response_roundtrip(
    instance: DescribeDelegationTokenResponse,
) -> None:
    writer = entity_writer(DescribeDelegationTokenResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DescribeDelegationTokenResponse))
    assert instance == result
