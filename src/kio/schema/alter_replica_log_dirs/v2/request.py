"""
Generated from AlterReplicaLogDirsRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i32
from kio.schema.types import TopicName


@dataclass(frozen=True, slots=True, kw_only=True)
class AlterReplicaLogDirTopic:
    __flexible__: ClassVar[bool] = True
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partitions: tuple[i32, ...] = field(metadata={"kafka_type": "int32"}, default=())
    """The partition indexes."""


@dataclass(frozen=True, slots=True, kw_only=True)
class AlterReplicaLogDir:
    __flexible__: ClassVar[bool] = True
    path: str = field(metadata={"kafka_type": "string"})
    """The absolute directory path."""
    topics: tuple[AlterReplicaLogDirTopic, ...]
    """The topics to add to the directory."""


@dataclass(frozen=True, slots=True, kw_only=True)
class AlterReplicaLogDirsRequest:
    __flexible__: ClassVar[bool] = True
    dirs: tuple[AlterReplicaLogDir, ...]
    """The alterations to make for each directory."""
