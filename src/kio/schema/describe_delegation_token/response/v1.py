"""
Generated from DescribeDelegationTokenResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribedDelegationTokenRenewer:
    __flexible__: ClassVar[bool] = False
    principal_type: str = field(metadata={"kafka_type": "string"})
    """The renewer principal type"""
    principal_name: str = field(metadata={"kafka_type": "string"})
    """The renewer principal name"""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribedDelegationToken:
    __flexible__: ClassVar[bool] = False
    principal_type: str = field(metadata={"kafka_type": "string"})
    """The token principal type."""
    principal_name: str = field(metadata={"kafka_type": "string"})
    """The token principal name."""
    issue_timestamp: int = field(metadata={"kafka_type": "int64"})
    """The token issue timestamp in milliseconds."""
    expiry_timestamp: int = field(metadata={"kafka_type": "int64"})
    """The token expiry timestamp in milliseconds."""
    max_timestamp: int = field(metadata={"kafka_type": "int64"})
    """The token maximum timestamp length in milliseconds."""
    token_id: str = field(metadata={"kafka_type": "string"})
    """The token ID."""
    hmac: bytes = field(metadata={"kafka_type": "bytes"})
    """The token HMAC."""
    renewers: tuple[DescribedDelegationTokenRenewer, ...]
    """Those who are able to renew this token before it expires."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeDelegationTokenResponse:
    __flexible__: ClassVar[bool] = False
    error_code: int = field(metadata={"kafka_type": "int16"})
    """The error code, or 0 if there was no error."""
    tokens: tuple[DescribedDelegationToken, ...]
    """The tokens."""
    throttle_time_ms: int = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
