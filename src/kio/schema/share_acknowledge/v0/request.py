"""
Generated from ``clients/src/main/resources/common/message/ShareAcknowledgeRequest.json``.
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
from kio.static.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class AcknowledgementBatch:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(79)
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
class AcknowledgePartition:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(79)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    acknowledgement_batches: tuple[AcknowledgementBatch, ...]
    """Record batches to acknowledge."""


@dataclass(frozen=True, slots=True, kw_only=True)
class AcknowledgeTopic:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(79)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    topic_id: uuid.UUID | None = field(metadata={"kafka_type": "uuid"})
    """The unique topic ID."""
    partitions: tuple[AcknowledgePartition, ...]
    """The partitions containing records to acknowledge."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ShareAcknowledgeRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(79)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    group_id: GroupId | None = field(metadata={"kafka_type": "string"}, default=None)
    """The group identifier."""
    member_id: str | None = field(metadata={"kafka_type": "string"})
    """The member ID."""
    share_session_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The current share session epoch: 0 to open a share session; -1 to close it; otherwise increments for consecutive requests."""
    topics: tuple[AcknowledgeTopic, ...]
    """The topics containing records to acknowledge."""
