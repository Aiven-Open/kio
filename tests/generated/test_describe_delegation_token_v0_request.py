from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.describe_delegation_token.v0.request import DescribeDelegationTokenOwner
from kio.schema.describe_delegation_token.v0.request import (
    DescribeDelegationTokenRequest,
)
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import setup_buffer

read_describe_delegation_token_owner: Final = entity_reader(
    DescribeDelegationTokenOwner
)


@given(from_type(DescribeDelegationTokenOwner))
@settings(max_examples=1)
def test_describe_delegation_token_owner_roundtrip(
    instance: DescribeDelegationTokenOwner,
) -> None:
    writer = entity_writer(DescribeDelegationTokenOwner)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_describe_delegation_token_owner(buffer)
    assert instance == result


read_describe_delegation_token_request: Final = entity_reader(
    DescribeDelegationTokenRequest
)


@given(from_type(DescribeDelegationTokenRequest))
@settings(max_examples=1)
def test_describe_delegation_token_request_roundtrip(
    instance: DescribeDelegationTokenRequest,
) -> None:
    writer = entity_writer(DescribeDelegationTokenRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_describe_delegation_token_request(buffer)
    assert instance == result
