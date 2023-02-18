"""
Generated from ListOffsetsRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import BrokerId
from kio.schema.entity import TopicName
from kio.schema.primitive import i32
from kio.schema.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class ListOffsetsPartition:
    __flexible__: ClassVar[bool] = False
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    timestamp: i64 = field(metadata={"kafka_type": "int64"})
    """The current timestamp."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ListOffsetsTopic:
    __flexible__: ClassVar[bool] = False
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partitions: tuple[ListOffsetsPartition, ...]
    """Each partition in the request."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ListOffsetsRequest:
    __flexible__: ClassVar[bool] = False
    replica_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The broker ID of the requestor, or -1 if this request is being made by a normal consumer."""
    topics: tuple[ListOffsetsTopic, ...]
    """Each topic in the request."""
