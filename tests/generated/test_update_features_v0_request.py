from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.update_features.v0.request import FeatureUpdateKey
from kio.schema.update_features.v0.request import UpdateFeaturesRequest
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(FeatureUpdateKey))
@settings(max_examples=1)
def test_feature_update_key_roundtrip(instance: FeatureUpdateKey) -> None:
    writer = entity_writer(FeatureUpdateKey)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(FeatureUpdateKey))
    assert instance == result


@given(from_type(UpdateFeaturesRequest))
@settings(max_examples=1)
def test_update_features_request_roundtrip(instance: UpdateFeaturesRequest) -> None:
    writer = entity_writer(UpdateFeaturesRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(UpdateFeaturesRequest))
    assert instance == result
