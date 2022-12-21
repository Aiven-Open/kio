"""
Generated from BrokerHeartbeatResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar


@dataclass(frozen=True, slots=True, kw_only=True)
class BrokerHeartbeatResponse:
    __flexible__: ClassVar[bool] = True
    throttle_time_ms: int = field(metadata={"kafka_type": "int32"})
    """Duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    error_code: int = field(metadata={"kafka_type": "int16"})
    """The error code, or 0 if there was no error."""
    is_caught_up: bool = field(metadata={"kafka_type": "bool"}, default=False)
    """True if the broker has approximately caught up with the latest metadata."""
    is_fenced: bool = field(metadata={"kafka_type": "bool"}, default=True)
    """True if the broker is fenced."""
    should_shut_down: bool = field(metadata={"kafka_type": "bool"})
    """True if the broker should proceed with its shutdown."""
