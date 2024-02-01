from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.expire_delegation_token.v2.response import ExpireDelegationTokenResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_expire_delegation_token_response: Final = entity_reader(
    ExpireDelegationTokenResponse
)


@pytest.mark.roundtrip
@given(from_type(ExpireDelegationTokenResponse))
def test_expire_delegation_token_response_roundtrip(
    instance: ExpireDelegationTokenResponse,
) -> None:
    writer = entity_writer(ExpireDelegationTokenResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_expire_delegation_token_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(ExpireDelegationTokenResponse))
def test_expire_delegation_token_response_java(
    instance: ExpireDelegationTokenResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
