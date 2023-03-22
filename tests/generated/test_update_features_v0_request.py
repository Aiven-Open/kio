from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.update_features.v0.request import FeatureUpdateKey
from kio.schema.update_features.v0.request import UpdateFeaturesRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import setup_buffer

read_feature_update_key: Final = entity_reader(FeatureUpdateKey)


@given(from_type(FeatureUpdateKey))
@settings(max_examples=1)
def test_feature_update_key_roundtrip(instance: FeatureUpdateKey) -> None:
    writer = entity_writer(FeatureUpdateKey)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_feature_update_key(buffer)
    assert instance == result


read_update_features_request: Final = entity_reader(UpdateFeaturesRequest)


@given(from_type(UpdateFeaturesRequest))
@settings(max_examples=1)
def test_update_features_request_roundtrip(instance: UpdateFeaturesRequest) -> None:
    writer = entity_writer(UpdateFeaturesRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_update_features_request(buffer)
    assert instance == result
