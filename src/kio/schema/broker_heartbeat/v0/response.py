"""
Generated from ``clients/src/main/resources/common/message/BrokerHeartbeatResponse.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.errors import ErrorCode
from kio.schema.response_header.v1.header import ResponseHeader
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i32Timedelta


@dataclass(frozen=True, slots=True, kw_only=True)
class BrokerHeartbeatResponse:
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(63)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """Duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The error code, or 0 if there was no error."""
    is_caught_up: bool = field(metadata={"kafka_type": "bool"}, default=False)
    """True if the broker has approximately caught up with the latest metadata."""
    is_fenced: bool = field(metadata={"kafka_type": "bool"}, default=True)
    """True if the broker is fenced."""
    should_shut_down: bool = field(metadata={"kafka_type": "bool"})
    """True if the broker should proceed with its shutdown."""
