"""
Generated from ExpireDelegationTokenRequest.json.

https://github.com/apache/kafka/tree/3.5.1/clients/src/main/resources/common/message/ExpireDelegationTokenRequest.json
"""

# ruff: noqa: A003

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.static.primitive import i16
from kio.static.primitive import i64Timedelta


@dataclass(frozen=True, slots=True, kw_only=True)
class ExpireDelegationTokenRequest:
    __version__: ClassVar[i16] = i16(2)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(40)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    hmac: bytes = field(metadata={"kafka_type": "bytes"})
    """The HMAC of the delegation token to be expired."""
    expiry_time_period: i64Timedelta = field(metadata={"kafka_type": "timedelta_i64"})
    """The expiry time period in milliseconds."""
