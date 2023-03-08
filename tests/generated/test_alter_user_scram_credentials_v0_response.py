from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.alter_user_scram_credentials.v0.response import (
    AlterUserScramCredentialsResponse,
)
from kio.schema.alter_user_scram_credentials.v0.response import (
    AlterUserScramCredentialsResult,
)
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(AlterUserScramCredentialsResult))
@settings(max_examples=1)
def test_alter_user_scram_credentials_result_roundtrip(
    instance: AlterUserScramCredentialsResult,
) -> None:
    writer = entity_writer(AlterUserScramCredentialsResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(AlterUserScramCredentialsResult))
    assert instance == result


@given(from_type(AlterUserScramCredentialsResponse))
@settings(max_examples=1)
def test_alter_user_scram_credentials_response_roundtrip(
    instance: AlterUserScramCredentialsResponse,
) -> None:
    writer = entity_writer(AlterUserScramCredentialsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(AlterUserScramCredentialsResponse))
    assert instance == result
