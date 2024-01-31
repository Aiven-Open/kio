from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.delete_acls.v3.response import DeleteAclsFilterResult
from kio.schema.delete_acls.v3.response import DeleteAclsMatchingAcl
from kio.schema.delete_acls.v3.response import DeleteAclsResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_delete_acls_matching_acl: Final = entity_reader(DeleteAclsMatchingAcl)


@pytest.mark.roundtrip
@given(from_type(DeleteAclsMatchingAcl))
@settings(max_examples=1)
def test_delete_acls_matching_acl_roundtrip(instance: DeleteAclsMatchingAcl) -> None:
    writer = entity_writer(DeleteAclsMatchingAcl)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_delete_acls_matching_acl(buffer)
    assert instance == result


read_delete_acls_filter_result: Final = entity_reader(DeleteAclsFilterResult)


@pytest.mark.roundtrip
@given(from_type(DeleteAclsFilterResult))
@settings(max_examples=1)
def test_delete_acls_filter_result_roundtrip(instance: DeleteAclsFilterResult) -> None:
    writer = entity_writer(DeleteAclsFilterResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_delete_acls_filter_result(buffer)
    assert instance == result


read_delete_acls_response: Final = entity_reader(DeleteAclsResponse)


@pytest.mark.roundtrip
@given(from_type(DeleteAclsResponse))
@settings(max_examples=1)
def test_delete_acls_response_roundtrip(instance: DeleteAclsResponse) -> None:
    writer = entity_writer(DeleteAclsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_delete_acls_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(DeleteAclsResponse))
def test_delete_acls_response_java(
    instance: DeleteAclsResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
