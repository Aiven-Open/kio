"""
Generated from DescribeClientQuotasRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar


@dataclass(frozen=True, slots=True, kw_only=True)
class ComponentData:
    __flexible__: ClassVar[bool] = False
    entity_type: str = field(metadata={"kafka_type": "string"})
    """The entity type that the filter component applies to."""
    match_type: int = field(metadata={"kafka_type": "int8"})
    """How to match the entity {0 = exact name, 1 = default name, 2 = any specified name}."""
    match: str | None = field(metadata={"kafka_type": "string"})
    """The string to match against, or null if unused for the match type."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeClientQuotasRequest:
    __flexible__: ClassVar[bool] = False
    components: tuple[ComponentData, ...]
    """Filter components to apply to quota entities."""
    strict: bool = field(metadata={"kafka_type": "bool"})
    """Whether the match is strict, i.e. should exclude entities with unspecified entity types."""
