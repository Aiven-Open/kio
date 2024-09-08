from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.voters_record.v0.data import Endpoint
from kio.schema.voters_record.v0.data import KRaftVersionFeature
from kio.schema.voters_record.v0.data import Voter
from kio.schema.voters_record.v0.data import VotersRecord
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_endpoint: Final = entity_reader(Endpoint)


@pytest.mark.roundtrip
@given(from_type(Endpoint))
def test_endpoint_roundtrip(instance: Endpoint) -> None:
    writer = entity_writer(Endpoint)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_endpoint(buffer)
    assert instance == result


read_k_raft_version_feature: Final = entity_reader(KRaftVersionFeature)


@pytest.mark.roundtrip
@given(from_type(KRaftVersionFeature))
def test_k_raft_version_feature_roundtrip(instance: KRaftVersionFeature) -> None:
    writer = entity_writer(KRaftVersionFeature)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_k_raft_version_feature(buffer)
    assert instance == result


read_voter: Final = entity_reader(Voter)


@pytest.mark.roundtrip
@given(from_type(Voter))
def test_voter_roundtrip(instance: Voter) -> None:
    writer = entity_writer(Voter)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_voter(buffer)
    assert instance == result


read_voters_record: Final = entity_reader(VotersRecord)


@pytest.mark.roundtrip
@given(from_type(VotersRecord))
def test_voters_record_roundtrip(instance: VotersRecord) -> None:
    writer = entity_writer(VotersRecord)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_voters_record(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(VotersRecord))
def test_voters_record_java(instance: VotersRecord, java_tester: JavaTester) -> None:
    java_tester.test(instance)
