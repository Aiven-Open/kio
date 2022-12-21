"""
Generated from SyncGroupResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar


@dataclass(frozen=True, slots=True, kw_only=True)
class SyncGroupResponse:
    __flexible__: ClassVar[bool] = False
    throttle_time_ms: int = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    error_code: int = field(metadata={"kafka_type": "int16"})
    """The error code, or 0 if there was no error."""
    assignment: bytes = field(metadata={"kafka_type": "bytes"})
    """The member assignment."""
