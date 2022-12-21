"""
Generated from RequestHeader.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar


@dataclass(frozen=True, slots=True, kw_only=True)
class RequestHeader:
    __flexible__: ClassVar[bool] = False
    request_api_key: int = field(metadata={"kafka_type": "int16"})
    """The API key of this request."""
    request_api_version: int = field(metadata={"kafka_type": "int16"})
    """The API version of this request."""
    correlation_id: int = field(metadata={"kafka_type": "int32"})
    """The correlation ID of this request."""
