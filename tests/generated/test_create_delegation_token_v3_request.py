from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.create_delegation_token.v3.request import CreatableRenewers
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(CreatableRenewers))
@settings(max_examples=1)
def test_creatable_renewers_roundtrip(instance: CreatableRenewers) -> None:
    writer = entity_writer(CreatableRenewers)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(CreatableRenewers))
    assert instance == result


from kio.schema.create_delegation_token.v3.request import CreateDelegationTokenRequest


@given(from_type(CreateDelegationTokenRequest))
@settings(max_examples=1)
def test_create_delegation_token_request_roundtrip(
    instance: CreateDelegationTokenRequest,
) -> None:
    writer = entity_writer(CreateDelegationTokenRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(CreateDelegationTokenRequest))
    assert instance == result
