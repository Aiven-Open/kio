"""
Generated from RenewDelegationTokenRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i16
from kio.schema.primitive import i64
from kio.schema.request_header.v1.header import RequestHeader


@dataclass(frozen=True, slots=True, kw_only=True)
class RenewDelegationTokenRequest:
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(39)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    hmac: bytes = field(metadata={"kafka_type": "bytes"})
    """The HMAC of the delegation token to be renewed."""
    renew_period_ms: i64 = field(metadata={"kafka_type": "int64"})
    """The renewal time period in milliseconds."""
