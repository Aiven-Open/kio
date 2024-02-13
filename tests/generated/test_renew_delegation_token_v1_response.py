from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.renew_delegation_token.v1.response import RenewDelegationTokenResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_renew_delegation_token_response: Final = entity_reader(
    RenewDelegationTokenResponse
)


@pytest.mark.roundtrip
@given(from_type(RenewDelegationTokenResponse))
def test_renew_delegation_token_response_roundtrip(
    instance: RenewDelegationTokenResponse,
) -> None:
    writer = entity_writer(RenewDelegationTokenResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_renew_delegation_token_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(RenewDelegationTokenResponse))
def test_renew_delegation_token_response_java(
    instance: RenewDelegationTokenResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
