from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.describe_client_quotas.v1.response import DescribeClientQuotasResponse
from kio.schema.describe_client_quotas.v1.response import EntityData
from kio.schema.describe_client_quotas.v1.response import EntryData
from kio.schema.describe_client_quotas.v1.response import ValueData
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


read_value_data: Final = entity_reader(ValueData)


@pytest.mark.roundtrip
@given(from_type(ValueData))
@settings(max_examples=1)
def test_value_data_roundtrip(instance: ValueData) -> None:
    writer = entity_writer(ValueData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_value_data(buffer)
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


read_describe_client_quotas_response: Final = entity_reader(
    DescribeClientQuotasResponse
)


@pytest.mark.roundtrip
@given(from_type(DescribeClientQuotasResponse))
@settings(max_examples=1)
def test_describe_client_quotas_response_roundtrip(
    instance: DescribeClientQuotasResponse,
) -> None:
    writer = entity_writer(DescribeClientQuotasResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_describe_client_quotas_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(DescribeClientQuotasResponse))
def test_describe_client_quotas_response_java(
    instance: DescribeClientQuotasResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
