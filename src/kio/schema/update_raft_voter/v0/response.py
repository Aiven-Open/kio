"""
Generated from ``clients/src/main/resources/common/message/UpdateRaftVoterResponse.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.errors import ErrorCode
from kio.schema.response_header.v1.header import ResponseHeader
from kio.schema.types import BrokerId
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i32Timedelta


@dataclass(frozen=True, slots=True, kw_only=True)
class CurrentLeader:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(82)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    leader_id: BrokerId = field(metadata={"kafka_type": "int32"}, default=BrokerId(-1))
    """The replica id of the current leader or -1 if the leader is unknown"""
    leader_epoch: i32 = field(metadata={"kafka_type": "int32"}, default=i32(-1))
    """The latest known leader epoch"""
    host: str = field(metadata={"kafka_type": "string"})
    """The node's hostname"""
    port: i32 = field(metadata={"kafka_type": "int32"})
    """The node's port"""


@dataclass(frozen=True, slots=True, kw_only=True)
class UpdateRaftVoterResponse:
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(82)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The error code, or 0 if there was no error"""
    current_leader: CurrentLeader = field(metadata={"tag": 0})
