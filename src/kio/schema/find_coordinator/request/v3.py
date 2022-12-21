"""
Generated from FindCoordinatorRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar


@dataclass(frozen=True, slots=True, kw_only=True)
class FindCoordinatorRequest:
    __flexible__: ClassVar[bool] = True
    key: str = field(metadata={"kafka_type": "string"})
    """The coordinator key."""
    key_type: int = field(metadata={"kafka_type": "int8"}, default=0)
    """The coordinator key type. (Group, transaction, etc.)"""
