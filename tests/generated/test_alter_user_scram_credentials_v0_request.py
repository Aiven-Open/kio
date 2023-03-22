from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.alter_user_scram_credentials.v0.request import (
    AlterUserScramCredentialsRequest,
)
from kio.schema.alter_user_scram_credentials.v0.request import ScramCredentialDeletion
from kio.schema.alter_user_scram_credentials.v0.request import ScramCredentialUpsertion
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import setup_buffer

read_scram_credential_deletion: Final = entity_reader(ScramCredentialDeletion)


@given(from_type(ScramCredentialDeletion))
@settings(max_examples=1)
def test_scram_credential_deletion_roundtrip(instance: ScramCredentialDeletion) -> None:
    writer = entity_writer(ScramCredentialDeletion)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_scram_credential_deletion(buffer)
    assert instance == result


read_scram_credential_upsertion: Final = entity_reader(ScramCredentialUpsertion)


@given(from_type(ScramCredentialUpsertion))
@settings(max_examples=1)
def test_scram_credential_upsertion_roundtrip(
    instance: ScramCredentialUpsertion,
) -> None:
    writer = entity_writer(ScramCredentialUpsertion)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_scram_credential_upsertion(buffer)
    assert instance == result


read_alter_user_scram_credentials_request: Final = entity_reader(
    AlterUserScramCredentialsRequest
)


@given(from_type(AlterUserScramCredentialsRequest))
@settings(max_examples=1)
def test_alter_user_scram_credentials_request_roundtrip(
    instance: AlterUserScramCredentialsRequest,
) -> None:
    writer = entity_writer(AlterUserScramCredentialsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_alter_user_scram_credentials_request(buffer)
    assert instance == result
