"""
Generated from ``clients/src/main/resources/common/message/CreateDelegationTokenResponse.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.errors import ErrorCode
from kio.schema.response_header.v0.header import ResponseHeader
from kio.static.constants import EntityType
from kio.static.primitive import TZAware
from kio.static.primitive import i16
from kio.static.primitive import i32Timedelta


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateDelegationTokenResponse:
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(38)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The top-level error, or zero if there was no error."""
    principal_type: str = field(metadata={"kafka_type": "string"})
    """The principal type of the token owner."""
    principal_name: str = field(metadata={"kafka_type": "string"})
    """The name of the token owner."""
    issue_timestamp: TZAware = field(metadata={"kafka_type": "datetime_i64"})
    """When this token was generated."""
    expiry_timestamp: TZAware = field(metadata={"kafka_type": "datetime_i64"})
    """When this token expires."""
    max_timestamp: TZAware = field(metadata={"kafka_type": "datetime_i64"})
    """The maximum lifetime of this token."""
    token_id: str = field(metadata={"kafka_type": "string"})
    """The token UUID."""
    hmac: bytes = field(metadata={"kafka_type": "bytes"})
    """HMAC of the delegation token."""
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
