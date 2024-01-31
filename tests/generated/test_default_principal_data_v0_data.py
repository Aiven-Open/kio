from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.default_principal_data.v0.data import DefaultPrincipalData
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_default_principal_data: Final = entity_reader(DefaultPrincipalData)


@pytest.mark.roundtrip
@given(from_type(DefaultPrincipalData))
@settings(max_examples=1)
def test_default_principal_data_roundtrip(instance: DefaultPrincipalData) -> None:
    writer = entity_writer(DefaultPrincipalData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_default_principal_data(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(DefaultPrincipalData))
def test_default_principal_data_java(
    instance: DefaultPrincipalData, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
