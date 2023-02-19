from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.default_principal_data.v0.data import DefaultPrincipalData
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(DefaultPrincipalData))
@settings(max_examples=1)
def test_default_principal_data_roundtrip(instance: DefaultPrincipalData) -> None:
    writer = entity_writer(DefaultPrincipalData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DefaultPrincipalData))
    assert instance == result
