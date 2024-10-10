from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.k_raft_version_record.v0.data import KRaftVersionRecord
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_k_raft_version_record: Final = entity_reader(KRaftVersionRecord)


@pytest.mark.roundtrip
@given(from_type(KRaftVersionRecord))
def test_k_raft_version_record_roundtrip(instance: KRaftVersionRecord) -> None:
    writer = entity_writer(KRaftVersionRecord)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_k_raft_version_record(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(KRaftVersionRecord))
def test_k_raft_version_record_java(
    instance: KRaftVersionRecord, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
