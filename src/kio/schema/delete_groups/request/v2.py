"""
Generated from DeleteGroupsRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import GroupId


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteGroupsRequest:
    __flexible__: ClassVar[bool] = True
    groups_names: tuple[GroupId, ...] = field(
        metadata={"kafka_type": "string"}, default=()
    )
    """The group names to delete."""
