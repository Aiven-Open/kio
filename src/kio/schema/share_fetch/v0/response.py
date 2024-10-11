"""
Generated from ``clients/src/main/resources/common/message/ShareFetchResponse.json``.
"""

import uuid

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.errors import ErrorCode
from kio.schema.response_header.v1.header import ResponseHeader
from kio.schema.types import BrokerId
from kio.static.constants import EntityType
from kio.static.primitive import Records
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i32Timedelta
from kio.static.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class LeaderIdAndEpoch:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(78)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    leader_id: i32 = field(metadata={"kafka_type": "int32"})
    """The ID of the current leader or -1 if the leader is unknown."""
    leader_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The latest known leader epoch."""


@dataclass(frozen=True, slots=True, kw_only=True)
class AcquiredRecords:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(78)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    first_offset: i64 = field(metadata={"kafka_type": "int64"})
    """The earliest offset in this batch of acquired records."""
    last_offset: i64 = field(metadata={"kafka_type": "int64"})
    """The last offset of this batch of acquired records."""
    delivery_count: i16 = field(metadata={"kafka_type": "int16"})
    """The delivery count of this batch of acquired records."""


@dataclass(frozen=True, slots=True, kw_only=True)
class PartitionData:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(78)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The fetch error code, or 0 if there was no fetch error."""
    error_message: str | None = field(metadata={"kafka_type": "string"}, default=None)
    """The fetch error message, or null if there was no fetch error."""
    acknowledge_error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The acknowledge error code, or 0 if there was no acknowledge error."""
    acknowledge_error_message: str | None = field(
        metadata={"kafka_type": "string"}, default=None
    )
    """The acknowledge error message, or null if there was no acknowledge error."""
    current_leader: LeaderIdAndEpoch
    records: Records | None = field(metadata={"kafka_type": "records"})
    """The record data."""
    acquired_records: tuple[AcquiredRecords, ...]
    """The acquired records."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ShareFetchableTopicResponse:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(78)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    topic_id: uuid.UUID | None = field(metadata={"kafka_type": "uuid"})
    """The unique topic ID."""
    partitions: tuple[PartitionData, ...]
    """The topic partitions."""


@dataclass(frozen=True, slots=True, kw_only=True)
class NodeEndpoint:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(78)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    node_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The ID of the associated node."""
    host: str = field(metadata={"kafka_type": "string"})
    """The node's hostname."""
    port: i32 = field(metadata={"kafka_type": "int32"})
    """The node's port."""
    rack: str | None = field(metadata={"kafka_type": "string"}, default=None)
    """The rack of the node, or null if it has not been assigned to a rack."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ShareFetchResponse:
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(78)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The top-level response error code."""
    error_message: str | None = field(metadata={"kafka_type": "string"}, default=None)
    """The top-level error message, or null if there was no error."""
    responses: tuple[ShareFetchableTopicResponse, ...]
    """The response topics."""
    node_endpoints: tuple[NodeEndpoint, ...]
    """Endpoints for all current leaders enumerated in PartitionData with error NOT_LEADER_OR_FOLLOWER."""
