"""
Generated from AlterConfigsResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i8
from kio.schema.primitive import i16
from kio.schema.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class AlterConfigsResourceResponse:
    __flexible__: ClassVar[bool] = True
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The resource error code."""
    error_message: str | None = field(metadata={"kafka_type": "string"})
    """The resource error message, or null if there was no error."""
    resource_type: i8 = field(metadata={"kafka_type": "int8"})
    """The resource type."""
    resource_name: str = field(metadata={"kafka_type": "string"})
    """The resource name."""


@dataclass(frozen=True, slots=True, kw_only=True)
class AlterConfigsResponse:
    __flexible__: ClassVar[bool] = True
    throttle_time_ms: i32 = field(metadata={"kafka_type": "int32"})
    """Duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    responses: tuple[AlterConfigsResourceResponse, ...]
    """The responses for each resource."""
