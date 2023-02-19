"""
Generated from ExpireDelegationTokenResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i16
from kio.schema.primitive import i32
from kio.schema.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class ExpireDelegationTokenResponse:
    __flexible__: ClassVar[bool] = False
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The error code, or 0 if there was no error."""
    expiry_timestamp_ms: i64 = field(metadata={"kafka_type": "int64"})
    """The timestamp in milliseconds at which this token expires."""
    throttle_time_ms: i32 = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""