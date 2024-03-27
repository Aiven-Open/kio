"""
Generated from ``clients/src/main/resources/common/message/DescribeClientQuotasRequest.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v1.header import RequestHeader
from kio.static.constants import EntityType
from kio.static.primitive import i8
from kio.static.primitive import i16


@dataclass(frozen=True, slots=True, kw_only=True)
class ComponentData:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(48)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    entity_type: str = field(metadata={"kafka_type": "string"})
    """The entity type that the filter component applies to."""
    match_type: i8 = field(metadata={"kafka_type": "int8"})
    """How to match the entity {0 = exact name, 1 = default name, 2 = any specified name}."""
    match: str | None = field(metadata={"kafka_type": "string"})
    """The string to match against, or null if unused for the match type."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeClientQuotasRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(48)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    components: tuple[ComponentData, ...]
    """Filter components to apply to quota entities."""
    strict: bool = field(metadata={"kafka_type": "bool"})
    """Whether the match is strict, i.e. should exclude entities with unspecified entity types."""
