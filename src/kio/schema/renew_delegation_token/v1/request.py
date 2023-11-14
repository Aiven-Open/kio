"""
Generated from RenewDelegationTokenRequest.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/RenewDelegationTokenRequest.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v1.header import RequestHeader
from kio.static.primitive import i16
from kio.static.primitive import i64Timedelta
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class RenewDelegationTokenRequest(ApiMessage):
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(39)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    hmac: bytes = field(metadata={"kafka_type": "bytes"})
    """The HMAC of the delegation token to be renewed."""
    renew_period: i64Timedelta = field(metadata={"kafka_type": "timedelta_i64"})
    """The renewal time period in milliseconds."""
