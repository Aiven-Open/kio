from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.renew_delegation_token.v1.request import RenewDelegationTokenRequest
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(RenewDelegationTokenRequest))
@settings(max_examples=1)
def test_renew_delegation_token_request_roundtrip(
    instance: RenewDelegationTokenRequest,
) -> None:
    writer = entity_writer(RenewDelegationTokenRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(RenewDelegationTokenRequest))
    assert instance == result
