from kio.schema.index import api_key_map
from kio.schema.index import schema_name_map
from kio.static.constants import EntityType


def test_smoke_test_api_key_map() -> None:
    assert api_key_map[3] == "metadata"


def test_smoke_test_schema_name_map() -> None:
    assert (
        schema_name_map["metadata"][12][EntityType.request]
        == "kio.schema.metadata.v12.request:MetadataRequest"
    )
    assert (
        schema_name_map["metadata"][12][EntityType.response]
        == "kio.schema.metadata.v12.response:MetadataResponse"
    )
