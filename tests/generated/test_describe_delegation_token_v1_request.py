from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.describe_delegation_token.v1.request import DescribeDelegationTokenOwner
from kio.schema.describe_delegation_token.v1.request import (
    DescribeDelegationTokenRequest,
)
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_describe_delegation_token_owner: Final = entity_reader(
    DescribeDelegationTokenOwner
)


@pytest.mark.roundtrip
@given(from_type(DescribeDelegationTokenOwner))
def test_describe_delegation_token_owner_roundtrip(
    instance: DescribeDelegationTokenOwner,
) -> None:
    writer = entity_writer(DescribeDelegationTokenOwner)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_describe_delegation_token_owner(buffer)
    assert instance == result


read_describe_delegation_token_request: Final = entity_reader(
    DescribeDelegationTokenRequest
)


@pytest.mark.roundtrip
@given(from_type(DescribeDelegationTokenRequest))
def test_describe_delegation_token_request_roundtrip(
    instance: DescribeDelegationTokenRequest,
) -> None:
    writer = entity_writer(DescribeDelegationTokenRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_describe_delegation_token_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(DescribeDelegationTokenRequest))
def test_describe_delegation_token_request_java(
    instance: DescribeDelegationTokenRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
