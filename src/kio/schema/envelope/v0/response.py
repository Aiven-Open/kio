"""
Generated from ``clients/src/main/resources/common/message/EnvelopeResponse.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.errors import ErrorCode
from kio.schema.response_header.v1.header import ResponseHeader
from kio.static.constants import EntityType
from kio.static.primitive import i16


@dataclass(frozen=True, slots=True, kw_only=True)
class EnvelopeResponse:
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(58)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    response_data: bytes | None = field(metadata={"kafka_type": "bytes"}, default=None)
    """The embedded response header and data."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The error code, or 0 if there was no error."""
