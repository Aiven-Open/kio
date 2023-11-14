"""
Generated from SaslAuthenticateResponse.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/SaslAuthenticateResponse.json
"""

import datetime
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.response_header.v1.header import ResponseHeader
from kio.static.constants import ErrorCode
from kio.static.primitive import i16
from kio.static.primitive import i64Timedelta
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class SaslAuthenticateResponse(ApiMessage):
    __version__: ClassVar[i16] = i16(2)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(36)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The error code, or 0 if there was no error."""
    error_message: str | None = field(metadata={"kafka_type": "string"})
    """The error message, or null if there was no error."""
    auth_bytes: bytes = field(metadata={"kafka_type": "bytes"})
    """The SASL authentication bytes from the server, as defined by the SASL mechanism."""
    session_lifetime: i64Timedelta = field(
        metadata={"kafka_type": "timedelta_i64"},
        default=i64Timedelta.parse(datetime.timedelta(milliseconds=0)),
    )
    """Number of milliseconds after which only re-authentication over the existing connection to create a new session can occur."""
