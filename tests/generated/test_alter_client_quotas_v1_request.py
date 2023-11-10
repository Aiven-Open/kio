from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.alter_client_quotas.v1.request import AlterClientQuotasRequest
from kio.schema.alter_client_quotas.v1.request import EntityData
from kio.schema.alter_client_quotas.v1.request import EntryData
from kio.schema.alter_client_quotas.v1.request import OpData
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_entity_data: Final = entity_reader(EntityData)


@given(from_type(EntityData))
@settings(max_examples=1)
def test_entity_data_roundtrip(instance: EntityData) -> None:
    writer = entity_writer(EntityData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_entity_data(buffer)
    assert instance == result


read_op_data: Final = entity_reader(OpData)


@given(from_type(OpData))
@settings(max_examples=1)
def test_op_data_roundtrip(instance: OpData) -> None:
    writer = entity_writer(OpData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_op_data(buffer)
    assert instance == result


read_entry_data: Final = entity_reader(EntryData)


@given(from_type(EntryData))
@settings(max_examples=1)
def test_entry_data_roundtrip(instance: EntryData) -> None:
    writer = entity_writer(EntryData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_entry_data(buffer)
    assert instance == result


read_alter_client_quotas_request: Final = entity_reader(AlterClientQuotasRequest)


@given(from_type(AlterClientQuotasRequest))
@settings(max_examples=1)
def test_alter_client_quotas_request_roundtrip(
    instance: AlterClientQuotasRequest,
) -> None:
    writer = entity_writer(AlterClientQuotasRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_alter_client_quotas_request(buffer)
    assert instance == result


@given(instance=from_type(AlterClientQuotasRequest))
def test_alter_client_quotas_request_java(
    instance: AlterClientQuotasRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
