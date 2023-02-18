"""
Generated from DescribeGroupsRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.types import GroupId


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeGroupsRequest:
    __flexible__: ClassVar[bool] = True
    groups: tuple[GroupId, ...] = field(metadata={"kafka_type": "string"}, default=())
    """The names of the groups to describe"""
    include_authorized_operations: bool = field(metadata={"kafka_type": "bool"})
    """Whether to include authorized operations."""
