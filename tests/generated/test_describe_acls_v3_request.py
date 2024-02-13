from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.describe_acls.v3.request import DescribeAclsRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_describe_acls_request: Final = entity_reader(DescribeAclsRequest)


@pytest.mark.roundtrip
@given(from_type(DescribeAclsRequest))
def test_describe_acls_request_roundtrip(instance: DescribeAclsRequest) -> None:
    writer = entity_writer(DescribeAclsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_describe_acls_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(DescribeAclsRequest))
def test_describe_acls_request_java(
    instance: DescribeAclsRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
