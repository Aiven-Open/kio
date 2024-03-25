from unittest import mock

import pytest

import kio.schema.metadata.v12.request
import kio.schema.metadata.v12.response

from kio.index import UnknownAPIKey
from kio.index import UnknownEntity
from kio.index import _get_entity_path
from kio.index import _name_from_key
from kio.index import _resolve
from kio.index import load_entity_module
from kio.index import load_entity_schema
from kio.index import load_payload_module
from kio.index import load_request_from_response
from kio.index import load_request_schema
from kio.index import load_response_from_request
from kio.index import load_response_schema
from kio.static.constants import EntityType


class TestNameFromKey:
    def test_returns_associated_module_name(self) -> None:
        assert _name_from_key(3) == "metadata"

    def test_raises_unknown_api_key_for_invalid_key(self) -> None:
        with pytest.raises(UnknownAPIKey):
            _name_from_key(-1)


class TestGetEntityPath:
    def test_returns_correct_entity_path(self) -> None:
        assert (
            _get_entity_path("metadata", 12, EntityType.request)
            == "kio.schema.metadata.v12.request:MetadataRequest"
        )

    def test_raises_unknown_entity_path_for_missing_schema_name(self) -> None:
        with pytest.raises(UnknownEntity):
            _get_entity_path("_metadata", 12, EntityType.request)

    def test_raises_unknown_entity_path_for_missing_version(self) -> None:
        with pytest.raises(UnknownEntity):
            _get_entity_path("metadata", 999_999, EntityType.request)

    def test_raises_unknown_entity_path_for_missing_entity_type(self) -> None:
        with pytest.raises(UnknownEntity):
            _get_entity_path("metadata", 12, EntityType.data)


class TestResolve:
    def test_can_resolve_existing_path(self) -> None:
        import kio.schema.metadata.v12.request

        assert (
            _resolve("kio.schema.metadata.v12.request:MetadataRequest")
            is kio.schema.metadata.v12.MetadataRequest
        )

    @pytest.mark.parametrize(
        "error",
        (ImportError, ValueError, AttributeError),
    )
    def test_reraises_import_errors_with_note(
        self,
        error: type[Exception],
    ) -> None:
        with (
            mock.patch("kio.index.resolve_name", side_effect=error),
            pytest.raises(error) as exc_info,
        ):
            _resolve("missing:missing")

        assert (
            "This error stems from a dynamic import in kio." in exc_info.value.__notes__
        )


class TestLoadEntityModule:
    def test_can_load_entity_module(self) -> None:
        loaded = load_entity_module("metadata", 12, EntityType.request)
        assert loaded is kio.schema.metadata.v12.request


class TestLoadPayloadModule:
    def test_can_load_payload_module(self) -> None:
        loaded = load_payload_module(3, 12, EntityType.request)
        assert loaded is kio.schema.metadata.v12.request


class TestLoadEntitySchema:
    def test_can_load_entity_schema(self) -> None:
        loaded = load_entity_schema("metadata", 12, EntityType.request)
        assert loaded is kio.schema.metadata.v12.MetadataRequest


class TestLoadResponseSchema:
    def test_can_load_response_schema(self) -> None:
        loaded = load_response_schema(3, 12)
        assert loaded is kio.schema.metadata.v12.MetadataResponse


class TestLoadRequestSchema:
    def test_can_load_request_schema(self) -> None:
        loaded = load_request_schema(3, 12)
        assert loaded is kio.schema.metadata.v12.MetadataRequest


class TestLoadResponseFromRequest:
    def test_can_load_response_from_request(self) -> None:
        loaded = load_response_from_request(kio.schema.metadata.v12.MetadataRequest)
        assert loaded is kio.schema.metadata.v12.MetadataResponse


class TestLoadRequestFromResponse:
    def test_can_load_request_from_response(self) -> None:
        loaded = load_request_from_response(kio.schema.metadata.v12.MetadataResponse)
        assert loaded is kio.schema.metadata.v12.MetadataRequest
