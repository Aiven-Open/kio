"""
Generated from EnvelopeResponse.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/EnvelopeResponse.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.response_header.v1.header import ResponseHeader
from kio.static.constants import ErrorCode
from kio.static.primitive import i16
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class EnvelopeResponse(ApiMessage):
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(58)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    response_data: bytes | None = field(metadata={"kafka_type": "bytes"}, default=None)
    """The embedded response header and data."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The error code, or 0 if there was no error."""
