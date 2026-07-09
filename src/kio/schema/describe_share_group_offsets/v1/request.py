"""
Generated from ``clients/src/main/resources/common/message/DescribeShareGroupOffsetsRequest.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.schema.types import GroupId
from kio.schema.types import TopicName
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeShareGroupOffsetsRequestTopic:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(90)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    topic_name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partitions: tuple[i32, ...] = field(metadata={"kafka_type": "int32"}, default=())
    """The partitions."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeShareGroupOffsetsRequestGroup:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(90)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    group_id: GroupId = field(metadata={"kafka_type": "string"})
    """The group identifier."""
    topics: tuple[DescribeShareGroupOffsetsRequestTopic, ...] | None
    """The topics to describe offsets for, or null for all topic-partitions."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeShareGroupOffsetsRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(90)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    groups: tuple[DescribeShareGroupOffsetsRequestGroup, ...]
    """The groups to describe offsets for."""
