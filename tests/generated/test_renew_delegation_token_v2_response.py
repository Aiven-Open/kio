from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.renew_delegation_token.v2.response import RenewDelegationTokenResponse
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(RenewDelegationTokenResponse))
@settings(max_examples=1)
def test_renew_delegation_token_response_roundtrip(
    instance: RenewDelegationTokenResponse,
) -> None:
    writer = entity_writer(RenewDelegationTokenResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(RenewDelegationTokenResponse))
    assert instance == result
