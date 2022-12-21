"""
Generated from CreateDelegationTokenResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateDelegationTokenResponse:
    __flexible__: ClassVar[bool] = True
    error_code: int = field(metadata={"kafka_type": "int16"})
    """The top-level error, or zero if there was no error."""
    principal_type: str = field(metadata={"kafka_type": "string"})
    """The principal type of the token owner."""
    principal_name: str = field(metadata={"kafka_type": "string"})
    """The name of the token owner."""
    issue_timestamp_ms: int = field(metadata={"kafka_type": "int64"})
    """When this token was generated."""
    expiry_timestamp_ms: int = field(metadata={"kafka_type": "int64"})
    """When this token expires."""
    max_timestamp_ms: int = field(metadata={"kafka_type": "int64"})
    """The maximum lifetime of this token."""
    token_id: str = field(metadata={"kafka_type": "string"})
    """The token UUID."""
    hmac: bytes = field(metadata={"kafka_type": "bytes"})
    """HMAC of the delegation token."""
    throttle_time_ms: int = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
