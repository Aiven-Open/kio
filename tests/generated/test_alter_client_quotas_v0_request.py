from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.alter_client_quotas.v0.request import EntityData
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


from kio.schema.alter_client_quotas.v0.request import OpData


@given(from_type(OpData))
@settings(max_examples=1)
def test_op_data_roundtrip(instance: OpData) -> None:
    writer = entity_writer(OpData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(OpData))
    assert instance == result


from kio.schema.alter_client_quotas.v0.request import EntryData


@given(from_type(EntryData))
@settings(max_examples=1)
def test_entry_data_roundtrip(instance: EntryData) -> None:
    writer = entity_writer(EntryData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(EntryData))
    assert instance == result


from kio.schema.alter_client_quotas.v0.request import AlterClientQuotasRequest


@given(from_type(AlterClientQuotasRequest))
@settings(max_examples=1)
def test_alter_client_quotas_request_roundtrip(
    instance: AlterClientQuotasRequest,
) -> None:
    writer = entity_writer(AlterClientQuotasRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(AlterClientQuotasRequest))
    assert instance == result
