"""
Generated from ``clients/src/main/resources/common/message/MetadataRequest.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v1.header import RequestHeader
from kio.schema.types import TopicName
from kio.static.constants import EntityType
from kio.static.primitive import i16


@dataclass(frozen=True, slots=True, kw_only=True)
class MetadataRequestTopic:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(4)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(3)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""


@dataclass(frozen=True, slots=True, kw_only=True)
class MetadataRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(4)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(3)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    topics: tuple[MetadataRequestTopic, ...] | None
    """The topics to fetch metadata for."""
    allow_auto_topic_creation: bool = field(
        metadata={"kafka_type": "bool"}, default=True
    )
    """If this is true, the broker may auto-create topics that we requested which do not already exist, if it is configured to do so."""
