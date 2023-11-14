"""
Generated from DescribeClientQuotasRequest.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/DescribeClientQuotasRequest.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.static.primitive import i8
from kio.static.primitive import i16
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class ComponentData:
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(48)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    entity_type: str = field(metadata={"kafka_type": "string"})
    """The entity type that the filter component applies to."""
    match_type: i8 = field(metadata={"kafka_type": "int8"})
    """How to match the entity {0 = exact name, 1 = default name, 2 = any specified name}."""
    match: str | None = field(metadata={"kafka_type": "string"})
    """The string to match against, or null if unused for the match type."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeClientQuotasRequest(ApiMessage):
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(48)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    components: tuple[ComponentData, ...]
    """Filter components to apply to quota entities."""
    strict: bool = field(metadata={"kafka_type": "bool"})
    """Whether the match is strict, i.e. should exclude entities with unspecified entity types."""
