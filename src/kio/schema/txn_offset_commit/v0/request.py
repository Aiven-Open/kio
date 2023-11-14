"""
Generated from TxnOffsetCommitRequest.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/TxnOffsetCommitRequest.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v1.header import RequestHeader
from kio.schema.types import GroupId
from kio.schema.types import ProducerId
from kio.schema.types import TopicName
from kio.schema.types import TransactionalId
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i64
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class TxnOffsetCommitRequestPartition:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(28)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The index of the partition within the topic."""
    committed_offset: i64 = field(metadata={"kafka_type": "int64"})
    """The message offset to be committed."""
    committed_metadata: str | None = field(metadata={"kafka_type": "string"})
    """Any associated metadata the client wants to keep."""


@dataclass(frozen=True, slots=True, kw_only=True)
class TxnOffsetCommitRequestTopic:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(28)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partitions: tuple[TxnOffsetCommitRequestPartition, ...]
    """The partitions inside the topic that we want to commit offsets for."""


@dataclass(frozen=True, slots=True, kw_only=True)
class TxnOffsetCommitRequest(ApiMessage):
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(28)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    transactional_id: TransactionalId = field(metadata={"kafka_type": "string"})
    """The ID of the transaction."""
    group_id: GroupId = field(metadata={"kafka_type": "string"})
    """The ID of the group."""
    producer_id: ProducerId = field(metadata={"kafka_type": "int64"})
    """The current producer ID in use by the transactional ID."""
    producer_epoch: i16 = field(metadata={"kafka_type": "int16"})
    """The current epoch associated with the producer ID."""
    topics: tuple[TxnOffsetCommitRequestTopic, ...]
    """Each topic that we want to commit offsets for."""
