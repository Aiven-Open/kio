from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.renew_delegation_token.v1.request import RenewDelegationTokenRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_renew_delegation_token_request: Final = entity_reader(RenewDelegationTokenRequest)


@pytest.mark.roundtrip
@given(from_type(RenewDelegationTokenRequest))
def test_renew_delegation_token_request_roundtrip(
    instance: RenewDelegationTokenRequest,
) -> None:
    writer = entity_writer(RenewDelegationTokenRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_renew_delegation_token_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(RenewDelegationTokenRequest))
def test_renew_delegation_token_request_java(
    instance: RenewDelegationTokenRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
