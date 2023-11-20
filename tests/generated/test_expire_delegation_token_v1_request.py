from __future__ import annotations

from typing import Final

import pytest
from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.expire_delegation_token.v1.request import ExpireDelegationTokenRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_expire_delegation_token_request: Final = entity_reader(
    ExpireDelegationTokenRequest
)


@pytest.mark.roundtrip
@given(from_type(ExpireDelegationTokenRequest))
@settings(max_examples=1)
def test_expire_delegation_token_request_roundtrip(
    instance: ExpireDelegationTokenRequest,
) -> None:
    writer = entity_writer(ExpireDelegationTokenRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_expire_delegation_token_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(ExpireDelegationTokenRequest))
def test_expire_delegation_token_request_java(
    instance: ExpireDelegationTokenRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
