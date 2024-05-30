"""
Generated from ``clients/src/main/resources/common/message/DescribeClientQuotasResponse.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.errors import ErrorCode
from kio.schema.response_header.v1.header import ResponseHeader
from kio.static.constants import EntityType
from kio.static.primitive import f64
from kio.static.primitive import i16
from kio.static.primitive import i32Timedelta


@dataclass(frozen=True, slots=True, kw_only=True)
class EntityData:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(48)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    entity_type: str = field(metadata={"kafka_type": "string"})
    """The entity type."""
    entity_name: str | None = field(metadata={"kafka_type": "string"})
    """The entity name, or null if the default."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ValueData:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(48)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    key: str = field(metadata={"kafka_type": "string"})
    """The quota configuration key."""
    value: f64 = field(metadata={"kafka_type": "float64"})
    """The quota configuration value."""


@dataclass(frozen=True, slots=True, kw_only=True)
class EntryData:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(48)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    entity: tuple[EntityData, ...]
    """The quota entity description."""
    values: tuple[ValueData, ...]
    """The quota values for the entity."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeClientQuotasResponse:
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(48)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The error code, or `0` if the quota description succeeded."""
    error_message: str | None = field(metadata={"kafka_type": "string"})
    """The error message, or `null` if the quota description succeeded."""
    entries: tuple[EntryData, ...] | None
    """A result entry."""
