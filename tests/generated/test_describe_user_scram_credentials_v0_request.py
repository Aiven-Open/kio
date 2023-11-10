from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.describe_user_scram_credentials.v0.request import (
    DescribeUserScramCredentialsRequest,
)
from kio.schema.describe_user_scram_credentials.v0.request import UserName
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_user_name: Final = entity_reader(UserName)


@given(from_type(UserName))
@settings(max_examples=1)
def test_user_name_roundtrip(instance: UserName) -> None:
    writer = entity_writer(UserName)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_user_name(buffer)
    assert instance == result


read_describe_user_scram_credentials_request: Final = entity_reader(
    DescribeUserScramCredentialsRequest
)


@given(from_type(DescribeUserScramCredentialsRequest))
@settings(max_examples=1)
def test_describe_user_scram_credentials_request_roundtrip(
    instance: DescribeUserScramCredentialsRequest,
) -> None:
    writer = entity_writer(DescribeUserScramCredentialsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_describe_user_scram_credentials_request(buffer)
    assert instance == result


@given(instance=from_type(DescribeUserScramCredentialsRequest))
def test_describe_user_scram_credentials_request_java(
    instance: DescribeUserScramCredentialsRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
