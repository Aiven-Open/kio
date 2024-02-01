from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.alter_user_scram_credentials.v0.response import (
    AlterUserScramCredentialsResponse,
)
from kio.schema.alter_user_scram_credentials.v0.response import (
    AlterUserScramCredentialsResult,
)
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_alter_user_scram_credentials_result: Final = entity_reader(
    AlterUserScramCredentialsResult
)


@pytest.mark.roundtrip
@given(from_type(AlterUserScramCredentialsResult))
@settings(max_examples=1)
def test_alter_user_scram_credentials_result_roundtrip(
    instance: AlterUserScramCredentialsResult,
) -> None:
    writer = entity_writer(AlterUserScramCredentialsResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_alter_user_scram_credentials_result(buffer)
    assert instance == result


read_alter_user_scram_credentials_response: Final = entity_reader(
    AlterUserScramCredentialsResponse
)


@pytest.mark.roundtrip
@given(from_type(AlterUserScramCredentialsResponse))
@settings(max_examples=1)
def test_alter_user_scram_credentials_response_roundtrip(
    instance: AlterUserScramCredentialsResponse,
) -> None:
    writer = entity_writer(AlterUserScramCredentialsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_alter_user_scram_credentials_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(AlterUserScramCredentialsResponse))
def test_alter_user_scram_credentials_response_java(
    instance: AlterUserScramCredentialsResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
