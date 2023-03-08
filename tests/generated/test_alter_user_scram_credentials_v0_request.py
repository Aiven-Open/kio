from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.alter_user_scram_credentials.v0.request import (
    AlterUserScramCredentialsRequest,
)
from kio.schema.alter_user_scram_credentials.v0.request import ScramCredentialDeletion
from kio.schema.alter_user_scram_credentials.v0.request import ScramCredentialUpsertion
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(ScramCredentialDeletion))
@settings(max_examples=1)
def test_scram_credential_deletion_roundtrip(instance: ScramCredentialDeletion) -> None:
    writer = entity_writer(ScramCredentialDeletion)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(ScramCredentialDeletion))
    assert instance == result


@given(from_type(ScramCredentialUpsertion))
@settings(max_examples=1)
def test_scram_credential_upsertion_roundtrip(
    instance: ScramCredentialUpsertion,
) -> None:
    writer = entity_writer(ScramCredentialUpsertion)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(ScramCredentialUpsertion))
    assert instance == result


@given(from_type(AlterUserScramCredentialsRequest))
@settings(max_examples=1)
def test_alter_user_scram_credentials_request_roundtrip(
    instance: AlterUserScramCredentialsRequest,
) -> None:
    writer = entity_writer(AlterUserScramCredentialsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(AlterUserScramCredentialsRequest))
    assert instance == result
