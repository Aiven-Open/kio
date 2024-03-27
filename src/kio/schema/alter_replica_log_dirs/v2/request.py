"""
Generated from ``clients/src/main/resources/common/message/AlterReplicaLogDirsRequest.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.schema.types import TopicName
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class AlterReplicaLogDirTopic:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(2)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(34)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partitions: tuple[i32, ...] = field(metadata={"kafka_type": "int32"}, default=())
    """The partition indexes."""


@dataclass(frozen=True, slots=True, kw_only=True)
class AlterReplicaLogDir:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(2)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(34)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    path: str = field(metadata={"kafka_type": "string"})
    """The absolute directory path."""
    topics: tuple[AlterReplicaLogDirTopic, ...]
    """The topics to add to the directory."""


@dataclass(frozen=True, slots=True, kw_only=True)
class AlterReplicaLogDirsRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(2)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(34)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    dirs: tuple[AlterReplicaLogDir, ...]
    """The alterations to make for each directory."""
