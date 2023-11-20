"""
Generated from DescribeGroupsResponse.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/DescribeGroupsResponse.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.response_header.v0.header import ResponseHeader
from kio.schema.types import GroupId
from kio.static.constants import ErrorCode
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i32Timedelta
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribedGroupMember:
    __version__: ClassVar[i16] = i16(4)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(15)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    member_id: str = field(metadata={"kafka_type": "string"})
    """The member ID assigned by the group coordinator."""
    group_instance_id: str | None = field(
        metadata={"kafka_type": "string"}, default=None
    )
    """The unique identifier of the consumer instance provided by end user."""
    client_id: str = field(metadata={"kafka_type": "string"})
    """The client ID used in the member's latest join group request."""
    client_host: str = field(metadata={"kafka_type": "string"})
    """The client host."""
    member_metadata: bytes = field(metadata={"kafka_type": "bytes"})
    """The metadata corresponding to the current group protocol in use."""
    member_assignment: bytes = field(metadata={"kafka_type": "bytes"})
    """The current assignment provided by the group leader."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribedGroup:
    __version__: ClassVar[i16] = i16(4)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(15)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The describe error, or 0 if there was no error."""
    group_id: GroupId = field(metadata={"kafka_type": "string"})
    """The group ID string."""
    group_state: str = field(metadata={"kafka_type": "string"})
    """The group state string, or the empty string."""
    protocol_type: str = field(metadata={"kafka_type": "string"})
    """The group protocol type, or the empty string."""
    protocol_data: str = field(metadata={"kafka_type": "string"})
    """The group protocol data, or the empty string."""
    members: tuple[DescribedGroupMember, ...]
    """The group members."""
    authorized_operations: i32 = field(
        metadata={"kafka_type": "int32"}, default=i32(-2147483648)
    )
    """32-bit bitfield to represent authorized operations for this group."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeGroupsResponse(ApiMessage):
    __version__: ClassVar[i16] = i16(4)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(15)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    groups: tuple[DescribedGroup, ...]
    """Each described group."""
