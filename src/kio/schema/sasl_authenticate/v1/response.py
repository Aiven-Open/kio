"""
Generated from ``clients/src/main/resources/common/message/SaslAuthenticateResponse.json``.
"""

import datetime

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.errors import ErrorCode
from kio.schema.response_header.v0.header import ResponseHeader
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i64Timedelta


@dataclass(frozen=True, slots=True, kw_only=True)
class SaslAuthenticateResponse:
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = False
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
