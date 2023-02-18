"""
Generated from RequestHeader.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i16
from kio.schema.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class RequestHeader:
    __flexible__: ClassVar[bool] = False
    request_api_key: i16 = field(metadata={"kafka_type": "int16"})
    """The API key of this request."""
    request_api_version: i16 = field(metadata={"kafka_type": "int16"})
    """The API version of this request."""
    correlation_id: i32 = field(metadata={"kafka_type": "int32"})
    """The correlation ID of this request."""
