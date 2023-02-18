from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.create_delegation_token.v0.response import CreateDelegationTokenResponse
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(CreateDelegationTokenResponse))
@settings(max_examples=1)
def test_create_delegation_token_response_roundtrip(
    instance: CreateDelegationTokenResponse,
) -> None:
    writer = entity_writer(CreateDelegationTokenResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(CreateDelegationTokenResponse))
    assert instance == result
