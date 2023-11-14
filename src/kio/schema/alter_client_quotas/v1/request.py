"""
Generated from AlterClientQuotasRequest.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/AlterClientQuotasRequest.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.static.primitive import f64
from kio.static.primitive import i16
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class EntityData:
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(49)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    entity_type: str = field(metadata={"kafka_type": "string"})
    """The entity type."""
    entity_name: str | None = field(metadata={"kafka_type": "string"})
    """The name of the entity, or null if the default."""


@dataclass(frozen=True, slots=True, kw_only=True)
class OpData:
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(49)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    key: str = field(metadata={"kafka_type": "string"})
    """The quota configuration key."""
    value: f64 = field(metadata={"kafka_type": "float64"})
    """The value to set, otherwise ignored if the value is to be removed."""
    remove: bool = field(metadata={"kafka_type": "bool"})
    """Whether the quota configuration value should be removed, otherwise set."""


@dataclass(frozen=True, slots=True, kw_only=True)
class EntryData:
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(49)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    entity: tuple[EntityData, ...]
    """The quota entity to alter."""
    ops: tuple[OpData, ...]
    """An individual quota configuration entry to alter."""


@dataclass(frozen=True, slots=True, kw_only=True)
class AlterClientQuotasRequest(ApiMessage):
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(49)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    entries: tuple[EntryData, ...]
    """The quota configuration entries to alter."""
    validate_only: bool = field(metadata={"kafka_type": "bool"})
    """Whether the alteration should be validated, but not performed."""
