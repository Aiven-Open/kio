"""
Generated from ``clients/src/main/resources/common/message/ShareFetchRequest.json``.
"""

import uuid

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.schema.types import GroupId
from kio.static.constants import EntityType
from kio.static.primitive import i8
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i32Timedelta
from kio.static.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class AcknowledgementBatch:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(78)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    first_offset: i64 = field(metadata={"kafka_type": "int64"})
    """First offset of batch of records to acknowledge."""
    last_offset: i64 = field(metadata={"kafka_type": "int64"})
    """Last offset (inclusive) of batch of records to acknowledge."""
    acknowledge_types: tuple[i8, ...] = field(
        metadata={"kafka_type": "int8"}, default=()
    )
    """Array of acknowledge types - 0:Gap,1:Accept,2:Release,3:Reject."""


@dataclass(frozen=True, slots=True, kw_only=True)
class FetchPartition:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(78)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    partition_max_bytes: i32 = field(metadata={"kafka_type": "int32"})
    """The maximum bytes to fetch from this partition. 0 when only acknowledgement with no fetching is required. See KIP-74 for cases where this limit may not be honored."""
    acknowledgement_batches: tuple[AcknowledgementBatch, ...]
    """Record batches to acknowledge."""


@dataclass(frozen=True, slots=True, kw_only=True)
class FetchTopic:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(78)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    topic_id: uuid.UUID | None = field(metadata={"kafka_type": "uuid"})
    """The unique topic ID."""
    partitions: tuple[FetchPartition, ...]
    """The partitions to fetch."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ForgottenTopic:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(78)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    topic_id: uuid.UUID | None = field(metadata={"kafka_type": "uuid"})
    """The unique topic ID."""
    partitions: tuple[i32, ...] = field(metadata={"kafka_type": "int32"}, default=())
    """The partitions indexes to forget."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ShareFetchRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(78)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    group_id: GroupId | None = field(metadata={"kafka_type": "string"}, default=None)
    """The group identifier."""
    member_id: str | None = field(metadata={"kafka_type": "string"})
    """The member ID."""
    share_session_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The current share session epoch: 0 to open a share session; -1 to close it; otherwise increments for consecutive requests."""
    max_wait: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The maximum time in milliseconds to wait for the response."""
    min_bytes: i32 = field(metadata={"kafka_type": "int32"})
    """The minimum bytes to accumulate in the response."""
    max_bytes: i32 = field(metadata={"kafka_type": "int32"}, default=i32(2147483647))
    """The maximum bytes to fetch.  See KIP-74 for cases where this limit may not be honored."""
    topics: tuple[FetchTopic, ...]
    """The topics to fetch."""
    forgotten_topics_data: tuple[ForgottenTopic, ...]
    """The partitions to remove from this share session."""
