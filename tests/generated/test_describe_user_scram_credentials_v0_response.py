from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.describe_user_scram_credentials.v0.response import CredentialInfo
from kio.schema.describe_user_scram_credentials.v0.response import (
    DescribeUserScramCredentialsResponse,
)
from kio.schema.describe_user_scram_credentials.v0.response import (
    DescribeUserScramCredentialsResult,
)
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_credential_info: Final = entity_reader(CredentialInfo)


@pytest.mark.roundtrip
@given(from_type(CredentialInfo))
@settings(max_examples=1)
def test_credential_info_roundtrip(instance: CredentialInfo) -> None:
    writer = entity_writer(CredentialInfo)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_credential_info(buffer)
    assert instance == result


read_describe_user_scram_credentials_result: Final = entity_reader(
    DescribeUserScramCredentialsResult
)


@pytest.mark.roundtrip
@given(from_type(DescribeUserScramCredentialsResult))
@settings(max_examples=1)
def test_describe_user_scram_credentials_result_roundtrip(
    instance: DescribeUserScramCredentialsResult,
) -> None:
    writer = entity_writer(DescribeUserScramCredentialsResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_describe_user_scram_credentials_result(buffer)
    assert instance == result


read_describe_user_scram_credentials_response: Final = entity_reader(
    DescribeUserScramCredentialsResponse
)


@pytest.mark.roundtrip
@given(from_type(DescribeUserScramCredentialsResponse))
@settings(max_examples=1)
def test_describe_user_scram_credentials_response_roundtrip(
    instance: DescribeUserScramCredentialsResponse,
) -> None:
    writer = entity_writer(DescribeUserScramCredentialsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_describe_user_scram_credentials_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(DescribeUserScramCredentialsResponse))
def test_describe_user_scram_credentials_response_java(
    instance: DescribeUserScramCredentialsResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
