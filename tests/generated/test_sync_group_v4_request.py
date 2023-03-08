from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.sync_group.v4.request import SyncGroupRequest
from kio.schema.sync_group.v4.request import SyncGroupRequestAssignment
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(SyncGroupRequestAssignment))
@settings(max_examples=1)
def test_sync_group_request_assignment_roundtrip(
    instance: SyncGroupRequestAssignment,
) -> None:
    writer = entity_writer(SyncGroupRequestAssignment)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(SyncGroupRequestAssignment))
    assert instance == result


@given(from_type(SyncGroupRequest))
@settings(max_examples=1)
def test_sync_group_request_roundtrip(instance: SyncGroupRequest) -> None:
    writer = entity_writer(SyncGroupRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(SyncGroupRequest))
    assert instance == result
