"""
Generated from DescribeConfigsResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i8
from kio.schema.primitive import i16
from kio.schema.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeConfigsSynonym:
    __flexible__: ClassVar[bool] = True
    name: str = field(metadata={"kafka_type": "string"})
    """The synonym name."""
    value: str | None = field(metadata={"kafka_type": "string"})
    """The synonym value."""
    source: i8 = field(metadata={"kafka_type": "int8"})
    """The synonym source."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeConfigsResourceResult:
    __flexible__: ClassVar[bool] = True
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
    __flexible__: ClassVar[bool] = True
    error_code: i16 = field(metadata={"kafka_type": "int16"})
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
    __flexible__: ClassVar[bool] = True
    throttle_time_ms: i32 = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    results: tuple[DescribeConfigsResult, ...]
    """The results for each resource."""