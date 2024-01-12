"""
Generated from SyncGroupResponse.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/SyncGroupResponse.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.response_header.v0.header import ResponseHeader
from kio.static.constants import EntityType
from kio.static.constants import ErrorCode
from kio.static.primitive import i16


@dataclass(frozen=True, slots=True, kw_only=True)
class SyncGroupResponse:
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(14)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The error code, or 0 if there was no error."""
    assignment: bytes = field(metadata={"kafka_type": "bytes"})
    """The member assignment."""
