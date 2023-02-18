"""
Generated from FindCoordinatorRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar


@dataclass(frozen=True, slots=True, kw_only=True)
class FindCoordinatorRequest:
    __flexible__: ClassVar[bool] = False
    key: str = field(metadata={"kafka_type": "string"})
    """The coordinator key."""
