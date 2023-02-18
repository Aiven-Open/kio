"""
Generated from ListGroupsResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import GroupId
from kio.schema.primitive import i16


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
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The error code, or 0 if there was no error."""
    groups: tuple[ListedGroup, ...]
    """Each group in the response."""
