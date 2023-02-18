"""
Generated from ListGroupsResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import GroupId
from kio.schema.primitive import i16
from kio.schema.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class ListedGroup:
    __flexible__: ClassVar[bool] = False
    group_id: GroupId = field(metadata={"kafka_type": "string"})
    """The group ID."""
    protocol_type: str = field(metadata={"kafka_type": "string"})
    """The group protocol type."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ListGroupsResponse:
    __flexible__: ClassVar[bool] = False
    throttle_time_ms: i32 = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The error code, or 0 if there was no error."""
    groups: tuple[ListedGroup, ...]
    """Each group in the response."""
