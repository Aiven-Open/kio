"""
Generated from AlterReplicaLogDirsResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import TopicName


@dataclass(frozen=True, slots=True, kw_only=True)
class AlterReplicaLogDirPartitionResult:
    __flexible__: ClassVar[bool] = True
    partition_index: int = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    error_code: int = field(metadata={"kafka_type": "int16"})
    """The error code, or 0 if there was no error."""


@dataclass(frozen=True, slots=True, kw_only=True)
class AlterReplicaLogDirTopicResult:
    __flexible__: ClassVar[bool] = True
    topic_name: TopicName = field(metadata={"kafka_type": "string"})
    """The name of the topic."""
    partitions: tuple[AlterReplicaLogDirPartitionResult, ...]
    """The results for each partition."""


@dataclass(frozen=True, slots=True, kw_only=True)
class AlterReplicaLogDirsResponse:
    __flexible__: ClassVar[bool] = True
    throttle_time_ms: int = field(metadata={"kafka_type": "int32"})
    """Duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    results: tuple[AlterReplicaLogDirTopicResult, ...]
    """The results for each topic."""
