"""
Generated from ApiVersionsResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i16
from kio.schema.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class ApiVersion:
    __flexible__: ClassVar[bool] = False
    api_key: i16 = field(metadata={"kafka_type": "int16"})
    """The API index."""
    min_version: i16 = field(metadata={"kafka_type": "int16"})
    """The minimum supported version, inclusive."""
    max_version: i16 = field(metadata={"kafka_type": "int16"})
    """The maximum supported version, inclusive."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ApiVersionsResponse:
    __flexible__: ClassVar[bool] = False
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The top-level error code."""
    api_keys: tuple[ApiVersion, ...]
    """The APIs supported by the broker."""
    throttle_time_ms: i32 = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
