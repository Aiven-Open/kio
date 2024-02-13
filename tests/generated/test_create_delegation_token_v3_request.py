from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.create_delegation_token.v3.request import CreatableRenewers
from kio.schema.create_delegation_token.v3.request import CreateDelegationTokenRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_creatable_renewers: Final = entity_reader(CreatableRenewers)


@pytest.mark.roundtrip
@given(from_type(CreatableRenewers))
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


@pytest.mark.roundtrip
@given(from_type(CreateDelegationTokenRequest))
def test_create_delegation_token_request_roundtrip(
    instance: CreateDelegationTokenRequest,
) -> None:
    writer = entity_writer(CreateDelegationTokenRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_create_delegation_token_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(CreateDelegationTokenRequest))
def test_create_delegation_token_request_java(
    instance: CreateDelegationTokenRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
