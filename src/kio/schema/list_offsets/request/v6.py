"""
Generated from ListOffsetsRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import BrokerId
from kio.schema.entity import TopicName
from kio.schema.primitive import i8
from kio.schema.primitive import i32
from kio.schema.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class ListOffsetsPartition:
    __flexible__: ClassVar[bool] = True
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    current_leader_epoch: i32 = field(metadata={"kafka_type": "int32"}, default=i32(-1))
    """The current leader epoch."""
    timestamp: i64 = field(metadata={"kafka_type": "int64"})
    """The current timestamp."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ListOffsetsTopic:
    __flexible__: ClassVar[bool] = True
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partitions: tuple[ListOffsetsPartition, ...]
    """Each partition in the request."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ListOffsetsRequest:
    __flexible__: ClassVar[bool] = True
    replica_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The broker ID of the requestor, or -1 if this request is being made by a normal consumer."""
    isolation_level: i8 = field(metadata={"kafka_type": "int8"})
    """This setting controls the visibility of transactional records. Using READ_UNCOMMITTED (isolation_level = 0) makes all records visible. With READ_COMMITTED (isolation_level = 1), non-transactional and COMMITTED transactional records are visible. To be more concrete, READ_COMMITTED returns all data from offsets smaller than the current LSO (last stable offset), and enables the inclusion of the list of aborted transactions in the result, which allows consumers to discard ABORTED transactional records"""
    topics: tuple[ListOffsetsTopic, ...]
    """Each topic in the request."""
