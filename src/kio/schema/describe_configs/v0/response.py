"""
Generated from DescribeConfigsResponse.json.

https://github.com/apache/kafka/tree/3.5.1/clients/src/main/resources/common/message/DescribeConfigsResponse.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.response_header.v0.header import ResponseHeader
from kio.static.constants import ErrorCode
from kio.static.primitive import i8
from kio.static.primitive import i16
from kio.static.primitive import i32Timedelta


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeConfigsResourceResult:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(32)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    name: str = field(metadata={"kafka_type": "string"})
    """The configuration name."""
    value: str | None = field(metadata={"kafka_type": "string"})
    """The configuration value."""
    read_only: bool = field(metadata={"kafka_type": "bool"})
    """True if the configuration is read-only."""
    is_default: bool = field(metadata={"kafka_type": "bool"})
    """True if the configuration is not set."""
    is_sensitive: bool = field(metadata={"kafka_type": "bool"})
    """True if this configuration is sensitive."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeConfigsResult:
    __version__: ClassVar[i16] = i16(0)
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
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(32)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    results: tuple[DescribeConfigsResult, ...]
    """The results for each resource."""
