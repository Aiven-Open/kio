from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.delete_acls.v1.request import DeleteAclsFilter
from kio.schema.delete_acls.v1.request import DeleteAclsRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_delete_acls_filter: Final = entity_reader(DeleteAclsFilter)


@pytest.mark.roundtrip
@given(from_type(DeleteAclsFilter))
@settings(max_examples=1)
def test_delete_acls_filter_roundtrip(instance: DeleteAclsFilter) -> None:
    writer = entity_writer(DeleteAclsFilter)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_delete_acls_filter(buffer)
    assert instance == result


read_delete_acls_request: Final = entity_reader(DeleteAclsRequest)


@pytest.mark.roundtrip
@given(from_type(DeleteAclsRequest))
@settings(max_examples=1)
def test_delete_acls_request_roundtrip(instance: DeleteAclsRequest) -> None:
    writer = entity_writer(DeleteAclsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_delete_acls_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(DeleteAclsRequest))
def test_delete_acls_request_java(
    instance: DeleteAclsRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
