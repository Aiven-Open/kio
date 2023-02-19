"""
Generated from DescribeClientQuotasResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import f64
from kio.schema.primitive import i16
from kio.schema.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class EntityData:
    __flexible__: ClassVar[bool] = False
    entity_type: str = field(metadata={"kafka_type": "string"})
    """The entity type."""
    entity_name: str | None = field(metadata={"kafka_type": "string"})
    """The entity name, or null if the default."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ValueData:
    __flexible__: ClassVar[bool] = False
    key: str = field(metadata={"kafka_type": "string"})
    """The quota configuration key."""
    value: f64 = field(metadata={"kafka_type": "float64"})
    """The quota configuration value."""


@dataclass(frozen=True, slots=True, kw_only=True)
class EntryData:
    __flexible__: ClassVar[bool] = False
    entity: tuple[EntityData, ...]
    """The quota entity description."""
    values: tuple[ValueData, ...]
    """The quota values for the entity."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeClientQuotasResponse:
    __flexible__: ClassVar[bool] = False
    throttle_time_ms: i32 = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The error code, or `0` if the quota description succeeded."""
    error_message: str | None = field(metadata={"kafka_type": "string"})
    """The error message, or `null` if the quota description succeeded."""
    entries: tuple[EntryData, ...]
    """A result entry."""
