"""
Generated from OffsetCommitRequest.json.
"""

# ruff: noqa: A003

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v1.header import RequestHeader
from kio.schema.types import GroupId
from kio.schema.types import TopicName
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetCommitRequestPartition:
    __version__: ClassVar[i16] = i16(5)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(8)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    committed_offset: i64 = field(metadata={"kafka_type": "int64"})
    """The message offset to be committed."""
    committed_metadata: str | None = field(metadata={"kafka_type": "string"})
    """Any associated metadata the client wants to keep."""


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetCommitRequestTopic:
    __version__: ClassVar[i16] = i16(5)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(8)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partitions: tuple[OffsetCommitRequestPartition, ...]
    """Each partition to commit offsets for."""


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetCommitRequest:
    __version__: ClassVar[i16] = i16(5)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(8)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    group_id: GroupId = field(metadata={"kafka_type": "string"})
    """The unique group identifier."""
    generation_id: i32 = field(metadata={"kafka_type": "int32"}, default=i32(-1))
    """The generation of the group."""
    member_id: str = field(metadata={"kafka_type": "string"})
    """The member ID assigned by the group coordinator."""
    topics: tuple[OffsetCommitRequestTopic, ...]
    """The topics to commit offsets for."""
