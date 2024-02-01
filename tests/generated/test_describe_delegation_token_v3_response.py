from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.describe_delegation_token.v3.response import DescribedDelegationToken
from kio.schema.describe_delegation_token.v3.response import (
    DescribedDelegationTokenRenewer,
)
from kio.schema.describe_delegation_token.v3.response import (
    DescribeDelegationTokenResponse,
)
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_described_delegation_token_renewer: Final = entity_reader(
    DescribedDelegationTokenRenewer
)


@pytest.mark.roundtrip
@given(from_type(DescribedDelegationTokenRenewer))
@settings(max_examples=1)
def test_described_delegation_token_renewer_roundtrip(
    instance: DescribedDelegationTokenRenewer,
) -> None:
    writer = entity_writer(DescribedDelegationTokenRenewer)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_described_delegation_token_renewer(buffer)
    assert instance == result


read_described_delegation_token: Final = entity_reader(DescribedDelegationToken)


@pytest.mark.roundtrip
@given(from_type(DescribedDelegationToken))
@settings(max_examples=1)
def test_described_delegation_token_roundtrip(
    instance: DescribedDelegationToken,
) -> None:
    writer = entity_writer(DescribedDelegationToken)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_described_delegation_token(buffer)
    assert instance == result


read_describe_delegation_token_response: Final = entity_reader(
    DescribeDelegationTokenResponse
)


@pytest.mark.roundtrip
@given(from_type(DescribeDelegationTokenResponse))
@settings(max_examples=1)
def test_describe_delegation_token_response_roundtrip(
    instance: DescribeDelegationTokenResponse,
) -> None:
    writer = entity_writer(DescribeDelegationTokenResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_describe_delegation_token_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(DescribeDelegationTokenResponse))
def test_describe_delegation_token_response_java(
    instance: DescribeDelegationTokenResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
