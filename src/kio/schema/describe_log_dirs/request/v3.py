"""
Generated from DescribeLogDirsRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import TopicName
from kio.schema.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribableLogDirTopic:
    __flexible__: ClassVar[bool] = True
    topic: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name"""
    partitions: tuple[i32, ...] = field(metadata={"kafka_type": "int32"}, default=())
    """The partition indexes."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeLogDirsRequest:
    __flexible__: ClassVar[bool] = True
    topics: tuple[DescribableLogDirTopic, ...]
    """Each topic that we want to describe log directories for, or null for all topics."""
