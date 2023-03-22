from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.create_delegation_token.v0.request import CreatableRenewers
from kio.schema.create_delegation_token.v0.request import CreateDelegationTokenRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import setup_buffer

read_creatable_renewers: Final = entity_reader(CreatableRenewers)


@given(from_type(CreatableRenewers))
@settings(max_examples=1)
def test_creatable_renewers_roundtrip(instance: CreatableRenewers) -> None:
    writer = entity_writer(CreatableRenewers)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_creatable_renewers(buffer)
    assert instance == result


read_create_delegation_token_request: Final = entity_reader(
    CreateDelegationTokenRequest
)


@given(from_type(CreateDelegationTokenRequest))
@settings(max_examples=1)
def test_create_delegation_token_request_roundtrip(
    instance: CreateDelegationTokenRequest,
) -> None:
    writer = entity_writer(CreateDelegationTokenRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_create_delegation_token_request(buffer)
    assert instance == result
