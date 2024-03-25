from pkgutil import resolve_name
from types import ModuleType
from typing import cast

from .schema.index import LoadableEntityType
from .schema.index import PayloadEntityType
from .schema.index import api_key_map
from .schema.index import schema_name_map
from .static.constants import EntityType
from .static.protocol import Entity
from .static.protocol import RequestPayload
from .static.protocol import ResponsePayload


class KioIndexError(RuntimeError): ...


class UnknownAPIKey(KioIndexError): ...


class UnknownEntity(KioIndexError): ...


def _name_from_key(api_key: int) -> str:
    """
    :raises UnknownAPIKey: When the given API key does not map to an API name.
    """
    try:
        return api_key_map[api_key]
    except KeyError as e:
        raise UnknownAPIKey(f"Failed mapping the given API key: {api_key!r}") from e


def _get_entity_path(name: str, version: int, entity_type: LoadableEntityType) -> str:
    """
    :raises UnknownEntity: When the given arguments do not map to a known entity.
    """
    try:
        return schema_name_map[name][version][entity_type]
    except KeyError:
        raise UnknownEntity(
            f"Failed mapping to a an entity path for ({name=!r}, {version=!r}, "
            f"entity_type={entity_type.name!r})."
        ) from None


def _resolve(path: str) -> object:
    try:
        return resolve_name(path)
    except (ImportError, ValueError, AttributeError) as e:
        e.add_note("This error stems from a dynamic import in kio.")
        raise


def load_entity_module(
    name: str,
    version: int,
    entity_type: LoadableEntityType,
) -> ModuleType:
    """
    Load a schema module given the schema name, version, and type.

    :raises UnknownEntity: When the given arguments do not map to a known entity.

    >>> load_entity_module("metadata", 12, EntityType.request)
    <module 'kio.schema.metadata.v12.request' from '.../kio/schema/metadata/v12/request.py'>
    """
    entity_path = _get_entity_path(name, version, entity_type)
    module_path = entity_path.split(":", 1)[0]
    resolved = _resolve(module_path)
    assert isinstance(resolved, ModuleType)
    return resolved


def load_payload_module(
    api_key: int,
    version: int,
    entity_type: PayloadEntityType,
) -> ModuleType:
    """
    Load a schema module of an API message payload, given the API key, version,
    and type.

    :raises UnknownAPIKey: When the given API key does not map to an API name.
    :raises UnknownEntity: When the given arguments do not map to a known entity.

    >>> load_payload_module(3, 12, EntityType.request)
    <module 'kio.schema.metadata.v12.request' from '.../kio/schema/metadata/v12/request.py'>
    """
    return load_entity_module(_name_from_key(api_key), version, entity_type)


def load_entity_schema(
    name: str,
    version: int,
    entity_type: LoadableEntityType,
) -> type[Entity]:
    """
    Load an entity schema module given the schema name, version, and type.

    :raises UnknownEntity: When the given arguments do not map to a known entity.

    >>> load_entity_schema("metadata", 12, EntityType.response)
    <class 'kio.schema.metadata.v12.response.MetadataResponse'>
    """
    resolved = _resolve(_get_entity_path(name, version, entity_type))
    assert isinstance(resolved, type)
    return cast(type[Entity], resolved)


def load_response_schema(api_key: int, version: int) -> type[ResponsePayload]:
    """
    Load a response payload schema entity given its API key, and version.

    :raises UnknownAPIKey: When the given API key does not map to an API name.
    :raises UnknownEntity: When the given arguments do not map to a known entity.

    >>> load_response_schema(3, 12)
    <class 'kio.schema.metadata.v12.response.MetadataResponse'>
    """
    resolved = load_entity_schema(_name_from_key(api_key), version, EntityType.response)
    return cast(type[ResponsePayload], resolved)


def load_request_schema(api_key: int, version: int) -> type[RequestPayload]:
    """
    Load a request payload schema entity given its API key, and version.

    :raises UnknownAPIKey: When the given API key does not map to an API name.
    :raises UnknownEntity: When the given arguments do not map to a known entity.

    >>> load_request_schema(3, 12)
    <class 'kio.schema.metadata.v12.request.MetadataRequest'>
    """
    resolved = load_entity_schema(_name_from_key(api_key), version, EntityType.request)
    return cast(type[RequestPayload], resolved)


def load_response_from_request(
    request_type: type[RequestPayload] | RequestPayload,
) -> type[ResponsePayload]:
    """
    Load a response payload schema entity given its corresponding request type.

    :raises UnknownAPIKey: When the given API key does not map to an API name.
    :raises UnknownEntity: When the given arguments do not map to a known entity.

    >>> from kio.schema.metadata.v12 import MetadataRequest
    >>> load_response_from_request(MetadataRequest)
    <class 'kio.schema.metadata.v12.response.MetadataResponse'>
    """
    return load_response_schema(request_type.__api_key__, request_type.__version__)


def load_request_from_response(
    response_type: type[ResponsePayload] | ResponsePayload,
) -> type[RequestPayload]:
    """
    Load a request payload schema entity given its corresponding response type.

    :raises UnknownAPIKey: When the given API key does not map to an API name.
    :raises UnknownEntity: When the given arguments do not map to a known entity.

    >>> from kio.schema.metadata.v12 import MetadataResponse
    >>> load_request_from_response(MetadataResponse)
    <class 'kio.schema.metadata.v12.request.MetadataRequest'>
    """
    return load_request_schema(response_type.__api_key__, response_type.__version__)
