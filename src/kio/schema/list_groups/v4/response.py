"""
Generated from ListGroupsResponse.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/ListGroupsResponse.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.response_header.v1.header import ResponseHeader
from kio.schema.types import GroupId
from kio.static.constants import ErrorCode
from kio.static.primitive import i16
from kio.static.primitive import i32Timedelta
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class ListedGroup:
    __version__: ClassVar[i16] = i16(4)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(16)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    group_id: GroupId = field(metadata={"kafka_type": "string"})
    """The group ID."""
    protocol_type: str = field(metadata={"kafka_type": "string"})
    """The group protocol type."""
    group_state: str = field(metadata={"kafka_type": "string"})
    """The group state name."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ListGroupsResponse(ApiMessage):
    __version__: ClassVar[i16] = i16(4)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(16)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The error code, or 0 if there was no error."""
    groups: tuple[ListedGroup, ...]
    """Each group in the response."""
