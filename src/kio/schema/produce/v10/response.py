"""
Generated from ``clients/src/main/resources/common/message/ProduceResponse.json``.
"""

import datetime

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.errors import ErrorCode
from kio.schema.response_header.v1.header import ResponseHeader
from kio.schema.types import BrokerId
from kio.schema.types import TopicName
from kio.static.constants import EntityType
from kio.static.primitive import TZAware
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i32Timedelta
from kio.static.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class BatchIndexAndErrorMessage:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(10)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(0)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    batch_index: i32 = field(metadata={"kafka_type": "int32"})
    """The batch index of the record that cause the batch to be dropped"""
    batch_index_error_message: str | None = field(
        metadata={"kafka_type": "string"}, default=None
    )
    """The error message of the record that caused the batch to be dropped"""


@dataclass(frozen=True, slots=True, kw_only=True)
class LeaderIdAndEpoch:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(10)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(0)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    leader_id: BrokerId = field(metadata={"kafka_type": "int32"}, default=BrokerId(-1))
    """The ID of the current leader or -1 if the leader is unknown."""
    leader_epoch: i32 = field(metadata={"kafka_type": "int32"}, default=i32(-1))
    """The latest known leader epoch"""


@dataclass(frozen=True, slots=True, kw_only=True)
class PartitionProduceResponse:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(10)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(0)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The error code, or 0 if there was no error."""
    base_offset: i64 = field(metadata={"kafka_type": "int64"})
    """The base offset."""
    log_append_time: TZAware | None = field(
        metadata={"kafka_type": "datetime_i64"}, default=None
    )
    """The timestamp returned by broker after appending the messages. If CreateTime is used for the topic, the timestamp will be -1.  If LogAppendTime is used for the topic, the timestamp will be the broker local time when the messages are appended."""
    log_start_offset: i64 = field(metadata={"kafka_type": "int64"}, default=i64(-1))
    """The log start offset."""
    record_errors: tuple[BatchIndexAndErrorMessage, ...]
    """The batch indices of records that caused the batch to be dropped"""
    error_message: str | None = field(metadata={"kafka_type": "string"}, default=None)
    """The global error message summarizing the common root cause of the records that caused the batch to be dropped"""
    current_leader: LeaderIdAndEpoch = field(
        metadata={"tag": 0}, default=LeaderIdAndEpoch()
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class TopicProduceResponse:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(10)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(0)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name"""
    partition_responses: tuple[PartitionProduceResponse, ...]
    """Each partition that we produced to within the topic."""


@dataclass(frozen=True, slots=True, kw_only=True)
class NodeEndpoint:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(10)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(0)
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
class ProduceResponse:
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(10)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(0)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    responses: tuple[TopicProduceResponse, ...]
    """Each produce response"""
    throttle_time: i32Timedelta = field(
        metadata={"kafka_type": "timedelta_i32"},
        default=i32Timedelta.parse(datetime.timedelta(milliseconds=0)),
    )
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    node_endpoints: tuple[NodeEndpoint, ...] = field(metadata={"tag": 0}, default=())
    """Endpoints for all current-leaders enumerated in PartitionProduceResponses, with errors NOT_LEADER_OR_FOLLOWER."""
