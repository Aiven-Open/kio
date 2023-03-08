from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.update_features.v0.response import UpdatableFeatureResult
from kio.schema.update_features.v0.response import UpdateFeaturesResponse
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(UpdatableFeatureResult))
@settings(max_examples=1)
def test_updatable_feature_result_roundtrip(instance: UpdatableFeatureResult) -> None:
    writer = entity_writer(UpdatableFeatureResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(UpdatableFeatureResult))
    assert instance == result


@given(from_type(UpdateFeaturesResponse))
@settings(max_examples=1)
def test_update_features_response_roundtrip(instance: UpdateFeaturesResponse) -> None:
    writer = entity_writer(UpdateFeaturesResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(UpdateFeaturesResponse))
    assert instance == result
