from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.alter_client_quotas.v1.response import AlterClientQuotasResponse
from kio.schema.alter_client_quotas.v1.response import EntityData
from kio.schema.alter_client_quotas.v1.response import EntryData
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_entity_data: Final = entity_reader(EntityData)


@pytest.mark.roundtrip
@given(from_type(EntityData))
@settings(max_examples=1)
def test_entity_data_roundtrip(instance: EntityData) -> None:
    writer = entity_writer(EntityData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_entity_data(buffer)
    assert instance == result


read_entry_data: Final = entity_reader(EntryData)


@pytest.mark.roundtrip
@given(from_type(EntryData))
@settings(max_examples=1)
def test_entry_data_roundtrip(instance: EntryData) -> None:
    writer = entity_writer(EntryData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_entry_data(buffer)
    assert instance == result


read_alter_client_quotas_response: Final = entity_reader(AlterClientQuotasResponse)


@pytest.mark.roundtrip
@given(from_type(AlterClientQuotasResponse))
@settings(max_examples=1)
def test_alter_client_quotas_response_roundtrip(
    instance: AlterClientQuotasResponse,
) -> None:
    writer = entity_writer(AlterClientQuotasResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_alter_client_quotas_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(AlterClientQuotasResponse))
def test_alter_client_quotas_response_java(
    instance: AlterClientQuotasResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
