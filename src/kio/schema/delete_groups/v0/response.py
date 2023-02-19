"""
Generated from DeleteGroupsResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i16
from kio.schema.primitive import i32
from kio.schema.types import GroupId


@dataclass(frozen=True, slots=True, kw_only=True)
class DeletableGroupResult:
    __flexible__: ClassVar[bool] = False
    group_id: GroupId = field(metadata={"kafka_type": "string"})
    """The group id"""
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The deletion error, or 0 if the deletion succeeded."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteGroupsResponse:
    __flexible__: ClassVar[bool] = False
    throttle_time_ms: i32 = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    results: tuple[DeletableGroupResult, ...]
    """The deletion results"""