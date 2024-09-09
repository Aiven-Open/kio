"""
Generated from ``clients/src/main/resources/common/message/AssignReplicasToDirsRequest.json``.
"""

import uuid

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.schema.types import BrokerId
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class PartitionData:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(73)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index"""


@dataclass(frozen=True, slots=True, kw_only=True)
class TopicData:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(73)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    topic_id: uuid.UUID | None = field(metadata={"kafka_type": "uuid"})
    """The ID of the assigned topic"""
    partitions: tuple[PartitionData, ...]


@dataclass(frozen=True, slots=True, kw_only=True)
class DirectoryData:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(73)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    id_: uuid.UUID | None = field(metadata={"kafka_type": "uuid"})
    """The ID of the directory"""
    topics: tuple[TopicData, ...]


@dataclass(frozen=True, slots=True, kw_only=True)
class AssignReplicasToDirsRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(73)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    broker_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The ID of the requesting broker"""
    broker_epoch: i64 = field(metadata={"kafka_type": "int64"}, default=i64(-1))
    """The epoch of the requesting broker"""
    directories: tuple[DirectoryData, ...]
