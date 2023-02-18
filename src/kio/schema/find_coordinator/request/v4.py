"""
Generated from FindCoordinatorRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i8


@dataclass(frozen=True, slots=True, kw_only=True)
class FindCoordinatorRequest:
    __flexible__: ClassVar[bool] = True
    key_type: i8 = field(metadata={"kafka_type": "int8"}, default=i8(0))
    """The coordinator key type. (Group, transaction, etc.)"""
    coordinator_keys: tuple[str, ...] = field(
        metadata={"kafka_type": "string"}, default=()
    )
    """The coordinator keys."""
