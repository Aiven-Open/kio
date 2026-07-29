from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.update_features.v2.response import UpdateFeaturesResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_update_features_response: Final = entity_reader(UpdateFeaturesResponse)


@pytest.mark.roundtrip
@given(from_type(UpdateFeaturesResponse))
def test_update_features_response_roundtrip(instance: UpdateFeaturesResponse) -> None:
    writer = entity_writer(UpdateFeaturesResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_update_features_response(
            buffer.getvalue(),
            0,
        )

    assert instance == result


@pytest.mark.java
@given(instance=from_type(UpdateFeaturesResponse))
def test_update_features_response_java(
    instance: UpdateFeaturesResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
