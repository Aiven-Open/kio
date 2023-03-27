"""
Generated from MetadataRequest.json.
"""

# ruff: noqa: A003

import uuid
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.schema.types import TopicName
from kio.static.primitive import i16


@dataclass(frozen=True, slots=True, kw_only=True)
class MetadataRequestTopic:
    __version__: ClassVar[i16] = i16(12)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(3)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    topic_id: uuid.UUID = field(metadata={"kafka_type": "uuid"})
    """The topic id."""
    name: TopicName | None = field(metadata={"kafka_type": "string"})
    """The topic name."""


@dataclass(frozen=True, slots=True, kw_only=True)
class MetadataRequest:
    __version__: ClassVar[i16] = i16(12)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(3)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    topics: tuple[MetadataRequestTopic, ...]
    """The topics to fetch metadata for."""
    allow_auto_topic_creation: bool = field(
        metadata={"kafka_type": "bool"}, default=True
    )
    """If this is true, the broker may auto-create topics that we requested which do not already exist, if it is configured to do so."""
    include_topic_authorized_operations: bool = field(metadata={"kafka_type": "bool"})
    """Whether to include topic authorized operations."""
