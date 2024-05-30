"""
Generated from ``clients/src/main/resources/common/message/ApiVersionsResponse.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.errors import ErrorCode
from kio.schema.response_header.v0.header import ResponseHeader
from kio.static.constants import EntityType
from kio.static.primitive import i16


@dataclass(frozen=True, slots=True, kw_only=True)
class ApiVersion:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(18)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    api_key: i16 = field(metadata={"kafka_type": "int16"})
    """The API index."""
    min_version: i16 = field(metadata={"kafka_type": "int16"})
    """The minimum supported version, inclusive."""
    max_version: i16 = field(metadata={"kafka_type": "int16"})
    """The maximum supported version, inclusive."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ApiVersionsResponse:
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(18)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The top-level error code."""
    api_keys: tuple[ApiVersion, ...]
    """The APIs supported by the broker."""
