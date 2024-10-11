from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.share_group_describe.v0.request import ShareGroupDescribeRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_share_group_describe_request: Final = entity_reader(ShareGroupDescribeRequest)


@pytest.mark.roundtrip
@given(from_type(ShareGroupDescribeRequest))
def test_share_group_describe_request_roundtrip(
    instance: ShareGroupDescribeRequest,
) -> None:
    writer = entity_writer(ShareGroupDescribeRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_share_group_describe_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(ShareGroupDescribeRequest))
def test_share_group_describe_request_java(
    instance: ShareGroupDescribeRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
