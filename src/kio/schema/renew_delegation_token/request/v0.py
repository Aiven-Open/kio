"""
Generated from RenewDelegationTokenRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class RenewDelegationTokenRequest:
    __flexible__: ClassVar[bool] = False
    hmac: bytes = field(metadata={"kafka_type": "bytes"})
    """The HMAC of the delegation token to be renewed."""
    renew_period_ms: i64 = field(metadata={"kafka_type": "int64"})
    """The renewal time period in milliseconds."""
