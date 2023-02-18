"""
Generated from ListGroupsRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar


@dataclass(frozen=True, slots=True, kw_only=True)
class ListGroupsRequest:
    __flexible__: ClassVar[bool] = True
    states_filter: tuple[str, ...] = field(
        metadata={"kafka_type": "string"}, default=()
    )
    """The states of the groups we want to list. If empty all groups are returned with their state."""
