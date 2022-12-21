"""
Generated from ExpireDelegationTokenRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar


@dataclass(frozen=True, slots=True, kw_only=True)
class ExpireDelegationTokenRequest:
    __flexible__: ClassVar[bool] = False
    hmac: bytes = field(metadata={"kafka_type": "bytes"})
    """The HMAC of the delegation token to be expired."""
    expiry_time_period_ms: int = field(metadata={"kafka_type": "int64"})
    """The expiry time period in milliseconds."""
