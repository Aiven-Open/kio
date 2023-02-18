from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.describe_client_quotas.v0.request import ComponentData
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(ComponentData))
@settings(max_examples=1)
def test_component_data_roundtrip(instance: ComponentData) -> None:
    writer = entity_writer(ComponentData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(ComponentData))
    assert instance == result


from kio.schema.describe_client_quotas.v0.request import DescribeClientQuotasRequest


@given(from_type(DescribeClientQuotasRequest))
@settings(max_examples=1)
def test_describe_client_quotas_request_roundtrip(
    instance: DescribeClientQuotasRequest,
) -> None:
    writer = entity_writer(DescribeClientQuotasRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DescribeClientQuotasRequest))
    assert instance == result
