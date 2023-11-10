from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.create_delegation_token.v1.response import CreateDelegationTokenResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_create_delegation_token_response: Final = entity_reader(
    CreateDelegationTokenResponse
)


@given(from_type(CreateDelegationTokenResponse))
@settings(max_examples=1)
def test_create_delegation_token_response_roundtrip(
    instance: CreateDelegationTokenResponse,
) -> None:
    writer = entity_writer(CreateDelegationTokenResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_create_delegation_token_response(buffer)
    assert instance == result


@given(instance=from_type(CreateDelegationTokenResponse))
def test_create_delegation_token_response_java(
    instance: CreateDelegationTokenResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
