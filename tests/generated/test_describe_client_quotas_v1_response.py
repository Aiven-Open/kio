from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.describe_client_quotas.v1.response import DescribeClientQuotasResponse
from kio.schema.describe_client_quotas.v1.response import EntityData
from kio.schema.describe_client_quotas.v1.response import EntryData
from kio.schema.describe_client_quotas.v1.response import ValueData
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(EntityData))
@settings(max_examples=1)
def test_entity_data_roundtrip(instance: EntityData) -> None:
    writer = entity_writer(EntityData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(EntityData))
    assert instance == result


@given(from_type(ValueData))
@settings(max_examples=1)
def test_value_data_roundtrip(instance: ValueData) -> None:
    writer = entity_writer(ValueData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(ValueData))
    assert instance == result


@given(from_type(EntryData))
@settings(max_examples=1)
def test_entry_data_roundtrip(instance: EntryData) -> None:
    writer = entity_writer(EntryData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(EntryData))
    assert instance == result


@given(from_type(DescribeClientQuotasResponse))
@settings(max_examples=1)
def test_describe_client_quotas_response_roundtrip(
    instance: DescribeClientQuotasResponse,
) -> None:
    writer = entity_writer(DescribeClientQuotasResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DescribeClientQuotasResponse))
    assert instance == result
