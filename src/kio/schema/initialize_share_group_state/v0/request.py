"""
Generated from ``clients/src/main/resources/common/message/InitializeShareGroupStateRequest.json``.
"""

import uuid

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class PartitionData:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(83)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    partition: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    state_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The state epoch for this share-partition."""
    start_offset: i64 = field(metadata={"kafka_type": "int64"})
    """The share-partition start offset, or -1 if the start offset is not being initialized."""


@dataclass(frozen=True, slots=True, kw_only=True)
class InitializeStateData:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(83)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    topic_id: uuid.UUID | None = field(metadata={"kafka_type": "uuid"})
    """The topic identifier."""
    partitions: tuple[PartitionData, ...]
    """The data for the partitions."""


@dataclass(frozen=True, slots=True, kw_only=True)
class InitializeShareGroupStateRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(83)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    group_id: str = field(metadata={"kafka_type": "string"})
    """The group identifier."""
    topics: tuple[InitializeStateData, ...]
    """The data for the topics."""
