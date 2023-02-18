"""
Generated from ExpireDelegationTokenRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class ExpireDelegationTokenRequest:
    __flexible__: ClassVar[bool] = True
    hmac: bytes = field(metadata={"kafka_type": "bytes"})
    """The HMAC of the delegation token to be expired."""
    expiry_time_period_ms: i64 = field(metadata={"kafka_type": "int64"})
    """The expiry time period in milliseconds."""
