from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.expire_delegation_token.v2.response import ExpireDelegationTokenResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import setup_buffer

read_expire_delegation_token_response: Final = entity_reader(
    ExpireDelegationTokenResponse
)


@given(from_type(ExpireDelegationTokenResponse))
@settings(max_examples=1)
def test_expire_delegation_token_response_roundtrip(
    instance: ExpireDelegationTokenResponse,
) -> None:
    writer = entity_writer(ExpireDelegationTokenResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_expire_delegation_token_response(buffer)
    assert instance == result
