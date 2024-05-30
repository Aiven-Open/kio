"""
Generated from ``clients/src/main/resources/common/message/DescribeConfigsResponse.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.errors import ErrorCode
from kio.schema.response_header.v0.header import ResponseHeader
from kio.static.constants import EntityType
from kio.static.primitive import i8
from kio.static.primitive import i16
from kio.static.primitive import i32Timedelta


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeConfigsSynonym:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(3)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(32)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    name: str = field(metadata={"kafka_type": "string"})
    """The synonym name."""
    value: str | None = field(metadata={"kafka_type": "string"})
    """The synonym value."""
    source: i8 = field(metadata={"kafka_type": "int8"})
    """The synonym source."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeConfigsResourceResult:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(3)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(32)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    name: str = field(metadata={"kafka_type": "string"})
    """The configuration name."""
    value: str | None = field(metadata={"kafka_type": "string"})
    """The configuration value."""
    read_only: bool = field(metadata={"kafka_type": "bool"})
    """True if the configuration is read-only."""
    config_source: i8 = field(metadata={"kafka_type": "int8"}, default=i8(-1))
    """The configuration source."""
    is_sensitive: bool = field(metadata={"kafka_type": "bool"})
    """True if this configuration is sensitive."""
    synonyms: tuple[DescribeConfigsSynonym, ...]
    """The synonyms for this configuration key."""
    config_type: i8 = field(metadata={"kafka_type": "int8"}, default=i8(0))
    """The configuration data type. Type can be one of the following values - BOOLEAN, STRING, INT, SHORT, LONG, DOUBLE, LIST, CLASS, PASSWORD"""
    documentation: str | None = field(metadata={"kafka_type": "string"})
    """The configuration documentation."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeConfigsResult:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(3)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(32)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The error code, or 0 if we were able to successfully describe the configurations."""
    error_message: str | None = field(metadata={"kafka_type": "string"})
    """The error message, or null if we were able to successfully describe the configurations."""
    resource_type: i8 = field(metadata={"kafka_type": "int8"})
    """The resource type."""
    resource_name: str = field(metadata={"kafka_type": "string"})
    """The resource name."""
    configs: tuple[DescribeConfigsResourceResult, ...]
    """Each listed configuration."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeConfigsResponse:
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(3)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(32)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    results: tuple[DescribeConfigsResult, ...]
    """The results for each resource."""
