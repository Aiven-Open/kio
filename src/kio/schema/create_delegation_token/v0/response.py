"""
Generated from CreateDelegationTokenResponse.json.
"""

# ruff: noqa: A003

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i16
from kio.schema.primitive import i32
from kio.schema.primitive import i64
from kio.schema.response_header.v0.header import ResponseHeader


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateDelegationTokenResponse:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(38)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The top-level error, or zero if there was no error."""
    principal_type: str = field(metadata={"kafka_type": "string"})
    """The principal type of the token owner."""
    principal_name: str = field(metadata={"kafka_type": "string"})
    """The name of the token owner."""
    issue_timestamp_ms: i64 = field(metadata={"kafka_type": "int64"})
    """When this token was generated."""
    expiry_timestamp_ms: i64 = field(metadata={"kafka_type": "int64"})
    """When this token expires."""
    max_timestamp_ms: i64 = field(metadata={"kafka_type": "int64"})
    """The maximum lifetime of this token."""
    token_id: str = field(metadata={"kafka_type": "string"})
    """The token UUID."""
    hmac: bytes = field(metadata={"kafka_type": "bytes"})
    """HMAC of the delegation token."""
    throttle_time_ms: i32 = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
