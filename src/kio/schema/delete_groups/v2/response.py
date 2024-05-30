"""
Generated from ``clients/src/main/resources/common/message/DeleteGroupsResponse.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.errors import ErrorCode
from kio.schema.response_header.v1.header import ResponseHeader
from kio.schema.types import GroupId
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i32Timedelta


@dataclass(frozen=True, slots=True, kw_only=True)
class DeletableGroupResult:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(2)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(42)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    group_id: GroupId = field(metadata={"kafka_type": "string"})
    """The group id"""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The deletion error, or 0 if the deletion succeeded."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteGroupsResponse:
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(2)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(42)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    results: tuple[DeletableGroupResult, ...]
    """The deletion results"""
