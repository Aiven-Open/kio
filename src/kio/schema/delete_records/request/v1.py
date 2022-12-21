"""
Generated from DeleteRecordsRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import TopicName


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteRecordsPartition:
    __flexible__: ClassVar[bool] = False
    partition_index: int = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    offset: int = field(metadata={"kafka_type": "int64"})
    """The deletion offset."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteRecordsTopic:
    __flexible__: ClassVar[bool] = False
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partitions: tuple[DeleteRecordsPartition, ...]
    """Each partition that we want to delete records from."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteRecordsRequest:
    __flexible__: ClassVar[bool] = False
    topics: tuple[DeleteRecordsTopic, ...]
    """Each topic that we want to delete records from."""
    timeout_ms: int = field(metadata={"kafka_type": "int32"})
    """How long to wait for the deletion to complete, in milliseconds."""
