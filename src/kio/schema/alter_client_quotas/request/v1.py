"""
Generated from AlterClientQuotasRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar


@dataclass(frozen=True, slots=True, kw_only=True)
class EntityData:
    __flexible__: ClassVar[bool] = True
    entity_type: str = field(metadata={"kafka_type": "string"})
    """The entity type."""
    entity_name: str | None = field(metadata={"kafka_type": "string"})
    """The name of the entity, or null if the default."""


@dataclass(frozen=True, slots=True, kw_only=True)
class OpData:
    __flexible__: ClassVar[bool] = True
    key: str = field(metadata={"kafka_type": "string"})
    """The quota configuration key."""
    value: float = field(metadata={"kafka_type": "float64"})
    """The value to set, otherwise ignored if the value is to be removed."""
    remove: bool = field(metadata={"kafka_type": "bool"})
    """Whether the quota configuration value should be removed, otherwise set."""


@dataclass(frozen=True, slots=True, kw_only=True)
class EntryData:
    __flexible__: ClassVar[bool] = True
    entity: tuple[EntityData, ...]
    """The quota entity to alter."""
    ops: tuple[OpData, ...]
    """An individual quota configuration entry to alter."""


@dataclass(frozen=True, slots=True, kw_only=True)
class AlterClientQuotasRequest:
    __flexible__: ClassVar[bool] = True
    entries: tuple[EntryData, ...]
    """The quota configuration entries to alter."""
    validate_only: bool = field(metadata={"kafka_type": "bool"})
    """Whether the alteration should be validated, but not performed."""
