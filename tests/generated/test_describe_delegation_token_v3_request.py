from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.describe_delegation_token.v3.request import DescribeDelegationTokenOwner
from kio.schema.describe_delegation_token.v3.request import (
    DescribeDelegationTokenRequest,
)
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(DescribeDelegationTokenOwner))
@settings(max_examples=1)
def test_describe_delegation_token_owner_roundtrip(
    instance: DescribeDelegationTokenOwner,
) -> None:
    writer = entity_writer(DescribeDelegationTokenOwner)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DescribeDelegationTokenOwner))
    assert instance == result


@given(from_type(DescribeDelegationTokenRequest))
@settings(max_examples=1)
def test_describe_delegation_token_request_roundtrip(
    instance: DescribeDelegationTokenRequest,
) -> None:
    writer = entity_writer(DescribeDelegationTokenRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DescribeDelegationTokenRequest))
    assert instance == result
